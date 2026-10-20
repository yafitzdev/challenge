"""Retry: after the agent stops, every module whose public tests fail is generated again by a fresh, short agent
session, up to `attempts` times. Only that one file may change, and the attempt is kept only if more of its tests
pass than before.

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


def run_test_file(candidate, test_file):
    """Run one public test file the way the evaluator does. Returns (passed, total, failure lines)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(('PYTHON', 'PYTEST'))}
    env.update(PYTHONPATH=os.pathsep.join([str(candidate), str(candidate / 'src')]), PYTHONHASHSEED='0',
               PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
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
    """{module file (relative to candidate/): [public test files that import it]}"""
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
            if name.startswith('src.') and len(name.split('.')) > 2:
                found.setdefault(name.replace('.', '/') + '.py', []).append(rel)
    return {m: sorted(set(t)) for m, t in found.items()}


def score(candidate, tests):
    results = [run_test_file(candidate, t) for t in tests]
    return sum(r[0] for r in results), sum(r[1] for r in results), [l for r in results for l in r[2]]


def retry_failing(config, workspace, output, run_agent):
    """Run the retry rounds; returns one record per attempt. run_agent(config, workspace, output, prompt)."""
    settings = config['retry']
    candidate = workspace / 'candidate'
    session_config = {**config, 'max_assistant_turns': settings['max_assistant_turns'],
                      'migration_timeout_seconds': settings['timeout_seconds']}
    template = (PROMPTS / 'during_work/retry_module.txt').read_text(encoding='utf-8')
    records = []
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
                out = output / 'retries' / f"{module.removeprefix('src/').replace('/', '.')}-{attempt}"
                out.mkdir(parents=True)
                run_agent(session_config, workspace, out, prompt)
                new_module = (candidate / module).read_bytes() if (candidate / module).exists() else None
                # Only the module may change: put every other file back as it was.
                shutil.rmtree(candidate)
                shutil.copytree(snapshot, candidate, symlinks=True)
                if new_module is not None:
                    (candidate / module).parent.mkdir(parents=True, exist_ok=True)
                    (candidate / module).write_bytes(new_module)
                new_passed, _, new_failures = score(candidate, tests)
                kept = new_passed > passed
                if not kept:
                    shutil.rmtree(candidate)
                    shutil.copytree(snapshot, candidate, symlinks=True)
            records.append({'module': module, 'attempt': attempt, 'before': passed, 'after': new_passed,
                            'total': total, 'kept': kept})
            print(f'retry {module} #{attempt}: {passed} -> {new_passed} of {total} ({"kept" if kept else "dropped"})',
                  flush=True)
            if kept:
                passed, failures = new_passed, new_failures
    return records
