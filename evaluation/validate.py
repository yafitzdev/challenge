"""Prove the frozen evaluator behaves before any agent runs.

Two checks per repo:
  1. The oracle (test_repositories/<repo>/oracle/, a reference Python port) must score as a successful migration
     (every passable test passes). Repos without an oracle (hard and big sets) skip this check.
  2. An empty candidate must pass no passable test (no fake tests left).

Usage: python evaluation/validate.py   -> writes evaluation/validation.json
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'evaluation'))
from evaluate import DATA, evaluate  # noqa: E402

manifest = json.loads((ROOT / 'evaluation/manifest.json').read_text())
rows, ok = [], True
for repo in manifest['cases']:
    oracle = evaluate(repo, DATA / repo / 'oracle') if (DATA / repo / 'oracle').exists() else None
    with tempfile.TemporaryDirectory() as empty:
        blank = evaluate(repo, Path(empty))
    good = (oracle is None or oracle['successful_migration']) and blank['passable_passed'] == 0
    ok &= good
    rows.append({'repo': repo, 'oracle_passable': f"{oracle['passable_passed']}/{oracle['passable_total']}" if oracle
                 else 'no oracle', 'empty_passable': f"{blank['passable_passed']}/{blank['passable_total']}", 'ok': good})
    print(rows[-1])
(ROOT / 'evaluation/validation.json').write_text(json.dumps({'all_ok': ok, 'repos': rows}, indent=2) + '\n')
sys.exit(0 if ok else 1)
