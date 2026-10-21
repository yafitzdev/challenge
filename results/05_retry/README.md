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

| Repo | Step 04 | Run 1 | Run 2 |
|---|---|---|---|
| kungfoo_geohash-java | 16/41 | 0/41 | 22/41 |
| awslabs_route53-infima | 0/42 | 18/42 | 0/42 |
| tamir7_Contacts | 0/30 | 16/30 | 9/30 |
| **Total** | **16** | **34** | **31** |

Run 1 is before the undo below, run 2 after it. Mean 32.5, twice step 04.

Push to continue ran in 5 of the 6 repo runs. It fixed every broken test import in 3 (route53 in run 1, geohash
and Contacts in run 2), changed nothing in 1 (route53 in run 2, which stayed 0) and made things worse in 1.

**Gap found and closed.** In run 1 on geohash, the first push round left 7 broken imports where there was 1
before (`No module named 'src.geohash.geohash'`), and that state was kept: geohash 0. Since then a push round that
leaves more broken imports than before is undone, like a module retry that makes things worse. It did not need to
fire in the later runs.

**Decision: keep.**
