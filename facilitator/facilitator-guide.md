# Facilitator Guide — Research Supercharged

Minute-by-minute script, demo cues, and contingencies. Pairs with
[workshop-plan.md](./workshop-plan.md) (the *why*) and the [labs](../labs/) (the *what*).

---

## Pre-flight checklist (day before)
> Provisioning + RBAC is a one-time admin job — follow the **[admin runbook](../admin/README.md)**
> (Basic Foundry account, model deployments, participant access). This checklist confirms it's done.
- [ ] Shared **Basic** Foundry project live (managed File Search — no Azure AI Search to wire up).
- [ ] All participants granted **Foundry User** at **account scope** (the project's *parent*
      resource — required to see model deployments + create agents; assign once to an Entra group
      for 20–30 people). See [admin/02-assign-participant-access.md](../admin/02-assign-participant-access.md).
- [ ] `model-router` deployed (Global Standard); quota sized for the whole room on one project.
      Teaching default for Labs 0–1 and all SDK rails (Lab 1 Web Search works on it).
- [ ] **`gpt-5.4` deployed** (Global Standard) — **required for Lab 2's portal File Search tool**,
      which does *not* accept `model-router`. Participants switch to it from Lab 2 on. Size its
      quota for the room too.
- [ ] Persona text handy to paste (it's in Lab 0 step 4) — the portal has **no agent-clone**
      feature, so participants create a **New agent** and paste the persona.
- [ ] **Dry-run all 4 lab scripts** end-to-end in the real tenant: `lab01`–`lab04`.
- [ ] Confirm the **portal labels** for Web Search, Knowledge/Files, Code Interpreter, MCP — these
      can drift; note the exact wording you'll say out loud.
- [ ] *(Optional)* **open-access corpus pack** zipped for Lab 2; **research MCP server** URL ready
      for Lab 4 (test it). If not, plan to demo Lab 4 and have everyone do the Build rail.
- [ ] Print/share the **data-posture rule** where everyone can see it.

## Room setup
- Two rails on the slides: 🟢 **Explore** (portal) and 🔵 **Build** (SDK). Ask for a show of hands
  at the start so floaters know who's where.
- Have **1 floater per ~10 participants**; floaters watch the shared agent list for naming chaos.

---

## Minute-by-minute

### 0:00 – 0:20 · Lab 0 — Hello, Research Copilot
- **Open (2 min):** the hook — "by 12, your agent will search the literature, read your papers,
  crunch data, and call tools. Let's start with the agent itself."
- **State the data rule (1 min)** — say it once, clearly. It recurs all day.
- **Do (12 min):** everyone creates `rc-<initials>`, pastes the persona, chats. Demo the
  **sensitive-ask refusal** live — it lands the Responsible-AI point early.
- **Cue:** make sure *everyone* has a replying agent before moving on — this is the one lab that
  gates the rest.

### 0:20 – 0:55 · Lab 1 — Search the Literature
- **Demo (3 min):** ask a current question *without* web search, then *with* it. The citations are
  the "wow".
- **Do (25 min):** add Web Search — in the **Add the Web Search Tool** dialog pick **"Search the
  web with Bing Search" (No setup required)**, *not* the Bing Custom Search option — then ask a
  topic in their own field, inspect sources, A/B it.
- **Cue:** everyone stays on **`model-router`** — Web Search works on it, no model switch needed.
  *(If a rare query errors, switching that agent to `gpt-5.4` is a reliable fallback.)*
- **Talking point:** training-cutoff vs. live grounding; "trust but verify" via citations.

### 0:55 – 1:35 · Lab 2 — Ground on Your Papers
- **Cue first:** File Search is **not** supported on `model-router` in the portal — have everyone
  switch their `rc-<initials>` agent to **`gpt-5.4`** before adding files (and keep it there for
  Labs 3–4). Otherwise they hit *"File search tool doesn't work with the model you selected."*
- **Cue:** when the **Attach files** dialog appears, tell them to rename the **Vector index name**
  with their **initials** (e.g. `jd-papers`) — one shared project, so it keeps indexes findable.
- **Demo (3 min):** upload 2–3 open-access PDFs, ask for a cited summary, then ask something
  *not* in them to show the honest "not in the documents" refusal.
- **Do (32 min):** participants use the starter pack or their own **public** docs.
- **Watch for:** people wanting to upload real/sensitive papers — redirect to public ones.

### 1:35 – 1:45 · ☕ Break

### 1:45 – 2:25 · Lab 3 — Analyse the Data
- **Demo (3 min):** attach `sample_experiments.csv`, ask for stats + a chart; point out the
  agent *writes and runs code* (numbers are computed, not guessed).
- **Do (30 min):** the **`S012` outlier** (trial 12) is the planted "aha" — make sure people find it.
- **Talking point:** why code interpreter beats asking a model to do arithmetic.

### 2:25 – 2:50 · Lab 4 — Add a Tool
- **Demo (3 min):** if the **MCP server** is up, add it by URL, ask the conversion question,
  **approve** the call. If not, demo the Build-rail `convert_units` tool instead.
- **Do (20 min):** Explore rail adds the MCP tool; Build rail writes the function tool and sees
  the assert pass. *(This is the flex lab — see contingencies.)*
- **Talking point:** tools turn a chatbot into an agent; approval keeps a human in the loop.

### 2:50 – 3:00 · Lab 5 — Take It Home
- Recap the four superpowers; hit **Responsible AI** (cite-or-decline, data posture, verify).
- Each person picks **one** way to apply it (the prompt in Lab 5).
- **Remind everyone to delete their `rc-<initials>` agents** to keep the shared project clean.

---

## Contingencies
- **Behind schedule?** Shorten Lab 2's "do" by 5 min, and/or compress **Lab 4** to a demo-only
  (everyone watches, no individual build). Never cut Lab 5's RAI wrap.
- **Web Search toggle missing/renamed?** Use the label you confirmed in the dry-run; if a region
  lacks it, fall back to the **Build rail** (`WebSearchTool()` is verified) on the projector.
- **MCP server down?** Demo Lab 4, then have the room do the local function tool — same lesson, no
  external dependency.
- **Quota / 429s on one shared project?** Stagger heavy labs (RAG indexing, code interpreter) by
  half the room; `model-router` helps spread load.
- **Someone pastes sensitive data?** Stop, reset the chat, restate the rule. No drama, just redirect.

## Common pitfalls (Build rail)
- Not running from `assets/` → `ModuleNotFoundError: common`.
- `.env` not filled / no `az login` → endpoint or auth error.
- `pip` wheel build failures → `pip install --upgrade pip setuptools wheel` then
  `pip install --prefer-binary -r requirements.txt`.
- Empty `assets/corpus/` → Lab 2 raises "No files to index"; add public docs first.
