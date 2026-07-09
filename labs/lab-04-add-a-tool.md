---
lab: 4
title: "Add a Tool"
duration: "25 min (≈ 2:25–2:50)"
foundry_feature: "Function calling & tools (MCP stretch)"
rails: ["🟢 Explore (portal)", "🔵 Build (SDK)"]
---

# Lab 4 — Add a Tool 🔧

**Goal:** connect Research Copilot to an **action** — a function or external service it can call
when it needs a fact or capability it shouldn't guess. This is what turns a chatbot into an
*agent*.

> **Why it matters for research:** the agent can't reliably know everything (precise
> conversions, a lookup in a catalogue, a live calculation). Tools let it **call out** to
> trustworthy code or services and use the real result.

> 📸 **Prefer a click-by-click walkthrough?** Follow the **[portal walkthrough](./lab-04-portal.md)** —
> the 🟢 portal-rail steps below, captured screen by screen (and kept current with the latest portal UI).

---

## 🟢 Explore (portal) — everyone

1. **Concept (1 min):** a *tool* is a capability you register on the agent. The model decides
   *when* to call it, you (or a service) run it, and the result flows back into the answer.
   You've already used hosted tools (Web Search, Code Interpreter); now we add an **external**
   one via **MCP** (Model Context Protocol — an open standard for tool servers).
2. **Attach the shared tool.** Creating an MCP server from scratch (**Tools → Add → Custom →
   MCP → Connect**) needs **Foundry Owner** rights, which participants don't have — so your
   facilitator has registered the workshop server **once** as a shared tool called
   **`research-tools`**. In the **left nav → Tools**, click **`research-tools`**, then **Use in an
   agent** and pick your `rc-<initials>` agent (no URL to paste). This one server exposes two tools:
   - **`convert_units`** — exact unit conversions (eV↔J, nm↔m, Å↔m, kPa↔atm, °C↔K).
   - **`search_arxiv`** — live search of the public [arXiv](https://arxiv.org/) preprint API.
3. Ask a question that needs it. The agent **pauses for your approval** before each call — choose
   **Approve once** to review every one (the portal's equivalent of *require approval = always*).
   Approve, then read the grounded result. Try both:
   - *"Use the tool to convert 1.8 eV to joules."* → calls `convert_units` (≈ `2.884e-19 J`).
   - *"Search arXiv for recent work on solid-state battery electrolytes and summarise the top 2."*
     → calls `search_arxiv` and cites real papers.

> 🛟 **No MCP server on the day?** No problem — the facilitator demos it once, and everyone does
> the Build rail below, which teaches the same idea with a local function tool (no server needed).
> You can also add a hosted tool (Web Search / Code Interpreter) to feel the same approve-a-call
> loop.

### ✅ Checkpoint
The agent **calls the tool** (you approve it) and answers using the **tool's result**, not a
guess.

---

## 🔵 Build (SDK)

Script for this lab: **[`assets/lab04_tool.py`](../assets/lab04_tool.py)** (SDK helpers in
**[`assets/common/research_common.py`](../assets/common/research_common.py)**). Run it from `assets/`:

```bash
python lab04_tool.py
```

You expose a plain Python function as a tool; when the question needs it, the model calls it,
you run the real code, and hand the result back. `run_with_trace` records which tools fired:

```python
from common.research_common import research_agent, function_tool, run_with_trace, cleanup, text_of

def convert_units(value, from_unit, to_unit):
    ...  # real Python — no hallucinated math

tool = function_tool("convert_units", "Convert a physical quantity between units.", CONVERT_SCHEMA)
agent = research_agent("tools", tools=[tool])
out, trace = run_with_trace(agent, text_of("convert_question"),
                            functions={"convert_units": convert_units})
assert "convert_units" in [c.name for c in trace.tool_calls]      # it used the tool
cleanup(agent)
```

> **🔗 From code to Foundry.** `function_tool()` returns a `FunctionTool` from
> `azure.ai.projects.models`. The model emits a `function_call`; `run_with_trace()` runs your Python
> and returns a `function_call_output` on the next Responses API turn — the **same tool-call → run →
> return loop** the portal shows (there you *approve* each call).
> Docs: [Function calling](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/function-calling).

> **📦 Libraries used.** `azure-ai-projects` provides `FunctionTool` (and `MCPTool` for the stretch);
> `openai` (the **Responses API**) drives the loop — `responses.create(..., previous_response_id=...)`
> threads your tool results back in.
> See [assets/README.md → Libraries used](../assets/README.md#libraries-used).

### 💡 Stretch — add an MCP server as a tool
Swap the function tool for the **same MCP server the portal rail uses** (the agent calls it the
same way). Try adding it yourself with the workshop server URL below — it exposes `convert_units`
and `search_arxiv`:

```python
from common.research_common import mcp_tool

MCP_URL = "https://mcp-research-tools.bravebay-a4d1d67d.westeurope.azurecontainerapps.io/mcp"
agent = research_agent("mcp", tools=[mcp_tool("research", MCP_URL,
                                              require_approval="always")])
```

> If your facilitator shared a different `…/mcp` URL for the day, use that instead.

> The server's source is in [`assets/mcp-server/`](../assets/mcp-server/); an admin deploys it to
> Azure Container Apps beforehand ([admin/03-deploy-mcp-server.md](../admin/03-deploy-mcp-server.md)).

> `mcp_tool()` returns an `MCPTool` from `azure.ai.projects.models` — the **same MCP server
> registration** the portal uses when a facilitator adds **Tools → MCP**.
> Docs: [Model Context Protocol tool](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol).

> **Go further (orchestration):** for multi-step research pipelines, look at **Workflow agents**
> (`WorkflowAgentDefinition`) or the **Microsoft Agent Framework** — code-first ways to chain
> several agents/tools. Pointers in the repo `README`.

---

⬅️ **Previous:** [Lab 3 — Analyse the data](./lab-03-analyse-the-data.md) · ➡️ **Next:** [Lab 5 — Take it home](./lab-05-take-it-home.md)
