# 08 Tools package: java_api and port_check

Two custom tools for the agent, both deterministic (no model call), in [java_tools.py](../../harness/src/java_tools.py).
Config: [config.json](config.json) (step 06 plus `java_api` and `port_check` in `tools`). Run summaries:
[runs/](runs/). Every session is told about them ([java_api_hint](../../harness/prompts/during_work/java_api_hint.txt),
[port_check_hint](../../harness/prompts/during_work/port_check_hint.txt)).

| Tool | Input | What it returns |
|---|---|---|
| `java_api` | a Java class name (`WGS84Point`, or `PhoneNumber.Type` for a nested type) | where the Java file and its tests are, and every non-private constructor, method, constant and enum value, each with the Python name to use (the spelling the public tests use, else snake_case) and whether it must be a `@staticmethod` |
| `port_check` | a Python module (`src/geohash/wgs84point.py`) | every non-private Java constructor, method or constant of the class it ports that the module does not define yet |

Why these two, from the tool logs of the Gemini runs (about 3,300 tool calls):
- 382 of about 1,100 reads failed, because the agent guessed file paths that did not exist.
- The main loss in the step READMEs is Java methods that the port leaves out or names differently.
- No tool output was cut off at Pi's 2,000-line / 50 KB limit, so output length needed no fix.

## Result

| Repo | Step 06 run 1 | Step 06 run 2 | Run 1 | Run 2 |
|---|---|---|---|---|
| kungfoo_geohash-java | 25/41 | 15/41 | 20/41 | 24/41 |
| awslabs_route53-infima | 17/42 | 5/42 | 1/42 | 0/42 |
| tamir7_Contacts | 24/30 | 26/30 | 22/30 | 7/30 |
| **Total** | **66** | **46** | **43** | **31** |

Mean 37.0 against 56.0 for step 06. Run 1 showed that java_api did not say which methods are static
(`missing 1 required positional argument`); run 2 has that fixed.

**The tools change how the agent works.** It used them a lot (java_api 84 and 69 calls, port_check 26 and 39), and
failed reads went from 42 and 60 per run in step 06 to 2. It stopped guessing paths.

**They do not change the score.** route53 stays near 0 in both runs: its tests import every class through the package,
and the classes were incomplete (`TwoDimensionalLattice` has no `get_dimension_names`, a method `get_endpoints`
returns None instead of []). port_check only checks names, so it cannot see a method that exists but does the wrong
thing. Contacts falling from 22 to 7 between runs is the kind of swing seen before (step 05: 16 and 9).

**Decision: drop.** The final harness stays step 06. A tool that saves the agent work does not make the port more
correct; behavior is what the hidden tests check.
