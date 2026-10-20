# 00 Baseline

The plain Pi agent with no help from the harness: tools read, bash, edit and write, 40 assistant turns, 600 s, one
plain prompt ([task/baseline.txt](../../harness/prompts/task/baseline.txt)). Model: DeepSeek flash, thinking off.
Config: [config.json](config.json). Run summaries: [runs/](runs/).

## Result

6 development repos, 184 passable hidden tests.

| Repo | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| shekhargulati_30-seconds-of-java | 7/7 | 7/7 | 7/7 |
| nzakas_props2js | 38/38 | 38/38 | 38/38 |
| tasomaniac_DelayedProgress | 26/26 | 20/26 | 22/26 |
| awslabs_route53-infima | 41/42 | 41/42 | 41/42 |
| kungfoo_geohash-java | 34/41 | 29/41 | **0/41** |
| tamir7_Contacts | 29/30 | 29/30 | 30/30 |
| **Total** | **175** | **164** | **138** |
| Successful migrations (of 6) | 3 | 2 | 3 |

Mean 159.0 of 184 (86%). The audit found nothing: no reads of the reference ports, hidden tests or project folder,
and no package installs.

## Failures

- **Turn limit.** 10 of 18 repo runs used all 40 turns and were stopped mid-work (every run of DelayedProgress and
  route53-infima). The code they had written by then still counted.
- **Output limit ends the session.** geohash run 3 scored 0 because no file was written. The agent tried to write
  a large file in one reply, hit the 8192-token output limit twice, and the second time Pi ended the session.
- **A hung command uses the whole session.** Seen in the setup check on the sanity repo aventrix_jnanoid: one
  shell command (a test run) never returned, and the session ended on the 600 s limit after 6 turns.

The first two failures cost the most points, and neither is about the model's skill: the harness stops the agent,
or loses its work. Step 01 (robustness) fixes these.
