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

---

## 🟢 Explore (portal) — everyone

1. **Concept (1 min):** a *tool* is a capability you register on the agent. The model decides
   *when* to call it, you (or a service) run it, and the result flows back into the answer.
   You've already used hosted tools (Web Search, Code Interpreter); now we add an **external**
   one via **MCP** (Model Context Protocol — an open standard for tool servers).
2. On your `rc-<initials>` agent, open **Tools → MCP** and add the **workshop research MCP
   server** (your facilitator shares the URL). Set **require approval = always** so you stay in
   the loop.
3. Ask a question that needs it, e.g. *"Use the tool to convert 1.8 eV to joules."*
4. **Approve** the tool call when prompted, and read the grounded result.

> 🛟 **No MCP server on the day?** The facilitator demos this once, and everyone does the Build
> rail below — which teaches the same idea with a local function tool (no server needed).

### ✅ Checkpoint
The agent **calls the tool** (you approve it) and answers using the **tool's result**, not a
guess.

---

## 🔵 Build (SDK)

Run it:

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

### 💡 Stretch — make it an MCP tool
Swap the function tool for an MCP server with the helper (the agent calls it the same way):

```python
from common.research_common import mcp_tool
agent = research_agent("mcp", tools=[mcp_tool("research", "https://<your-mcp-url>",
                                              require_approval="always")])
```

> **Go further (orchestration):** for multi-step research pipelines, look at **Workflow agents**
> (`WorkflowAgentDefinition`) or the **Microsoft Agent Framework** — code-first ways to chain
> several agents/tools. Pointers in the repo `README`.

➡️ **Next:** [Lab 5 — Take it home](./lab-05-take-it-home.md)
