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

---

## 🟢 Explore (portal) — everyone

> ### ⚠️ First, switch this agent to **`gpt-4.1`**
> The teaching default **`model-router` does *not* support the Web Search tool.** On your
> `rc-<initials>` agent, open the **model** selector and pick **`gpt-4.1`** (Web Search runs only
> on Azure OpenAI models — `gpt-4.1` is our pick for today). Save, then add the tool below.

1. On your `rc-<initials>` agent, open **Tools** → add the **Web Search** grounding tool.
   *(Your facilitator will point out the exact label and the **search context size** option —
   how much of each page the agent reads.)*
2. Ask a current, public research question:
   > *"What are the most significant developments in solid-state battery research in the last
   > two years? Summarise the top 3 and cite a source for each."*

   *(Swap in **your own field** — that's the point.)*
3. **Inspect the citations.** Expand the sources / annotations and click through to at least
   one. Are they credible? Recent?
4. **A/B it:** temporarily **remove** the Web Search tool and ask the same question. Notice the
   answer gets vaguer and loses citations. Re-add the tool. *This contrast is the lesson.*

### ✅ Checkpoint
The grounded answer names **3 developments**, each with a **clickable, recent source**, and
visibly beats the no-tool version.

---

## 🔵 Build (SDK) — optional

Run it:

```bash
python lab01_websearch.py
```

The core is three lines — `WebSearchTool` is **hosted**, so the service does the searching
server-side and you just read the result and its citations:

```python
from common.research_common import research_agent, web_search_tool, run_response, citations_of, cleanup, text_of, WEBSEARCH_MODEL

# model=gpt-4.1 (via WEBSEARCH_MODEL) — Web Search needs an Azure OpenAI model, not model-router.
agent = research_agent("websearch", tools=[web_search_tool("high")], model=WEBSEARCH_MODEL)  # "low"|"medium"|"high"
resp = run_response(agent, text_of("search_recent"))
print(resp.output_text)
print(citations_of(resp))                                              # titles + URLs the agent used
cleanup(agent)
```

> No Bing connection or API key to provision — `WebSearchTool()` works out of the box on the
> current Foundry API. **Just remember Web Search runs only on Azure OpenAI models, so the agent
> is pinned to `gpt-4.1` (override with `FOUNDRY_WEBSEARCH_MODEL`), not `model-router`.**
> *(There's also a connection-based `BingGroundingTool` if your org needs a managed/keyed search
> backend — out of scope for today.)*

---

## 💡 Go further
- Dial `search_context_size` from `"low"` → `"high"` and watch depth vs. speed change.
- Ask a **comparison** question (try the `compare_methods` prompt) and see it synthesise across
  several pages in one answer.

➡️ **Next:** [Lab 2 — Ground on your papers](./lab-02-ground-on-your-papers.md)
