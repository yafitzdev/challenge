# 04 Retry

The retry mechanism ([retry.py](../../harness/src/retry.py)). After the agent stops, every module whose public
tests still fail is written again by a fresh, short agent session, up to 2 times. Only that one file may change,
and the new version is kept only if more of its public tests pass than before. Config: [config.json](config.json)
(step 03 plus `retry`). Run summaries: [runs/](runs/).

| Setting | Value | Meaning |
|---|---|---|
| `attempts` | 2 | Tries per failing module. |
| `max_assistant_turns`, `timeout_seconds` | 15, 300 | Budget of one retry session. |

How a module's tests are found: a public test file belongs to every project module it imports
(`from src.geohash.util.long_util import LongUtil` -> `src/geohash/util/long_util.py`). The retry session gets the
module path, its test files and the first line of each failure
([retry_module.txt](../../harness/prompts/during_work/retry_module.txt)). The hidden tests are never used.

## Result

6 development repos, 184 passable hidden tests.

| Repo | Step 03 run 1 | Step 03 run 2 | Run 1 | Run 2 |
|---|---|---|---|---|
| shekhargulati_30-seconds-of-java | 7/7 | 7/7 | 7/7 | 7/7 |
| nzakas_props2js | 38/38 | 38/38 | 32/38 | 38/38 |
| tasomaniac_DelayedProgress | 18/26 | 22/26 | 22/26 | 18/26 |
| awslabs_route53-infima | 40/42 | 41/42 | 41/42 | 40/42 |
| kungfoo_geohash-java | 29/41 | 36/41 | 35/41 | 33/41 |
| tamir7_Contacts | 30/30 | 27/30 | 30/30 | 28/30 |
| **Total** | **162** | **171** | **167** | **164** |
| Successful migrations (of 6) | 3 | 2 | 2 | 2 |

Mean 165.5 of 184, step 03 166.5: no gain. 18 retry sessions ran, all on DelayedProgress and geohash, and only 2
were kept (geohash double_util 0 -> 2 of 2, DelayedProgress dialog 3 -> 4 of 7).

**Why it did not help: the public tests are a poor trigger.** Some public tests fail even on the reference port,
so no correct migration can pass them. Run against the reference port, these modules fail public tests:

| Repo | Modules the reference port fails public tests on |
|---|---|
| tasomaniac_DelayedProgress | delayed_progress_bar (7 of 10), delayed_progress_dialog (5 of 7) |
| kungfoo_geohash-java | bounding_box, wgs84point, bounding_box_geohash_iterator, bounding_box_sampler, double_util, geohash_size_table, long_util |
| tamir7_Contacts | address (0 of 5), email, event, phonenumber |

Every module retried in these runs is on that list. So the retries chased tests that cannot pass, and "keep the
version with more public tests passing" can even move a module away from the hidden tests. The mechanism works as
built (it ran, kept the better version, and changed only the one file); what it lacks is a trustworthy signal.

**Decision: keep the mechanism, not as a step of its own.** It goes on as the failure path of decomposition (step
05), where every module gets its own request anyway. On its own, it adds time (mean 262 s per repo run, up from about
150 s) and no points.

## Failures

- **Turn limit.** 7 of 12 main sessions used all 40 turns (7 of 12 in step 03).
- **A retry session read its own log.** The sandbox shows each session its output folder (it writes its log
  there). One retry session on DelayedProgress found that folder and read its own events.jsonl. That is not the
  answers, only its own conversation, but it was wasted turns.
