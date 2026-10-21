# 06 Decomposition package

Instead of one long session for the whole repository, the work is split into small requests
([decompose.py](../../harness/src/decompose.py)). Thesis: smaller requests mean less context, fewer
hallucinations, better code. Config: [config.json](config.json) (step 05 plus `decompose`). Run summary:
[runs/](runs/).

1. **Plan.** A short session (15 turns) reads the Java repository and writes plan.json: one entry per Python module,
   with the Java file it ports and the modules it depends on ([decompose_plan](../../harness/prompts/task/decompose_plan.txt)).
   The harness adds every module that project_structure.txt lists or a public test imports.
2. **Modules.** In dependency order, a fresh session (15 turns, 300 s) writes one module
   ([write_module](../../harness/prompts/during_work/write_module.txt)). It is told which modules exist and which
   public tests cover this one, and it ports the Java unit test of its class to a scratch file and runs it
   (`self_test`), so modules without public tests have a check too. Only that one file is kept. Package
   `__init__.py` files come last, so the classes they re-export exist.
3. **Retry package** (step 05) as the failure path.

## Result

| Repo | Step 05 | Run 1 |
|---|---|---|
| kungfoo_geohash-java | 0/41 | **25/41** |
| awslabs_route53-infima | 18/42 | 17/42 |
| tamir7_Contacts | 16/30 | **24/30** |
| **Total** | **34** | **66** |

The thesis holds with the weak model. Each session only has to get one class right, and it has the Java class and
that class's tests in front of it. On geohash, the largest repo, that is the difference between 0 (and 16 in step
04) and 25. It is slower: geohash took 12 minutes against 2 to 10 with one session.

What still fails: classes that are written but incomplete (route53: `Lattice` has no `get_all_endpoints`), and
the package re-export when the plan is empty (holdout, [08](../08_holdout/)).

**Decision: keep, final harness.**
