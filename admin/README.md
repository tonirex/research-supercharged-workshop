# Admin & pre-workshop setup — Research Supercharged

The **one-time** jobs an admin does **before** the workshop: stand up the shared Foundry project
and grant participants access. Running the session itself is covered separately in
**[../facilitator/](../facilitator/)**.

> **Workshop model:** shared **_Basic_** Foundry project(s) for the whole room (~20–30 people);
> everyone builds agents named `rc-<initials>` in a shared project. The DSO workshop provisions **two**
> identical projects in **two regions** (`swedencentral` + `eastus2`) and splits the roster to
> load-balance quota + rate limits — see
> [01-provision-foundry.md → What you'll build](./01-provision-foundry.md#what-youll-build). (A dry run
> or small group can use **one** region.) Trade-offs (quota, naming, blast radius) are discussed in
> [../facilitator/workshop-plan.md](../facilitator/workshop-plan.md).

## Do it in order

| Step | Doc | Outcome |
|------|-----|---------|
| 1 | **[01-provision-foundry.md](./01-provision-foundry.md)** | **Two regions** (`swedencentral` + `eastus2`), each: resource group → **Basic** Foundry account → project → `model-router` + `gpt-4.1` deployments (gpt-4.1 required for portal File Search) → SDK endpoint. Then split the roster evenly |
| 2 | **[02-assign-participant-access.md](./02-assign-participant-access.md)** | **Foundry User** RBAC for participants (per-user or Entra group), project managed identity, and verification |
| 3 *(optional)* | **[03-deploy-mcp-server.md](./03-deploy-mcp-server.md)** | Deploy the **Lab 4 MCP server** to Azure Container Apps → public `…/mcp` URL to hand the facilitator |

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
  [01-provision-foundry.md → Step 2](./01-provision-foundry.md#step-2--foundry-account-basic).)
- An admin identity with a role that can **create resources and assign roles** — i.e. **Owner**
  (or **Contributor** + **User Access Administrator**) on the subscription or target resource group.
  In Foundry terms, **Foundry Account Owner** can create the account/project and assign Foundry User.
- A list of participant emails (Entra users in your tenant). For 20–30 people, prefer an **Entra
  security group** so you assign the role **once**.

Set the shared variable both runbook docs use (PowerShell) — keep this shell open across steps 1 and 2:

```powershell
$sub = "<your-subscription-id>"
az account set --subscription $sub
# Per-region $rg / $acct / $proj are set inside 01-provision-foundry.md — you provision TWO regions
# (swedencentral + eastus2). Doc 02 reuses $rg / $acct, so run it once per region's account.
```

> **Regions:** the DSO workshop uses **two** regions — `swedencentral` **and** `eastus2` — to
> load-balance the roster (see
> [01-provision-foundry.md → What you'll build](./01-provision-foundry.md#what-youll-build)). Both are
> validated **feature-identical** (Web Search, File Search, Code Interpreter, Function, MCP; both models
> available) and were stood up + smoke-tested end-to-end. Quota is **per-region** — check
> `az cognitiveservices usage list --location <region>` and request increases where needed. (A quick dry
> run can use just one region.)

---

## Validation — this setup was run end-to-end ✅

Provisioned with these steps (account `dso-foundry-ws-d457yk`, project `research-workshop`,
**swedencentral**, Basic; the original single-region validation used RG `rg-foundry-workshop`) and
every executable lab passed live:

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

> **Two-region parity — validated end-to-end.** Both regions were provisioned with these steps and
> exercised live. **swedencentral** ran all five labs (table above). **eastus2** was then stood up via
> the [two-region flow](./01-provision-foundry.md#what-youll-build): Basic
> `AIServices` account (`allowProjectManagement=true`), project `research-workshop`, and **both**
> deployments `model-router 2025-11-18` + `gpt-4.1 2025-04-14` (GlobalStandard, cap 100, all
> `Succeeded`). A representative participant (`janedoe`) was granted **Foundry User at account
> scope**, and a **live two-model agent smoke test passed** against the eastus2 endpoint
> (`model-router` applied the persona + citations; `gpt-4.1` answered). The project was left pristine
> (0 agents, 0 vector stores). eastus2 is confirmed feature-identical to swedencentral for every lab.

> **Lab 4 MCP server (step 3, optional):** the server code + MCP Streamable-HTTP transport were
> validated locally (`convert_units` returns `1.8 eV → 2.884e-19 J`; tools advertise over `/mcp`).
> The Azure Container Apps **deploy script** is provided ready-to-run — do a dry-run deploy before
> the workshop and confirm the portal agent can reach `…/mcp` (see
> [03-deploy-mcp-server.md](./03-deploy-mcp-server.md)).

---

## Teardown (after the workshop)

```powershell
# Deletes the accounts, projects, deployments, and all agents/vector stores in one shot.
# The DSO workshop uses two regional resource groups — delete both:
az group delete --name rg-foundry-workshop-swe  --yes --no-wait
az group delete --name rg-foundry-workshop-eus2 --yes --no-wait
```

Remind participants to delete their `rc-<initials>` agents at the end of Lab 5; a full
`az group delete` is the clean way to remove everything when the workshop is over.
