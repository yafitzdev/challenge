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
cp .env.example .env        # then put your DeepSeek and OpenRouter keys in .env

python harness/src/run.py --split development --config results/00_baseline/config.json
python evaluation/validate.py
```

`--split` is one of `sanity`, `development`, `holdout`, `hard`, `big` (see `evaluation/split.json`);
`--repos a b` runs single repos. Raw output goes to `runs/<name>/` (git-ignored).

## Journey

Two parts. Part 1 makes the harness measure honestly, with a strong model (DeepSeek flash, 6 development repos,
184 passable hidden tests, 2 runs per step). Part 2 makes it help a weak model (Gemini 2.5 Flash Lite, 3
development repos, 113 tests, 1 run per step, to save money). Each step builds on the one before.

### Part 1: a trustworthy harness (strong model)

| Step | Change | Run 1 | Run 2 | Decision |
|---|---|---|---|---|
| [00 baseline](results/00_baseline/) | plain Pi agent (read, bash, edit, write), 40 turns, 600 s, plain prompt | 175 | 164 | starting point (mean 169.5 of 184) |
| [01 robustness](results/01_robustness/) | 120 s per shell command; resume after a provider error or output-limit cut | 169 | 169 | keep: no change on dev (mean 169.0), removes two ways to lose a repo run |
| [02 sandbox](results/02_sandbox/) | agent sees only its workspace; inputs and /usr read-only; no network for commands | 161 | 163 | keep: integrity (mean 162.0, mostly noise) |

With a strong model on small repos, the score is about 90% from the start; part 1 is about trust, not points.

### Part 2: a harness that helps a weak model

| Step | Change | Run 1 | Run 2 |
|---|---|---|---|
| [03 baseline](results/03_weak_baseline/) | part 1's harness, weak model | 0 | |
| [04 robustness v2](results/04_robustness_v2/) | start in candidate/, candidate link, loop breaker | 16 | |
| [05 retry package](results/05_retry/) | push to continue while test imports fail (a round that breaks more is undone); retry failing modules | 34 | 31 |
| [06 decomposition package](results/06_decomposition/) | plan, then one short session per module with a self-test; retry as failure path | 66 | 46 |
| [07 tools package](results/07_tools/) | a run_tests tool with a short structured report | 38 | 37 (dropped) |

Steps 05 to 07 got a second run when push to continue was fixed (a round that broke imports was kept); per-repo
numbers are in each step's README.

Final harness: step 06. The tools package (07) did not help and was dropped. With the weak model every step adds points, and decomposition gives the largest jump
(mean 32.5 -> 56.0): a session that only has to port one class, with that class's tests in front of it, gets it right far
more often.

### Holdout check

[09](results/09_holdout/): the final harness against part 2's baseline on the 5 holdout repos no step looked at,
Gemini, 1 run, 184 tests: **24 -> 55**, one repo fully migrated. The largest repo (ElSql, 97 tests) stays 0 in both:
its plan session wrote no plan.

### Known gaps

- An empty plan leaves decomposition with nothing to split (holdout, ElSql).
- 1 or 2 runs per part-2 step: the same config varied by 20 tests (step 06), so only large differences count.
