#!/usr/bin/env bash
# Starts the local hybrid search page. Needs the standalone Ollama instance running (for query
# embeddings) and a built index (codes/.cache/search_index.json — run build_search_index.py
# first, or after processing new lectures).
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"
./start_ollama.sh
../.venv/bin/python3 search_server.py
