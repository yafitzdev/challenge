"""Retry: what happens after the agent stops.

1. Push to continue: while a module the public tests import cannot be imported (not written, broken, or a name
   missing), a fresh short session is sent back to the repository with the exact import errors, up to
   `push_to_continue` times. It may change any file, but a round that leaves more broken imports is undone.
   Weak models often stop before writing every module.
2. Per module: every module whose public tests fail is generated again by a fresh, short agent session, up to
   `attempts` times. Only that one file may change, and the attempt is kept only if more of its tests pass than
   before.

Which tests belong to which module: a public test file belongs to every module of the project it imports
(`from src.geohash.util.long_util import LongUtil` -> src/geohash/util/long_util.py).
Only the public tests are used here; the hidden tests stay with the evaluator.
"""
import ast
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

PROMPTS = Path(__file__).resolve().parents[1] / 'prompts'
TEST_TIMEOUT_SECONDS = 120
MAX_FAILURE_LINES = 15


def test_env(candidate):
    """The environment the evaluator runs tests in."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(('PYTHON', 'PYTEST'))}
    env.update(PYTHONPATH=os.pathsep.join([str(candidate), str(candidate / 'src')]), PYTHONHASHSEED='0',
               PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    return env


def run_test_file(candidate, test_file):
    """Run one public test file the way the evaluator does. Returns (passed, total, failure lines)."""
    env = test_env(candidate)
    with tempfile.TemporaryDirectory() as tmp:
        xml = Path(tmp) / 'report.xml'
        cmd = [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--noconftest', '--tb=short',
               f'--junitxml={xml}', test_file]
        try:
            subprocess.run(cmd, cwd=candidate, env=env, capture_output=True, text=True, encoding='utf-8',
                           errors='replace', timeout=TEST_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            return 0, 1, [f'{test_file}: did not finish within {TEST_TIMEOUT_SECONDS} s (endless loop?)']
        if not xml.exists():
            return 0, 1, [f'{test_file}: pytest could not run']
        passed, total, lines = 0, 0, []
        for case in ET.parse(xml).getroot().iter('testcase'):
            problem = next((c for c in case if c.tag in ('failure', 'error')), None)
            if case.find('skipped') is not None and problem is None:
                continue
            total += 1
            if problem is None:
                passed += 1
                continue
            text = problem.text or ''
            e_lines = [l[1:].strip() for l in text.splitlines() if l.startswith('E ') and l[1:].strip()]
            why = e_lines[0] if e_lines else (problem.get('message') or problem.tag).strip().split('\n')[0]
            lines.append(f"{test_file}::{case.get('name')}: {why[:300]}")
    return passed, max(total, 1), lines


def module_tests(candidate):
    """{module file (relative to candidate/): [public test files that import it]}. Packages count as their
    __init__.py once the folder exists."""
    found = {}
    for test in sorted((candidate / 'public_tests').rglob('test_*.py')):
        rel = test.relative_to(candidate).as_posix()
        try:
            tree = ast.parse(test.read_text(encoding='utf-8', errors='replace'))
        except SyntaxError:
            continue
        names = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module]
        names += [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]
        for name in names:
            if not name.startswith('src.') or len(name.split('.')) < 2:
                continue
            path = name.replace('.', '/')
            # `from src.pkg import Name` imports the package itself: its __init__.py.
            module = path + '/__init__.py' if (candidate / path).is_dir() else path + '.py'
            found.setdefault(module, []).append(rel)
    return {m: sorted(set(t)) for m, t in found.items()}


def test_imports(candidate):
    """{module: names} for every project module the public tests import (`from src.x import A, B` -> {A, B})."""
    found = {}
    for test in sorted((candidate / 'public_tests').rglob('test_*.py')):
        try:
            tree = ast.parse(test.read_text(encoding='utf-8', errors='replace'))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith('src.'):
                found.setdefault(node.module, set()).update(a.name for a in node.names if a.name != '*')
            elif isinstance(node, ast.Import):
                for a in node.names:
                    if a.name.startswith('src.'):
                        found.setdefault(a.name, set())
    return found


def import_problems(candidate):
    """One line per import of the public tests that fails (module not written, broken, or a name missing), with
    Python's own error. No model call."""
    problems = []
    for module, names in sorted(test_imports(candidate).items()):
        code = f'from {module} import {", ".join(sorted(names))}' if names else f'import {module}'
        try:
            proc = subprocess.run([sys.executable, '-c', code], cwd=candidate, env=test_env(candidate),
                                  capture_output=True, text=True, encoding='utf-8', errors='replace',
                                  timeout=TEST_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            problems.append(f'{code}: did not finish within {TEST_TIMEOUT_SECONDS} s')
            continue
        if proc.returncode:
            lines = [l for l in proc.stderr.splitlines() if l.strip()]
            problems.append(f'{code}: {lines[-1][:300] if lines else "import failed"}')
    return problems


def push_to_continue(session_config, workspace, output, run_agent, rounds):
    """Send fresh sessions back to the repository while imports fail. Returns one record per round.
    A round that leaves more broken imports than before is undone (step 07: one round turned 2 into 7)."""
    candidate = workspace / 'candidate'
    template = (PROMPTS / 'during_work/push_to_continue.txt').read_text(encoding='utf-8')
    records = []
    problems = import_problems(candidate)
    for round_ in range(1, rounds + 1):
        if not problems:
            break
        out = output / 'retries' / f'push-{round_}'
        out.mkdir(parents=True)
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = Path(tmp) / 'candidate'
            shutil.copytree(candidate, snapshot, symlinks=True)
            run_agent(session_config, workspace, out,
                      template.format(problems='\n'.join(f'- {p}' for p in problems[:MAX_FAILURE_LINES])))
            after = import_problems(candidate)
            kept = len(after) <= len(problems)
            if not kept:
                restore(snapshot, candidate)
        records.append({'push': round_, 'problems_before': len(problems), 'problems_after': len(after),
                        'kept': kept, 'problems': problems[:MAX_FAILURE_LINES]})
        print(f'push {round_}: {len(problems)} -> {len(after)} import problems ({"kept" if kept else "undone"})',
              flush=True)
        if kept:
            problems = after
    return records


def score(candidate, tests):
    results = [run_test_file(candidate, t) for t in tests]
    return sum(r[0] for r in results), sum(r[1] for r in results), [l for r in results for l in r[2]]


def restore(snapshot, candidate):
    shutil.rmtree(candidate)
    shutil.copytree(snapshot, candidate, symlinks=True)


def isolated_session(config, workspace, out, prompt, module, run_agent):
    """Run one agent session that may change only `module`: every other file is put back as it was."""
    candidate = workspace / 'candidate'
    out.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        snapshot = Path(tmp) / 'candidate'
        shutil.copytree(candidate, snapshot, symlinks=True)
        run_agent(config, workspace, out, prompt)
        new_module = (candidate / module).read_bytes() if (candidate / module).exists() else None
        restore(snapshot, candidate)
        if new_module is not None:
            (candidate / module).parent.mkdir(parents=True, exist_ok=True)
            (candidate / module).write_bytes(new_module)


def retry_failing(config, workspace, output, run_agent):
    """Run push to continue, then the per-module retries; returns one record per round and attempt.
    run_agent(config, workspace, output, prompt)."""
    settings = config['retry']
    candidate = workspace / 'candidate'
    session_config = {**config, 'max_assistant_turns': settings['max_assistant_turns'],
                      'migration_timeout_seconds': settings['timeout_seconds']}
    records = push_to_continue(session_config, workspace, output, run_agent, settings.get('push_to_continue', 0))
    template = (PROMPTS / 'during_work/retry_module.txt').read_text(encoding='utf-8')
    for module, tests in module_tests(candidate).items():
        passed, total, failures = score(candidate, tests)
        for attempt in range(1, settings['attempts'] + 1):
            if passed == total:
                break
            with tempfile.TemporaryDirectory() as tmp:
                snapshot = Path(tmp) / 'candidate'
                shutil.copytree(candidate, snapshot, symlinks=True)
                prompt = template.format(module=module, tests='\n'.join(f'- {t}' for t in tests),
                                         passed=passed, total=total,
                                         failures='\n'.join(f'- {l}' for l in failures[:MAX_FAILURE_LINES]))
                name = module.removeprefix('src/').replace('/', '.')
                isolated_session(session_config, workspace, output / 'retries' / f'{name}-{attempt}', prompt,
                                 module, run_agent)
                new_passed, new_total, new_failures = score(candidate, tests)
                kept = new_passed > passed
                if not kept:
                    restore(snapshot, candidate)
            records.append({'module': module, 'attempt': attempt, 'before': passed, 'after': new_passed,
                            'total': total, 'kept': kept})
            print(f'retry {module} #{attempt}: {passed} -> {new_passed} of {total} ({"kept" if kept else "dropped"})',
                  flush=True)
            if kept:
                # A test file that could not be loaded counted as 1; now its real number of tests is known.
                passed, total, failures = new_passed, new_total, new_failures
    return records
