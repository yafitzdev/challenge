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

Needs Linux, Python 3.12+ and Node 22, and root for the sandbox (step 02 on; it uses mount namespaces). Part 1
configs call DeepSeek (`DEEPSEEK_API_KEY`), part 2 configs call Gemini through OpenRouter (`OPENROUTER_API_KEY`).

```bash
python -m pip install -r evaluation/requirements.txt
(cd harness && npm ci)
cp .env.example .env        # then put your DeepSeek and OpenRouter keys in .env

python evaluation/validate.py                     # proves the scorer
python harness/src/run.py --split development --config results/00_baseline/config.json
python harness/src/run.py --repos kungfoo_geohash-java awslabs_route53-infima tamir7_Contacts \
    --config results/06_decomposition/config.json                         # final harness, part 2 dev repos
python harness/src/run.py --split holdout --config results/06_decomposition/config.json   # final harness, holdout
```

`--split` is one of `sanity`, `development`, `holdout`, `hard`, `big` (see `evaluation/split.json`);
`--repos a b` runs single repos. Raw output goes to `runs/<name>/` (git-ignored).

## Journey

Two parts. Part 1 makes the harness measure honestly, with a strong model (DeepSeek flash, 6 development repos,
184 passable hidden tests, 2 runs per step). Part 2 makes it help a weak model (Gemini 2.5 Flash Lite, 3
development repos, 113 tests, 1 or 2 runs per step, to save money). Each kept step builds on the one before;
a dropped step is measured on top of step 06 and then removed.

### Part 1: a trustworthy harness (strong model)

| Step | Change | Run 1 | Run 2 | Decision |
|---|---|---|---|---|
| [00 baseline](results/00_baseline/) | plain Pi agent (read, bash, edit, write), 40 turns, 600 s, plain prompt | 175 | 164 | starting point (mean 169.5 of 184) |
| [01 robustness](results/01_robustness/) | 120 s per shell command; resume after a provider error or output-limit cut | 169 | 169 | keep: no change on dev (mean 169.0), removes two ways to lose a repo run |
| [02 sandbox](results/02_sandbox/) | agent sees only its workspace; inputs and /usr read-only; no network for commands | 161 | 163 | keep: integrity (mean 162.0, mostly noise) |

With a strong model on small repos, the score is about 90% from the start; part 1 is about trust, not points.

### Part 2: a harness that helps a weak model

| Step | Change | Run 1 | Run 2 | Decision |
|---|---|---|---|---|
| [03 baseline](results/03_weak_baseline/) | part 1's harness, weak model | 0 | | starting point |
| [04 robustness v2](results/04_robustness_v2/) | start in candidate/, candidate link, loop breaker | 16 | | keep |
| [05 retry package](results/05_retry/) | push to continue while test imports fail (a round that breaks more is undone); retry failing modules | 34 | 31 | keep (mean 32.5) |
| [06 decomposition package](results/06_decomposition/) | plan, then one short session per module with a self-test; retry as failure path | 66 | 46 | keep, final (mean 56.0) |
| [07 tools package](results/07_tools/) | a run_tests tool with a short structured report | 38 | 37 | drop (mean 37.5) |
| [08 tools package v2](results/08_java_tools/) | java_api (Java class API with Python names) and port_check (Java members a module lacks) | 43 | 31 | drop (mean 37.0) |
| [09 instructions package](results/09_instructions/) | a Java-to-Python rule sheet in every session, built from the most common test errors | 48 | 45 | drop (mean 46.5) |

Run 2 of steps 05 to 07 came after a fix to push to continue: in the first version, a round that broke more imports
was kept, now it is undone. Per-repo numbers and failures are in each step's README.

Final harness: step 06. Every kept step adds points, and decomposition gives the largest jump (mean 32.5 -> 56.0):
a session that only has to port one class, with that class's tests in front of it, gets it right far more often.
The tools packages (07, 08) and the instructions package (09) scored below 06 and were dropped: the weak model
used the tools and saw the rules, but extra instructions and tool output did not make its ports more complete.

Successful migrations (every passable test passes): part 1, 2 or 3 of 6 repos per run; part 2, none of the 3
repos in any run, so the test pass rate is the measure there (06: 58.4% and 40.7% of 113 tests).

### Holdout check

[10](results/10_holdout/): on the 5 holdout repos no step looked at, Gemini, 1 run each, 184 tests: the plain agent
with none of our fixes **16**, part 1's harness **24**, the final harness **55** (8.7% -> 13.0% -> 29.9%);
successful migrations 0 -> 0 -> 1 of 5. The largest repo (ElSql, 97 tests) stays 0 in all three: its plan session
wrote no plan.

### What caused what

| Change | Effect | Evidence |
|---|---|---|
| 01 command timeout, resume after errors | no change on dev; a repo run is no longer lost to a hung command | jnanoid: a hung test command was stopped after 120 s, 9 -> 21 of 22 |
| 02 sandbox | score unchanged (noise); the agent can no longer see the reference ports or hidden tests | in step 01 a `find /` listed reference ports; since step 02 the run audit counts no read of ports or hidden tests |
| 04 start in candidate/, link, loop breaker | 0 -> 16 | the weak model had written its code outside candidate/, where nothing is scored |
| 05 push to continue, module retries | 16 -> 32.5 | route53 0 -> 18 in run 1 once the missing `Lattice` import was pushed; Contacts 0 -> 16 and 9 |
| 06 decomposition | 32.5 -> 56.0; holdout 24 -> 55 | one short session per class: Contacts 24 and 26 of 30, signaturepad 18 of 18 |

Limits: 1 or 2 runs per part-2 step, and the same config varied by 20 tests (06: 66 and 46), so only differences
well above that count. With the weak model no development repo was fully migrated in any run.

### What still fails (weak model)

From the error tally over all Gemini runs ([09](results/09_instructions/)):

- Missing modules or names: a test imports something the port never wrote or re-exported (`ModuleNotFoundError`
  95 times, `cannot import name` about 30).
- Static members turned into instance members, or left out (`type object 'X' has no attribute 'y'`, 61 times).
- Incomplete classes: the class exists but lacks Java methods (route53: `Lattice` has no `get_all_endpoints`).
- Nested types and enums flattened or renamed (Contacts: `PhoneNumber.Type`).

### Known gaps

- An empty plan leaves decomposition with nothing to split (holdout, ElSql).
- 1 or 2 runs per part-2 step: the same config varied by 20 tests (step 06), so only large differences count.
