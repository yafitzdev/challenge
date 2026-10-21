# 07 Tools package

The agent gets a `run_tests` tool ([run_tests.py](../../harness/src/run_tests.py)) instead of running pytest through
bash. It runs the public tests the way the evaluator does and returns a short report: passed and failed per test
file, the first error line of each failure (with the src/ line it came from), and the modules the tests cannot
import, with the file to create. Every session (main, module, push and retry) is told about it
([run_tests_hint](../../harness/prompts/during_work/run_tests_hint.txt)). Config: [config.json](config.json)
(step 06 plus `run_tests` in `tools`). Run summaries: [runs/](runs/).

Why: the brief names "additional tools" and "structured build and test feedback" as levers, and a weak model
reading pages of raw pytest output often misreads them.

## Result

| Repo | Step 06 | Run 1 |
|---|---|---|
| kungfoo_geohash-java | 25/41 | 0/41 |
| awslabs_route53-infima | 17/42 | 19/42 |
| tamir7_Contacts | 24/30 | 19/30 |
| **Total** | **66** | **38** |

Holdout, same 5 repos as [08](../08_holdout/): 46 of 184, against 55 for step 06.

The agent did use it: 695 run_tests calls against 147 bash calls in the module sessions. It did not help.

- geohash fell to 0 for the reason already known from step 05: a push round broke more imports than it fixed
  (2 before, 7 after) and is kept anyway. Without geohash the two versions are level (38 against 41).
- On the holdout it is mixed: signaturepad 18 -> 4, ElSql 0 -> 6, the rest within 1 test.

With 1 run, a few points either way are noise; there is no sign of a gain.

**Decision: drop.** The final harness stays step 06. The structured report likely matters less here than in a
single long session, because each module session already gets the exact failing tests in its prompt.
