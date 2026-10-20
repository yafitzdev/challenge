# 05 Decomposition

Instead of one long session for the whole repository, the work is split into small requests
([decompose.py](../../harness/src/decompose.py)). Thesis: smaller requests mean less context, fewer
hallucinations, better code.

1. **Plan.** A short session (15 turns) reads the Java repository and writes plan.json: one entry per Python
   module, with the Java file it ports and the modules it depends on
   ([decompose_plan.txt](../../harness/prompts/task/decompose_plan.txt)). The harness adds every module that
   project_structure.txt lists or a public test imports, so the plan cannot leave out a module the tests need.
2. **Modules.** In dependency order, a fresh session (15 turns, 300 s) writes one module
   ([write_module.txt](../../harness/prompts/during_work/write_module.txt)). It is told which modules already exist
   and which public tests cover this one. Only that one file is kept from the session. Package `__init__.py` files
   that the tests import from come last.
3. **Retry** (step 04) as the failure path: a module whose public tests still fail is written again, up to 2 times.

Config: [config.json](config.json) (step 04 plus `decompose`). Run summaries: [runs/](runs/).

## Result

6 development repos, 184 passable hidden tests.

| Repo | Step 04 run 1 | Step 04 run 2 | Run 1 | Run 2 |
|---|---|---|---|---|
| shekhargulati_30-seconds-of-java | 7/7 | 7/7 | 7/7 | 7/7 |
| nzakas_props2js | 32/38 | 38/38 | 38/38 | 38/38 |
| tasomaniac_DelayedProgress | 22/26 | 18/26 | 18/26 | 18/26 |
| awslabs_route53-infima | 41/42 | 40/42 | 33/42 | 34/42 |
| kungfoo_geohash-java | 35/41 | 33/41 | 35/41 | 36/41 |
| tamir7_Contacts | 30/30 | 28/30 | 24/30 | 30/30 |
| **Total** | **167** | **164** | **155** | **163** |
| Successful migrations (of 6) | 2 | 2 | 2 | 3 |

Mean 159.0 of 184, step 04 165.5: worse.

A first pair of runs scored 129 and 127, because route53 got 0 of 42: its tests import from the package
(`from src.awslabs_route53_infima import Lattice`), and the harness never wrote the package `__init__.py`. That is
fixed (the package file now gets its own session, last), and the table shows the runs after the fix.

**Why it lost points: modules without public tests have nothing to check against.** On route53 the failing hidden
tests are all in modules no public test imports (answer_set, rubber_tree, sub_list_iterator,
stateful_searching_shuffle_sharder). In one long session the agent tests these on its own; a module session is told
only about the public tests of its module, so for these it writes code and stops. That led to variant 05b.

**Decision: try 05b** (each module session also ports the Java unit test of its class).

| | Step 04 | 05 |
|---|---|---|
| Agent sessions per run | 14 to 16 | 57 |
| Sessions that hit their turn limit | 12 to 13 | 18 to 21 |
| Tokens per run | 8.6 to 9.3 M | 6.7 to 7.3 M |
| Slowest repo (geohash) | 12 to 13 min | 18 to 24 min |
