# Research Tools MCP server (Lab 4)

A tiny [Model Context Protocol](https://modelcontextprotocol.io/) server that gives a
Foundry agent real tools it can call. The **admin deploys it once** to Azure Container
Apps before the workshop; on the day, participants just paste one HTTPS URL into their
agent (**Tools → MCP**).

## What it exposes

| Tool | What it does | Why it's here |
| --- | --- | --- |
| `convert_units` | Exact unit conversions (eV↔J, nm↔m, Å↔m, kPa↔atm, °C↔K) in real Python. | Same logic as the SDK rail's function tool (`assets/lab04_tool.py`), so the portal (MCP) and code (function-tool) rails return identical numbers. |
| `search_arxiv` | Live search of the public [arXiv](https://arxiv.org/) preprint API (open access, no key). | The "wow": the agent reaches a real external research service it otherwise can't see. |

The server speaks the MCP **Streamable HTTP** transport, so the endpoint the agent
connects to is:

```
https://<app-fqdn>/mcp
```

A plain `GET /healthz` returns `ok` for quick liveness checks.

## Deploy it (admin, before the workshop)

Full walkthrough: [`admin/03-deploy-mcp-server.md`](../../admin/03-deploy-mcp-server.md).

From this folder, after `az login`:

```powershell
# Windows PowerShell
./deploy.ps1
```

```bash
# macOS / Linux
./deploy.sh
```

The script builds the image in the cloud (no local Docker needed), deploys it with a
public ingress, pins one always-on replica (no cold start), validates `/healthz`, and
prints the `…/mcp` URL to share.

## Run it locally (optional, to hack on it)

```bash
pip install -r requirements.txt
python server.py           # serves http://0.0.0.0:8000/mcp  (+ /healthz)
```

## Security posture

Public and **unauthenticated by design** — it only serves public data and stateless
math, so there is nothing to protect and participants connect with zero setup. **Do not
add secrets or private/classified data to this server.** To lock it down later, front it
with API Management or an API key and pass the header via the Foundry MCP tool config.

## Files

| File | Purpose |
| --- | --- |
| `server.py` | The MCP server (FastMCP, Streamable HTTP). |
| `requirements.txt` | Runtime deps (`mcp`, `httpx`, `uvicorn`). |
| `Dockerfile` | Container image (python:3.12-slim). |
| `deploy.ps1` / `deploy.sh` | One-shot Azure Container Apps deploy. |
| `.dockerignore` | Keeps the build context small. |
