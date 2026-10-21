# 10 Holdout check

The final harness (step 06) against part 2's baseline (step 03) on the 5 holdout repos, which no step looked at.
Gemini 2.5 Flash Lite, 1 run each, 184 passable hidden tests. Configs:
[03](../03_weak_baseline/config.json), [06](../06_decomposition/config.json). Run summaries: [runs/](runs/).

## Result

| Repo | Baseline (03) | Final (06) |
|---|---|---|
| gcacace_android-signaturepad | 0/18 | **18/18** |
| bmwcarit_hmm-lib | 6/19 | 9/19 |
| tuenti_SmsRadar | 0/16 | 5/16 |
| AllenDowney_ThinkJavaCode | 18/34 | 23/34 |
| OpenGamma_ElSql | 0/97 | 0/97 |
| **Total** | **24** | **55** |

The gain holds on repositories the harness was never tuned on: 24 -> 55 of 184, and one repo fully migrated
(signaturepad, 18 of 18). Every repo improves or stays.

**ElSql, the largest repo (97 tests), is 0 in both.** The plan session wrote no plan, so decomposition had only the
package `__init__.py` to write, and the three push rounds could not write the whole library from there
(`No module named 'opengamma.elsql.container_sql_fragment'`). Next fix: when the plan is empty, plan again or fall
back to one Java file per module.
