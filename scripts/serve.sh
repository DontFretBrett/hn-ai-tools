#!/bin/bash
# Start/restart only the server managed by this project's pidfile.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/logs"
PIDFILE="$ROOT/logs/server.pid"
LOCKDIR="$ROOT/logs/serve.lock"
if ! mkdir "$LOCKDIR" 2>/dev/null; then
  echo 'Another serve.sh invocation is running (logs/serve.lock).' >&2
  exit 1
fi
trap 'rmdir "$LOCKDIR"' EXIT
if [ -f "$PIDFILE" ]; then
  old_pid="$(cat "$PIDFILE")"
  if [[ "$old_pid" =~ ^[0-9]+$ ]] && [ "$old_pid" -gt 1 ] && kill -0 "$old_pid" 2>/dev/null; then
    old_command="$(ps -p "$old_pid" -o args=)"
    case "$old_command" in
      *"-m http.server 8788 --bind 0.0.0.0 --directory $ROOT/web")
        kill "$old_pid"
        for unused in {1..30}; do
          kill -0 "$old_pid" 2>/dev/null || break
          sleep 0.1
        done
        ;;
      *) echo 'Pidfile points to another process; leaving that process alone.' >&2 ;;
    esac
  fi
  rm -f "$PIDFILE"
fi
PYTHON="$ROOT/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then PYTHON="$(command -v python3)"; fi
nohup "$PYTHON" -m http.server 8788 --bind 0.0.0.0 --directory "$ROOT/web" > "$ROOT/logs/server.log" 2>&1 < /dev/null &
server_pid=$!
printf '%s\n' "$server_pid" > "$PIDFILE"
sleep 0.5
if ! kill -0 "$server_pid" 2>/dev/null; then
  rm -f "$PIDFILE"
  echo 'Server failed to start. See logs/server.log (the port may already be in use).' >&2
  exit 1
fi
echo "Serving http://0.0.0.0:8788 (PID $server_pid; logs/server.log)"
