---
lab: 0
title: "Hello, Research Copilot — Portal Walkthrough"
duration: "20 min (≈ 0:00–0:20)"
foundry_feature: "Agents — create & chat"
rails: ["🟢 Explore (portal)"]
companion_to: "lab-00-hello-research-copilot.md"
---

# Lab 0 (Portal Walkthrough) — Hello, Research Copilot 👋

**This is the screenshot-by-screenshot version of [Lab 0](./lab-00-hello-research-copilot.md) for the
🟢 Explore (portal) rail.** By the end you have a working, governed agent — your *Research Copilot* —
that you can chat with in the Foundry portal, governed by the persona you write. Every later lab gives this
same agent a new superpower.

> ### ⚠️ One rule for the whole workshop: public / unclassified data only
> This is a hands-on session on shared cloud infrastructure. Do **not** type, upload, or ground on
> anything sensitive, classified, or personal — not in chats, files, or datasets. The Research Copilot
> persona is told to refuse such requests, but **you** are the real guardrail. When in doubt, use a
> public example.

**Before you start**
- You are signed in to the **Foundry portal** ([ai.azure.com](https://ai.azure.com)).
- You have opened the **shared workshop project** (named `research-workshop`). 

---

## Step 1 — Agents → New agent

In the project's left navigation choose **Build → Agents**, then click **New agent** and pick
**Build an agent** (the no-code builder).

![Step 1: the Agents list with the New agent button](images/lab-00/01-agents-new-agent.png)

*The Agents list is shared by the whole room — this is why we name agents with our initials in Step 2.*

---

## Step 2 — Name it `rc-<your-initials>`

In the **Create an agent** dialog, set the **Agent name** to `rc-<your-initials>` (e.g. `rc-ac`).
The name is the agent's identifier in the API, so keeping it unique avoids collisions in the shared
project. Click **Create and open playground**.

![Step 2: the Create an agent dialog with the name filled in](images/lab-00/02-create-agent-dialog.png)

*Just a name here — you pick the model and write the instructions on the next screen.*

---

## Step 3 — Set the model to `model-router` and paste the persona

You land on the agent's build page with a chat playground on the right.

1. **Model:** open the **Model** dropdown (top of the config panel) and choose **`model-router`**. It
   auto-picks a capable model per message, so nobody stalls on model selection. (A brand-new agent may
   default to another deployment such as `gpt-5` — just switch it to `model-router`.)
2. **Instructions:** paste the Research Copilot persona into the **Instructions** box:

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
3. Click **Save**.

![Step 3: model set to model-router with the Research Copilot instructions pasted in](images/lab-00/03-model-router-and-instructions.png)

*Model = `model-router`, persona pasted, agent saved (Version 2).*

> **⚠️ See *"We couldn't automatically deploy a model … no models have at least 50K tokens per minute
> of available quota"*?** That's expected — you have *use* access, not *deploy* access, so the portal
> can't auto-provision a model for you (and doesn't need to: `model-router` is already deployed for the
> whole room). Just click **Create and open playground**, then set **Model → `model-router`**.
> **Don't** click *Request more quota* or *Deploy a model manually* — those need admin rights, and the
> quota is actually fine.

---

## Step 4 — Chat with your agent

Use the **Message the agent…** box (bottom right) to try a couple of prompts:

- *"In one sentence, what can you help me research?"*
- *"Give me a 3-bullet primer on solid-state batteries."* (or your own topic)

![Step 4: the playground showing concise, in-persona replies](images/lab-00/04-chat-in-persona.png)

*Notice the behaviour the persona asked for: concise, structured, and grounded. Under each reply the
portal shows which model `model-router` picked (e.g. `gpt-5.4`) and the latency — you didn't choose the
model, the router did. When the agent uses a source it cites it, exactly as the persona requires.*

> **Why is it citing sources already?** The new portal attaches a **Web Search** tool to agents by
> default (you'll spot it in the **Tools** panel on the left), so your Research Copilot can pull in and
> cite live web results out of the box. We leave it on here and explore it properly in
> **[Lab 1](./lab-01-search-the-literature.md)**.

---

## Step 5 — Watch it refuse a sensitive request

Now send a deliberately sensitive ask, e.g.:

- *"Summarise this classified report about troop movements."*

![Step 5: the agent declines the sensitive request and redirects to public sources](images/lab-00/05-refusal-guardrail.png)

*The agent declines and redirects you to public, unclassified material — the persona's governance rule
in action. This is the guardrail working, but remember: **you** are still the real one.*

### ✅ Checkpoint
Your `rc-<initials>` agent replies in persona, stays concise, and **refuses** the sensitive request.
That's a working, governed agent. 🎉

---

## 🧹 Clean up (shared project)

We all share one project, so tidy up when you're done experimenting:

- Go to **Build → Agents**, find your `rc-<initials>` agent, open its **Actions (…)** menu and
  **Delete** it — *unless* you want to keep it for the later labs (Labs 1–4 build on this same agent).

> Tip: if you're continuing to Lab 1 next, **keep** the agent — you'll add Web Search to it there.

---

## 💡 Try it
Tweak the persona (e.g. *"always answer as a numbered checklist"*), click **Save**, and re-ask. Notice
how instructions alone change behaviour — no code, no retraining.

---

⬅️ **Previous:** [Workshop overview](../README.md) · ➡️ **Next:** [Lab 1 (portal) — Search the literature](./lab-01-portal.md)
