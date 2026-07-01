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

**Scope:** assign at the **Foundry account** (the *parent resource* of the project). Per Microsoft
docs, *"on the parent resource of your project, you need the Foundry User role to access model
deployments and create agents."*

> ⚠️ **Do NOT assign at project scope only.** Model deployments live at the **account** level, and
> Azure RBAC inherits **downward** (account → project), not upward. A project-scoped assignment
> can't read the account's deployments, so participants get an **empty "Deployed models" list and
> can't create agents** (the portal tells them to ask for *Foundry Owner*). Account scope fixes both
> — and Foundry User at account scope **still can't deploy or manage models** (that needs Owner),
> so it stays least-privilege. With one project in the account, account scope exposes nothing extra.

Get the account resource ID:

```powershell
$acctScope = "/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct"
```

> **Two-region setup?** If you provisioned two projects
> ([01-provision-foundry.md §7](./01-provision-foundry.md#7-scale-out-across-two-regions-load-balancing)),
> run this assignment **once per account** — set `$rg`/`$acct` to each region's values and grant that
> region's **half** of the roster (ideally one Entra group per region). Everything below is per-account.

---

## a. One participant (e.g. the representative `janedoe`)

```powershell
$jane = az ad user show --id "janedoe@<tenant>.onmicrosoft.com" --query id -o tsv
az role assignment create `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --assignee-object-id $jane --assignee-principal-type User `
  --scope $acctScope
```

## b. The whole room (recommended for 20–30 people) — assign **once** to a group

```powershell
# Create a security group, add participants, assign the role to the GROUP at account scope.
$grp = az ad group create --display-name "foundry-workshop-participants" `
        --mail-nickname "foundry-workshop-participants" --query id -o tsv
# add each participant: az ad group member add --group $grp --member-id <userObjectId>
az role assignment create `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --assignee-object-id $grp --assignee-principal-type Group `
  --scope $acctScope
```

## c. Project managed identity (recommended)

Per Microsoft guidance, also give the **project's managed identity** the Foundry User role on the
**account** (needed by some agent-service operations). If you created the account/project with the
Azure CLI as an **Owner**, this is assigned automatically; with the ARM REST path, assign it:

```powershell
$projMI = az cognitiveservices account project show `
  --name $acct --resource-group $rg --project-name $proj --query identity.principalId -o tsv
az role assignment create `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --assignee-object-id $projMI --assignee-principal-type ServicePrincipal `
  --scope $acctScope
```

## d. Verify

```powershell
# Confirm the participant (or group) has Foundry User at the ACCOUNT scope:
az role assignment list --scope $acctScope `
  --query "[?roleDefinitionName=='Foundry User'].{principal:principalName,type:principalType}" -o table
```

---

## Participants finding the project

A participant signs in at **https://ai.azure.com**, picks the tenant, and opens the
**`research-workshop`** project. Account-scope **Foundry User** lets them see the project, view the
deployed models, and create/run agents.

> **Symptoms of the wrong scope:** if a participant is *in* the project but the **Deployed models**
> list is empty and agent creation is blocked (portal asks for *Foundry Owner*), their role is at
> **project** scope only — re-assign at **account** scope (see the ⚠️ note above). Allow a few
> minutes for RBAC to propagate, then have them refresh / sign out and back in.

The Build-rail endpoint + `.env` handoff is covered in
[01-provision-foundry.md §6](./01-provision-foundry.md#6-hand-the-endpoint-to-build-rail-participants).

---

## Troubleshooting — participant can't see deployed models / can't create agents

**Symptom:** a participant is signed in and *inside* the `research-workshop` project, but the
**Deployments → Deployed models** list is **empty** and they **can't create an agent** — the portal
shows *"You do not have permissions to deploy models… ask your administrator to assign you the
Foundry Owner role."*

**Cause:** their **Foundry User** role is assigned at **project** scope only. Model deployments are
**account-level** resources and Azure RBAC inherits **downward** (account → project) not upward, so a
project-scoped role can't read them — and agent creation needs to pick a deployment. (This is *not*
a request to make them Foundry Owner — that would let them deploy/manage models. Keep them Foundry
User, just at the right scope.)

**1. Diagnose** — list the participant's Foundry assignments across every scope:

```powershell
$sub  = "<your-subscription-id>"
$rg   = "rg-foundry-workshop"
$acct = "dso-foundry-ws-<unique>"
$acctScope = "/subscriptions/$sub/resourceGroups/$rg/providers/Microsoft.CognitiveServices/accounts/$acct"

$uid = az ad user show --id "<participant>@<tenant>.onmicrosoft.com" --query id -o tsv
az role assignment list --assignee $uid --all --include-inherited `
  --query "[?contains(roleDefinitionName,'Foundry')].{role:roleDefinitionName, scope:scope}" -o table
```

If the only scope shown ends in `…/projects/research-workshop` (and **not** the bare
`…/accounts/<acct>`), that's the problem.

**2. Fix** — add Foundry User at the **account** scope:

```powershell
az role assignment create `
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" `
  --assignee-object-id $uid --assignee-principal-type User `
  --scope $acctScope
```

> Doing the whole room? Assign it **once to the Entra group** at `$acctScope` (see §b) rather than
> per user.

**3. Verify + refresh** — re-run the diagnose command and confirm a row with the bare
`…/accounts/<acct>` scope now appears. RBAC changes take **a few minutes** to propagate; have the
participant **hard-refresh** the portal (or sign out and back in) before re-checking. The deployed
models should now be visible and agent creation unblocked.

---

✅ **Done.** Confirm the [pre-flight checklist](../facilitator/facilitator-guide.md) and you're ready
to run the workshop.
