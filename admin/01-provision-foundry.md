# 1 · Provision the Foundry resources (two regions)

> **Goal — new deployment for the DSO workshop:** stand up **two identical _Basic_ Foundry projects**
> — one in **`swedencentral`**, one in **`eastus2`** — and **split the roster evenly** between them.
> Two regional projects give you **independent model quota (TPM/RPM)** *and* **double the hosted-agent
> session-concurrency ceiling**, so one region's rate limits can't throttle the whole room. The labs
> are **identical** on both — this is purely a capacity/logistics move.

Prerequisites (Owner rights, CLI) are in **[README.md](./README.md)**. When both regions are up,
continue to **[02-assign-participant-access.md](./02-assign-participant-access.md)** to grant access.

> **Just doing a dry run or a small group?** Provision **one** region: run **Steps 1–4** once and
> **skip Step 5**. Everything else is identical.

---

## What you'll build

Two resource groups, each holding one **Basic** Foundry account + one project (`research-workshop`),
each with the two lab models. Half the participants use each region.

| | Region A | Region B |
|---|---|---|
| **Region** (`$loc`) | `swedencentral` | `eastus2` |
| **Resource group** (`$rg`) | `rg-foundry-workshop-swe` | `rg-foundry-workshop-eus2` |
| **Account** (`$acct`, globally unique) | `dso-foundry-ws-swe-<unique>` | `dso-foundry-ws-eus2-<unique>` |
| **Project** (`$proj`) | `research-workshop` | `research-workshop` |
| **Models** | `model-router` + `gpt-5.4` | `model-router` + `gpt-5.4` |
| **Roster half** | initials **A–M** | initials **N–Z** |

**Both regions support every lab tool** — verified against the official *tool support by region* table
**and** a live model-catalog check, and **stood up + smoke-tested end-to-end** in both regions:

| Capability (as used in the labs) | swedencentral | eastus2 |
|---|:--:|:--:|
| **Web Search** — *Search the web with Bing Search* (Lab 1) | ✅ | ✅ |
| **File Search** — managed vector store (Lab 2) | ✅ | ✅ |
| Code Interpreter (Lab 3) | ✅ | ✅ |
| Function / MCP tools (Lab 4) | ✅ | ✅ |
| `model-router 2025-11-18` · `gpt-5.4 2026-03-05` (GlobalStandard) | ✅ | ✅ |

