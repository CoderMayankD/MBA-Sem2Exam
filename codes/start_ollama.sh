#!/usr/bin/env bash
# Starts the standalone Ollama v0.33.2 instance the pipeline uses (port 11435), separate from
# the system Ollama service on :11434 (which is stuck on v0.6.4 — updating it needs sudo, which
# wasn't available when this was set up). Run this after every reboot before using the pipeline.
set -e
export OLLAMA_HOST=127.0.0.1:11435
export OLLAMA_MODELS="$HOME/.ollama-standalone-models"
if curl -s "http://127.0.0.1:11435/api/version" > /dev/null 2>&1; then
  echo "Already running on :11435"
else
  nohup "$HOME/.local/share/ollama-standalone/bin/ollama" serve > /tmp/ollama-standalone.log 2>&1 &
  disown
  sleep 2
  echo "Started standalone Ollama on :11435 (log: /tmp/ollama-standalone.log)"
fi
curl -s "http://127.0.0.1:11435/api/version"
echo
