# Dialogue Engine (Plug-and-Play)

Portable AI dialogue service for games (Ollama optional).

## Goals
- Engine-agnostic HTTP API (`/v1/...`)
- Local-first model support (Ollama)
- Persona + world-state aware prompts
- Memory store (SQLite)
- Safe fallback responses on failure

## Providers
- `built_in` (**New default**): Downloads a lightweight GGUF model via HuggingFace and runs it directly within the engine process using `llama.cpp`. Truly plug-and-play.
- `template`: no model dependency, fully self-contained static responses.
- `ollama`: local model server.
- `openai_compatible`: any OpenAI-style endpoint (local or remote).

Switch providers in `config.yaml`.

## Quick Start (Built-in Local Model)
1) Create env and install deps (includes `llama-cpp-python` and `huggingface-hub`):

```bat
F:\dev-test\dialogue-engine\setup_env.bat
```

2) Ensure `config.yaml` is set to `built_in` (this is the default):
```yaml
model:
  provider: built_in
  repo_id: bartowski/SmolLM2-1.7B-Instruct-GGUF
  filename: SmolLM2-1.7B-Instruct-Q4_K_M.gguf
  n_ctx: 2048
```

3) Run server (will automatically download the model on first boot):

```bat
F:\dev-test\dialogue-engine\run_server.bat
```

4) Health check:

```bash
curl http://127.0.0.1:8787/v1/health
```

## API
- `GET /v1/health`
- `POST /v1/dialogue/generate`
- `POST /v1/memory/write`

See `examples/requests.http` for payloads.

## Godot Integration
Use `examples/godot/dialogue_client.gd` as a drop-in client.
## Quick Start (With Ollama)
1) Set in `config.yaml`:

```yaml
model:
  provider: ollama
  name: tinyllama:1.1b
```

2) Pull model:

```bash
ollama pull tinyllama:1.1b
```

3) Start server with `run_server.bat`.
