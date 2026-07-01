---
lab: "bonus-01"
title: "Evaluate in the portal"
duration: "Bonus · self-paced (~15 min)"
foundry_feature: "Evaluations (portal)"
rails: ["🟢 Explore (portal)"]
---

# 🌟 Bonus 01 — Evaluate in the portal 📊

**Goal:** put a **number** on quality. Instead of eyeballing an answer, run built-in
**evaluators** over a set of Q&A rows and read per-row scores *and the reason the judge gave*.

> **Why it matters for research:** "looks good" doesn't scale. Evaluators let you compare prompts,
> models, or agents on the same yardstick — relevance, coherence, groundedness, safety — before you
> trust an assistant with real work.

Based on Microsoft Learn: [Run evaluations from the Microsoft Foundry portal](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluate-generative-ai-app).

---

## Before you start
- You have **Foundry User** on the workshop project (same as every lab).
- A **judge model** is available for AI-assisted evaluators — `model-router` (validated) or
  `gpt-4.1`. (The F1/similarity evaluator needs no model.)
- Grab the sample dataset **[`assets/data/eval_qa.jsonl`](../../assets/data/eval_qa.jsonl)** — 8
  research Q&A rows with `query`, `response`, and `ground_truth`. Row 8 is a deliberately vague
  answer, so you can watch an evaluator flag it.

---

## 🟢 Path A — evaluate a dataset (recommended first)

You score **pre-existing answers** — no agent needed. Fast and deterministic.

1. In the left pane, open **Evaluation** → **+ Create** (or **Create a new evaluation**).
2. **Evaluation target → Dataset.** (You're scoring answers that already exist.)
3. **Data source → Existing dataset.** Upload `eval_qa.jsonl` (or pick it if the facilitator
   pre-loaded it). Only **CSV/JSONL** are accepted.
4. **Field mapping** — confirm the columns map to the evaluator inputs:
   - `query` → **query**  · `response` → **response**  · `ground_truth` → **ground_truth**
   The portal usually auto-maps these; fix any that show **Unassigned**.
5. **Testing criteria** — add these built-in evaluators:
   - **Relevance** — is the answer on-topic for the question? *(AI-assisted → pick the judge model)*
   - **Coherence** — is it logically well-formed? *(AI-assisted)*
   - **F1 score** (or **Similarity**) — overlap with `ground_truth`. *(no model)*
6. Give it a **name** like `eval-<your-initials>` and **Submit**.
7. When **Status = Completed** (usually a minute or two), open it and read the results:
   - A per-row table of **pass/fail + score**, and for the AI judges a **reason** column.
   - Sort or scan for the weak row (#8) — it should score **low on coherence/relevance**, with a
     reason explaining why. That's the evaluator earning its keep.

### ✅ Checkpoint
You can point to **one row and its score**, and read the **judge's reason** for it — and the vague
answer scores lower than the good ones.

---

## 🟢 Path B — evaluate *your own* agent (variation)

Score the `rc-<initials>` agent you built in Labs 0–4 instead of a static dataset. The portal runs
your agent to produce the responses, then evaluates them.

1. **Evaluation** → **+ Create** → **Evaluation target → Agent** → choose your `rc-<initials>` agent.
2. **Scope → Individual turns.**
3. **Data source:**
   - **Existing dataset** — reuse `eval_qa.jsonl` (its `query` column drives your agent), **or**
   - **Synthetic data** — let Foundry generate test questions from a short prompt (e.g.
     *"questions a materials researcher would ask"*).
4. **Configure agents** (optional) — tweak the system/user prompt used during the run; the default
   `{{item.query}}` passes each question straight to your agent.
5. **Testing criteria** — for a research agent, pick **Relevance**, **Groundedness**, **Fluency**,
   **Coherence**; add safety evaluators (**Violence**, **Hate/Unfairness**, …) if you want a safety
   read too.
6. **Submit**, wait for **Completed**, and compare scores across evaluators.

> **Groundedness** needs context to judge against. Use it when your data has a `context` column (or
> for an agent that retrieves) — otherwise stick to Relevance/Coherence/F1 for the plain dataset.

---

## Tips & troubleshooting
- **No scores / evaluator failed?** Check field mapping — required inputs (query/response) must be
  assigned, and AI-assisted evaluators need a judge model selected.
- **Quota:** the judge model counts against your Azure OpenAI quota. Keep the dataset small (8 rows
  is plenty here); use `gpt-4.1-mini`-class judges for cheap runs on big sets.
- **Read the reason, not just the number.** The "why" is what tells you how to fix a prompt.

## Where this goes next
- Do the same thing **in code** → [bonus-02 — Cloud evaluation with the SDK](./bonus-02-cloud-evaluation-sdk.md),
  so you can wire evaluations into CI and track quality over time.

⬅️ Back to [bonus labs](./README.md) · [workshop overview](../../README.md)
