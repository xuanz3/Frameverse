#!/bin/bash
cd "$(dirname "$0")" || exit 1
if command -v node >/dev/null 2>&1; then
  node server.mjs &
elif command -v python3 >/dev/null 2>&1; then
  python3 -m http.server 8000 --bind 127.0.0.1 &
else
  echo "Install Node.js or Python 3 to preview FRAMEVERSE."
  read -r -p "Press Enter to exit..." _
  exit 1
fi
PID=$!
trap 'kill "$PID" 2>/dev/null' EXIT
sleep 1
open http://localhost:8000/
wait "$PID"
