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

One deployment (`model-router`) covers every lab; a second (`gpt-4.1`) is an **optional** Web
Search fallback. Size capacity for the **whole room** on one project.

```powershell
# model-router — ALL labs 0-4 (auto-picks a capable model; handles Web Search too)
az cognitiveservices account deployment create `
  --name $acct --resource-group $rg `
  --deployment-name model-router `
  --model-name model-router --model-version 2025-11-18 --model-format OpenAI `
  --sku-name GlobalStandard --sku-capacity 100

# gpt-4.1 — OPTIONAL Web Search fallback (model-router handles Web Search fine)
az cognitiveservices account deployment create `
  --name $acct --resource-group $rg `
  --deployment-name gpt-4.1 `
  --model-name gpt-4.1 --model-version 2025-04-14 --model-format OpenAI `
  --sku-name GlobalStandard --sku-capacity 100
```

> **Why deploy `gpt-4.1` (optional):** Web Search works on `model-router` (verified), so all labs
> run on the default. Deploy `gpt-4.1` only if you want a reliable Web Search **fallback**. See
> [../labs/lab-01-search-the-literature.md](../labs/lab-01-search-the-literature.md).
>
> **Capacity sizing:** `100` = 100K TPM / 100 requests-per-min per deployment — fine for a dry run.
> For 20–30 concurrent participants, request **as much `model-router` quota as the subscription
> allows** (and some for `gpt-4.1` if you deployed the fallback) and stagger the heavy labs (RAG
> indexing, code interpreter). File Search
> embeddings are **managed in Basic** — you do **not** deploy `text-embedding-3-large` yourself.
>
> **No managed `text-embedding-3-large` deployment is required** for Lab 2 — verified: File Search
> built and queried a managed vector store with only `model-router` deployed.

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

➡️ **Next:** grant participants access — **[02-assign-participant-access.md](./02-assign-participant-access.md)**.
