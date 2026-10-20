# 07 Weak model

The same harness versions with a weak model, Gemini 2.5 Flash Lite (via OpenRouter), to test the decomposition
thesis where it should matter most. To save money: 1 run each, 3 development repos (geohash, the largest; route53,
the most modules; Contacts, small, as a control), 113 passable hidden tests.

| Version | Config | What it is |
|---|---|---|
| Baseline | [config_baseline.json](config_baseline.json) | step 00 |
| One session | [config_single_session.json](config_single_session.json) | step 04: every fix, one long session, retry |
| Decomposition | [config_decomposition.json](config_decomposition.json) | step 05b, the final harness |

## Result

| Repo | Baseline | One session | Decomposition |
|---|---|---|---|
| kungfoo_geohash-java | 0/41 | 8/41 | **24/41** |
| awslabs_route53-infima | 0/42 | 0/42 | 0/42 |
| tamir7_Contacts | 15/30 | 23/30 | 20/30 |
| **Total** | **15** | **31** | **44** |

With the weak model the harness matters, and decomposition helps most where the thesis says it should: on
geohash, the largest repo, one long session got 8 of 41 and decomposition got 24. The baseline agent stopped
after 2 turns there and wrote no code at all. With 1 run per version, only large gaps like these count; Contacts
(23 against 20) is within noise.

**route53 is 0 everywhere, for one reason each time.** Its tests import every class through the package
(`from src.awslabs_route53_infima import Lattice`), so one missing module breaks all 42 tests. Gemini often
answers once and stops without doing the work: in decomposition the session for lattice.py ended after 1 turn
with no file, and the package's `__init__.py` then could not import it. One session stopped after 4 turns without
writing src/ at all. Retry did not help: it only rewrites the module whose tests fail (`__init__.py`), not the
missing module that file imports.

**Candidate next step:** when a session stops without writing its module, send it on (the "push to continue" fix
from the earlier harness), and let retry follow a failing import to the missing module.

## Rate limits

The first two tries were spoiled by Gemini's upstream rate limit (HTTP 429 "temporarily rate-limited upstream"):
with 9 agents at once, and again with 1 at a time. Every version now waits and goes on after a 429 (30 s, then 60,
90, 120, 180), and the wait does not count as session time ([agent.mjs](../../harness/src/agent.mjs)). That is not a
lever; it is on for all three versions. These runs went one agent at a time and needed 26 waits in total.

Cost of all three tries: about $0.50.
