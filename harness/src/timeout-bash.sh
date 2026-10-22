#!/usr/bin/env bash
# Shell for the agent's bash tool: runs each command with a time limit.
# Pi starts its shell as `<shell> -c <command>`, so wrapping the shell limits every command.
limit="${HARNESS_COMMAND_TIMEOUT:-120}"
# Inside the sandbox, every command runs in its own (unprivileged) user and network namespace without network.
net=()
[ -n "${HARNESS_NO_NETWORK:-}" ] && net=(unshare --user --net)
timeout --kill-after=5 "$limit" "${net[@]}" bash "$@"
code=$?
if [ "$code" -eq 124 ] || [ "$code" -eq 137 ]; then
  echo "[harness] command stopped after ${limit} s (per-command time limit). Make it faster or test a smaller case." >&2
fi
exit "$code"
