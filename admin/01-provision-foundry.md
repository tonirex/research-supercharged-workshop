# 1 · Provision the Foundry resources

Stand up the shared **Basic** Foundry account + project and deploy the lab models. Prerequisites
and the `$sub/$rg/$loc/$acct/$proj` variables are in **[README.md](./README.md)** — set them in a
PowerShell session and keep it open. When you're done here, continue to
**[02-assign-participant-access.md](./02-assign-participant-access.md)**.

```powershell
# (from README — set these first if you haven't)
$sub  = "<your-subscription-id>"
$rg   = "rg-foundry-workshop"
$loc  = "swedencentral"
$acct = "dso-foundry-ws-<unique>"   # globally unique, DNS-safe, lowercase
$proj = "research-workshop"
az account set --subscription $sub
```

---

## 2. Resource group (new)

```powershell
az group create --name $rg --location $loc
```

---

## 3. Foundry account — **Basic** (project-enabled, no BYO search/storage)

The flag that enables projects is `allowProjectManagement`. Creating the account **without**
connecting search/storage keeps it **Basic**.

**Primary path (current Azure CLI ≥ ~2.80 with the `cognitiveservices` project commands):**

```powershell
az cognitiveservices account create `
  --name $acct --resource-group $rg `
  --kind AIServices --sku S0 --location $loc `
  --custom-domain $acct `
  --allow-project-management --yes
```

> **CLI version note:** on CLI **2.73.0** the `--allow-project-management` flag and the
> `az cognitiveservices account project` subgroup were **not yet available**. If `az` rejects the
> flag, either `az upgrade` **or** use the version-independent **ARM REST** fallback below (this is
> what we validated).

**Fallback path (ARM REST via `az rest` — works on any CLI):**

```powershell
$api  = "2026-05-01"
$body = @{
  location = $loc; kind = "AIServices"; sku = @{ name = "S0" }
  identity = @{ type = "SystemAssigned" }
  properties = @{ allowProjectManagement = $true; customSubDomainName = $acct }
} | ConvertTo-Json -Depth 6
$body | Set-Content "$env:TEMP\acct.json" -Encoding utf8
az rest --method put `
  --uri "https://management.azure.com/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct`?api-version=$api" `
  --body "@$env:TEMP\acct.json"
# Poll properties.provisioningState until "Succeeded" before the next step.
```

---

## 4. Project (new)

**Primary path (current CLI):**

```powershell
az cognitiveservices account project create `
  --name $acct --resource-group $rg --project-name $proj --location $loc
```

**Fallback (ARM REST):**

```powershell
$body = @{
  location = $loc; identity = @{ type = "SystemAssigned" }
  properties = @{ displayName = "Research Supercharged Workshop" }
} | ConvertTo-Json -Depth 6
$body | Set-Content "$env:TEMP\proj.json" -Encoding utf8
az rest --method put `
  --uri "https://management.azure.com/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct/projects/$proj`?api-version=$api" `
  --body "@$env:TEMP\proj.json"
```

Get the **SDK endpoint** participants will use (Build rail `.env`):

```powershell
az rest --method get `
  --uri "https://management.azure.com/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct/projects/$proj`?api-version=$api" `
  --query "properties.endpoints"
# -> "AI Foundry API": https://<acct>.services.ai.azure.com/api/projects/<proj>
```

---

## 5. Deploy the lab models

Deploy **two** models. `model-router` is the teaching default (Labs 0–1 portal + all SDK rails);
`gpt-4.1` is **required** for Lab 2's portal **File Search** tool, which does not accept
`model-router`. Size capacity for the participants on **this** project — for a full room, split
across two regions (see [§7](#7-scale-out-across-two-regions-load-balancing)).

```powershell
# model-router — teaching default: Labs 0-1 portal + ALL SDK rails (auto-picks a capable model)
az cognitiveservices account deployment create `
  --name $acct --resource-group $rg `
  --deployment-name model-router `
  --model-name model-router --model-version 2025-11-18 --model-format OpenAI `
  --sku-name GlobalStandard --sku-capacity 100

# gpt-4.1 — REQUIRED for Lab 2 portal File Search (model-router rejected there); also a Web Search fallback
az cognitiveservices account deployment create `
  --name $acct --resource-group $rg `
  --deployment-name gpt-4.1 `
  --model-name gpt-4.1 --model-version 2025-04-14 --model-format OpenAI `
  --sku-name GlobalStandard --sku-capacity 100