> Source: [Tool support by region and model](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/tool-best-practice#tool-support-by-region-and-model).
> Quota is **per-region and independent** — that's exactly why splitting helps. Check each region's
> headroom with `az cognitiveservices usage list --location <region>` and request an increase per
> region if needed.

---

## Before you start

- **Azure CLI ≥ 2.80.0**, signed in as an **Owner** (or Contributor + User Access Administrator) on the
  subscription: `az login`. **2.80.0 is the floor** — it's the release that adds
  `az cognitiveservices account project` (Step 3); `--allow-project-management` (Step 2) landed in 2.78.0
  and `deployment create` is legacy. Enforce it up front so a stale CLI fails fast instead of half-way
  through:

  ```powershell
  $min = [version]"2.80.0"
  $cur = [version](az version --query '"azure-cli"' -o tsv)
  if ($cur -lt $min) { throw "Azure CLI $cur is too old — need >= $min. Run 'az upgrade' (or reinstall)." }
  "Azure CLI $cur — OK"
  ```

  (Can't upgrade the CLI? Use the [ARM REST fallback](#arm-rest-fallback-any-cli-version) — it works on
  any version and is what this workshop was originally validated on.)
- Choose the two **globally-unique** account names now (lowercase, DNS-safe).

Set the shared variables and **Region A** values. You'll run **Steps 1–4 once per region** — start with
Region A, then switch to Region B in Step 5:

```powershell
$sub  = "<your-subscription-id>"
az account set --subscription $sub

# ---- Region A (swedencentral) ----
$loc  = "swedencentral"
$rg   = "rg-foundry-workshop-swe"
$acct = "dso-foundry-ws-swe-<unique>"   # globally unique, DNS-safe, lowercase
$proj = "research-workshop"
```

---

## Step 1 — Resource group

```powershell
az group create --name $rg --location $loc
```

---

## Step 2 — Foundry account (Basic)

A **Basic** account is project-enabled (`--allow-project-management`) with **no** connected Azure AI
Search/Storage, so File Search (Lab 2) uses a **Microsoft-managed** vector store — nothing else to
provision or pay for.

```powershell
az cognitiveservices account create `
  --name $acct --resource-group $rg `
  --kind AIServices --sku S0 --location $loc `
  --custom-domain $acct `
  --allow-project-management true `
  --assign-identity `
  --yes
```

The command waits for provisioning and prints the account (expect `provisioningState: Succeeded` and a
system-assigned identity). `--custom-domain $acct` is **required** — it gives the account its
`<acct>.services.ai.azure.com` host for token auth; `--allow-project-management true` is what makes it a
project-enabled Foundry (Basic) account.

> **No CLI ≥ 2.80.0?** Do this step via the [ARM REST fallback](#arm-rest-fallback-any-cli-version).

---

## Step 3 — Project + SDK endpoint

Create the project, then **record the SDK endpoint** (participants' Build-rail `.env`):

```powershell
az cognitiveservices account project create `
  --name $acct --resource-group $rg `
  --project-name $proj --location $loc `
  --display-name "Research Supercharged Workshop"

# The endpoint each participant in THIS region uses — write it down. The host is the account's
# custom domain, so it's deterministic:
"https://$acct.services.ai.azure.com/api/projects/$proj"
# -> https://<acct>.services.ai.azure.com/api/projects/research-workshop
# (Confirm against the portal: project -> Overview -> Endpoint.)
```

The project gets a **system-assigned managed identity** by default — that's the identity you grant
**Foundry User** to in [02-assign-participant-access.md](./02-assign-participant-access.md).

> **No CLI ≥ 2.80.0?** Do this step via the [ARM REST fallback](#arm-rest-fallback-any-cli-version).

---

## Step 4 — Deploy the two lab models

Deploy **two** models. `model-router` is the teaching default (Labs 0–1 portal + all SDK rails);
`gpt-5.4` is **required** for Lab 2's portal **File Search** tool, which does not accept
`model-router`. Size capacity for the **whole room** on one project.

```powershell
az cognitiveservices account deployment create `
  --name $acct --resource-group $rg `
  --deployment-name model-router `
  --model-name model-router --model-version 2025-11-18 --model-format OpenAI `
  --sku-name GlobalStandard --sku-capacity 100

# gpt-5.4 — REQUIRED for Lab 2 portal File Search (model-router rejected there); also a Web Search fallback
az cognitiveservices account deployment create `
  --name $acct --resource-group $rg `
  --deployment-name gpt-5.4 `
  --model-name gpt-5.4 --model-version 2026-03-05 --model-format OpenAI `
  --sku-name GlobalStandard --sku-capacity 100
```

> **Why deploy `gpt-5.4`:** Lab 2's **portal** File Search tool does **not** accept `model-router`
> (participants get *"File search tool doesn't work with the model you selected"*), so they switch
> their agent to `gpt-5.4` from Lab 2 on. It also serves as a Web Search fallback. (Lab 1 Web
> Search and all **SDK** rails — including SDK File Search — run fine on `model-router`.) See
> [../labs/lab-02-ground-on-your-papers.md](../labs/lab-02-ground-on-your-papers.md).
>
> **Model versions age out.** If a deploy is rejected with `ServiceModelDeprecating` ("cannot be
> used for new deployments"), that pinned version has deprecated — drop `--model-version` to take the
> current default, or pin a newer one (e.g. a later `gpt-5.x`). List what's deployable first:
> `az cognitiveservices account list-models --name $acct --resource-group $rg --query "[?name=='gpt-5.4'].version" -o tsv`.
> `gpt-5.4` `2026-03-05` was current when this was written.
>
> **Capacity sizing:** `100` = 100K TPM / 100 requests-per-min per deployment — fine for a dry run.
> For 20–30 concurrent participants, request **as much `model-router` + `gpt-5.4` quota as the
> subscription allows** and stagger the heavy labs (RAG indexing, code interpreter). File Search
> embeddings are **managed in Basic** — you do **not** deploy `text-embedding-3-large` yourself.
>
> **No managed `text-embedding-3-large` deployment is required** for Lab 2 — verified: File Search
> built and queried a managed vector store with no embedding deployment (Basic manages it).

---

## Step 5 — Repeat for the second region

Provision **Region B**. Re-set the four region variables and run **Steps 1 → 4 again** (`$sub` and
`$api` stay the same):

```powershell
# ---- Region B (eastus2) ----
$loc  = "eastus2"
$rg   = "rg-foundry-workshop-eus2"
$acct = "dso-foundry-ws-eus2-<unique>"   # a DIFFERENT globally-unique name
$proj = "research-workshop"
# now re-run Step 1, Step 2, Step 3 (capture this region's endpoint), Step 4.
```

You should finish with **two** SDK endpoints — one per region:

```
https://dso-foundry-ws-swe-<unique>.services.ai.azure.com/api/projects/research-workshop    # roster A–M
https://dso-foundry-ws-eus2-<unique>.services.ai.azure.com/api/projects/research-workshop    # roster N–Z
```

---

## Step 6 — Split the roster & hand out access

Assign **~half** the roster to each project — e.g. **initials A–M → swedencentral**, **N–Z → eastus2**
(or just split the roster list in two). Everyone still names agents `rc-<initials>` — no clashes, the
two projects are completely separate. Give each half **their** region's access:

- **🟢 Explore (portal):** the project link from **https://ai.azure.com** → `research-workshop` in
  **their** region's account.
- **🔵 Build (SDK):** their region's endpoint in `assets/.env`:

  ```
  FOUNDRY_PROJECT_ENDPOINT=https://<their-region-acct>.services.ai.azure.com/api/projects/research-workshop
  FOUNDRY_MODEL_NAME=model-router
  # FOUNDRY_WEBSEARCH_MODEL=gpt-5.4   # optional Web Search fallback (model-router works)
  INITIALS=<their-initials>
  ```

  Then `cd assets; az login; pip install -r requirements.txt; python lab01_websearch.py`.

➡️ **Next:** grant **Foundry User** RBAC — on **both** accounts, each for its half of the room — in
**[02-assign-participant-access.md](./02-assign-participant-access.md)**.

---

## Verify both projects

Run once **per region** (set `$rg`/`$acct` to each region's values). Expect the account and **both**
deployments to report `Succeeded`:

```powershell
az cognitiveservices account show -n $acct -g $rg `
  --query "{kind:kind, state:properties.provisioningState}" -o json

az cognitiveservices account deployment list -n $acct -g $rg `
  --query "[].{name:name, model:properties.model.name, ver:properties.model.version, sku:sku.name, cap:sku.capacity, state:properties.provisioningState}" -o table
```

Expected: `kind = AIServices`; two deployments — `model-router 2025-11-18` and `gpt-5.4 2026-03-05`,
both `GlobalStandard` / `Succeeded`. (This is exactly what was validated live in both regions.)

---

## Teardown

After the workshop, delete **both** resource groups — this removes the accounts, projects, deployments,
and every participant's agents/vector stores in one shot:

```powershell
az group delete --name rg-foundry-workshop-swe  --yes --no-wait
az group delete --name rg-foundry-workshop-eus2 --yes --no-wait
```

---

## ARM REST fallback (any CLI version)

Only needed if you **can't** reach Azure CLI **2.80.0** (e.g. a locked build agent). This is the path
the workshop was originally validated on — it calls ARM REST directly, so any CLI version works. Set
`$api` once, then use these blocks **in place of Step 2 / Step 3** (Steps 1 and 4 are unchanged):

```powershell
$api = "2026-05-01"
```

**Account (replaces Step 2):**

```powershell
$acctUri = "https://management.azure.com/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct" + "?api-version=$api"
$body = @{
  location = $loc; kind = "AIServices"; sku = @{ name = "S0" }
  identity = @{ type = "SystemAssigned" }
  properties = @{ allowProjectManagement = $true; customSubDomainName = $acct }
} | ConvertTo-Json -Depth 6
$body | Set-Content "$env:TEMP\acct.json" -Encoding utf8
az rest --method put --uri $acctUri --body "@$env:TEMP\acct.json"

do { Start-Sleep 8; $state = az rest --method get --uri $acctUri --query "properties.provisioningState" -o tsv }
while ($state -ne "Succeeded" -and $state -ne "Failed")
"account: $state"
```

**Project + endpoint (replaces Step 3):**

```powershell
$projUri = "https://management.azure.com/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct/projects/$proj" + "?api-version=$api"
$body = @{
  location = $loc; identity = @{ type = "SystemAssigned" }
  properties = @{ displayName = "Research Supercharged Workshop" }
} | ConvertTo-Json -Depth 6
$body | Set-Content "$env:TEMP\proj.json" -Encoding utf8
az rest --method put --uri $projUri --body "@$env:TEMP\proj.json"

do { Start-Sleep 6; $pstate = az rest --method get --uri $projUri --query "properties.provisioningState" -o tsv }
while ($pstate -ne "Succeeded" -and $pstate -ne "Failed")
"project: $pstate"

# The endpoint each participant in THIS region will use — write it down:
az rest --method get --uri $projUri --query "properties.endpoints.\"AI Foundry API\"" -o tsv
# -> https://<acct>.services.ai.azure.com/api/projects/research-workshop
```
