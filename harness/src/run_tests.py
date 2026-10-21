"""The run_tests tool (step 07): runs pytest the way the evaluation does and returns a short, structured
report instead of raw pytest output.

Raw output of a failing run is long, and a weak model reads the first screen and guesses. This report says:
how many passed and failed per test file, the one-line reason of each failure, and which modules the tests
tried to import but do not exist (with the file to create).

Usage: python harness/src/run_tests.py <candidate> [test path, default public_tests]
"""
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from retry import test_env  # noqa: E402  (the environment the evaluator uses)

TIMEOUT = 120
MAX_FAILURES = 25


def reason(node):
    """One line that says why a test failed: the exception line pytest marks with 'E', else the message."""
    text = node.text or ''
    e_lines = [l[1:].strip() for l in text.splitlines() if l.startswith('E ') and l[1:].strip()]
    line = e_lines[0] if e_lines else ((node.get('message') or node.tag).strip().splitlines() or [node.tag])[0]
    where = re.findall(r'^(src/[\w/]+\.py):(\d+)', node.text or '', re.M)
    suffix = f' (at {where[-1][0]}:{where[-1][1]})' if where else ''
    return (line[:300] + suffix).strip()


def missing_module(text):
    found = re.search(r"No module named '([\w.]+)'", text)
    return found.group(1) if found else None


def main():
    candidate = Path(sys.argv[1]).resolve()
    target = sys.argv[2] if len(sys.argv) > 2 else 'public_tests'
    with tempfile.TemporaryDirectory() as tmp:
        xml = Path(tmp) / 'report.xml'
        cmd = [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--tb=short', '--continue-on-collection-errors', f'--junitxml={xml}', target]
        try:
            proc = subprocess.run(cmd, cwd=candidate, env=test_env(candidate), capture_output=True, text=True,
                                  timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f'The tests did not finish within {TIMEOUT} s. Look for an endless loop, or run one file at a time.')
            return
        if not xml.exists():
            print('pytest could not run:\n' + (proc.stdout + proc.stderr)[-2000:])
            return
        root = ET.parse(xml).getroot()
    per_file = defaultdict(lambda: [0, 0])
    failures, missing = [], defaultdict(set)
    for case in root.iter('testcase'):
        # A file that cannot even be imported shows up as one error named after the file (collection failure).
        collection = not case.get('classname')
        file = case.get('file') or (case.get('name') if collection else case.get('classname')).replace('.', '/') + '.py'
        problem = next((c for c in case if c.tag in ('failure', 'error')), None)
        if case.find('skipped') is not None and problem is None:
            continue
        per_file[file][problem is not None] += 1
        if problem is not None:
            module = missing_module((problem.text or '') + (problem.get('message') or ''))
            if module:
                missing[module].add(file)
            elif collection:
                failures.append(f'{file}: the whole file cannot be loaded: {reason(problem)}')
            else:
                failures.append(f"{file}::{case.get('name')}: {reason(problem)}")
    passed = sum(p for p, _ in per_file.values())
    failed = sum(f for _, f in per_file.values())
    out = [f'{passed} passed, {failed} failed ({target})']
    if missing:
        out.append('\nMissing modules (tests cannot import them; create these files first):')
        for module, files in sorted(missing.items()):
            if module == 'src':
                out.append(f'- src: there is no src/ folder in {candidate.name}/ (needed by {len(files)} test file(s))')
                continue
            path = 'src/' + module.removeprefix('src.').replace('.', '/') + '.py'
            out.append(f'- {module} -> create {path} (needed by {len(files)} test file(s))')
    out.append('\nPer test file (a file that cannot be loaded counts as 1 failed):')
    out += [f'- {f}: {p} passed, {n} failed' for f, (p, n) in sorted(per_file.items())]
    if failures:
        out.append(f'\nFailures ({len(failures)}, first line of each error):')
        out += [f'- {f}' for f in failures[:MAX_FAILURES]]
        if len(failures) > MAX_FAILURES:
            out.append(f'- ... {len(failures) - MAX_FAILURES} more; run one test file to see them.')
    if not per_file:
        out.append((proc.stdout + proc.stderr)[-1500:])
    print('\n'.join(out))


if __name__ == '__main__':
    main()
