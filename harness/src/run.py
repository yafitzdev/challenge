"""Run the migration agent on one or more repositories and score each result.

For every repository:
  1. Stage a fresh workspace outside the project folder:
       source/      the Java repository (test_repositories/<repo>/repository)
       candidate/   project_structure.txt + the public Python tests; the agent writes its code here
       CONTRACT.txt how the candidate will be scored
     The hidden tests (test_repositories/<repo>/hidden_tests) and the oracle are never copied in.
  2. Start one Pi session in that workspace (harness/src/agent.mjs).
  3. Score candidate/ with the frozen evaluator (evaluation/evaluate.py).
  4. Save everything under runs/<run-name>/<repo>/ (git-ignored; results/ keeps the score summaries).

Usage:
    python harness/src/run.py --split development --config results/00_baseline/config.json
    python harness/src/run.py --repos aventrix_jnanoid yankils_hello-world --config ... [--run-name NAME]
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / 'harness'
sys.path.insert(0, str(ROOT / 'evaluation'))
from evaluate import evaluate  # noqa: E402  (the frozen evaluator)
from decompose import PLAN_FILE, decompose  # noqa: E402
from retry import retry_failing  # noqa: E402

AGENT = HARNESS / 'src/agent.mjs'
# The cloud proxy injects the real key for the model API, so a placeholder is enough there.
DUMMY_KEY = 'dummy-key-replaced-by-proxy'

CONTRACT = """\
Evaluation contract

- Your Python implementation in candidate/ is scored with pytest after this session ends.
- Scoring uses the visible tests in candidate/public_tests/ AND additional hidden tests
  that check the same API more thoroughly. Implement the full Java behavior, not only
  what the visible tests touch.
- Before scoring, every test file, conftest.py and pytest config file in candidate/ is
  replaced by the frozen originals, so editing tests changes nothing.
