# 03 Weak-model baseline

Part 2 starts here: part 1's harness (step 02, sandbox) unchanged, with a weak model, Gemini 2.5 Flash Lite (via
OpenRouter). Config: [config.json](config.json) (step 02 with the model swapped). Run summary: [runs/](runs/).

To save money, part 2 runs once per step on 3 development repos: geohash (the largest), route53 (the most
modules), Contacts (small). 113 passable hidden tests.

## Result

| Repo | Run 1 |
|---|---|
| kungfoo_geohash-java | 0/41 |
| awslabs_route53-infima | 0/42 |
| tamir7_Contacts | 0/30 |
| **Total** | **0** |

Every repo is 0, for one reason: a test file that cannot import its module scores nothing, and Gemini always left
one import broken.

- geohash: code was written, but classes the tests import were missing (`cannot import name 'BoundingBox'`).
- route53: the session ended after 12 turns and 20 s without writing any code.
- Contacts: the package `__init__.py` imports a module Gemini made up (`import DatabaseUtils`), so every test of the
  package fails to load.

The agent also stopped on its own in all three repos (no turn or time limit hit): it says it is done when it is not.
Steps 04 and 05 target exactly this.
