---
lab: 1
title: "Search the Literature"
duration: "35 min (≈ 0:20–0:55)"
foundry_feature: "Web Search (hosted grounding — no connection needed)"
rails: ["🟢 Explore (portal)", "🔵 Build (SDK) — optional"]
---

# Lab 1 — Search the Literature 🔎

**Goal:** give Research Copilot a live window onto the public web so it answers with
**current, cited** information instead of stale model memory.

> **Why it matters for research:** a model's training data has a cutoff. Web Search lets the
> agent pull in this week's papers, news, and pages — and show you *where* each claim came
> from, so you can verify it.

> 📸 **Prefer a click-by-click walkthrough?** Follow the **[portal walkthrough](./lab-01-portal.md)** —
> the 🟢 portal-rail steps below, captured screen by screen.

---

## 🟢 Explore (portal) — everyone

> **Stay on `model-router`.** Web Search works on the teaching default — no model switch needed.
> *(If your agent ever errors on a web-search query, switching the model to **`gpt-5.4`** is a
> reliable fallback, but you shouldn't need it.)*

> **Heads-up — the new portal enables Web Search by default.** When you create an agent with
> **Build an agent**, the current Foundry UI already attaches the **Web Search** tool — you'll see
> it listed under **Tools** with a *Grounding with Bing* cost note. If it's already there you don't
> need to add it again: just confirm the search type below, then use the **A/B test in step 4** to
> feel the on-vs-off difference for yourself.

1. On your `rc-<initials>` agent, open **Tools** → **Add** → **Web Search** *(skip this if Web
   Search is already listed — see the note above)*. In the **Add the Web
   Search Tool** dialog, under **Search type** choose **"Search the web with Bing Search"
   (No setup required)** — **not** *"Search specific domains with Bing Custom Search"* (that option
   needs a Bing Custom Search connection you don't have). Click **Add**.
   *(Your facilitator will also point out the **search context size** option — how much of each
   page the agent reads.)*
2. Ask a current, public research question:
   > *"What are the most significant developments in solid-state battery research in the last
   > two years? Summarise the top 3 and cite a source for each."*

   *(Swap in **your own field** — that's the point.)*
3. **Inspect the citations.** Expand the sources / annotations and click through to at least
   one. Are they credible? Recent?
4. **A/B it — Web Search on vs off:** you've just seen the **on** case (grounded, cited answers).
   Now temporarily **remove** the Web Search tool and ask the *same* question. Notice the
   answer gets vaguer and loses citations. Re-add the tool. *This on/off contrast is the lesson —
   and it's exactly why the portal now enables Web Search by default.*

### ✅ Checkpoint
The grounded answer names **3 developments**, each with a **clickable, recent source**, and
visibly beats the no-tool version.

---

## 🔵 Build (SDK) — optional

Script for this lab: **[`assets/lab01_websearch.py`](../assets/lab01_websearch.py)** (SDK helpers in
**[`assets/common/research_common.py`](../assets/common/research_common.py)**). Run it from `assets/`:

```bash
python lab01_websearch.py
```

The core is three lines — `WebSearchTool` is **hosted**, so the service does the searching
server-side and you just read the result and its citations:

```python
from common.research_common import research_agent, web_search_tool, run_response, citations_of, cleanup, text_of, WEBSEARCH_MODEL

# Web Search runs on model-router (the default). WEBSEARCH_MODEL defaults to model-router;
# set FOUNDRY_WEBSEARCH_MODEL only to pin a fallback like gpt-5.4.
agent = research_agent("websearch", tools=[web_search_tool("high")], model=WEBSEARCH_MODEL)  # "low"|"medium"|"high"
resp = run_response(agent, text_of("search_recent"))
print(resp.output_text)
print(citations_of(resp))                                              # titles + URLs the agent used
cleanup(agent)
```

> No Bing connection or API key to provision — `WebSearchTool()` works out of the box on the
> current Foundry API, including on the default **`model-router`**. *(Need a specific model? Pin
> one via `FOUNDRY_WEBSEARCH_MODEL`, e.g. `gpt-5.4`, as a fallback.)*
> *(There's also a connection-based `BingGroundingTool` if your org needs a managed/keyed search
> backend — out of scope for today.)*

> **🔗 From code to Foundry.** `web_search_tool()` returns a `WebSearchTool` from
> `azure.ai.projects.models` — the **same hosted Web Search tool** you add under **Tools** in the
> portal. The search runs server-side in Foundry (no Bing connection), and `citations_of()` reads
> the `url_citation` annotations the service attaches to the response.
> Docs: [Web Search tool for agents](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/web-search).

> **📦 Libraries used.** `azure-ai-projects` provides `WebSearchTool` and creates the agent; `openai`
> (the **Responses API**) runs the turn — `run_response()` calls `responses.create(...)`, then you
> read `.output_text` plus the citation annotations.
> See [assets/README.md → Libraries used](../assets/README.md#libraries-used).

---

## 💡 Go further
- Dial `search_context_size` from `"low"` → `"high"` and watch depth vs. speed change.
- Ask a **comparison** question (try the `compare_methods` prompt) and see it synthesise across
  several pages in one answer.

➡️ **Next:** [Lab 2 — Ground on your papers](./lab-02-ground-on-your-papers.md)
