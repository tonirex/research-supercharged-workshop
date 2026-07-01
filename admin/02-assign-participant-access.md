# 2 · Assign participant access (RBAC)

Grant participants the least-privilege role that lets them **build and run agents** in the shared
project — and nothing else. Assumes [01-provision-foundry.md](./01-provision-foundry.md) is done and
the `$sub/$rg/$acct/$proj` variables are still set in your PowerShell session.

---

## Role to assign: **Foundry User**

The least-privilege Foundry role. It grants the data-plane actions to **build and run agents** (web
search, file search, code interpreter, function/MCP tools) plus reader access — and **nothing else**.

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

---

## a. One participant (e.g. the representative `janedoe`)

```powershell
$jane = az ad user show --id "janedoe@<tenant>.onmicrosoft.com" --query id -o tsv
az role assignment create `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --assignee-object-id $jane --assignee-principal-type User `
  --scope $projScope
```

## b. The whole room (recommended for 20–30 people) — assign **once** to a group

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

## c. Project managed identity (recommended)

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

## d. Verify

```powershell
# Confirm the participant (or group) has Foundry User at the project scope:
az role assignment list --scope $projScope `
  --query "[?roleDefinitionName=='Foundry User'].{principal:principalName,type:principalType}" -o table
```

---

## Participants finding the project

A participant signs in at **https://ai.azure.com**, picks the tenant, and opens the
**`research-workshop`** project. Project-scope **Foundry User** is enough to see and use it.

> If a participant can't *find* the project in the portal, assign Foundry User at the **account**
> scope instead (broader, still no management rights).

The Build-rail endpoint + `.env` handoff is covered in
[01-provision-foundry.md §6](./01-provision-foundry.md#6-hand-the-endpoint-to-build-rail-participants).

---

✅ **Done.** Confirm the [pre-flight checklist](../facilitator/facilitator-guide.md) and you're ready
to run the workshop.
