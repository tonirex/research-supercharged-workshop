# Build (SDK) rail — setup & run

The 🔵 Build rail recreates each lab in ~10 lines of Python on the **current Foundry agents API**
(`azure-ai-projects` 2.x). All the SDK plumbing lives in **`common/research_common.py`** so the
lab scripts stay short.

> ⚠️ **Public / unclassified data only.** Don't upload sensitive, classified, or personal data to
> any agent, vector store, or code-interpreter session.

## Prerequisites
- **Python 3.10+**
- Access to the **shared workshop project** (endpoint from your facilitator)
- `az login` working (the SDK auths with `DefaultAzureCredential`)

## GitHub Codespaces (recommended — zero local install)
This repo ships a **devcontainer** (`.devcontainer/`) that pre-installs Python 3.12, the Azure CLI,
and all Build-rail dependencies, and seeds `assets/.env` for you on first build.

1. **Code ▸ Create codespace** on your branch — wait for the container to finish building.
2. In the terminal, sign in: `az login --use-device-code` (copy the code into your browser).
3. Edit **`assets/.env`** → set `FOUNDRY_PROJECT_ENDPOINT` and `INITIALS`.
4. `cd assets`, then run the labs (see **Run the labs** below).

Prefer your own machine? Use the manual setup instead:

## One-time setup (run inside `assets/`)
```bash
az login
copy .env.example .env        # macOS/Linux: cp .env.example .env
#  → edit .env: FOUNDRY_PROJECT_ENDPOINT, INITIALS (FOUNDRY_MODEL_NAME defaults to model-router)
pip install -r requirements.txt
```

| Variable | What |
|----------|------|
| `FOUNDRY_PROJECT_ENDPOINT` | `https://<account>.services.ai.azure.com/api/projects/<project>` (shared project) |
| `FOUNDRY_MODEL_NAME` | model deployment — `model-router` (default) auto-picks a good model |
| `FOUNDRY_WEBSEARCH_MODEL` | *optional* — pin a fallback model for Web Search (defaults to `model-router`, which works) |
| `INITIALS` | your initials → agents are named `rc-<initials>` to keep the shared project tidy |

## Run the labs
Run each from the `assets/` folder:
```bash
python lab01_websearch.py        # Lab 1 — web search + citations
python lab02_filesearch.py       # Lab 2 — RAG over assets/corpus (add your docs first)
python lab03_codeinterpreter.py  # Lab 3 — analyse assets/data/sample_experiments.csv
python lab04_tool.py             # Lab 4 — function calling (asserts the tool was used)
```

## The helper — `common/research_common.py`
Everything you need, on the current API:

| Function | Does |
|----------|------|
| `research_agent(suffix, tools=, …)` | create an `rc-<initials>` agent (`create_version` + `PromptAgentDefinition`) |
| `run_text(agent, text)` / `run_response(...)` | single-turn call via the Responses API |
| `run_with_trace(agent, text, functions=)` | runs the function-tool loop and records which tools fired |
| `web_search_tool()` · `file_search_tool(vs)` · `code_interpreter_tool()` | hosted tools |
| `function_tool(...)` · `mcp_tool(...)` | your own function / an MCP server |
| `build_vector_store(folder=)` | index `assets/corpus` into a vector store |
| `citations_of(response)` · `cleanup(*agents)` | pull cited sources · delete your agents |

## Troubleshooting
- **`Set FOUNDRY_PROJECT_ENDPOINT…`** → your `.env` isn't filled in, or you're not running from `assets/`.
- **Auth errors** → run `az login`; make sure you can see the shared project in the portal.
- **`pip install` fails building a wheel** (e.g. `cryptography`) → upgrade build tools first, then retry:
  ```bash
  python -m pip install --upgrade pip setuptools wheel
  pip install --prefer-binary -r requirements.txt
  ```
- **`ModuleNotFoundError: common`** → run the script from the `assets/` folder (the scripts add it to
  the path automatically, but the working directory must contain `common/`).
- **Lab 2 says "No files to index"** → add a few public docs to `assets/corpus/` first.
