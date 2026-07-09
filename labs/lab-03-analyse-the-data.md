---
lab: 3
title: "Analyse the Data"
duration: "40 min (≈ 1:45–2:25)"
foundry_feature: "Code Interpreter (hosted Python sandbox)"
rails: ["🟢 Explore (portal)", "🔵 Build (SDK) — optional"]
---

# Lab 3 — Analyse the Data 📊

**Goal:** let Research Copilot **run real Python** to analyse a dataset — computing exact
numbers and drawing charts — instead of estimating in its head.

> **Why it matters for research:** language models are unreliable at arithmetic and stats.
> The Code Interpreter gives the agent a sandbox to actually *compute* — so a mean is a real
> mean and a trend is a real fit. You bring the question; it writes and runs the code.

> ### ⚠️ Reminder: public / synthetic data only
> We ship a small **synthetic** dataset (`assets/data/sample_experiments.csv`). Use it, or your
> own **public/unclassified** CSV. Never upload sensitive data to the sandbox.

> 📸 **Prefer a click-by-click walkthrough?** Follow the **[portal walkthrough](./lab-03-portal.md)** —
> the 🟢 portal-rail steps below, captured screen by screen (and kept current with the latest portal UI).

---

## 🟢 Explore (portal) — everyone

1. On your `rc-<initials>` agent, open **Tools** → add **Code Interpreter**.
2. **Upload** `assets/data/sample_experiments.csv` **to the tool**: on the **Code Interpreter**
   row under **Tools**, click **Files → browse for files**, pick the CSV, and **Attach**.
   *(The chat composer's paperclip only accepts images/PDFs, so data files go in at the tool level.)*
3. Ask:
   > *"Describe this dataset. Compute summary statistics for each numeric column, plot
   > `energy_density_whkg` over `trial`, and tell me whether it's improving. Then identify the
   > row that breaks that upward trend (a contextual outlier vs. its neighbours) and explain why."*
4. Watch it **write Python, run it, and report real numbers**, then open the chart it produces —
   in the current portal it comes back as a **downloadable plot link** rather than rendering
   inline. Look for the one row that breaks the upward trend. *(Hint: check around **trial 12 /
   sample `S012`**.)*

### ✅ Checkpoint
The agent produces a **chart** (offered as a downloadable plot) + **computed statistics**, says
energy density is **improving across trials**, and flags **`S012` (trial 12)** as the row that
**breaks the trend** — its yield/energy dips far below its neighbours.

---

## 🔵 Build (SDK) — optional

Script for this lab: **[`assets/lab03_codeinterpreter.py`](../assets/lab03_codeinterpreter.py)** (SDK
helpers in **[`assets/common/research_common.py`](../assets/common/research_common.py)**). It reads
**[`assets/data/sample_experiments.csv`](../assets/data/sample_experiments.csv)**. Run it from `assets/`:

```bash
python lab03_codeinterpreter.py
```

`CodeInterpreterTool` is **hosted**, so attaching it is all it takes — the agent runs Python
server-side:

```python
from common.research_common import research_agent, code_interpreter_tool, run_text, cleanup, DATA

csv_text = (DATA / "sample_experiments.csv").read_text(encoding="utf-8")
agent = research_agent("data", tools=[code_interpreter_tool()])
print(run_text(agent, "You have a Python sandbox. Analyse this CSV:\n" + csv_text +
                      "\nReport summary stats, quantify the energy_density trend, and name the row that breaks it."))
cleanup(agent)
```

> We paste the small CSV inline so the lab runs anywhere. In the **portal** you attach the file
> to the **Code Interpreter** tool instead, and it returns the chart as a **downloadable plot** —
> either way the agent runs real Python on your data.

> **🔗 From code to Foundry.** `code_interpreter_tool()` returns a `CodeInterpreterTool` from
> `azure.ai.projects.models` — the **same hosted Python sandbox** as the portal's **Code Interpreter**
> tool. The code the agent writes runs server-side in Foundry, not on your laptop.
> Docs: [Code Interpreter tool](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/code-interpreter).

> **📦 Libraries used.** `azure-ai-projects` provides `CodeInterpreterTool` and creates the agent;
> `openai` (the **Responses API**) runs the turn — `run_text()` sends the prompt and returns
> `.output_text`.
> See [assets/README.md → Libraries used](../assets/README.md#libraries-used).

---

## 💡 Go further
- Ask it to **fit a linear regression** of energy density on trial and report slope + R².
- Ask for a **cleaned dataset** with the outlier removed, then re-plot.

---

⬅️ **Previous:** [Lab 2 — Ground on your papers](./lab-02-ground-on-your-papers.md) · ➡️ **Next:** [Lab 4 — Add a tool](./lab-04-add-a-tool.md)
