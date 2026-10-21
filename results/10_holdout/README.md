# 10 Holdout check

The final harness (step 06) against two baselines on the 5 holdout repos, which no step looked at: the plain agent
with none of our fixes (step 00's config with Gemini) and part 1's harness (step 03). Gemini 2.5 Flash Lite, 1 run
each, 184 passable hidden tests. Configs: [plain](config_plain.json), [03](../03_weak_baseline/config.json),
[06](../06_decomposition/config.json). Run summaries: [runs/](runs/).

## Result

| Repo | Plain (00) | Baseline (03) | Final (06) |
|---|---|---|---|
| gcacace_android-signaturepad | 0/18 | 0/18 | **18/18** |
| bmwcarit_hmm-lib | 13/19 | 6/19 | 9/19 |
| tuenti_SmsRadar | 3/16 | 0/16 | 5/16 |
| AllenDowney_ThinkJavaCode | 0/34 | 18/34 | 23/34 |
| OpenGamma_ElSql | 0/97 | 0/97 | 0/97 |
| **Total** | **16** | **24** | **55** |

The gain holds on repositories the harness was never tuned on: 16 -> 24 -> 55 of 184 (8.7% -> 13.0% -> 29.9%),
and one repo fully migrated (signaturepad, 18 of 18). Against 03 every repo improves or stays; against the plain
agent one repo is lower (hmm-lib, 13 against 9), which is within the run-to-run spread we saw.

The plain agent was also run on part 2's 3 development repos ([runs/plain_dev.json](runs/plain_dev.json)): 0 of
113, the same as step 03 (geohash hit the turn limit; route53 and Contacts
stopped on their own). Without the sandbox, the plain agent on SmsRadar ran `pip install` twice; pip only reported that pytest
was already installed, so nothing changed.

**ElSql, the largest repo (97 tests), is 0 in all three.** The plan session wrote no plan, so decomposition had only the
package `__init__.py` to write, and the three push rounds could not write the whole library from there
(`No module named 'opengamma.elsql.container_sql_fragment'`). Next fix: when the plan is empty, plan again or fall
back to one Java file per module.