```

> **Why deploy `gpt-4.1`:** Lab 2's **portal** File Search tool does **not** accept `model-router`
> (participants get *"File search tool doesn't work with the model you selected"*), so they switch
> their agent to `gpt-4.1` from Lab 2 on. It also serves as a Web Search fallback. (Lab 1 Web
> Search and all **SDK** rails — including SDK File Search — run fine on `model-router`.) See
> [../labs/lab-02-ground-on-your-papers.md](../labs/lab-02-ground-on-your-papers.md).
>
> **Capacity sizing:** `100` = 100K TPM / 100 requests-per-min per deployment — fine for a dry run.
> For 20–30 concurrent participants, request **as much `model-router` + `gpt-4.1` quota as the
> subscription allows**, stagger the heavy labs (RAG indexing, code interpreter), **and/or split the
> room across two regions** ([§7](#7-scale-out-across-two-regions-load-balancing)) so each project
> only serves ~half the room. File Search embeddings are **managed in Basic** — you do **not** deploy
> `text-embedding-3-large` yourself.
>
> **No managed `text-embedding-3-large` deployment is required** for Lab 2 — verified: File Search
> built and queried a managed vector store with no embedding deployment (Basic manages it).

---

## 6. Hand the endpoint to Build-rail participants

- **🟢 Explore (portal):** share the project link from **https://ai.azure.com** → `research-workshop`.
- **🔵 Build (SDK):** participants fill `assets/.env`:

  ```
  FOUNDRY_PROJECT_ENDPOINT=https://<acct>.services.ai.azure.com/api/projects/<proj>
  FOUNDRY_MODEL_NAME=model-router
  # FOUNDRY_WEBSEARCH_MODEL=gpt-4.1   # optional Web Search fallback (model-router works)
  INITIALS=<their-initials>
  ```

  Then `cd assets; az login; pip install -r requirements.txt; python lab01_websearch.py`.

---

## 7. Scale out across two regions (load balancing)

For a full room (20–30 people) provision **two identical projects in two regions** and split the
roster evenly between them. Each Foundry account has its **own** model quota (TPM/RPM) *and* its own
hosted-agent session-concurrency ceiling, so two regional projects roughly **double the effective
capacity** and stop one region's rate limits from throttling the whole room. The labs are
**identical** on both — this is purely a capacity/logistics move, not a content change.

### eastus2 supports every lab tool (validated)

`eastus2` was checked against the official *tool support by region* table **and** the live model
catalog — it matches `swedencentral` for everything the labs use:

| Capability (as used in the labs) | swedencentral | eastus2 |
|---|:--:|:--:|
| **Web Search** — *Search the web with Bing Search* (Lab 1, Grounding with Bing) | ✅ | ✅ |
| **File Search** — managed vector store (Lab 2) | ✅ | ✅ |
| Code Interpreter (Lab 3) | ✅ | ✅ |
| Function / MCP tools (Lab 4) | ✅ | ✅ |
| `model-router` `2025-11-18` available (GlobalStandard) | ✅ | ✅ |
| `gpt-4.1` `2025-04-14` available (GlobalStandard) | ✅ | ✅ |

> **Sources:** the [Tool support by region and model](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/tool-best-practice#tool-support-by-region-and-model)
> table lists `eastus2` as **yes** for File Search, Grounding with Bing Search, Code Interpreter,
> Function and MCP; a live `az cognitiveservices model list --location eastus2` confirms both models
> are offered. Quota is **per-region and independent** — that's exactly why splitting helps. Check
> each region's headroom with `az cognitiveservices usage list --location <region>` and request an
> increase per region if needed.

### Provision both

Give each region its **own resource group** (clean, independent teardown) and a **globally-unique**
account name. Keep the **same project name** (`research-workshop`) in both so participants hear one
instruction. Run the single-region flow (**steps 2–6**) **once per region** with these values:

| Var | Region A | Region B |
|---|---|---|
| `$loc`  | `swedencentral` | `eastus2` |
| `$rg`   | `rg-foundry-workshop-swe` | `rg-foundry-workshop-eus2` |
| `$acct` | `dso-foundry-ws-swe-<unique>` | `dso-foundry-ws-eus2-<unique>` |
| `$proj` | `research-workshop` | `research-workshop` |

```powershell
# Driver: run steps 2-6 for each region. Edit the two <unique> suffixes first.
$sub = "<your-subscription-id>"; az account set --subscription $sub
$proj = "research-workshop"
$regions = @(
  @{ loc='swedencentral'; rg='rg-foundry-workshop-swe';  acct='dso-foundry-ws-swe-<unique>'  },
  @{ loc='eastus2';       rg='rg-foundry-workshop-eus2'; acct='dso-foundry-ws-eus2-<unique>' }
)
foreach ($r in $regions) {
  $loc = $r.loc; $rg = $r.rg; $acct = $r.acct
  az group create --name $rg --location $loc          # step 2
  #  ... now run step 3 (account, Basic), step 4 (project + capture endpoint),
  #      step 5 (deploy model-router + gpt-4.1) exactly as above, using this $loc/$rg/$acct/$proj.
  #  Record each project's SDK endpoint from step 4.
}
```

You finish with **two** SDK endpoints — hand each half of the room **their** region's endpoint:

```
https://dso-foundry-ws-swe-<unique>.services.ai.azure.com/api/projects/research-workshop
https://dso-foundry-ws-eus2-<unique>.services.ai.azure.com/api/projects/research-workshop
```

### Split the roster evenly

Assign **~half** the participants to each project — e.g. **initials A–M → swedencentral**,
**N–Z → eastus2** (or just split the roster list in two). Each half uses **their** region's portal
project and **their** region's endpoint in `.env`; everyone still names agents `rc-<initials>` — no
clashes, because the two projects are completely separate. Grant **Foundry User** RBAC on **each**
account for its half of the room (ideally one Entra group per region) — see
[02-assign-participant-access.md](./02-assign-participant-access.md).

> **Teardown (both regions):**
> ```powershell
> az group delete --name rg-foundry-workshop-swe  --yes --no-wait
> az group delete --name rg-foundry-workshop-eus2 --yes --no-wait
> ```

---

➡️ **Next:** grant participants access — **[02-assign-participant-access.md](./02-assign-participant-access.md)**.
