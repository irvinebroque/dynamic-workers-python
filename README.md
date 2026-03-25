## Simple Python Dynamic Worker Demo

This repo now shows only the basics:

- a host Cloudflare Worker written in Python
- a Dynamic Worker written in Python
- the host forwards the incoming request to the Dynamic Worker
- the Dynamic Worker returns a simple hello-world response

It mirrors the Dynamic Workers docs example, but written entirely in Python.

### Files

- `src/entry.py` is the whole demo
- the Dynamic Worker source is embedded as a Python string in `src/entry.py`

### Run locally

```bash
uv venv
uv sync
uv run pywrangler dev
```

Then open:

- `http://127.0.0.1:8787/`

### How it works

- `wrangler.jsonc` configures the `LOADER` binding with `worker_loaders`
- `src/entry.py` defines the Dynamic Worker source as a Python string
- `env.LOADER.load()` creates a one-off Dynamic Worker at request time
- the host forwards the incoming request to the loaded worker via `request.js_object`
- the child response is converted back with `python_from_rpc`
- the Dynamic Worker returns `Hello from a dynamic Worker`
