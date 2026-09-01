#!/usr/bin/env bash
# Runs on every system boot (see setup instructions in codes/README-ollama.md / crontab).
# Safely resumes lecture processing wherever it left off: process_lecture.py --all only
# processes recordings whose notes file isn't marked "status: done" yet (see
# process_lecture.py's _notes_are_done), so a crash, reboot, or manual kill mid-lecture just
# means that one lecture gets redone from scratch — everything already finished is skipped.
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"

# Standalone Ollama (the system one is stuck on an old version, see README-ollama.md)
./start_ollama.sh

# Wait for it to actually be ready before hammering it with requests.
for i in $(seq 1 30); do
  curl -s http://127.0.0.1:11435/api/version > /dev/null 2>&1 && break
  sleep 2
done

LOG="/tmp/lecture_pipeline_resume_$(date +%Y%m%d_%H%M%S).log"
echo "Resuming lecture processing, logging to $LOG"

for subject in "Managerial Accounting" "Managing People and Organization"; do
  ../.venv/bin/python3 process_lecture.py --subject "$subject" --all >> "$LOG" 2>&1
done

echo "Resume run finished. See $LOG for details."
