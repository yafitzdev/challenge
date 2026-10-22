# 01 Robustness

Two fixes for ways a session can end or stall for reasons that have nothing to do with the migration.
Config: [config.json](config.json) (the baseline plus two keys). Run summaries: [runs/](runs/).

| Key | What it does | Failure it fixes |
|---|---|---|
| `command_timeout_seconds: 120` | Every shell command the agent runs is stopped after 120 s, and the agent is told why ([timeout-bash.sh](../../harness/src/timeout-bash.sh)). | One command that never returned used the whole 600 s session. |
| `resume_after_errors: 3` | When the session ends on a provider error, or because a reply hit the output limit, the harness sends the agent on with a short note ([provider_error](../../harness/prompts/during_work/provider_error.txt), [output_limit](../../harness/prompts/during_work/output_limit.txt)), up to 3 times. | A reply cut off at the output limit ends a Pi session; once this left a repo with no code at all (geohash, baseline run 3, 0 of 41). |

## Result

6 development repos, 184 passable tests (public and hidden).

| Repo | Baseline 1 | Baseline 2 | Baseline 3 | Run 1 | Run 2 |
|---|---|---|---|---|---|
| shekhargulati_30-seconds-of-java | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| nzakas_props2js | 38/38 | 38/38 | 38/38 | 38/38 | 38/38 |
| tasomaniac_DelayedProgress | 26/26 | 20/26 | 22/26 | 20/26 | 20/26 |
| awslabs_route53-infima | 41/42 | 41/42 | 41/42 | 41/42 | 40/42 |
| kungfoo_geohash-java | 34/41 | 29/41 | 0/41 | 33/41 | 35/41 |
| tamir7_Contacts | 29/30 | 29/30 | 30/30 | 30/30 | 29/30 |
| **Total** | **175** | **164** | **138** | **169** | **169** |
| Successful migrations (of 6) | 3 | 2 | 3 | 3 | 2 |

Mean 169.0 of 184, baseline 159.0 (169.5 without baseline run 3, the run the output-limit fix targets). Neither fix fired on the development repos (no command
was stopped, no session ended on an error). On the sanity repo aventrix_jnanoid, where a test command hung in the
baseline setup check, the command was stopped after 120 s and the agent carried on: 9 to 21 of 22.

**Decision: keep.** Both fixes remove a way to lose a whole repo run, and they cost nothing when they don't fire.

## Failures

- **Turn limit.** 9 of 12 repo runs still used all 40 turns (8 of 12 in the baseline). This is now the most
  common way a run ends.
- **The agent can see outside its workspace.** In run 2 on Contacts the agent ran `find / -name address.py`, and
  the output listed copies of the reference ports elsewhere on the machine. It did not open them, but nothing
  stopped it. Step 02 (sandbox) closes this.
