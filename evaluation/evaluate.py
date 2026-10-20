"""Score one migrated repository against the frozen tests.

The candidate's own copies of the tests are thrown away and replaced with the frozen
ones, so an agent that edits or deletes tests gains nothing. Every test listed in the
manifest counts, so a test that is missing or never runs counts as failed.

v2 (2026-10-18, Yan's decision): each test file runs in its own pytest process. Before, one
file that failed to import stopped the whole run and every test of the repo counted as failed.
v3 (2026-10-19): new data layout, test_repositories/<repo>/{repository,public_tests,hidden_tests}; same files, same tests.

Usage:
    python evaluation/evaluate.py --repo aventrix_jnanoid --candidate path/to/candidate [--output result.json]
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'evaluation/manifest.json'
DATA = ROOT / 'test_repositories'
FILE_TIMEOUT_SECONDS = 120  # per test file
TEST_DIRS = ('hidden_tests', 'public_tests')
# Files a candidate could use to change how pytest or Python behaves, instead of writing real code.
TAMPER_FILES = {'conftest.py', 'pytest.ini', 'tox.ini', 'setup.cfg', 'pyproject.toml',
                'sitecustomize.py', 'usercustomize.py', 'pytest.py'}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def file_hashes(base, skip=()):
    """Hash of every file under base, except in the top-level folders named in skip."""
    return {p.relative_to(base).as_posix(): sha256(p) for p in sorted(Path(base).rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and p.relative_to(base).parts[0] not in skip}


def verify_data(manifest, repo):
    """Fail loudly if the frozen inputs on disk differ from what the manifest locked."""
    case = manifest['cases'][repo]
    if file_hashes(DATA / repo / 'repository') != case['repository_sha256']:
        raise SystemExit(f'{repo}: test_repositories/{repo}/repository does not match the manifest; the frozen inputs changed.')
    # The tests and project_structure.txt; the oracle is not an input of the evaluation.
    if file_hashes(DATA / repo, skip=('repository', 'oracle')) != case['tests_sha256']:
        raise SystemExit(f'{repo}: the tests in test_repositories/{repo} do not match the manifest; the frozen inputs changed.')


def stage(repo, candidate, work):
    """Copy the candidate's code, drop its tests and config files, add the frozen tests."""
    ignore = shutil.ignore_patterns('__pycache__', '.pytest_cache', *TEST_DIRS, *TAMPER_FILES)
    shutil.copytree(candidate, work, ignore=ignore)
    for name in TEST_DIRS:
        frozen = DATA / repo / name
        if frozen.exists():
            shutil.copytree(frozen, work / name)
    (work / 'pytest.ini').write_text('[pytest]\n', encoding='utf-8')  # our own empty config pins the rootdir


def node_id(work, classname, name):
    """Turn a JUnit (classname, name) pair back into a pytest node id like 'hidden_tests/x/test_a.py::TestA::test_b'."""
    if not classname:  # a file that failed to import is reported without a class; its tests count as missing
        return name
    parts = classname.split('.')
    for cut in range(len(parts), 0, -1):
        path = Path(*parts[:cut]).with_suffix('.py')
        if (work / path).is_file():
            return '::'.join([path.as_posix(), *parts[cut:], name])
    return f'{classname}::{name}'


def test_files(work):
    return sorted(p.relative_to(work).as_posix() for d in TEST_DIRS if (work / d).exists()
                  for p in (work / d).rglob('*.py') if p.name.startswith('test_') or p.name.endswith('_test.py'))


def run_pytest(work):
    """Run each test file in its own pytest process, so a file that fails to import (or hangs) only fails
    its own tests instead of stopping the whole run."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(('PYTHON', 'PYTEST'))}
    env.update(PYTHONPATH=os.pathsep.join([str(work), str(work / 'src')]), PYTHONHASHSEED='0',
               PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONIOENCODING='utf-8')
    outcomes, logs, timed_out = {}, [], False
    for i, test_file in enumerate(test_files(work)):
        report = work / f'.junit-{i}.xml'
        cmd = [sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--noconftest',
               f'--junitxml={report}', test_file]
        try:
            proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True,
                                  encoding='utf-8', errors='replace', timeout=FILE_TIMEOUT_SECONDS)
            logs.append(f'### {test_file}\n{proc.stdout}{proc.stderr}')
        except subprocess.TimeoutExpired:
            logs.append(f'### {test_file}\ntimed out after {FILE_TIMEOUT_SECONDS} s')
            timed_out = True
        if report.exists():
            for case in ET.parse(report).iter('testcase'):
                tags = {child.tag for child in case}
                status = 'failed' if tags & {'failure', 'error'} else 'skipped' if 'skipped' in tags else 'passed'
                outcomes[node_id(work, case.get('classname', ''), case.get('name', ''))] = status
    return outcomes, '\n'.join(logs), timed_out


def evaluate(repo, candidate):
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    verify_data(manifest, repo)
    case = manifest['cases'][repo]
    with tempfile.TemporaryDirectory(prefix='eval-') as tmp:
        work = Path(tmp) / repo
        stage(repo, Path(candidate), work)
        outcomes, log, timed_out = run_pytest(work)
    tests = {}
    for test in case['tests']:
        status = outcomes.get(test['id'], 'missing')  # skipped and missing both count as not passed
        tests[test['id']] = {'status': status, 'passable': test['passable']}
    passed = [t for t in tests.values() if t['status'] == 'passed']
    passable = [t for t in tests.values() if t['passable']]
    passable_passed = [t for t in passable if t['status'] == 'passed']
    return {
        'repo': repo,
        'tests_total': len(tests),
        'tests_passed': len(passed),
        'raw_pass_rate': len(passed) / len(tests),
        'passable_total': len(passable),
        'passable_passed': len(passable_passed),
        'passable_pass_rate': len(passable_passed) / len(passable),
        'successful_migration': len(passable_passed) == len(passable),
        'timed_out': timed_out,
        'tests': tests,
        'pytest_log_tail': log[-4000:],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--candidate', required=True, type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = evaluate(args.repo, args.candidate)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    summary = {k: v for k, v in result.items() if k not in ('tests', 'pytest_log_tail')}
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
