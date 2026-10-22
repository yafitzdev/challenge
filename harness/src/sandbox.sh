#!/usr/bin/env bash
# Runs a command (the Pi agent) in its own mount and process namespace.
# Inside, /home, /root, /mnt, /tmp, /run and the project folder (wherever it is cloned) are empty; only these are put
# back:
#   the harness code (read-only), the run's output folder, the agent's workspace, and the proxy CA bundle.
# So `find /` cannot reach the project, the reference ports, hidden tests, old runs or other agents' workspaces,
# and /proc only shows the sandbox's own processes. Also read-only: /usr (the Python the evaluator uses) and the
# inputs the agent must not change (Java source, contract, project_structure.txt, public tests).
# The agent runs as the unprivileged user nobody, so it cannot undo these mounts. Its shell commands get no network
# (timeout-bash.sh); Pi itself keeps it for the model API.
# Usage: sandbox.sh <harness dir> <output dir> <workspace dir> <command...>
set -euo pipefail
harness=$(realpath "$1") output=$(realpath "$2") workspace=$(realpath "$3")
shift 3
root=$(dirname "$harness")
chown -R 65534:65534 "$output" "$workspace"
exec unshare --mount --pid --fork --kill-child --mount-proc --propagation private \
  bash -c '
set -euo pipefail
harness=$1 output=$2 workspace=$3 root=$4
shift 4
stage=$(mktemp -d /sandbox-stage.XXXXXX)
mkdir -p "$stage"/{harness,output,workspace,ccr}
mount --bind "$harness" "$stage/harness"
mount --bind "$output" "$stage/output"
mount --bind "$workspace" "$stage/workspace"
[ -d /root/.ccr ] && mount --bind /root/.ccr "$stage/ccr"
for d in /home /root /mnt /tmp /run; do [ -d "$d" ] && mount -t tmpfs -o mode=755 tmpfs "$d"; done
# The project folder (the parent of harness/) holds the reference ports and hidden tests; hide it too, wherever it is
# cloned (unless it already sits under one of the folders above).
if [ "$root" != / ] && [ -d "$root" ]; then mount -t tmpfs -o mode=755 tmpfs "$root"; fi
chmod 1777 /tmp
mkdir -p "$harness" "$output" "$workspace" /root/.ccr
mount --bind "$stage/harness" "$harness" && mount -o remount,bind,ro "$harness"
mount --bind "$stage/output" "$output"
mount --bind "$stage/workspace" "$workspace"
if mountpoint -q "$stage/ccr"; then mount --bind "$stage/ccr" /root/.ccr && mount -o remount,bind,ro /root/.ccr; fi
for d in harness output workspace ccr; do mountpoint -q "$stage/$d" && umount "$stage/$d"; rmdir "$stage/$d"; done
rmdir "$stage"
mount --bind /usr /usr && mount -o remount,bind,ro /usr
for p in source CONTRACT.txt candidate/project_structure.txt candidate/public_tests; do
  if [ -e "$workspace/$p" ]; then mount --bind "$workspace/$p" "$workspace/$p" && mount -o remount,bind,ro "$workspace/$p"; fi
done
export HARNESS_NO_NETWORK=1 HOME=/tmp
cd "$harness"
exec setpriv --reuid=65534 --regid=65534 --clear-groups --inh-caps=-all --bounding-set=-all --no-new-privs "$@"
' sandbox "$harness" "$output" "$workspace" "$root" "$@"
