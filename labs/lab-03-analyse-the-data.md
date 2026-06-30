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

---

## 🟢 Explore (portal) — everyone

1. On your `rc-<initials>` agent, open **Tools** → add **Code Interpreter**.
2. **Upload** `assets/data/sample_experiments.csv` (drag it into the chat or attach it).
3. Ask:
   > *"Describe this dataset. Compute summary statistics for each numeric column, plot
   > `energy_density_whkg` over `trial`, and tell me whether it's improving. Then identify the
   > row that breaks that upward trend (a contextual outlier vs. its neighbours) and explain why."*
4. Watch it **write code, run it, render a chart inline**, and report numbers. Look for the one
   row that breaks the upward trend. *(Hint: check around **trial 12 / sample `S012`**.)*

### ✅ Checkpoint
The agent shows a **chart** + **computed statistics**, says energy density is **improving
across trials**, and flags **`S012` (trial 12)** as the row that **breaks the trend** — its
yield/energy dips far below its neighbours.

---

## 🔵 Build (SDK) — optional

Run it:

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

> We paste the small CSV inline so the lab runs anywhere. In the **portal** you simply attach
> the file and charts render inline — the nicer experience for this lab.

---

## 💡 Go further
- Ask it to **fit a linear regression** of energy density on trial and report slope + R².
- Ask for a **cleaned dataset** with the outlier removed, then re-plot.

➡️ **Next:** [Lab 4 — Add a tool](./lab-04-add-a-tool.md)
