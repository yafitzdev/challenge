# 09 Instructions package

Every session (plan, module, push and retry) gets a fixed rule sheet after its task
([java_python_rules.txt](../../harness/prompts/during_work/java_python_rules.txt)). Config: [config.json](config.json)
(step 06 plus `rules`). Run summaries: [runs/](runs/).

The 8 rules come from a tally of the test errors in all earlier Gemini runs, not from guessing:

| Rule | Error it targets (count over all runs) |
|---|---|
| every imported module exists; `__init__.py` re-exports what tests import | `ModuleNotFoundError` (95), `cannot import name` (about 30) |
| static methods stay `@staticmethod`, static fields stay class attributes | `type object 'X' has no attribute 'y'` (61) |
| nested Java types stay nested; enums keep member names; `fromValue` becomes a classmethod | `PhoneNumber has no attribute 'Type'`, `Type has no attribute 'HOME'` |
| overloads become one method with optional parameters | `takes no arguments`, `missing 1 required positional argument` |
| no undefined type variable `T` in annotations | `name 'T' is not defined` |
| empty list for an empty collection, None only for Java null | `assert None == []` |
| relative imports, no import cycles | `partially initialized module` |
| names exactly as the tests spell them | `has no attribute ... Did you mean` |

## Result

| Repo | Step 06 run 1 | Step 06 run 2 | Run 1 | Run 2 |
|---|---|---|---|---|
| kungfoo_geohash-java | 25/41 | 15/41 | 19/41 | 19/41 |
| awslabs_route53-infima | 17/42 | 5/42 | 17/42 | 18/42 |
| tamir7_Contacts | 24/30 | 26/30 | 12/30 | 8/30 |
| **Total** | **66** | **46** | **48** | **45** |

Mean 46.5 against 56.0 for step 06. The rules reached every session (checked in the saved messages).

- **route53 got steadier:** 17 and 18, against 17 and 5. Every push round ended with all test imports working.
- **Contacts got worse:** 12 and 8, against 24 and 26. The rule it needed most was ignored: `PhoneNumber.Type` and
  `Event.Type` are still missing, the error rule 3 names.

A rule in the prompt is advice; the weak model follows some and not others, and the swing between runs is larger
than the effect.

**Decision: drop.** The final harness stays step 06.