- Tests run from candidate/ with PYTHONPATH=candidate:candidate/src and no network.
- Module paths and names must match candidate/project_structure.txt.
"""

# Every key a config may set. A typo would otherwise switch a setting off without anyone noticing.
CONFIG_KEYS = {
    'version', 'provider', 'api_key_env', 'model', 'base_url', 'thinking', 'max_output_tokens', 'tools',
    'automatic_retries', 'compaction', 'prompt_file', 'max_assistant_turns', 'migration_timeout_seconds',
    'command_timeout_seconds', 'resume_after_errors', 'sandbox',
    'start_in_candidate', 'candidate_link', 'loop_breaker', 'retry', 'decompose', 'rules',
}


def load_config(path):
    config = json.loads(path.read_text(encoding='utf-8'))
    unknown = sorted(config.keys() - CONFIG_KEYS)
    if unknown:
        raise SystemExit(f'{path}: unknown config keys {", ".join(unknown)}')
    return config


def api_key(config):
    """Real key from the environment or .env (Yan's PC); otherwise the proxy placeholder (cloud)."""
    var = config.get('api_key_env', 'DEEPSEEK_API_KEY')
    if os.environ.get(var):
        return os.environ[var]
    env_file = ROOT / '.env'
    if env_file.exists():
        for line in env_file.read_text(encoding='utf-8').splitlines():
            name, _, value = line.partition('=')
            if name.strip() == var and value.strip():
                return value.strip()
    return DUMMY_KEY


def stage(repo, workspace, config):
    data = ROOT / 'test_repositories' / repo
    shutil.copytree(data / 'repository', workspace / 'source')
    candidate = workspace / 'candidate'
    candidate.mkdir()
    shutil.copy2(data / 'project_structure.txt', candidate)
    shutil.copytree(data / 'public_tests', candidate / 'public_tests')
    (workspace / 'CONTRACT.txt').write_text(CONTRACT, encoding='utf-8')
    if config.get('candidate_link'):
        # Agents often write to candidate/... although their working directory already is candidate/. A link
        # candidate/candidate -> . makes those paths land in the right place; conftest.py keeps pytest from
        # following the link forever. Both are left out when the candidate is copied out.
        (candidate / 'candidate').symlink_to('.')
        (candidate / 'conftest.py').write_text("collect_ignore = ['candidate']  # added by the harness\n",
                                               encoding='utf-8')


def keep_candidate(folder, names):
    """What not to copy out of the workspace: caches, and the harness's own candidate link and conftest.py."""
    skip = {'__pycache__', '.pytest_cache'}
    return [n for n in names if n in skip or (Path(folder, n).is_symlink() and n == 'candidate')
            or (n == 'conftest.py' and Path(folder, 'candidate').is_symlink())]


def prompt_path(config):
    """Each config names its prompt file, so one config file fully describes a harness version."""
    return HARNESS / 'prompts' / config.get('prompt_file', 'task/baseline.txt')


def run_agent(config, workspace, output, prompt=None):
    # With a command limit, the agent's shell is a wrapper that stops any command running too long.
    limit = config.get('command_timeout_seconds')
    job = {'config': config, 'workspace': str(workspace), 'output': str(output),
           'bash': str(HARNESS / 'src/timeout-bash.sh') if limit else shutil.which('bash'),
           'prompt': prompt or prompt_path(config).read_text(encoding='utf-8'),
           # The custom tools' commands (agent.mjs); only used when the config lists the tool.
           'run_tests': [sys.executable, str(HARNESS / 'src/run_tests.py'), str(workspace / 'candidate')],
           'java_tools': [sys.executable, str(HARNESS / 'src/java_tools.py'), str(workspace)]}
    job_file = output / 'job.json'
    job_file.write_text(json.dumps(job, indent=2), encoding='utf-8')
    # NODE_USE_ENV_PROXY makes Node's fetch use HTTPS_PROXY when one is set (the cloud); no effect otherwise.
    env = {**os.environ, 'MODEL_API_KEY': api_key(config), 'NODE_USE_ENV_PROXY': '1'}
    if limit:
        env['HARNESS_COMMAND_TIMEOUT'] = str(limit)
    started = time.time()
    try:
        cmd = ['node', str(AGENT), str(job_file)]
        if config.get('sandbox'):
            # The agent sees only its workspace, its output folder and the harness code (sandbox.sh).
            cmd = ['bash', str(HARNESS / 'src/sandbox.sh'), str(HARNESS), str(output), str(workspace), *cmd]
        proc = subprocess.run(cmd, cwd=HARNESS, env=env,
                              capture_output=True, text=True, encoding='utf-8', errors='replace',
                              timeout=config['migration_timeout_seconds'] + 1000)  # room for rate-limit waits (agent.mjs)
        log, exit_code = proc.stdout + proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as e:
        log, exit_code = f'{e.stdout or ""}{e.stderr or ""}\nkilled: harness timeout', None
    (output / 'agent.log').write_text(log, encoding='utf-8')
    return exit_code, time.time() - started


def audit_events(output):
    """Flag tool calls that reached for things the agent must not use. A flag means: read the log."""
    # The main session's events plus those of every retry session (retries/<module>-<n>/events.jsonl).
    text = ''.join(f.read_text(encoding='utf-8') for f in sorted(output.rglob('events.jsonl')))
    patterns = {'oracles': r'/oracle\b', 'project_folder': r'challenge_v2|test_repositories',
                'hidden_tests': r'hidden_tests', 'package_install': r'pip install|npm install'}
    events = [json.loads(line) for line in text.splitlines()]
    calls = [json.dumps(e.get('args', '')) for e in events if e.get('type') == 'tool_execution_start']
    flags = {name: sum(bool(re.search(p, c)) for c in calls) for name, p in patterns.items()}
    # Also scan what came back: a broad command like `find /` can show project paths without naming them.
    outputs = [json.dumps(e.get('result', '')) for e in events if e.get('type') == 'tool_execution_end']
    flags['output_shows_project'] = sum(bool(re.search(r'/oracle/|hidden_tests/|challenge_v2|test_repositories', o))
                                        for o in outputs)
    return flags


def migrate_repo(repo, config, run_dir):
    """Phase 1: stage a workspace, run the agent, keep its candidate. Safe to run in parallel (API-bound)."""
    output = run_dir / repo
    output.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix='migrate-') as tmp:
        workspace = Path(tmp) / 'workspace'
        workspace.mkdir()
        stage(repo, workspace, config)
        started = time.time()
        if config.get('decompose'):
            # One short session per module instead of one long session (decompose.py).
            plan = decompose(config, workspace, output, run_agent)
            plan_file = workspace / 'candidate' / PLAN_FILE
            if plan_file.exists():
                shutil.move(plan_file, output / PLAN_FILE)
            (output / 'decompose.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
            exit_code, seconds = 0, 0
        else:
            exit_code, seconds = run_agent(config, workspace, output)
        if config.get('retry'):
            # Modules whose public tests still fail get fresh, short sessions (retry.py).
            retries = retry_failing(config, workspace, output, run_agent)
            (output / 'retries.json').write_text(json.dumps(retries, indent=2) + '\n', encoding='utf-8')
        shutil.copytree(workspace / 'candidate', output / 'candidate',
                        ignore=keep_candidate)
        seconds = time.time() - started
    print(f'{repo}: agent done in {seconds:.0f}s', flush=True)
    return exit_code, seconds


def score_repo(repo, run_dir, exit_code, seconds):
    """Phase 2: score one candidate with the frozen evaluator. Run one repo at a time."""
    output = run_dir / repo
    score = evaluate(repo, output / 'candidate')
    (output / 'score.json').write_text(json.dumps(score, indent=2) + '\n', encoding='utf-8')
    agent = json.loads((output / 'agent-result.json').read_text(encoding='utf-8')) \
        if (output / 'agent-result.json').exists() else {}
    row = {'repo': repo, 'agent_exit_code': exit_code, 'agent_seconds': round(seconds, 1),
           'agent_completed': agent.get('completed'), 'agent_limit': agent.get('limit'),
           'agent_error': agent.get('error'), 'assistant_turns': agent.get('assistant_turns'),
           'usage': agent.get('usage'), 'resumes': agent.get('resumes'),
           'decompose': json.loads((output / 'decompose.json').read_text(encoding='utf-8'))
           if (output / 'decompose.json').exists() else None,
           'retries': json.loads((output / 'retries.json').read_text(encoding='utf-8'))
           if (output / 'retries.json').exists() else None, 'audit': audit_events(output),
           **{k: score[k] for k in ('tests_passed', 'tests_total', 'raw_pass_rate', 'passable_passed',
                                    'passable_total', 'passable_pass_rate', 'successful_migration')}}
    print(json.dumps({k: row[k] for k in ('repo', 'passable_passed', 'passable_total',
                                          'successful_migration', 'agent_limit', 'audit')}), flush=True)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--split', choices=['sanity', 'development', 'holdout'])
    group.add_argument('--repos', nargs='+')
    parser.add_argument('--config', type=Path, required=True, help='an experiment config, e.g. results/00_baseline/config.json')
    parser.add_argument('--run-name')
    parser.add_argument('--workers', type=int, help='agents running at the same time (default: all repos)')
    args = parser.parse_args()

    split = json.loads((ROOT / 'evaluation/split.json').read_text(encoding='utf-8'))
    repos = split[args.split] if args.split else args.repos
    config = load_config(args.config)
    name = args.run_name or f"{datetime.now(timezone.utc):%Y%m%d-%H%M%S}-{config['version']}-{args.split or 'custom'}"
    run_dir = ROOT / 'runs' / name
    run_dir.mkdir(parents=True)
    (run_dir / 'config.json').write_text(json.dumps(config, indent=2), encoding='utf-8')
    shutil.copy2(prompt_path(config), run_dir / 'prompt.txt')

    # The agents only wait on the model API, so they run in parallel; scoring runs pytest, so it stays sequential.
    with ThreadPoolExecutor(max_workers=args.workers or len(repos)) as pool:
        agent_runs = list(pool.map(lambda repo: migrate_repo(repo, config, run_dir), repos))
    rows = [score_repo(repo, run_dir, *agent_run) for repo, agent_run in zip(repos, agent_runs)]
    passed = sum(r['tests_passed'] for r in rows)
    total = sum(r['tests_total'] for r in rows)
    p_passed = sum(r['passable_passed'] for r in rows)
    p_total = sum(r['passable_total'] for r in rows)
    summary = {'run': name, 'config': config['version'], 'repos': repos,
               'successful_migrations': sum(r['successful_migration'] for r in rows),
               'raw_pass_rate': passed / total, 'passable_pass_rate': p_passed / p_total,
               'per_repo': rows}
    (run_dir / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k != 'per_repo'}, indent=2))


if __name__ == '__main__':
    main()
