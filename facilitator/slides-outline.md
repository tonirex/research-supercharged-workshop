# Slides Outline — Research Supercharged

A deck skeleton for the 3-hour session. ~40 slides: section dividers + a few teach
slides per lab + a "hands-on hold" slide the room stares at while they work. Build the
real deck from this; keep text light and let the **portal + code** do the talking.

**Conventions**
- 🟢 = Explore (portal) · 🔵 = Build (SDK) — show both on every lab divider.
- *Cue:* = facilitator action (what to say/do/demo), not slide text.
- Time-boxes match [workshop-plan.md](./workshop-plan.md) §5 and the
  [facilitator-guide.md](./facilitator-guide.md).

---

## Part 0 · Open (0:00–0:20)

**Slide 1 — Title**
- *Research Supercharged: Azure AI for the Curious Mind*
- Subtitle: build a research agent that searches, reads, computes, and acts.
- Logos, facilitator name, date.
- *Cue:* energy hook — "in 3 hours your agent goes from blank to four superpowers."

**Slide 2 — The one rule: public data only**
- Unclassified / public information **only**, all day, both rails.
- Why: shared project, shared infra, mixed access.
- *Cue:* say it once, clearly. Point back here whenever someone reaches for real data.

**Slide 3 — What you'll build today**
- One agent → **Research Copilot** → gains a superpower per lab.
- Superpowers: 🔎 Search · 📚 Ground · 📊 Analyse · 🛠️ Act.
- *Cue:* this single agent is the spine of the whole day.

**Slide 4 — Two rails, nobody blocked**
- 🟢 **Explore** — portal, clicks, everyone.
- 🔵 **Build** — Python SDK, optional, deeper.
- Same Foundry agent underneath; switch rails anytime.
- *Cue:* show of hands — who's 🟢, who's 🔵. Floaters note it.

**Slide 5 — Agenda**
- 0 Hello · 1 Search · 2 Ground · ☕ · 3 Analyse · 4 Act · 5 Take it home.
- Mark the ☕ break and the 12:00 finish.

**Slide 6 — Platform in one line**
- Microsoft Foundry · current agents API (`azure-ai-projects` 2.x) · `model-router`.
- *Cue:* not the classic portal — everything here is the current experience.

---

## Lab 0 · Hello, Research Copilot (0:00–0:20)

**Slide 7 — Section divider: Lab 0 — Hello** (🟢🔵)
- Outcome: everyone has a governed `rc-<initials>` agent that replies.

**Slide 8 — What is an agent here?**
- Model + instructions (persona) + (soon) tools, as one governed object.
- Naming: `rc-<initials>` on the shared project.

**Slide 9 — The persona: cite-or-decline**
- Research Copilot grounds answers and refuses sensitive asks.
- *Cue:* live-demo the **refusal** — lands Responsible AI on slide 1 of the work.

**Slide 10 — 🛠️ Hands-on: create your agent** (hold slide)
- 🟢 New agent → paste persona → chat.
- 🔵 `research_agent()` → `run_text(...)`.
- ✅ Checkpoint: your agent replies *and* declines a sensitive ask.
- *Cue:* gate here — everyone needs a working agent before Lab 1.

---

## Lab 1 · Search the Literature (0:20–0:55)

**Slide 11 — Section divider: Lab 1 — Search** (🟢🔵)
- Superpower 🔎: answers grounded in the **live web**, with citations.

**Slide 12 — Why search? Training cutoff vs. now**
- Models don't know yesterday; web search closes the gap.
- *Cue:* ask a current question **without** search → wrong/old → then **with**.

**Slide 13 — Web Search in Foundry**
- 🟢 Tools → Web Search → *Search the web with Bing Search* (no setup required).
- 🔵 `WebSearchTool()` — **no Bing connection needed**.
- Citations come back in the response.

**Slide 14 — 🛠️ Hands-on: ask your field** (hold slide)
- Add Web Search → ask a question in your own domain → inspect sources → A/B it.
- ✅ Checkpoint: a cited answer you can trace.
- *Cue:* "trust but verify" — open a citation.

---

## Lab 2 · Ground on Your Papers (0:55–1:35)

