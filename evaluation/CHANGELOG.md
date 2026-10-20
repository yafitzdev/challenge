# Evaluator changes

## v4: data/ renamed to test_repositories/ (2026-10-19, decided by Yan)

**Change:** paths only. `data/<repo>/...` is now `test_repositories/<repo>/...`; test ids, hashes and the manifest are
unchanged. **Re-validation:** `evaluation/validate.py` passes for all 21 repos.

## v3: new data layout (2026-10-19, decided by Yan)

**Change:** paths only. `data/source/<repo>` is now `data/<repo>/repository`, `data/target/<repo>/tests/original`
is now `data/<repo>/hidden_tests`, public tests and project_structure.txt moved up to `data/<repo>/`, and the
oracles moved from `oracles/<repo>/src` to `data/<repo>/oracle/src`. Test ids changed from `tests/original/...` to
`hidden_tests/...` in manifest.json and excluded_tests.json. The unused `run_tests.sh` per repo was dropped.

**Re-validation:** every file hash in the old manifest matches the moved file (checked before rewriting the
manifest). The 13 oracles, an empty candidate for all 21 repos and the 6 stored weak14 run-1 candidates were scored
before and after the move: 40 scorings, 2449 test results, 0 differences. `evaluation/validate.py` passes for all
21 repos (it now also covers the repos without an oracle, with the empty-candidate check only).

## Manifest: 16 build-cache files dropped (2026-10-19, decided by Yan)

**Change:** 16 entries removed from `source_sha256` in manifest.json for 3 hard repos:
1ssqq1lxr_iot_push (`.idea/uiDesigner.xml`), Netflix_dyno-queues (9 files under `.gradle/`),
cyrildiagne_ar-cptext (6 files under `mobile/.gradle/`).

**Why:** these are IDE and Gradle cache files. Git ignored them, so they never reached GitHub, and a fresh clone
failed the "frozen inputs unchanged" check. Their bytes only existed in an old cloud session. No test, no Java
source and nothing in data/<repo>/hidden_tests changed. 10 similar files for 3 other repos were still in the shared folder;
they were restored byte for byte and force-added to git so future clones are complete.

**Re-validation:** all 21 repos match the manifest; an empty candidate passes 0 tests in each of the 3 repos
(0 of 32, 0 of 21, 0 of 22). The hard repos have no oracles, so there is no oracle check for them (as before).
Agents in earlier runs saw these cache files in source/, agents from now on do not; they hold no code.

## v2: per-file scoring (2026-10-18, decided by Yan)

**Change:** evaluate.py runs every test file in its own pytest process (timeout 120 s per file) instead of one
pytest run over all files (300 s total).

**Why:** pytest stops the whole run when one file fails to import ("collection error"). One missing module made
every test of a repo count as failed. Example: geohash scored 0 of 41 in every run, although most of the port worked.
A file that hangs now also only fails its own tests.

**Re-validation** (evaluation/validate.py): all 13 oracles pass all passable tests; an empty candidate passes 0.
The re-validation found 2 fake tests in the holdout repo AllenDowney_ThinkJavaCode
(`public_tests/test_ch13_public.py::test_public_logic`, `public_tests/test_ch14_public.py::test_public_placeholder`):
they pass with no code at all. v1 hid this because another file's collection error stopped the run.
Both are now marked not passable (manifest.json, excluded_tests.json). Only their ids were looked at.

**Re-scoring** (scripts/rescore.py): every saved run was scored again, no agent was re-run.
Old results are kept next to the new ones as score_v1.json / summary_v1.json.

### Development runs, passable tests passed, v2 scoring
Each column is one complete run of the 6 development repos.

| Repo | Baseline | Iter 1 | Iter 2 run 1 | Iter 2 run 2 | Iter 3 run 1 | Iter 3 run 2 |
|---|---|---|---|---|---|---|
| 30-seconds-of-java | 7 of 7 | 7 of 7 | 7 of 7 | 7 of 7 | 7 of 7 | 7 of 7 |
| props2js | 38 of 38 | 38 of 38 | 38 of 38 | 38 of 38 | 38 of 38 | 38 of 38 |
| DelayedProgress | 18 of 26 | 16 of 26 | 18 of 26 | 14 of 26 | 26 of 26 | 2 of 26 |
| route53-infima | 36 of 42 | 37 of 42 | 34 of 42 | 40 of 42 | 40 of 42 | 37 of 42 |
| geohash-java | 32 of 41 | 34 of 41 | 37 of 41 | 33 of 41 | 37 of 41 | 29 of 41 |
| Contacts | 30 of 30 | 30 of 30 | 30 of 30 | 30 of 30 | 28 of 30 | 29 of 30 |
| **All 6 repos** | 161 of 184 (87.5%) | 162 of 184 (88.0%) | 164 of 184 (89.1%) | 162 of 184 (88.0%) | 176 of 184 (95.7%) | 142 of 184 (77.2%) |
| Successful migrations | 3 of 6 | 3 of 6 | 3 of 6 | 3 of 6 | 3 of 6 | 2 of 6 |

Averages over repeated runs: iteration 2 = 88.6%, iteration 3 = 86.4%. Baseline (1 run) = 87.5%.

### What changed in the story
- geohash was never really at 0: the ports passed 29 to 37 of 41 tests. The missing module cost only its own file.
- Iteration 1's route53 "0 of 42" was the evaluator's 300 s timeout on one slow file; per file it is 37 of 42.
  So iteration 1 was not worse than the baseline after all (88.0% vs 87.5%), it simply did not help.
- The conclusions about iterations 2 and 3 stay the same: no clear gain, and large run-to-run variance
  (DelayedProgress 26 of 26 vs 2 of 26 with the same config).
