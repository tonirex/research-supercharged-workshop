---
lab: 5
title: "Take It Home"
duration: "10 min (≈ 2:50–3:00)"
foundry_feature: "Wrap-up, Responsible AI, next steps"
rails: ["🟢 Everyone"]
---

# Lab 5 — Take It Home 🎒

You started with a plain chat agent and gave it four research superpowers:

| Lab | Superpower | Foundry feature |
|-----|------------|-----------------|
| 1 | **Search** the live literature, with citations | Web Search |
| 2 | **Ground** answers in your own documents | File Search / RAG |
| 3 | **Compute** real stats & charts on data | Code Interpreter |
| 4 | **Act** by calling tools / services | Function calling · MCP |

Together that's an **agentic research assistant**: it can find, read, calculate, and do — and
tell you where every answer came from.

> 📸 **Prefer a click-by-click walkthrough?** Follow the **[portal walkthrough](./lab-05-portal.md)** —
> the recap and the agent-cleanup steps, captured screen by screen.

---

## 🧭 Responsible AI for research (the part that matters most)
- **Cite or decline.** A research aid that invents sources is worse than none. Our persona is
  told to ground claims and admit uncertainty — keep that bar.
- **Unclassified by default.** Everything today was public/synthetic on purpose. For real work,
  match the data's classification to an approved environment before you connect it.
- **Human-in-the-loop.** Tools that *act* used approval. Keep a person on consequential steps.
- **Verify, then trust.** Treat outputs as a fast first draft a domain expert checks — not a
  verdict.

## 🚀 Where to go next
- **Evaluate & observe:** measure quality before anything leaves a demo. Try the **bonus labs** →
  [Evaluate in the portal](./bonus/bonus-01-evaluate-in-portal.md) and
  [Cloud evaluation with the SDK](./bonus/bonus-02-cloud-evaluation-sdk.md) — run **evaluators**
  (relevance, coherence, groundedness, safety) over a dataset or your own agent. Pair with
  **tracing** (OpenTelemetry → Azure Monitor) for production.
- **Orchestrate:** chain several agents/tools with **Workflow agents** or the **Microsoft Agent
  Framework** for multi-step research pipelines.
- **Deploy:** publish your agent as a **hosted agent** so a teammate (or app) can call it.
- **Keep building:** the current SDK samples live in
  `Azure/azure-sdk-for-python → sdk/ai/azure-ai-projects/samples/agents/`.
- **Learn at your own pace:** keep exploring with interactive, self-directed modules on
  **Microsoft Learn** → [aka.ms/AI-103onLearn](https://aka.ms/AI-103onLearn).

## ✍️ Apply it to your work (pick one, 2 min)
- *Which of the four superpowers would save you the most time this month?*
- *What public corpus would you point Lab 2 at?*
- *What's one tool (an internal API, a calculation) you'd want in Lab 4?*

---

## 🧹 Before you leave
Please **delete the agents you created** in the shared project (`rc-<your-initials>*`) to keep
it tidy for the next group. From the portal: Agents → select yours → delete. From code:
`cleanup(agent)` (the lab scripts already do this).

**Thank you — go supercharge your research!** 🔬✨

---

⬅️ **Previous:** [Lab 4 — Add a tool](./lab-04-add-a-tool.md) · ➡️ **Next:** [Bonus labs — Evaluate & observe](./bonus/README.md) · ↩️ Back to [the workshop overview](../README.md)
