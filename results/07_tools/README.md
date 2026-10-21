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

| Repo | Step 06 run 1 | Step 06 run 2 | Run 1 | Run 2 |
|---|---|---|---|---|
| kungfoo_geohash-java | 25/41 | 15/41 | 0/41 | 14/41 |
| awslabs_route53-infima | 17/42 | 5/42 | 19/42 | 2/42 |
| tamir7_Contacts | 24/30 | 26/30 | 19/30 | 21/30 |
| **Total** | **66** | **46** | **38** | **37** |

Run 1 is before the push undo (step 05), run 2 after it. Holdout, run 1, same 5 repos as [09](../09_holdout/):
46 of 184, against 55 for step 06.

The agent did use the tool: 695 run_tests calls against 147 bash calls in the module sessions of run 1.

Run 1 lost geohash (0) to the push gap from step 05, so it was rerun once the gap was closed. The rerun did not
change the picture: 37 against 46 for step 06 with the same fix. Across both runs, 37.5 against 56.0.

**Decision: drop.** The final harness stays step 06. The structured report likely matters less here than in a
single long session, because each module session already gets the exact failing tests in its prompt.
