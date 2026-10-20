# 06 Holdout check

The final harness and the baseline, each run twice on the 5 holdout repos. No step of the journey looked at these
repos. Final harness: step 05b (robustness, sandbox, robustness v2, retry, decomposition with self-test), config
[config.json](config.json). Baseline: [00_baseline/config.json](../00_baseline/config.json). Run summaries:
[runs/](runs/).

## Result

5 holdout repos, 184 passable hidden tests.

| Repo | Baseline run 1 | Baseline run 2 | Final run 1 | Final run 2 |
|---|---|---|---|---|
| gcacace_android-signaturepad | 18/18 | 18/18 | 18/18 | 18/18 |
| bmwcarit_hmm-lib | 19/19 | 19/19 | 19/19 | 19/19 |
| tuenti_SmsRadar | 14/16 | 15/16 | 12/16 | 14/16 |
| AllenDowney_ThinkJavaCode | **0/34** | 28/34 | 30/34 | 31/34 |
| OpenGamma_ElSql | 77/97 | 79/97 | 86/97 | 87/97 |
| **Total** | **128** | **159** | **165** | **169** |
| Successful migrations (of 5) | 2 | 2 | 2 | 2 |

Final mean 167.0 of 184, baseline 143.5: **+23.5**. On the development repos the two were level (169.5 and
164.0), so the gain shows up only here, in two ways:

- **No lost repo.** Baseline run 1 scored 0 on ThinkJavaCode: the model API answered "502 upstream request failed"
  at turn 3 and the session ended with no code. Step 01's resume after a provider error is the fix for exactly this.
- **The largest repo gains most.** ElSql (97 tests) went from 77 and 79 to 86 and 87. The baseline used all 40
  turns on it in run 2; under decomposition no session ran out of turns. This matches the one sign for
  decomposition on the development repos (geohash, the largest there).

SmsRadar is 1.5 tests lower on average. It is 3 to 7 times slower under decomposition (300 to 900 s per repo
against 35 to 155 s).

## Integrity

The audit flagged one baseline run: on ElSql the agent ran `find / -name "*.py" -path "*spring*"`, and the output
listed hidden test files of other repos on this machine. It did not open them. The baseline has no sandbox (that
is step 02); the final harness's runs show no flags.
