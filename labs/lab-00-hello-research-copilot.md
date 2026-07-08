---
lab: 0
title: "Hello, Research Copilot"
duration: "20 min (≈ 0:00–0:20)"
foundry_feature: "Agents — create & chat"
rails: ["🟢 Explore (portal)", "🔵 Build (SDK) — optional"]
---

# Lab 0 — Hello, Research Copilot 👋

**Goal:** everyone in the room has a working agent they can chat with — before we add a
single tool. This is your *Research Copilot*; every later lab gives it a new superpower.

> ### ⚠️ One rule for the whole workshop: public / unclassified data only
> This is a hands-on session on shared cloud infrastructure. Do **not** type, upload, or
> ground on anything sensitive, classified, or personal — not in chats, files, or datasets.
> The Research Copilot persona is told to refuse such requests, but **you** are the real
> guardrail. When in doubt, use a public example.

> 📸 **Prefer a click-by-click walkthrough?** Follow the **[portal walkthrough](./lab-00-portal.md)** —
> the 🟢 portal-rail steps below, captured screen by screen.

---

## 🟢 Explore (portal) — everyone

1. Open the shared workshop project in the **Foundry portal** → **Agents** → **New agent**.
2. **Name it `rc-<your-initials>`** (e.g. `rc-ac`). We all share one project, so the initials
   keep the agent list legible and avoid collisions.
3. **Model:** choose **`model-router`** — it auto-picks a capable model so nobody stalls on
   model selection.

   > **⚠️ See *"We couldn't automatically deploy a model … no models have at least 50K tokens per
   > minute of available quota"*?** That's expected — you have *use* access, not *deploy* access, so
   > the portal can't auto-provision a model for you (and doesn't need to: `model-router` is already
   > deployed for the whole room). Just click **Create and open playground**, then set the agent's
   > **Deployment → `model-router`**. **Don't** click *Request more quota* or *Deploy a model
   > manually* — those need admin rights, and the quota is actually fine.
4. **Instructions:** paste the Research Copilot persona:

   ```text
   You are Research Copilot, an assistant that helps a researcher explore a topic faster:
   searching public sources, grounding answers in documents the user provides, analysing
   data, and summarising findings clearly.

   Rules:
   - Use ONLY public, unclassified information. Never request, store, or reason over
     sensitive, classified, or personal data. If asked to, decline and explain why.
   - Ground your claims. When you use a web result or a provided document, cite it. If you
     are unsure or have no source, say so plainly — never invent citations or numbers.
   - Be concise and structured: lead with the answer, then the supporting evidence.
   - You are a research aid, not an authority. Flag clearly when a human should verify.
   ```
5. Open the **playground / chat** and try:
   - *"In one sentence, what can you help me research?"*
   - *"Give me a 3-bullet primer on solid-state batteries."* (or your own topic)
   - A deliberately sensitive ask, e.g. *"Summarise this classified report…"* → watch it **decline**.

### ✅ Checkpoint
Your `rc-<initials>` agent replies in persona, stays concise, and **refuses** the sensitive
request. That's a working, governed agent. 🎉

---

## 🔵 Build (SDK) — optional, for the code-curious

One-time setup (in `assets/`):

```bash
az login                      # auth for DefaultAzureCredential
copy .env.example .env        # then fill FOUNDRY_PROJECT_ENDPOINT + INITIALS
pip install -r requirements.txt
```

Then create + chat with the *same kind* of agent from code:

```python
from common.research_common import research_agent, run_text, cleanup

agent = research_agent("hello")              # creates rc-<initials>-hello in the shared project
print(run_text(agent, "In one sentence, what can you help me research?"))
cleanup(agent)                               # tidy up the shared project when you're done
```

> The portal agent and the SDK agent are the **same object type** in Foundry — the portal is
> just a UI over the API you're calling here.

---

## 💡 Try it
Tweak the persona (e.g. *"always answer as a numbered checklist"*) and re-ask. Notice how
instructions alone change behaviour — no code, no retraining.

➡️ **Next:** [Lab 1 — Search the literature](./lab-01-search-the-literature.md)
