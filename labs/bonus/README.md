# 🌟 Bonus labs — Evaluate & observe

Optional, **self-paced** extensions for after the core workshop (Labs 0–5). They pick up the
Lab 5 "Evaluate & observe" thread: before an agent leaves a demo, you want to **measure** its
quality — is it relevant, coherent, grounded, safe? — not just eyeball it.

There are two rails, same as the main workshop:

| Bonus | Rail | You'll do | Based on |
| --- | --- | --- | --- |
| **[bonus-01 — Evaluate in the portal](./bonus-01-evaluate-in-portal.md)** | 🟢 Explore | Run built-in evaluators on a dataset (or your own agent) from the Foundry **Evaluation** UI and read per-row scores + reasons. | [Run evaluations from the portal](https://learn.microsoft.com/en-us/azure/foundry/how-to/evaluate-generative-ai-app) |
| **[bonus-02 — Cloud evaluation with the SDK](./bonus-02-cloud-evaluation-sdk.md)** | 🔵 Build | Upload a dataset and run a **cloud** evaluation in code (`evals.create` / `runs.create`), poll for results, open the report. | [Cloud evaluation (SDK)](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/cloud-evaluation?tabs=python) |

Both use the same tiny sample dataset: **[`../../assets/data/eval_qa.jsonl`](../../assets/data/eval_qa.jsonl)**
(8 research Q&A rows with `query` / `response` / `ground_truth`, including one deliberately weak
answer so you can see an evaluator catch it).

## What you need

- The same access as the core labs (**Foundry User** on the project — you already have it).
- A **judge model** deployment for the AI-assisted evaluators. `model-router` works (validated);
  `gpt-4.1` is a fine alternative. F1/similarity evaluators need no model.
- For the SDK rail: the same `.env` + `az login` as Labs 1–4, and `azure-ai-projects>=2.2.0`
  (already in [`../../assets/requirements.txt`](../../assets/requirements.txt)).

> These are **not** timed into the 2.5–3 h schedule — do them if you finish early or want to take
> the idea back to your own project.

⬅️ Back to [the workshop overview](../../README.md)
