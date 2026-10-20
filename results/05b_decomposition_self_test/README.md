# 05b Decomposition with self-test

Step 05, plus one line in every module session's prompt: find the Java unit test of this class in ../source/,
port its cases to a scratch test file, and run it too. The scratch file is thrown away with the session's other
files; it only gives the session a check where no public test covers the module. Config: [config.json](config.json)
(step 05 plus `decompose.self_test`). Run summaries: [runs/](runs/).

## Result

6 development repos, 184 passable hidden tests.

| Repo | Step 04 run 1 | Step 04 run 2 | 05 run 1 | 05 run 2 | Run 1 | Run 2 |
|---|---|---|---|---|---|---|
| shekhargulati_30-seconds-of-java | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 | 7/7 |
| nzakas_props2js | 32/38 | 38/38 | 38/38 | 38/38 | 38/38 | 38/38 |
| tasomaniac_DelayedProgress | 22/26 | 18/26 | 18/26 | 18/26 | 18/26 | 18/26 |
| awslabs_route53-infima | 41/42 | 40/42 | 33/42 | 34/42 | 33/42 | 41/42 |
| kungfoo_geohash-java | 35/41 | 33/41 | 35/41 | 36/41 | 37/41 | 35/41 |
| tamir7_Contacts | 30/30 | 28/30 | 24/30 | 30/30 | 28/30 | 28/30 |
| **Total** | **167** | **164** | **155** | **163** | **161** | **167** |

Mean 164.0 of 184: back to the level of one long session (step 04: 165.5, step 03: 166.5), not above it.
geohash, the repo with the most modules (13), does best under decomposition: 35 to 37 of 41, against 29 to 36
with one session. It also takes longest: 32 and 43 minutes, against about 13.

**Verdict on the thesis, for this model:** with DeepSeek flash on these small repositories, smaller requests do
not give better code. The whole repository fits in one session's context, so there is little bloat to remove,
while module sessions lose the overview (they do not see how the other modules were written). The one sign in
favor is geohash, the largest repo. The thesis is about weak models and large inputs; the place to test it is the
weak model (Gemini 2.5 Flash Lite), where one long session failed most often.

**Decision: keep, as the final harness.** It costs no points against step 04, uses about the same tokens (9.2 to
9.5 M per run) and is 2 to 3 times slower; it is the design to build on for larger repositories and weaker
models. The holdout check (step 06) runs with it.
