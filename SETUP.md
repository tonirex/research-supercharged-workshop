# Facilitator Setup & Logistics — Research Supercharged

One-time admin runbook to stand up the **shared Foundry project** for the workshop and grant
participants access. Pairs with [facilitator-guide.md](./facilitator-guide.md) (run-of-show) and
[workshop-plan.md](./workshop-plan.md) (the *why* behind one shared project).

> **Model for this workshop:** a **single shared, _Basic_ Foundry project** for the whole room
> (~20–30 people). Everyone builds agents named `rc-<initials>` in the *same* project. This is the
> simplest thing to run on one subscription; the trade-offs (quota, naming, blast radius) are
> discussed in [workshop-plan.md](./workshop-plan.md).

---

## 0. What "Basic" means here (and why we use it)

A Foundry account can be created in one of two ways, which only changes **where File Search
(Lab 2) stores its vector data**:

| Setup | Vector store / file storage | Needs Azure AI Search? |
|-------|-----------------------------|------------------------|
| **Basic** (this workshop) | **Microsoft-managed** search + storage (IDs look like `vs_…`) | **No** |
| **Standard** | *Your* connected Azure AI Search + Blob Storage | Yes (BYO resources) |

We deliberately use **Basic**: no Azure AI Search or Storage account to provision, connect, or pay
for. File Search "just works" against a managed vector store. (The lab code never changes between
the two — only the backing store differs.) Basic is what you get when you create the account with
`allowProjectManagement` and **do not** connect your own search/storage/Cosmos resources.

---

## 1. Prerequisites

- **Azure CLI** signed in: `az login`. (Validated with CLI `2.73.0`; see the version note in §3.)
- An admin identity with a role that can **create resources and assign roles** — i.e. **Owner**
  (or **Contributor** + **User Access Administrator**) on the subscription or target resource group.
  In Foundry terms, **Foundry Account Owner** can create the account/project and assign Foundry User.
- A list of participant emails (Entra users in your tenant). For 20–30 people, prefer an **Entra
  security group** (see §6) so you assign the role **once**.

Set the variables this runbook uses (PowerShell):

```powershell
$sub  = "<your-subscription-id>"
$rg   = "rg-foundry-workshop"
$loc  = "swedencentral"          # proven model-router + gpt-4.1 capacity
$acct = "dso-foundry-ws-<unique>"  # custom domain must be GLOBALLY unique, DNS-safe (lowercase)
$proj = "research-workshop"
az account set --subscription $sub
```

> **Region:** `swedencentral` was validated for this workshop (good `model-router` + `gpt-4.1`
> quota). `eastus2` also works but had far lower `model-router` quota in our subscription. Pick one
> region and keep the account, project, and deployments together.

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

Two deployments cover every lab. Size capacity for the **whole room** on one project.

```powershell
# model-router — Labs 0/2/3/4 (auto-picks a capable model)
az cognitiveservices account deployment create `
  --name $acct --resource-group $rg `
  --deployment-name model-router `
  --model-name model-router --model-version 2025-11-18 --model-format OpenAI `
  --sku-name GlobalStandard --sku-capacity 100

# gpt-4.1 — Lab 1 Web Search (model-router does NOT support Web Search)
az cognitiveservices account deployment create `
  --name $acct --resource-group $rg `
  --deployment-name gpt-4.1 `
  --model-name gpt-4.1 --model-version 2025-04-14 --model-format OpenAI `
  --sku-name GlobalStandard --sku-capacity 100
```

> **Why `gpt-4.1` too:** the hosted **Web Search** tool requires an Azure OpenAI model;
> `model-router` doesn't support it. Labs 2–4 stay on `model-router`. See
> [lab-01](./labs/lab-01-search-the-literature.md).
>
> **Capacity sizing:** `100` = 100K TPM / 100 requests-per-min per deployment — fine for a dry run.
> For 20–30 concurrent participants, request **as much `model-router` + `gpt-4.1` quota as the
> subscription allows** and stagger the heavy labs (RAG indexing, code interpreter). File Search
> embeddings are **managed in Basic** — you do **not** deploy `text-embedding-3-large` yourself.
>
> **No managed `text-embedding-3-large` deployment is required** for Lab 2 — verified: File Search
> built and queried a managed vector store with only the two deployments above.

---

## 6. RBAC — give participants access (least privilege)

**Role to assign:** **Foundry User** — the least-privilege Foundry role. It grants the data-plane
actions to **build and run agents** (web search, file search, code interpreter, function/MCP tools)
plus reader access — and **nothing else**.

| Built-in role | Build/run agents | Manage models | Create projects/accounts | Assign roles | Publish agents |
|---|:--:|:--:|:--:|:--:|:--:|
| **Foundry User** (participants) | ✅ | ✘ | ✘ | ✘ | ✘ |
| Foundry Project Manager | ✅ | ✘ | ✘ | ✅ (Foundry User only) | ✅ |
| Foundry Account Owner | ✘ | ✅ | ✅ | ✅ | ✘ |
| Foundry Owner | ✅ | ✅ | ✅ | ✅ | ✅ |