**Slide 15 — Section divider: Lab 2 — Ground / RAG** (🟢🔵)
- Superpower 📚: answers grounded in **your own documents**.

**Slide 16 — RAG in one picture**
- Files → vector store → agent retrieves → cites the source passage.
- *Cue:* one diagram; don't over-explain embeddings.

**Slide 17 — Knowledge in Foundry**
- 🟢 Knowledge → upload files (creates a vector store).
- 🔵 `build_vector_store()` + `file_search_tool()`.

**Slide 18 — Honesty: "not in your documents"**
- *Cue:* ask something **not** in the docs → show the honest decline, not a guess.

**Slide 19 — 🛠️ Hands-on: bring public papers** (hold slide)
- Use the starter pack **or** your own **public** PDFs → cited summary → a specific Q.
- ✅ Checkpoint: an answer cites a passage from *your* file.
- *Cue:* watch for sensitive uploads — redirect to public.

---

**Slide 20 — ☕ Break (10 min)**
- Big timer. "Back at HH:MM."

---

## Lab 3 · Analyse the Data (1:45–2:25)

**Slide 21 — Section divider: Lab 3 — Analyse** (🟢🔵)
- Superpower 📊: the agent **writes and runs code** on data.

**Slide 22 — Why code interpreter?**
- Models guess arithmetic; code interpreter **computes** it (and charts it).
- *Cue:* contrast "ask a model to average 20 rows" vs. running pandas.

**Slide 23 — Code Interpreter in Foundry**
- 🟢 Tools → Code Interpreter, attach the CSV.
- 🔵 `CodeInterpreterTool()`; CSV embedded in the prompt for portability.

**Slide 24 — 🛠️ Hands-on: find the outlier** (hold slide)
- Ask for stats + a chart on `sample_experiments.csv`.
- ✅ Checkpoint: you find the **S012 / trial-12** anomaly.
- *Cue:* make sure everyone lands the outlier — it's the planted "aha".

---

## Lab 4 · Add a Tool (2:25–2:50)

**Slide 25 — Section divider: Lab 4 — Act** (🟢🔵)
- Superpower 🛠️: the agent **calls a tool**, with a human approving.

**Slide 26 — Tools turn a chatbot into an agent**
- Function calling / MCP = reach beyond text.
- Human-in-the-loop **approval** keeps control.

**Slide 27 — Two ways to add a tool**
- 🟢 Tools → MCP (add a server by URL) → **approve** the call.
- 🔵 `function_tool()` → local `convert_units` → assert it fired.
- *Cue:* if no MCP server, demo once; everyone does the Build-rail function.

**Slide 28 — 🛠️ Hands-on: a tool call** (hold slide)
- Ask the conversion question → watch the tool fire → approve.
- ✅ Checkpoint: response uses the tool's result, not a guess.
- *(Flex lab — see facilitator contingencies if running late.)*

---

## Lab 5 · Take It Home (2:50–3:00)

**Slide 29 — Section divider: Lab 5 — Take it home**

**Slide 30 — Your four superpowers**
- 🔎 Search · 📚 Ground · 📊 Analyse · 🛠️ Act — recap with the agent you built.

**Slide 31 — Responsible AI for a research aid**
- Cite-or-decline · public-data posture · verify before you trust.
- Next step before real use: **evaluation + observability**.

**Slide 32 — Pick one thing to apply**
- *Cue:* each person names one way to use this in their work (Lab 5 prompt).

**Slide 33 — Clean up & resources**
- Delete your `rc-<initials>` agent.
- Links: this repo, `Foundry-Agent-Lab`, `azure-ai-projects` samples, hosted-agents docs.

**Slide 34 — Thank you / Q&A**

---

## Backup slides (appendix — show only if asked)
- **B1 — Architecture:** portal agent == SDK agent (same object).
- **B2 — The Build rail setup:** `pip install`, `.env`, `az login`, run from `assets/`.
- **B3 — Helper API:** the `research_common.py` public surface (one-liners).
- **B4 — Troubleshooting:** `ModuleNotFoundError: common`, empty corpus, wheel builds, 429s.
- **B5 — Beyond today:** multi-agent, evaluation/red-team, deploy as a hosted agent.
