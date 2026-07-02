---
lab: "bonus-02"
title: "Cloud evaluation with the SDK"
duration: "Bonus · self-paced (~15 min)"
foundry_feature: "Cloud evaluation (SDK)"
rails: ["🔵 Build (SDK)"]
---

# 🌟 Bonus 02 — Cloud evaluation with the SDK 🧪

**Goal:** run the same kind of evaluation as Bonus 01, but **in code** — upload a dataset, kick off
a **cloud** evaluation (the service does the scoring, not your laptop), poll for results, and open
the report. This is the shape you'd drop into CI to catch quality regressions.

> **Why it matters for research:** once evaluation is a script, you can re-run it on every prompt
> tweak or model change and *track* whether groundedness/relevance went up or down — reproducibly.

Based on Microsoft Learn: [Run evaluations in the cloud by using the Microsoft Foundry SDK](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/cloud-evaluation?tabs=python).

---

## Before you start
- Same setup as Labs 1–4: `.env` filled in + `az login`
  (see [../../assets/README.md](../../assets/README.md)).
- `azure-ai-projects>=2.2.0` (already pinned in
  [../../assets/requirements.txt](../../assets/requirements.txt)).
- A **judge model** for the AI-assisted evaluators. Defaults to your `FOUNDRY_MODEL_NAME`
  (`model-router`, validated); set `FOUNDRY_EVAL_MODEL=gpt-4.1` to pin a specific one.

---

## Run it

From the `assets/` folder:

```bash
python bonus_cloud_eval.py
```

The script ([`assets/bonus_cloud_eval.py`](../../assets/bonus_cloud_eval.py)) walks the full flow
against the sample dataset [`assets/data/eval_qa.jsonl`](../../assets/data/eval_qa.jsonl):

1. **Upload** the JSONL as a versioned data asset.
2. **Define** the schema + evaluators (testing criteria), mapping data fields with `{{item.field}}`.
3. **Create** the evaluation and **start a run** against the dataset.
4. **Poll** until it completes, then print pass rates + a portal **report URL**.

The heart of it (three built-in evaluators — two AI-assisted, one pure-overlap):

```python
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam, SourceFileID)

project = rc.get_project();  openai_client = rc.get_openai()

data_id = project.datasets.upload_file(name=f"rc-{rc.INITIALS}-evalset",
                                       version=version, file_path="data/eval_qa.jsonl").id

testing_criteria = [
    {"type": "azure_ai_evaluator", "name": "relevance", "evaluator_name": "builtin.relevance",
     "initialization_parameters": {"model": JUDGE_MODEL},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}},
    {"type": "azure_ai_evaluator", "name": "coherence", "evaluator_name": "builtin.coherence",
     "initialization_parameters": {"model": JUDGE_MODEL},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}},
    {"type": "azure_ai_evaluator", "name": "f1", "evaluator_name": "builtin.f1_score",
     "data_mapping": {"response": "{{item.response}}", "ground_truth": "{{item.ground_truth}}"}},
]

eval_object = openai_client.evals.create(name=f"rc-{rc.INITIALS}-dataset-eval",
    data_source_config=DataSourceConfigCustom(type="custom", item_schema={...}),
    testing_criteria=testing_criteria)

eval_run = openai_client.evals.runs.create(eval_id=eval_object.id, name="run",
    data_source=CreateEvalJSONLRunDataSourceParam(
        type="jsonl", source=SourceFileID(type="file_id", id=data_id)))
```

---

## What you'll see (validated live)

```
Uploading eval_qa.jsonl (version 20260702...) ...
Creating evaluation (judge model: model-router) ...
Polling for results (a few minutes) ...

Status: completed
Result counts: ResultCounts(errored=0, failed=5, passed=3, total=8, skipped=0)

Per-criteria pass rates:
  relevance     passed=7  failed=1
  coherence     passed=7  failed=1
  f1            passed=3  failed=5

Open the full report in the portal:
  https://ai.azure.com/.../evaluations/eval_.../run/evalrun_...
```

Read it like this:

- **relevance / coherence 7 ✅ 1 ❌** — the seven solid answers pass; the one **deliberately vague
  row** (#8) fails on both. The AI judge caught exactly what you'd want it to.
- **f1 3 ✅ 5 ❌** — F1 is strict *token overlap* with `ground_truth`. Our good answers are correct
  **paraphrases**, so they overlap only partially. **This is the lesson:** different evaluators
  measure different things — an LLM judge rewards *meaning*, F1 rewards *wording*. Use quality
  judges for open-ended answers and keep F1/similarity for near-exact expected outputs.
- Open the **report URL** to drill into per-row scores and each judge's **reason**.

> **`Total = 8`** because each evaluator runs on all 8 rows. The top-line `passed/failed` counts
> items across criteria; the per-criteria block is what you actually compare.

---

## Try this
- Swap in **`builtin.groundedness`** if you add a `context` field, or **`builtin.fluency`** /
  **`builtin.similarity`** to the `testing_criteria` list.
- Point `DATASET` at your **own** JSONL (answers from your `rc-<initials>` agent) and re-run — now
  you're grading your own agent, reproducibly.
- Set `FOUNDRY_EVAL_MODEL=gpt-4.1` and compare whether the judge model changes any borderline rows.

## Notes
- Cloud evaluation is **asynchronous** — the script polls; a run takes a few minutes.
- Each participant's dataset/eval is namespaced `rc-<initials>-…`, so runs don't collide in the
  shared project. The dataset version is timestamped so you can re-run freely.
- The judge model counts against Azure OpenAI quota; the 8-row set is intentionally tiny.

⬅️ Back to [bonus labs](./README.md) · [workshop overview](../../README.md)
