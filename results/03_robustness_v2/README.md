# 03 Robustness v2

Three small guards against the agent working in the wrong place or going in circles. Config:
[config.json](config.json) (step 02 plus three keys and a new prompt). Run summaries: [runs/](runs/).

| Key | What it does | Failure it guards against |
|---|---|---|
| `start_in_candidate` | The agent's tools start in candidate/, where the code goes; the prompt ([start_in_candidate.txt](../../harness/prompts/task/start_in_candidate.txt)) says the Java source is at `../source/`. | Code written outside candidate/ is never scored. |
| `candidate_link` | candidate/candidate is a link back to candidate/, so a path like `candidate/src/x.py` written from inside candidate/ still lands in the right place. | Code written to candidate/candidate/, never scored. |
| `loop_breaker: 3` | When the same tool call fails 3 times with the same output and no file changed in between, the harness tells the agent to check where it is and try something else ([loop_breaker.txt](../../harness/prompts/during_work/loop_breaker.txt)). | One stuck command repeated until the turns run out. |

## Result

6 development repos, 184 passable hidden tests.

| Repo | Step 02 run 1 | Step 02 run 2 | Run 1 | Run 2 |
|---|---|---|---|---|
| shekhargulati_30-seconds-of-java | 7/7 | 7/7 | 7/7 | 7/7 |
| nzakas_props2js | 32/38 | 38/38 | 38/38 | 38/38 |
| tasomaniac_DelayedProgress | 16/26 | 16/26 | 18/26 | 22/26 |
| awslabs_route53-infima | 40/42 | 41/42 | 40/42 | 41/42 |
| kungfoo_geohash-java | 36/41 | 33/41 | 29/41 | 36/41 |
| tamir7_Contacts | 30/30 | 28/30 | 30/30 | 27/30 |
| **Total** | **161** | **163** | **162** | **171** |
| Successful migrations (of 6) | 2 | 2 | 3 | 2 |

Mean 166.5 of 184, step 02 162.0. The +4.5 is within the run-to-run spread. None of the three guards fired: no
write went outside candidate/ (also not in steps 00 to 02), nothing used the candidate/candidate link, and no
failing call repeated 3 times. DeepSeek flash simply does not make these mistakes. Step 01's resume did fire once
(geohash run 2, a dropped connection at turn 24, and the session went on).

**Decision: keep.** They cost nothing when they don't fire, and they are the fixes for failures a weaker model
makes (in the earlier harness, 11 of 24 weak-model repo runs wrote their code outside candidate/).

## Failures

- **Turn limit.** 7 of 12 repo runs used all 40 turns (9 of 12 in step 02). Still the main way a run ends.
