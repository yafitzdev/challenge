"""The java_api and port_check tools (step 08). Both are deterministic: no model call.

java_api <Class>     finds the Java file of a class (or nested type) in source/ and lists its non-private constructors, methods,
                     fields, constants, enum values and nested types, each with the Python name to use: the
                     spelling the public tests use if they use one, otherwise snake_case.
port_check <module>  compares a Python module in candidate/ with the Java class it ports and lists every
                     non-private Java member that has no Python counterpart yet.

Why: in the Gemini runs 382 of about 1,100 reads failed on guessed paths, and the step READMEs show the main loss is
Java methods that the port leaves out or names differently (results/06_decomposition/README.md).

Usage: python harness/src/java_tools.py <workspace> api <ClassName>
       python harness/src/java_tools.py <workspace> check <path/to/module.py>
"""
import ast
import difflib
import re
import sys
from pathlib import Path

# Java methods that Python spells as special methods.
SPECIAL = {'toString': '__str__', 'equals': '__eq__', 'hashCode': '__hash__', 'compareTo': '__lt__',
           'iterator': '__iter__', 'size': '__len__'}
MAX_MEMBERS = 80


def strip(java):
    """Java source without comments, string and char literals (so braces inside them do not count)."""
    java = re.sub(r'/\*.*?\*/', ' ', java, flags=re.S)
    java = re.sub(r'//[^\n]*', ' ', java)
    java = re.sub(r'"(\\.|[^"\\])*"', '""', java)
    return re.sub(r"'(\\.|[^'\\])*'", "''", java)


def segments(body):
    """Top-level declarations of a class body: (header text, body text or None for a `;` declaration)."""
    out, depth, start, i = [], 0, 0, 0
    while i < len(body):
        ch = body[i]
        if ch == '{':
            if depth == 0:
                header, open_at = body[start:i], i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                out.append((header.strip(), body[open_at + 1:i]))
                start = i + 1
        elif ch == ';' and depth == 0:
            out.append((body[start:i].strip(), None))
            start = i + 1
        i += 1
    return out


def type_body(java, name):
    """Body of the class, interface or enum called `name` in stripped Java source."""
    match = re.search(rf'\b(class|interface|enum|record)\s+{name}\b[^{{]*\{{', java)
    if not match:
        return None, None
    depth, i = 1, match.end()
    while i < len(java) and depth:
        depth += {'{': 1, '}': -1}.get(java[i], 0)
        i += 1
    return match.group(1), java[match.end():i - 1]


def snake(name):
    return re.sub(r'(?<=[a-z0-9])([A-Z])|(?<=[A-Z])([A-Z])(?=[a-z])', r'_\1\2', name).lower()


def members(kind, body, cls):
    """[(member kind, Java name, signature)] for the non-private members of one type body."""
    found = []
    parts = segments(body)
    if kind == 'enum' and parts:
        # The constants come first, up to the first `;`.
        constants = parts[0][0] if parts[0][1] is None else ''
        for name in re.findall(r'(?:^|,)\s*@?(\w+)\s*(?:\([^)]*\))?', constants):
            found.append(('enum value', name, name))
        parts = parts[1:] if constants else parts
    for header, block in parts:
        header = re.sub(r'@\w+(\([^)]*\))?', ' ', header).strip()
        if not header or re.search(r'\bprivate\b', header) or header.startswith('static') and block is not None \
                and '(' not in header:
            continue  # private, or a static initializer block
        nested = re.search(r'\b(class|interface|enum|record)\s+(\w+)', header)
        if nested and '(' not in header.split(nested.group(0))[0]:
            found.append((f'nested {nested.group(1)}', nested.group(2), header))
            continue
        call = re.search(r'([\w<>\[\], ?]+?\s+)?(\w+)\s*\(([^)]*)\)', header)
        if call and (block is not None or kind == 'interface' or 'abstract' in header):
            name = call.group(2)
            params = ', '.join(p.split()[-1] for p in call.group(3).split(',') if p.strip())
            # Static methods must stay static in Python (step 08 run 1: `missing 1 required positional argument`).
            static = bool(re.search(r'\bstatic\b', header.split('(')[0]))
            what = 'constructor' if name == cls else 'static method' if static else 'method'
            mods = r'\b(public|protected|static|final|abstract|synchronized|native|default)\b'
            ret = '' if what == 'constructor' else re.sub(mods, '', call.group(1) or '').strip() + ' '
            found.append((what, name, f'{ret}{name}({params})'.strip()))
            continue
        if block is None and '(' not in header.split('=')[0]:
            decl = header.split('=')[0].split()
            if len(decl) >= 2:
                value = header.split('=', 1)[1].strip()[:60] if '=' in header else ''
                constant = 'static' in header and 'final' in header
                found.append(('constant' if constant else 'field', decl[-1],
                              f'{decl[-2]} {decl[-1]}' + (f' = {value}' if value and constant else '')))
    return found


def test_names(candidate):
    """Every identifier the public tests use, to spell the Python names the way they do."""
    names = set()
    for test in (candidate / 'public_tests').rglob('*.py'):
        names.update(re.findall(r'\b\w+\b', test.read_text(encoding='utf-8', errors='replace')))
    return names


