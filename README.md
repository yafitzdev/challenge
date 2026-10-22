# Exxeta take-home challenge

### A Java → Python migration harness

---

## Summary

The task ([docs/challenge.pdf](docs/challenge.pdf)): build a lean, reproducible harness that specializes an existing
coding agent for migrating whole repositories (here Java → Python), then improve it step by step and show with
measurements which change improved the agent's work. Building a new benchmark is explicitly not part of the task;
comparable, reproducible evaluation is.

---

## The journey

Three phases. Phase 1 builds the simplest possible harness. Phase 2 runs it with a strong model to find and fix flaws
in the harness itself. Phase 3 runs the fixed harness with a weak model to find where the harness can make up for the
model's weaknesses, and adds fix packages for them. After the phases, the results are checked on repositories that
were never used while building.

---

<details>
<summary><strong>Phase 1: the dumb harness</strong></summary>

<br />

The starting point is deliberately plain: hand an existing coding agent a Java repository and one prompt, let it work,
then score what it wrote. No checks, no retries, no isolation.

**The agent.** [Pi](https://www.npmjs.com/package/@earendil-works/pi-coding-agent) (`@earendil-works/pi-coding-agent`
1.3.0), an open-source coding agent, used as a library ([harness/src/agent.mjs](harness/src/agent.mjs)). It talks to the
model through an OpenAI-compatible API and has four tools: `read`, `write`, `edit` (exact text replacement) and `bash`.
One session, at most 40 turns (a turn is one model answer, usually one tool call) and 600 seconds, thinking off, one
plain prompt ([harness/prompts/task/baseline.txt](harness/prompts/task/baseline.txt)).

**One run, per repository** ([harness/src/run.py](harness/src/run.py)):

1. Stage a fresh workspace in a temp folder: `source/` (the Java repository), `candidate/` (where the Python goes; it
   holds `project_structure.txt`, the list of Python files to create, and the public tests) and `CONTRACT.txt` (how
   the result is scored). The hidden tests and the reference Python port are never copied in.
2. Run one agent session in that workspace.
3. Score `candidate/` with the frozen evaluator.

**The test bench.** 13 small Java repositories from RepoTransBench, a public Java → Python migration benchmark. Each
comes with public tests (the agent may read and run them) and hidden tests (only the scorer runs them). The
repositories were split at random with a fixed seed ([evaluation/split.json](evaluation/split.json)), each group with
one job:

| Group | Repos | Job |
|---|---|---|
| sanity | 2 | tiny; only checks that the harness runs at all |
| development | 6 | the repos we run, read the failures of, and tune on |
| holdout | 5 | never looked at while building; only for the final checks |

**The score.** The frozen evaluator ([evaluation/evaluate.py](evaluation/evaluate.py)) replaces every test file the
agent wrote with the frozen originals, then runs each public and hidden test file on its own (120 s per file), so one
file that cannot be imported costs only its own tests. A test counts only if the reference Python port passes it
("passable"); [evaluation/validate.py](evaluation/validate.py) proves the scorer: every reference port scores 100%,
empty code 0%. Two numbers per run: **tests passed** (passable public and hidden tests together) and **successful
migrations** (repos where every passable test passes).

| Test set | Passable tests | of which hidden | of which public |
|---|---|---|---|
| 6 development repos (phase 2) | 184 | 109 | 75 |
| 3 development repos (phase 3: geohash, route53, Contacts) | 113 | 73 | 40 |
| 5 holdout repos | 184 | 145 | 39 |

</details>

---

<details>
<summary><strong>Phase 2: strong model harness validation</strong></summary>

<br />

Run the dumb harness with a strong model (DeepSeek flash). When a strong model fails, the cause is usually the
harness, not the model, so its failures expose harness flaws. Fix each flaw, run again, keep the fix if the run shows
it works. Development: 6 development repos (184 tests), average score of 2 runs per step. Holdout: the 5 holdout
repos (184 tests), 1 run per step.

| Step | Flaw found | Fix | Development (184) | Holdout (184) |
|---|---|---|---|---|
| [00 dumb harness](results/00_baseline/) | | | 169.5 | 173 |
| [01 robustness](results/01_robustness/) | one shell command that never returned used up the whole session; an answer cut off at the output limit ended the session | every shell command is stopped after 120 s; after an API error or a cut-off answer the agent is sent on with a short note, up to 3 times | 169.0 | 179 |
| [02 sandbox](results/02_sandbox/) | the agent's `find /` listed the reference ports: nothing stopped it from reading the answers | Linux namespaces: the agent sees only its workspace; Java source, public tests and the system Python are read-only; its commands have no network | 162.0 | 179 |

