# 02 Sandbox

The agent now runs in its own sandbox ([sandbox.sh](../../harness/src/sandbox.sh)), so it can only use what it is
meant to use. Config: [config.json](config.json) (step 01 plus `sandbox: true`). Run summaries: [runs/](runs/).

| Part | What it does | Why |
|---|---|---|
| Own view of the files | The agent sees only its workspace, its output folder and the harness code (read-only). The project folder, the reference ports, the hidden tests, old runs and other agents' workspaces are not there. | In step 01 a `find /` listed copies of the reference ports. |
| Read-only inputs | The Java source, the contract, project_structure.txt and the public tests cannot be changed; neither can /usr (the Python the scorer uses). | Editing a public test to make it pass, or installing a package into the scorer's Python, would fake a result. |
| No network for commands | Every shell command runs without network. Pi itself still reaches the model API. | The tests run without network; the agent should not download code either. |

Checked before the runs: inside the sandbox the project folder does not exist, writing to source/ fails with
"Read-only file system", and `curl` cannot connect, while Pi's own requests go through.

Hardened after all runs (review, 2026-10-22): the agent now runs as the unprivileged user nobody, so it cannot undo
these mounts (`umount /home` fails), and the project folder is hidden wherever the repo is cloned. In the measured runs
the agent ran as root; no audit shows it reaching anything outside the workspace.

## Result

6 development repos, 184 passable tests (public and hidden).

| Repo | Step 01 run 1 | Step 01 run 2 | Run 1 | Run 2 |
|---|---|---|---|---|
| shekhargulati_30-seconds-of-java | 7/7 | 7/7 | 7/7 | 7/7 |
| nzakas_props2js | 38/38 | 38/38 | 32/38 | 38/38 |
| tasomaniac_DelayedProgress | 20/26 | 20/26 | 16/26 | 16/26 |
| awslabs_route53-infima | 41/42 | 40/42 | 40/42 | 41/42 |
| kungfoo_geohash-java | 33/41 | 35/41 | 36/41 | 33/41 |
| tamir7_Contacts | 30/30 | 29/30 | 30/30 | 28/30 |
| **Total** | **169** | **169** | **161** | **163** |
| Successful migrations (of 6) | 3 | 2 | 2 | 2 |

Mean 162.0 of 184, step 01 169.0. The audit found no reads of anything outside the workspace. The sandbox
blocked the agent only 3 times in 12 repo runs, each a write into public_tests/ (an `__init__.py`), and no command
needed the network. So the 7 points are mostly run-to-run noise: props2js lost 6 in run 1 when it hit the turn limit
and got all 38 in run 2.

**Decision: keep.** Without it a score can't be trusted, because nothing stops the agent from reading the answers.

## Failures

- **Turn limit.** 9 of 12 repo runs used all 40 turns (9 of 12 in step 01). Still the main way a run ends.
- **Read-only public tests break a chained command.** A command like `touch public_tests/__init__.py && cat > ...`
  stops at the failed touch, so the rest of it is not run. The agent sees the error and usually works around it.
