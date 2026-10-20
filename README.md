# Java → Python migration harness

A harness around a coding agent (the [Pi SDK](https://www.npmjs.com/package/@earendil-works/pi-coding-agent)) that
migrates small Java repositories to Python, plus a frozen evaluation that scores each migration with hidden tests.
The task is described in [docs/challenge.pdf](docs/challenge.pdf).

## Layout

```
test_repositories/<repo>/  repository/ (Java), public_tests/ (the agent sees these), hidden_tests/ (scoring only),
                           project_structure.txt (the Python files to create), oracle/ (reference Python port, if any)
evaluation/                the frozen scorer (evaluate.py), its test list (manifest.json), the repo split, validate.py
harness/                   src/ (run.py is the entry point; agent.mjs drives the Pi agent), prompts/, package.json
results/<step>/            one folder per step of the journey: config.json, runs/ (score summaries), README.md
```

## How we measure

Each hidden test file is scored in its own pytest run (120 s per file), so a file that cannot be imported costs
only its own tests, not the whole repo. Two numbers per run: passable hidden tests passed (passable = the reference
port passes them), and successful migrations (repos where every passable test passes). `evaluation/validate.py`
proves the scorer: every reference port scores 100% of passable tests, empty code scores 0%.

## Run it

Needs Linux, Python 3.12+ and Node 22.

```bash
python -m pip install -r evaluation/requirements.txt
(cd harness && npm ci)
cp .env.example .env        # then put your DeepSeek key in .env

python harness/src/run.py --split development --config results/00_baseline/config.json
python evaluation/validate.py
```

`--split` is one of `sanity`, `development`, `holdout`, `hard`, `big` (see `evaluation/split.json`);
`--repos a b` runs single repos. Raw output goes to `runs/<name>/` (git-ignored).

## Journey

| Step | Change | Run 1 | Run 2 | Decision |
|---|---|---|---|---|
| [00 baseline](results/00_baseline/) | plain Pi agent (read, bash, edit, write), 40 turns, 600 s, plain prompt | 175 | 164 | starting point (mean 169.5 of 184) |
| [01 robustness](results/01_robustness/) | 120 s per shell command; resume after a provider error or output-limit cut | 169 | 169 | keep: no change on dev (mean 169.0), removes two ways to lose a repo run |
| [02 sandbox](results/02_sandbox/) | agent sees only its workspace; inputs and /usr read-only; no network for commands | 161 | 163 | keep: integrity (mean 162.0, mostly noise) |
| [03 robustness v2](results/03_robustness_v2/) | start in candidate/; candidate/candidate link; loop breaker | 162 | 171 | keep: guards never fired with DeepSeek (mean 166.5) |