The score stays at about 90% throughout (the differences are run-to-run noise): a strong model on small repos needs
little help. What phase 2 delivers is a harness that cannot lose a run to a stuck command and cannot be fooled by an
agent that reads the answers. Step 02 is the **harness baseline** for phase 3.

</details>

---

<details>
<summary><strong>Phase 3: weak model harness improvement</strong></summary>

<br />

Run the harness baseline with a weak model (Gemini 2.5 Flash Lite). It fails a lot, which shows where the harness can
make up for the model's weaknesses. Add one fix package per weakness, run again, keep it only if it helps. To save
money: 3 of the development repos (113 tests), average score of 1 or 2 runs per step.

| Step | Weakness found | Fix package | Average score |
|---|---|---|---|
| [03 harness baseline](results/03_weak_baseline/) | | • step 02 with the weak model | 0 |
| [04 robustness v2](results/04_robustness_v2/) | writes its code next to `candidate/`, where nothing is scored; repeats one failing command | • tools start inside `candidate/`<br>• a link `candidate/candidate → candidate/` catches doubled paths<br>• a note after the same command fails 3 times with the same error | 16 |
| [05 retry](results/05_retry/) | says it is done while modules or classes are missing; one missing class fails a whole test file | • the harness tries every import of the public tests (no model call)<br>• while one fails, a fresh session gets the exact errors, up to 3 times; a round that breaks more is undone<br>• a module whose public tests fail is rewritten by a fresh session that may change only that file, up to 2 times<br>• a rewrite is kept only if more tests pass | 32.5 |
| [06 decomposition](results/06_decomposition/) | one session has to port the whole repo and loses track | • one short session (15 turns) per Python module, in dependency order<br>• each sees only its Java class, the modules already written and its public tests<br>• each ports the Java unit test of its class as a self-check<br>• package files last<br>• retry (05) as the failure path | 56.0 |
| [07 tools](results/07_tools/) | | • a `run_tests` tool that returns a short test report | 37.5 |
| [08 Java tools](results/08_java_tools/) | | • `java_api`: a Java class's members with Python names<br>• `port_check`: members a module still lacks | 37.0 |
| [09 instructions](results/09_instructions/) | | • a Java → Python rule sheet in every session, built from the most common test errors | 46.5 |

Steps 04 to 06 were kept, each on top of the one before. 07 to 09 were each tried on top of 06, scored below it and
were removed. Decomposition gives the largest jump (32.5 → 56.0): a session that only has to port one class, with
that class's tests in front of it, gets it right far more often. The module list is the harness's own: on geohash the
model's plan session never produced a usable plan, and the harness built the list from `project_structure.txt` and
the modules the public tests import. Step 06 is the **final harness**. Per-repo numbers and failure analyses are in
each step's README.

</details>

---

## Results

Phase 3 with the weak model (Gemini 2.5 Flash Lite), starting from the harness baseline that phase 2 built with the
strong model. Score = passable tests passed, averaged over the runs of a step. Development: the 3 development repos of
phase 3 (113 tests). Holdout: the 5 repos never looked at while building (184 tests).

| Step | Average score, development (113) | Average score, holdout (184) |
|---|---|---|
| 02 harness baseline | 0 | 24 |
| 04 robustness v2 | 16 | 0 |
| 05 retry | 32.5 | 45 |
| 06 decomposition (final harness) | 56.0 | 55 |
| 07 tools (dropped) | 37.5 | 46 |
| 08 Java tools (dropped) | 37.0 | 40 |
| 09 instructions (dropped) | 46.5 | 35 |

---

<details>
<summary><strong>Run it</strong></summary>

<br />

Needs Linux, Python 3.12+, Node 22, and root for the sandbox (step 02 on; it uses mount namespaces). Phase 2 configs
call DeepSeek (`DEEPSEEK_API_KEY`), phase 3 configs call Gemini through OpenRouter (`OPENROUTER_API_KEY`).

```bash
python -m pip install -r evaluation/requirements.txt
(cd harness && npm ci)
cp .env.example .env        # then put your DeepSeek and OpenRouter keys in .env

python evaluation/validate.py                     # proves the scorer
python harness/src/run.py --split development --config results/00_baseline/config.json
python harness/src/run.py --repos kungfoo_geohash-java awslabs_route53-infima tamir7_Contacts \
    --config results/06_decomposition/config.json                         # final harness, phase 3 repos
python harness/src/run.py --split holdout --config results/06_decomposition/config.json   # final harness, holdout
```

`--split` is one of `sanity`, `development`, `holdout`; `--repos a b` runs single repos. Raw output goes
to `runs/<name>/` (git-ignored); each step's `results/<step>/` keeps its config, run summaries and README.

</details>


---
