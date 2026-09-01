# Why there are two Ollama instances on this machine

The system's Ollama (`/usr/local/bin/ollama`, systemd service, port `11434`) is stuck on
**v0.6.4** — too old to pull `gemma4:12b`. Updating it needs `sudo`, which wasn't available
non-interactively when this pipeline was built, and the interactive update was never run.

Workaround: a second, newer Ollama (**v0.33.2**) is installed standalone at
`~/.local/share/ollama-standalone/`, with its own model directory
(`~/.ollama-standalone-models/`) so it never needed root access. It runs on port **11435** and
is what `codes/config.yaml`'s `ollama_host` points at. It holds `gemma4:12b` and
`nomic-embed-text`. The old system instance on `:11434` is left alone (unused by this pipeline).

**After a reboot**, the standalone instance won't be running — start it with:

```
codes/start_ollama.sh
```

If you ever do update the system Ollama (`curl -fsSL https://ollama.com/install.sh | sh`,
needs your password), you can simplify by switching `ollama_host` in `config.yaml` back to
`http://localhost:11434` and dropping the standalone instance entirely.
