# 05 Retry package

What happens after the agent stops ([retry.py](../../harness/src/retry.py)). Config: [config.json](config.json)
(step 04 plus `retry`). Run summary: [runs/](runs/).

1. **Push to continue.** The harness tries every import of the public tests (`from src.x import A, B`) with no
   model call. While one fails (module not written, broken, or a class missing), a fresh session is sent back to the
   repository with Python's exact errors ([push_to_continue](../../harness/prompts/during_work/push_to_continue.txt)),
   up to 3 times. It may change any file.
2. **Retry per module.** Every module whose public tests still fail is written again by a fresh session that may
   change only that file ([retry_module](../../harness/prompts/during_work/retry_module.txt)), up to 2 times. A new
   version is kept only if more of its public tests pass.

| Setting | Value | Meaning |
|---|---|---|
| `push_to_continue` | 3 | Push rounds while imports fail. |
| `attempts` | 2 | Tries per failing module. |
| `max_assistant_turns`, `timeout_seconds` | 15, 300 | Budget of one push or retry session. |

The first version of push to continue only checked that each module imports, not the names the tests import from
it, so route53's missing `Lattice` went unnoticed. That run was thrown away; the table shows the run after the fix.

## Result

| Repo | Step 04 | Run 1 |
|---|---|---|
| kungfoo_geohash-java | 16/41 | 0/41 |
| awslabs_route53-infima | 0/42 | **18/42** |
| tamir7_Contacts | 0/30 | **16/30** |
| **Total** | **16** | **34** |

route53 is no longer 0: one push round wrote the classes the package was missing, and all its imports work.
On Contacts every module imports; module retries improved event.py (2 -> 5 of 5 public tests) and address.py
(1 -> 2); the rest of its gain comes from a different main session (1 run per step).

geohash fell to 0, and push to continue made it worse: before the first push 1 import failed, after it 7
(`No module named 'src.geohash.geohash'`), and the next two rounds did not repair it. A push round is not
undone when it makes things worse, unlike a module retry. With 1 run, how much is the agent and how much the
harness cannot be told apart; the mechanism is clear from the log.

**Decision: keep.** Known gap: a push round should be kept only if it leaves fewer broken imports.
