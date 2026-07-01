# Admin & pre-workshop setup — Research Supercharged

The **one-time** jobs an admin does **before** the workshop: stand up the shared Foundry project
and grant participants access. Running the session itself is covered separately in
**[../facilitator/](../facilitator/)**.

> **Workshop model:** a **single shared, _Basic_ Foundry project** for the whole room (~20–30
> people). Everyone builds agents named `rc-<initials>` in the *same* project. It's the simplest
> thing to run on one subscription; the trade-offs (quota, naming, blast radius) are discussed in
> [../facilitator/workshop-plan.md](../facilitator/workshop-plan.md).

## Do it in order

| Step | Doc | Outcome |
|------|-----|---------|
| 1 | **[01-provision-foundry.md](./01-provision-foundry.md)** | Resource group → **Basic** Foundry account → project → `model-router` deployment (+ optional `gpt-4.1` fallback) → SDK endpoint |
| 2 | **[02-assign-participant-access.md](./02-assign-participant-access.md)** | **Foundry User** RBAC for participants (per-user or Entra group), project managed identity, and verification |

When both are done, hand the project link + endpoint to participants and confirm the
**pre-flight checklist** in [../facilitator/facilitator-guide.md](../facilitator/facilitator-guide.md).

---

## What "Basic" means here (and why we use it)

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

## Prerequisites

- **Azure CLI** signed in: `az login`. (Validated with CLI `2.73.0`; see the version note in
  [01-provision-foundry.md §Foundry account](./01-provision-foundry.md#3-foundry-account--basic-project-enabled-no-byo-searchstorage).)
- An admin identity with a role that can **create resources and assign roles** — i.e. **Owner**
  (or **Contributor** + **User Access Administrator**) on the subscription or target resource group.
  In Foundry terms, **Foundry Account Owner** can create the account/project and assign Foundry User.
- A list of participant emails (Entra users in your tenant). For 20–30 people, prefer an **Entra
  security group** so you assign the role **once**.

Set the variables both runbook docs use (PowerShell) — keep this shell open across steps 1 and 2:

```powershell
$sub  = "<your-subscription-id>"
$rg   = "rg-foundry-workshop"
$loc  = "swedencentral"             # proven model-router + gpt-4.1 capacity
$acct = "dso-foundry-ws-<unique>"   # custom domain must be GLOBALLY unique, DNS-safe (lowercase)
$proj = "research-workshop"
az account set --subscription $sub
```

> **Region:** `swedencentral` was validated for this workshop (good `model-router` + `gpt-4.1`
> quota). `eastus2` also works but had far lower `model-router` quota in our subscription. Pick one
> region and keep the account, project, and deployments together.

---

## Validation — this setup was run end-to-end ✅

Provisioned with these steps (RG `rg-foundry-workshop`, account `dso-foundry-ws-d457yk`, project
`research-workshop`, **swedencentral**, Basic) and every executable lab passed live:

| Lab | Feature | Result |
|-----|---------|--------|
| 0 | Persona + governance | ✅ in-persona; **declined** a classified-data request |
| 1 | Web Search (`model-router`) | ✅ grounded answer + deduped citations |
| 2 | File Search (**Basic** managed vector store) | ✅ built `vs_…`, cited source files, **no Azure AI Search** |
| 3 | Code Interpreter | ✅ computed stats, flagged the `S012` outlier |
| 4 | Function tool | ✅ agent called `convert_units` |

`Foundry User` was assigned to the representative participant `janedoe` at **account scope** (the
project's parent resource — required so participants can see model deployments and create agents)
and verified. The project was swept clean afterward (0 agents, 0 vector stores).

---

## Teardown (after the workshop)

```powershell
# Deletes the account, project, deployments, and all agents/vector stores in one shot:
az group delete --name $rg --yes --no-wait
```

Remind participants to delete their `rc-<initials>` agents at the end of Lab 5; a full
`az group delete` is the clean way to remove everything when the workshop is over.