def python_name(kind, name, used):
    if kind == 'constructor':
        return '__init__'
    if kind in ('constant', 'enum value') or kind.startswith('nested'):
        return name
    if name in SPECIAL:
        return SPECIAL[name]
    return name if name in used and snake(name) not in used else snake(name)


def java_files(workspace, cls):
    files = sorted((workspace / 'source').rglob(f'{cls}.java'))
    return [f for f in files if '/test/' not in f.as_posix()] or files


def api(workspace, cls):
    parts = cls.removesuffix('.java').split('.')
    cls = parts[-1]
    # A nested type (PhoneNumber.Type) lives in its outer class's file.
    files = java_files(workspace, parts[-2]) if len(parts) > 1 else java_files(workspace, cls)
    if not files:
        files = [f for f in sorted((workspace / 'source').rglob('*.java')) if '/test/' not in f.as_posix()
                 and type_body(strip(f.read_text(encoding='utf-8', errors='replace')), cls)[1] is not None]
        if len(files) > 1:
            return (f'{cls} is a nested type in several classes: ' + ', '.join(f.stem for f in files[:10])
                    + f'. Ask for one, e.g. java_api("{files[0].stem}.{cls}").')
    if not files:
        stems = sorted({f.stem for f in (workspace / 'source').rglob('*.java')})
        near = difflib.get_close_matches(cls, stems, n=10, cutoff=0.6)
        return f'No {cls}.java in ../source/.' + (f' Similar: {", ".join(near[:10])}' if near else '')
    java = strip(files[0].read_text(encoding='utf-8', errors='replace'))
    kind, body = type_body(java, cls)
    if body is None:
        return f'{files[0].relative_to(workspace)}: no class {cls} found in it.'
    used = test_names(workspace / 'candidate')
    found = members(kind, body, cls)
    tests = sorted(f.relative_to(workspace).as_posix() for f in (workspace / 'source').rglob(f'{cls}*Test.java'))
    out = [f'{kind} {cls}: ../{files[0].relative_to(workspace).as_posix()}'
           + (f' (also {len(files) - 1} more file(s) with this name)' if len(files) > 1 else '')]
    if tests:
        out.append('Java tests: ' + ', '.join(f'../{t}' for t in tests))
    out.append('\nMembers (Java signature -> Python name):')
    out += [f'- {k}: {sig} -> {python_name(k, n, used)}' + (' (@staticmethod)' if k == 'static method' else '')
            for k, n, sig in found[:MAX_MEMBERS]]
    if len(found) > MAX_MEMBERS:
        out.append(f'- ... {len(found) - MAX_MEMBERS} more; read the Java file.')
    if not found:
        out.append('- (no non-private members)')
    return '\n'.join(out)


def python_names(module):
    """Every name a Python module defines: classes, functions, methods, attributes, constants."""
    tree = ast.parse(module.read_text(encoding='utf-8', errors='replace'))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            names.add(node.id)
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
            names.add(node.attr)
    return names


def check(workspace, module):
    candidate = workspace / 'candidate'
    path = (candidate / module).resolve()
    if not path.is_file():
        return f'{module}: no such file in candidate/.'
    try:
        defined = python_names(path)
    except SyntaxError as e:
        return f'{module}: SyntaxError line {e.lineno}: {e.msg}'
    # The Java class: a file whose name matches the module (wgs84point.py <- WGS84Point.java), else a class the
    # module defines.
    stems = {f.stem.lower(): f.stem for f in (workspace / 'source').rglob('*.java') if '/test/' not in f.as_posix()}
    key = path.stem.replace('_', '').lower()
    classes = [stems[key]] if key in stems else [stems[n.lower()] for n in sorted(defined) if n.lower() in stems]
    if not classes:
        return f'{module}: no Java class matches this module; pass the module that ports a Java class.'
    used = test_names(candidate)
    out = []
    for cls in classes[:3]:
        java = strip(java_files(workspace, cls)[0].read_text(encoding='utf-8', errors='replace'))
        kind, body = type_body(java, cls)
        if body is None:
            continue
        found = members(kind, body, cls)
        missing = []
        for k, n, sig in found:
            if k == 'field':
                continue  # private state is free to differ; fields rarely belong to the API
            want = python_name(k, n, used)
            if k == 'constructor':
                ok = cls in defined
            else:
                ok = {want, n, snake(n)} & defined
            if not ok:
                missing.append(f'- {k}: {sig} -> expected {want}')
        if missing:
            out.append(f'{cls} ({len(found)} members): {len(missing)} not found in {module}:')
            out += missing[:MAX_MEMBERS]
        else:
            out.append(f'{cls}: every non-private Java member has a Python counterpart in {module}.')
    return '\n'.join(out) + '\n(Names only: this does not check behavior. Run the tests for that.)'


def main():
    workspace, command, arg = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
    print(api(workspace, arg) if command == 'api' else check(workspace, arg))


if __name__ == '__main__':
    main()
