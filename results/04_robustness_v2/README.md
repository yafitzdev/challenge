# 04 Robustness v2

The small fixes the weak model showed we need: it gets lost in the workspace and repeats failing commands.
Config: [config.json](config.json) (step 03 plus the keys below). Run summary: [runs/](runs/).

| Key | What it does | Failure it fixes |
|---|---|---|
| `start_in_candidate` | The agent's tools start in candidate/, where the code goes; the Java source is at `../source/` ([prompt](../../harness/prompts/task/start_in_candidate.txt)). | Weak models wrote code next to candidate/, where the scorer never looks. |
| `candidate_link` | A link candidate/candidate -> candidate/, so a path like `candidate/src/x.py` still lands in the right place. | The same mistake from inside candidate/. |
| `loop_breaker: 3` | When the same tool call fails 3 times with the same output and no file changed in between, the harness tells the agent ([loop_breaker](../../harness/prompts/during_work/loop_breaker.txt)). | Sessions that spend their turns re-running one failing command. |

## Result

| Repo | Step 03 | Run 1 |
|---|---|---|
| kungfoo_geohash-java | 0/41 | 16/41 |
| awslabs_route53-infima | 0/42 | 0/42 |
| tamir7_Contacts | 0/30 | 0/30 |
| **Total** | **0** | **16** |

geohash now gets working code (16 of 41; the session used all its turns: 40, plus 2 answers after the provider
errors that robustness resumed). The other two are still 0:

- route53: the package `__init__.py` does not export the classes the tests import (`cannot import name 'Lattice'`).
- Contacts: every module imports, but the API is wrong (`PhoneNumber() takes no arguments`, no `Event.Type`).

**Decision: keep.** Next failure to fix: the agent stops while imports are still broken (step 05).

**Bug found after the runs.** The loop-breaker note reached the agent with its placeholders unfilled (`{tool}`,
`{count}`, `{call}`, `{cwd}`) in this step and every later one: the prompt loader in agent.mjs ignored the values.
The agent still got the instruction to stop repeating the call and check where it is, just without the details.
Fixed afterwards in agent.mjs; the measured runs used the unfilled note.
