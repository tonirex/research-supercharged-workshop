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

---

## Prerequisites

- **Azure CLI ≥ 2.80.0** signed in: `az login`. 2.80.0 is the floor for the CLI provisioning commands
  (`az cognitiveservices account project` create); the runbook **enforces** it with a version gate — see
  [01-provision-foundry.md → Before you start](./01-provision-foundry.md#before-you-start). (An
  [ARM REST fallback](./01-provision-foundry.md#arm-rest-fallback-any-cli-version) works on any CLI
  version.)
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
> run can use just one region). The original validation used `gpt-4.1`; now use `gpt-5.4` and confirm
> its region availability/quota before deployment.

---

## Do it in order

| Step | Doc | Outcome |
|------|-----|---------|
| 1 | **[01-provision-foundry.md](./01-provision-foundry.md)** | **Two regions** (`swedencentral` + `eastus2`), each: resource group → **Basic** Foundry account → project → `model-router` + `gpt-5.4` deployments (gpt-5.4 required for portal File Search) → SDK endpoint. Then split the roster evenly |
| 2 | **[02-assign-participant-access.md](./02-assign-participant-access.md)** | **Foundry User** RBAC for participants (per-user or Entra group), project managed identity, and verification |
| 3 *(optional)* | **[03-deploy-mcp-server.md](./03-deploy-mcp-server.md)** | Deploy the **Lab 4 MCP server** to Azure Container Apps → public `…/mcp` URL to hand the facilitator |

When both are done, hand the project link + endpoint to participants and confirm the
**pre-flight checklist** in [../facilitator/facilitator-guide.md](../facilitator/facilitator-guide.md).

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
