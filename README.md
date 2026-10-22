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
model's weaknesses, and adds fix packages for them. Every step is also scored on holdout repositories, which were
never used to decide what to keep.

---

<details>
<summary><strong>Phase 1: the dumb harness</strong></summary>

<br />

The starting point is deliberately plain: hand an existing coding agent a Java repository and one prompt, let it work,
then score what it wrote. No checks, no retries, no isolation.

**The agent** 

[Pi](https://www.npmjs.com/package/@earendil-works/pi-coding-agent) (`@earendil-works/pi-coding-agent`
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

**The test bench** 

13 small Java repositories from RepoTransBench, a public Java → Python migration benchmark. Each
comes with public tests (the agent may read and run them) and hidden tests (only the scorer runs them). The
repositories were split at random with a fixed seed ([evaluation/split.json](evaluation/split.json)), each group with
one job:

| Group | Repos | Job |
|---|---|---|
| sanity | 2 | tiny; only checks that the harness runs at all |
| development | 6 | the repos we run, read the failures of, and tune on |
| holdout | 5 | never used to decide what to keep; only for checks |

**The score** 

The frozen evaluator ([evaluation/evaluate.py](evaluation/evaluate.py)) replaces every test file the
agent wrote with the frozen originals, then runs each public and hidden test file on its own (120 s per file), so one
file that cannot be imported costs only its own tests. A test counts only if the reference Python port passes it
("passable"); [evaluation/validate.py](evaluation/validate.py) checks the scorer: every reference port scores 100%,
empty code 0%. Each test file runs isolated ([evaluation/isolate.sh](evaluation/isolate.sh)): no project folder, no
network, an unprivileged user; files in the candidate that would replace pytest or a standard-library module are
dropped first. Tests the reference port cannot pass are left out of scoring, each with its reason in
[evaluation/excluded_tests.json](evaluation/excluded_tests.json) (for example a test that expects `[]` where the
Java original returns `null`). Two numbers per run: **tests passed** (passable public and hidden tests together) and
**successful migrations** (repos where every passable test passes).

| Test set | All tests | Passable tests | of which hidden | of which public |
|---|---|---|---|---|
| 6 development repos (phase 2) | 232 | 184 | 109 | 75 |
| 3 development repos (phase 3: geohash, route53, Contacts) | 139 | 113 | 73 | 40 |
| 5 holdout repos | 244 | 184 | 145 | 39 |

</details>

---

<details>
<summary><strong>Phase 2: strong model harness validation</strong></summary>

<br />

Run the dumb harness with a strong model (DeepSeek flash). When a strong model fails, the cause is usually the
harness, not the model, so its failures expose harness flaws. Fix each flaw, run again, keep the fix if the run shows
it works. Development: 6 development repos (184 tests), average of 2 runs per step (3 for the dumb harness). Holdout:
the 5 holdout repos (184 tests), 1 run per step.

| Note           | Step                                   | Flaw found                                                                                                               | Fix                                                                                                                                              | Development   | Holdout |
|----------------|----------------------------------------|--------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|---------------|---------|
| ⭐ Checkpoint 0 | [dumb harness](results/00_baseline/)   |                                                                                                                          |                                                                                                                                                  | 159.0         | 173     |
|                | [+ robustness](results/01_robustness/) | one shell command that never returned used up the whole session; an answer cut off at the output limit ended the session | every shell command is stopped after 120 s; after an API error or a cut-off answer the agent is sent on with a short note, up to 3 times         | 169.0         | 179     |
|                | [+ sandbox](results/02_sandbox/)       | the agent's `find /` listed the reference ports: nothing stopped it from reading the answers                             | Linux namespaces: the agent sees only its workspace; Java source, public tests and the system Python are read-only; its commands have no network | 162.0         | 179     |
| ⭐ Checkpoint 1 | basic harness | | | 162.0         | 179     |

The score stays between 86% and 92% (the differences are mostly run-to-run noise): a strong model on small repos needs
little help. The dumb harness's lowest run (138) lost a whole repo when an over-long answer ended the session; that is
what the robustness fix targets. What phase 2 delivers is a harness that cannot lose a run to a stuck command or a
cut-off answer, and cannot be fooled by an agent that reads the answers. This is checkpoint 1, the **basic harness** that phase 3 starts from.

</details>

---

<details>
<summary><strong>Phase 3: weak model harness improvement</strong></summary>

<br />

Run the basic harness with a weak model (Gemini 2.5 Flash Lite). It fails a lot, which shows where the harness can
make up for the model's weaknesses. Add one fix package per weakness, run again, keep it only if it helps. To save
money: development = 3 of the development repos (113 tests), average of 1 or 2 runs per step. Holdout: the 5
holdout repos (184 tests), 1 run per step.

| Note          | Step                                         | Weakness found                                                                                  | Fix package                                                                                                                                                                                                                                                                                                                                            | Development   | Holdout |
|---------------|----------------------------------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|---------|
| ⭐ Checkpoint 1 | [basic harness](results/03_weak_baseline/)   |                                                                                                 |                                                                                                                                                                                                                                                                                                                                                        | 0             | 24      |
|               | [+ robustness v2](results/04_robustness_v2/) | writes its code next to `candidate/`, where nothing is scored; repeats one failing command      | • tools start inside `candidate/`<br>• a link `candidate/candidate → candidate/` catches doubled paths<br>• a note after the same command fails 3 times with the same error                                                                                                                                                                            | 16            | 0       |
|               | [+ retry](results/05_retry/)                 | says it is done while modules or classes are missing; one missing class fails a whole test file | • the harness tries every import of the public tests (no model call)<br>• while one fails, a fresh session gets the exact errors, up to 3 times; a round that breaks more is undone<br>• a module whose public tests fail is rewritten by a fresh session that may change only that file, up to 2 times<br>• a rewrite is kept only if more tests pass | 32.5          | 45      |
|               | [+ decomposition](results/06_decomposition/) | one session has to port the whole repo and loses track                                          | • the harness lists the modules to write, from `project_structure.txt` and the modules the public tests import (a plan session is asked too, but never produced a usable list)<br>• one short session (15 turns) per listed module, package files last<br>• each session finds its Java class in `../source/` and sees the modules already written and its public tests<br>• each ports the Java unit test of its class as a self-check<br>• retry as the failure path | 56.0          | 55      |
| 🌟 Checkpoint 2 | final harness                                |                                                                                                 |                                                                                                                                                                                                                                                                                                                                                        | 56.0          | 55      |

Robustness v2, retry and decomposition were kept, each on top of the one before. Decomposition gives the largest jump
(32.5 → 56.0): a session that only has to port one module, with that module's tests in front of it, gets it right far
more often. The gain is uneven: it comes from geohash and Contacts, where the module list had 14 and 5 entries. On
route53 the list held only package files, so decomposition changed little there. The module list is the harness's
own: in all 11 repo runs of the final harness the model's plan session produced no usable entry. Robustness v2 rests on
one development run, and its gain came from one repo (geohash, 0 → 16). Per-repo numbers and failure analyses are in
each step's README.

**Tried and dropped.** Three more packages were each tried on top of the final harness (development 56.0, holdout 55).
None beat it, so each was removed again.

| Note          | Step                                         | Weakness found                                                                                  | Fix package                                                                                                                                                                                                                                                                                                                                            | Development   | Holdout |
|---------------|----------------------------------------------|-------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|---------|
| ✗ dropped     | [+ tools](results/07_tools/)                 | reads pages of raw pytest output and misreads them                                              | • a `run_tests` tool that returns a short test report                                                                                                                                                                                                                                                                                                  | 37.5          | 46      |
| ✗ dropped     | [+ Java tools](results/08_java_tools/)       | guesses Java file paths that don't exist (382 of about 1,100 reads failed); leaves out Java methods or names them differently | • `java_api`: a Java class's members with Python names<br>• `port_check`: members a module still lacks                                                                                                                                                                                                                                                 | 37.0          | 40      |
| ✗ dropped     | [+ instructions](results/09_instructions/)   | repeats the same Java → Python mistakes: missing modules and names, static members made instance members, nested types flattened | • a Java → Python rule sheet in every session, built from the most common test errors                                                                                                                                                                                                                                                                  | 46.5          | 35      |


</details>

---

## Results

Phase 3 with the weak model (Gemini 2.5 Flash Lite), starting from the basic harness that phase 2 built with the
strong model, averaged over the runs of a step. Tests = passable tests passed. Migrations = successful migrations,
repos where every passable test passes. Development: the 3 development repos of phase 3 (113 tests). Holdout: the 5
holdout repos (184 tests); the runs of the basic and the final harness are in [results/10_holdout](results/10_holdout/),
the others under each step's `runs/holdout.json`.

| Note | Step | Development tests (113) | Development migrations (of 3) | Holdout tests (184) | Holdout migrations (of 5) |
|---|---|---|---|---|---|
| ⭐ Checkpoint 1 | basic harness | 0 | 0 | 24 | 0 |
| | + robustness v2 | 16 | 0 | 0 | 0 |
| | + retry | 32.5 | 0 | 45 | 1 |
| | + decomposition | 56.0 | 0 | 55 | 1 |
| 🌟 Checkpoint 2 | final harness | 56.0 | 0 | 55 | 1 |

Holdout scores are single runs. Without retry, one early stop or a session cut off at the turn limit costs a whole
repo (robustness v2: 0); from retry on the scores stay high.

How the holdout was used: what to keep was decided on the development repos only. The final harness's holdout run
(55) was made once step 06 was chosen, before the dropped packages were tried; the holdout runs of the other steps
were added at the end, with the code as it is in this repo.

---

## Limits

- **Few runs.** Development scores are averages of 1 to 3 runs, holdout scores single runs. Runs of the same setup
  differed by up to 37 tests (dumb harness: 175 and 138), so only large differences count.
- **The weak model never ports a development repo completely.** Even the final harness leaves failing tests in all 3
  (best: Contacts, 26 of 30). On the holdout it ports 1 of 5 completely (signaturepad, 18 of 18).
- **One holdout repo caps the holdout score, and that is a harness gap.** The biggest holdout repo, OpenGamma ElSql (a
  Java library that loads SQL from external files), holds 97 of the 184 holdout tests. With the weak model it scores 0
  at every kept step. In the final harness the reason is the module list: it came out as the package file only, so
  decomposition had nothing to split. In the dropped tools run, where the plan session did list its modules, it scored
  6. A fallback that lists one module per Java class is the next fix. The strong model ports it almost completely
  (95 to 97 of 97).
- **The loop-breaker note had a bug in every measured run.** It reached the agent with its placeholders unfilled
  (`{tool}`, `{count}`); fixed afterwards in agent.mjs, so this one note reads differently from the measured runs.
- **The scorer and the sandbox were hardened after the runs.** A review found two ways a candidate could fake a score
  (shipping its own `pytest` package; reading a reference port by its path while being scored), and that the agent,
  running as root, could undo the sandbox's mounts. All three are closed now: scoring and the retry checks run the
  candidate's code isolated, and the agent runs as an unprivileged user. No measured run used any of them: re-scoring
  all 122 stored repo runs with the hardened scorer gives the same result for every test, and every audit shows 0 reads
  of the reference ports.
- **The code changed between some runs.** The undo for a worse push round landed between run 1 and run 2 of steps
  05 to 07 (see their READMEs). From now on each run summary records the commit it ran with (`harness_commit`).

---

<details>
<summary><strong>Run it</strong></summary>

<br />

Needs Linux, Python 3.12+, Node 22, `unshare` and `mountpoint` (util-linux) and `timeout` (coreutils), and root for the
sandbox (from the sandbox step on; it uses mount namespaces). Phase 2 configs call DeepSeek (model `deepseek-flash`,
`DEEPSEEK_API_KEY`), phase 3 configs call Gemini 2.5 Flash Lite through OpenRouter (`google/gemini-2.5-flash-lite`,
`OPENROUTER_API_KEY`). A missing key stops the run; only where a proxy adds the key to every request, set
`HARNESS_KEY_FROM_PROXY=1`. All runs in this repo were made between 2026-10-20 and 2026-10-22.

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

`--split` is one of `sanity`, `development`, `holdout`; `--repos a b` runs single repos. All repos of a run work in
parallel (`--workers N` limits that); scoring then runs one repo at a time. Raw output goes to `runs/<name>/`
(git-ignored); each step's `results/<step>/` keeps its config, run summaries and README.

</details>


---
