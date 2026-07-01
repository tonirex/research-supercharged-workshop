# Research Supercharged — Workshop Plan (design rationale)

> Facilitator-facing design doc. Participants use the [README](../README.md) and
> [labs](../labs/); this explains *why* the workshop is shaped the way it is.

## 1. Overview
- **Title:** *Research Supercharged: Azure AI for the Curious Mind*
- **Audience:** DSO researchers, scientists & engineers — technically capable but mixed in
  cloud/AI experience; "curious minds" who want a fast, credible on-ramp.
- **Format:** ~3 hours, hands-on, single shared Foundry project.
- **Platform:** Microsoft Foundry, **current** agents API (`azure-ai-projects` 2.x).
- **Anchor:** one agent, **Research Copilot**, gains a superpower per lab (search → ground →
  compute → act). Domain-agnostic so each participant applies it to their own field.

## 2. Learning goals
By the end, a participant can:
1. Create and govern an agent in the portal (and, optionally, from code).
2. Ground answers in the **live web** and in **their own documents**, with citations.
3. Use a **code interpreter** to compute real results on data.
4. Extend an agent with **tools** (function calling / MCP) and human-in-the-loop approval.
5. Articulate the **Responsible-AI** basics for a research aid (cite-or-decline, data posture,
   verification).

## 3. Design principles
- **Hands-on first.** Every lab has the participant *doing*, not watching. Demos are ≤ 3 min.
- **Two rails, no one blocked.** 🟢 **Explore** (portal, everyone) + 🔵 **Build** (SDK, optional).
  A non-coder completes 100% on 🟢; an engineer goes deeper on 🔵. Switch freely.
- **Public data only.** Reinforced in the README, every relevant lab, and the persona itself —
  essential for a defence-science audience on shared infra.
- **Portal-led, code-backed.** The portal agent and the SDK agent are the *same* Foundry object,
  so the rails never diverge conceptually.
- **One shared project.** Simplest to run for a mixed room; naming convention `rc-<initials>`
  keeps it legible. A read-only `rc-reference` agent lets people clone a head-start.

## 4. The "Research Copilot" scenario
Deliberately **domain-agnostic**: a research assistant that finds, reads, calculates, and acts.
- Works for any DSO discipline — bring-your-own-topic for web search and bring-your-own-corpus
  for RAG.
- Ships with **synthetic** data (`assets/data/sample_experiments.csv`) and **public** default
  prompts so it runs even if a participant brings nothing.
- Avoids any sensitive/operational framing by construction.

## 5. Run-of-show

| Time | Lab | Foundry feature | Outcome |
|------|-----|-----------------|---------|
| 0:00–0:20 | 0 · Hello | Agents | Everyone has a governed `rc-<initials>` agent |
| 0:20–0:55 | 1 · Search | Web Search | Cited answer from the live web |
| 0:55–1:35 | 2 · Ground | File Search / RAG | Cited answer from own documents |
| 1:35–1:45 | ☕ Break | — | — |
| 1:45–2:25 | 3 · Analyse | Code Interpreter | Real stats + chart + outlier found |
| 2:25–2:50 | 4 · Act | Function calling / MCP | Agent calls a tool, with approval |
| 2:50–3:00 | 5 · Take it home | RAI + next steps | A plan to apply it |

**Timing discipline:** Labs 1–4 are time-boxed. If a lab over-runs, extend **+5 min once**, else
move on — the next lab doesn't depend on a *finished* previous one (only on having an agent).
**Lab 4 is the designed drop point** if the day runs late (see facilitator guide).

## 6. Foundry feature mapping (current API)

| Lab | Portal (🟢) | SDK (🔵) — `azure-ai-projects` 2.x |
|-----|------------|-----------------------------------|
| 0 | New agent + instructions | `create_version` + `PromptAgentDefinition` |
| 1 | Tools → Web Search | `WebSearchTool()` (hosted, no connection) |
| 2 | Knowledge → files (vector store) | `openai.vector_stores.*` + `FileSearchTool` |
| 3 | Tools → Code Interpreter | `CodeInterpreterTool()` |
| 4 | Tools → MCP | `FunctionTool(...)` / `MCPTool(...)` |

> Pattern source: official samples in
> `Azure/azure-sdk-for-python → sdk/ai/azure-ai-projects/samples/agents/`.

## 7. Provisioning & prerequisites
**Operator (day before):**
- Shared Foundry project on the **current** experience, all participants added (Entra guests or a
  shared login).
- Model deployments: **`model-router`** (teaching default) **and `gpt-4.1`** (required for Lab 1
  Web Search — `model-router` doesn't support that tool), both Global Standard; quota sized for
  the room sharing one project.
- A read-only **`rc-reference`** agent to clone.
- *(Optional)* a small **open-access corpus pack** for Lab 2 and a **research MCP server** for
  Lab 4 (with fallback to facilitator demo).
- Dry-run all four lab scripts end-to-end in the real tenant.

**Per participant:**
- 🟢 Explore: a browser + project access. Nothing to install.
- 🔵 Build: Python 3.10+, `az login`, repo cloned, `.env` filled.

## 8. Responsible AI & data posture
- **Public/unclassified only**, everywhere — the non-negotiable for this audience.
- Persona enforces **cite-or-decline** and refuses sensitive asks (demonstrated in Lab 0).
- Lab 4 uses **human-in-the-loop approval** for actions.
- Lab 5 frames **evaluation + observability** as the required next step before real use.

## 9. Risks & fallbacks
| Risk | Fallback |
|------|----------|
| Web Search availability/label differs in the portal | Facilitator confirms the exact toggle in the dry-run; SDK path is verified |
| No MCP server deployed for Lab 4 | Facilitator demos once; everyone does the Build-rail function tool (no server needed) |
| Running late | Drop **Lab 4** to the stretch slot; Lab 5 wrap is fixed |
| Mixed Azure access at 9am | Default everyone to 🟢 Explore on the shared project |
| Model/feature name drift | Default to `model-router`; re-confirm portal labels in the dry-run |

## 10. Reference workshops
- **Backbone:** [`microsoft-foundry/Foundry-Agent-Lab`](https://github.com/microsoft-foundry/Foundry-Agent-Lab)
  — modular hello → websearch → rag → code → mcp demos; the structural inspiration here.
- **Runnable patterns:** `azure-ai-projects` 2.x samples (the source of truth for the Build rail).
- **Deeper/optional self-study:** [`dhangerkapil/agentic-ai-immersion`](https://github.com/dhangerkapil/agentic-ai-immersion)
  (evaluation, red-team, multi-agent) and the VS Code *hosted-agents* docs for deployment.
