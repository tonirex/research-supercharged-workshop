# 3 · Deploy the Lab 4 MCP server (Azure Container Apps)

**Optional but recommended** — do this once before the workshop so **Lab 4 (portal rail)**
has a real remote tool for participants to connect to. It publishes a small
[MCP](https://modelcontextprotocol.io/) server to **Azure Container Apps** with a public
HTTPS endpoint. On the day, participants paste **one URL** into their agent
(**Tools → MCP**) — no per-person setup.

> **Skip it?** Lab 4 still works without this: the **SDK rail** uses a local function tool,
> and the portal rail has a "no MCP server on the day" fallback (a built-in tool). Deploy
> this only if you want participants to experience connecting to a live remote MCP tool.

Source lives in **[`../assets/mcp-server/`](../assets/mcp-server/)** (server + Dockerfile +
deploy scripts). What it exposes:

| Tool | Does |
| --- | --- |
| `convert_units` | Exact unit conversions (eV↔J, nm↔m, Å↔m, kPa↔atm, °C↔K) — same logic as the SDK rail. |
| `search_arxiv` | Live search of the public arXiv preprint API (open access, no key). |

---

## Prerequisites

- **Azure CLI** signed in (`az login`) as an identity with **Contributor** (or Owner) on
  the subscription or the workshop resource group.
- Reuses the workshop resource group from
  [01-provision-foundry.md](./01-provision-foundry.md) (`rg-foundry-workshop`) so teardown
  stays a single `az group delete`. No Docker needed locally — the image is built in the
  cloud.

---

## Deploy it (one command)

From the repo, `cd` into the server folder and run the script for your OS:

```powershell
# Windows PowerShell
cd assets/mcp-server
./deploy.ps1
```

```bash
# macOS / Linux
cd assets/mcp-server
./deploy.sh
```

Defaults match this workshop (`-ResourceGroup rg-foundry-workshop`,
`-Location swedencentral`, `-AppName mcp-research-tools`). Override if needed, e.g.
`./deploy.ps1 -ResourceGroup my-rg -Location eastus2`.

The script:

1. Registers the `containerapp` CLI extension + `Microsoft.App` / `Microsoft.OperationalInsights` providers.
2. Ensures the resource group exists.
3. Runs `az containerapp up --source .` — builds the image in the cloud (ACR), creates a
   Container Apps environment, and deploys the app with an **external (public) ingress** on
   port **8000**.
4. Pins **min 1 replica** (no cold start during the workshop), max 3.
5. Validates `/healthz` and prints the MCP URL.

**First run takes a few minutes** (it provisions an ACR + environment). Expected tail:

```
============================================================
 MCP server is live. Share this URL with participants (Lab 4):

   https://mcp-research-tools.<hash>.swedencentral.azurecontainerapps.io/mcp

 Health check:  https://mcp-research-tools.<hash>.swedencentral.azurecontainerapps.io/healthz
 Tear down:     az group delete --name rg-foundry-workshop --yes --no-wait
============================================================
```

> **Prefer raw CLI?** The script is just:
> ```bash
> az containerapp up --name mcp-research-tools --resource-group rg-foundry-workshop \
>   --location swedencentral --environment cae-foundry-workshop \
>   --source . --ingress external --target-port 8000
> ```
> then `az containerapp update ... --min-replicas 1 --max-replicas 3`.

---

## Validate

```powershell
# 1) Liveness (should print: ok)
curl.exe https://<app-fqdn>/healthz

# 2) MCP handshake — confirm the tools are advertised (optional; needs the mcp package)
#    pip install mcp, then:
python -c "import asyncio; from mcp import ClientSession; from mcp.client.streamable_http import streamablehttp_client;
async def m():
    async with streamablehttp_client('https://<app-fqdn>/mcp') as (r,w,_):
        async with ClientSession(r,w) as s:
            await s.initialize(); print([t.name for t in (await s.list_tools()).tools])
asyncio.run(m())"
# -> ['convert_units', 'search_arxiv']
```

Best end-to-end check: in the Foundry portal, open a test agent → **Tools → MCP** → paste
`https://<app-fqdn>/mcp` → ask *"Convert 1.8 eV to joules."* The agent should call
`convert_units` and answer `≈ 2.884e-19 J`.

---

## Hand it to the facilitator

Give the facilitator the **`https://<app-fqdn>/mcp`** URL. They share it on a slide / in
chat at the start of Lab 4. Participants set **Require approval = Always** so they can watch
each call (see [../labs/lab-04-add-a-tool.md](../labs/lab-04-add-a-tool.md)).

---

## Cost & teardown

A single always-on ACA replica (0.5 vCPU / 1 GiB) is a few cents/hour; drop `--min-replicas`
to 0 after the workshop if you want to keep it around cheaply (adds a small cold-start
delay). It lives in `rg-foundry-workshop`, so the standard teardown removes it too:

```powershell
az group delete --name rg-foundry-workshop --yes --no-wait
```

---

## Security posture

The server is **public and unauthenticated by design** — it serves only public data and
stateless math, so there's nothing to protect and participants connect with zero setup.
**Do not add secrets or private/classified data to it.** To lock it down for reuse beyond
the workshop, front it with API Management or an API key and pass the header from the
Foundry MCP tool config.
