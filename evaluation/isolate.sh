#!/usr/bin/env bash
# Runs a command on a migrated candidate (pytest, an import check) so the candidate's code cannot see anything
# but the folders it is given: own mount, process and network namespace; /home, /root, /mnt, /tmp, /run and the
# project folder are empty; /usr is read-only; the command runs as the unprivileged user nobody, so it cannot
# undo the mounts. Used by the evaluator and by the harness's own test and import checks.
# Usage: isolate.sh <dir>... -- <command...>   (each <dir> is put back read-write at its own path; runs in the first)
set -euo pipefail
root=$(realpath "$(dirname "$0")/..")
dirs=()
while [ "$1" != -- ]; do dirs+=("$(realpath "$1")"); shift; done
shift
chown -R 65534:65534 "${dirs[@]}"
exec unshare --mount --pid --net --fork --kill-child --mount-proc --propagation private \
  bash -c '
set -euo pipefail
root=$1 n=$2
shift 2
dirs=("${@:1:$n}")
shift "$n"
stage=$(mktemp -d /isolate-stage.XXXXXX)
for i in "${!dirs[@]}"; do mkdir "$stage/$i" && mount --bind "${dirs[$i]}" "$stage/$i"; done
for d in /home /root /mnt /tmp /run; do [ -d "$d" ] && mount -t tmpfs -o mode=755 tmpfs "$d"; done
if [ "$root" != / ] && [ -d "$root" ]; then mount -t tmpfs -o mode=755 tmpfs "$root"; fi
chmod 1777 /tmp
for i in "${!dirs[@]}"; do mkdir -p "${dirs[$i]}" && mount --bind "$stage/$i" "${dirs[$i]}" && umount "$stage/$i" && rmdir "$stage/$i"; done
rmdir "$stage"
cd "${dirs[0]}"
mount --bind /usr /usr && mount -o remount,bind,ro /usr
export HOME=/tmp
exec setpriv --reuid=65534 --regid=65534 --clear-groups --inh-caps=-all --bounding-set=-all --no-new-privs "$@"
' isolate "$root" "${#dirs[@]}" "${dirs[@]}" "$@"