> The Foundry roles were **recently renamed**: *Foundry User/Owner/Account Owner/Project Manager*
> were previously *Azure AI User/Owner/Account Owner/Project Manager*. Role **IDs are unchanged** —
> **use the GUID** in scripts to avoid name-rollout issues.
>
> ⚠️ Do **not** use `Cognitive Services *` roles or **Azure AI Developer** for Foundry project
> access — they don't apply to Foundry projects (per Microsoft docs).

**Role IDs:**

| Role | ID |
|------|----|
| **Foundry User** | `53ca6127-db72-4b80-b1b0-d745d6d5456d` |
| Foundry Project Manager | `eadc314b-1a2d-4efa-be10-5d325db5065e` |
| Foundry Account Owner | `e47c6f54-e4a2-4754-9501-8e0985b135e1` |
| Foundry Owner | `c883944f-8b7b-4483-af10-35834be79c4a` |

**Scope:** assign at the **project** (least privilege — participants see only this project, not
other projects in the account). Get the project resource ID:

```powershell
$projScope = az cognitiveservices account project show `
  --name $acct --resource-group $rg --project-name $proj --query id -o tsv
# (or build it: /subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct/projects/$proj)
```

### 6a. One participant (e.g. the representative `janedoe`)

```powershell
$jane = az ad user show --id "janedoe@<tenant>.onmicrosoft.com" --query id -o tsv
az role assignment create `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --assignee-object-id $jane --assignee-principal-type User `
  --scope $projScope
```

### 6b. The whole room (recommended for 20–30 people) — assign **once** to a group

```powershell
# Create a security group, add participants, assign the role to the GROUP at project scope.
$grp = az ad group create --display-name "foundry-workshop-participants" `
        --mail-nickname "foundry-workshop-participants" --query id -o tsv
# add each participant: az ad group member add --group $grp --member-id <userObjectId>
az role assignment create `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --assignee-object-id $grp --assignee-principal-type Group `
  --scope $projScope
```

### 6c. Project managed identity (recommended)

Per Microsoft guidance, also give the **project's managed identity** the Foundry User role on the
**account** (needed by some agent-service operations). If you created the account/project with the
Azure CLI as an **Owner**, this is assigned automatically; with the ARM REST path, assign it:

```powershell
$projMI = az cognitiveservices account project show `
  --name $acct --resource-group $rg --project-name $proj --query identity.principalId -o tsv
$acctScope = "/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct"
az role assignment create `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --assignee-object-id $projMI --assignee-principal-type ServicePrincipal `
  --scope $acctScope
```

### 6d. Verify

```powershell
# Confirm the participant (or group) has Foundry User at the project scope:
az role assignment list --scope $projScope `
  --query "[?roleDefinitionName=='Foundry User'].{principal:principalName,type:principalType}" -o table
```

> **Portal discovery:** a participant signs in at **https://ai.azure.com**, picks the tenant, and
> opens the **`research-workshop`** project. Project-scope **Foundry User** is enough to see and use
> it. If a participant can't *find* the project in the portal, assign Foundry User at the **account**
> scope instead (broader, still no management rights).

---

## 7. Point participants at the project

- **🟢 Explore (portal):** share the project link from **https://ai.azure.com** → `research-workshop`.
- **🔵 Build (SDK):** in `assets/.env`:

  ```
  FOUNDRY_PROJECT_ENDPOINT=https://<acct>.services.ai.azure.com/api/projects/<proj>
  FOUNDRY_MODEL_NAME=model-router
  FOUNDRY_WEBSEARCH_MODEL=gpt-4.1
  INITIALS=<their-initials>
  ```

  Then `cd assets; az login; pip install -r requirements.txt; python lab01_websearch.py`.

---

## 8. Validation — this setup was run end-to-end ✅

Provisioned with the steps above (RG `rg-foundry-workshop`, account `dso-foundry-ws-d457yk`,
project `research-workshop`, **swedencentral**, Basic) and every executable lab passed live:

| Lab | Feature | Result |
|-----|---------|--------|
| 0 | Persona + governance | ✅ in-persona; **declined** a classified-data request |
| 1 | Web Search (`gpt-4.1`) | ✅ grounded answer + deduped citations |
| 2 | File Search (**Basic** managed vector store) | ✅ built `vs_…`, cited source files, **no Azure AI Search** |
| 3 | Code Interpreter | ✅ computed stats, flagged the `S012` outlier |
| 4 | Function tool | ✅ agent called `convert_units` |

`Foundry User` was assigned to the representative participant `janedoe` at **project scope** and
verified. The project was swept clean afterward (0 agents, 0 vector stores).

---

## 9. Teardown (after the workshop)

```powershell
# Deletes the account, project, deployments, and all agents/vector stores in one shot:
az group delete --name $rg --yes --no-wait
```

Remind participants to delete their `rc-<initials>` agents at the end of Lab 5; a full
`az group delete` is the clean way to remove everything when the workshop is over.
