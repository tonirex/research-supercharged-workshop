"""Bonus lab — Cloud evaluation with the Microsoft Foundry SDK.

Uploads a small research Q&A dataset to the project, runs three built-in evaluators as a
**cloud** evaluation (the service does the work, not your laptop), polls until it finishes,
then prints per-criteria pass rates and a portal report URL you can open.

Evaluators used:
  * relevance  — is the answer relevant to the question?           (AI-assisted, needs a judge model)
  * coherence  — is the answer logically well-formed?              (AI-assisted, needs a judge model)
  * f1_score   — token overlap of answer vs. ground_truth          (no model needed)

Docs: https://learn.microsoft.com/azure/foundry/how-to/develop/cloud-evaluation?tabs=python

Run from the assets/ folder (after `az login`):
    python bonus_cloud_eval.py

Requires: azure-ai-projects>=2.2.0 and a judge-model deployment. Defaults to your
FOUNDRY_MODEL_NAME (model-router); set FOUNDRY_EVAL_MODEL to pin one (e.g. gpt-5.4).
"""
import os
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from common import research_common as rc  # noqa: E402

from openai.types.eval_create_params import DataSourceConfigCustom  # noqa: E402
from openai.types.evals.create_eval_jsonl_run_data_source_param import (  # noqa: E402
    CreateEvalJSONLRunDataSourceParam,
    SourceFileID,
)

DATASET = pathlib.Path(__file__).resolve().parent / "data" / "eval_qa.jsonl"
JUDGE_MODEL = os.environ.get("FOUNDRY_EVAL_MODEL") or rc.MODEL


def main() -> None:
    project = rc.get_project()
    openai_client = rc.get_openai()
    initials = rc.INITIALS

    # 1) Upload the dataset -> a versioned data asset in the project.
    #    Timestamp the version so re-runs never collide with an existing one.
    version = os.environ.get("DATASET_VERSION") or time.strftime("%Y%m%d%H%M%S")
    print(f"Uploading {DATASET.name} (version {version}) ...")
    data_id = project.datasets.upload_file(
        name=f"rc-{initials}-evalset",
        version=version,
        file_path=str(DATASET),
    ).id
    print("  dataset id:", data_id)

    # 2) Describe the data schema and pick evaluators (testing criteria).
    #    data_mapping wires JSONL fields -> evaluator inputs with {{item.<field>}}.
    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "response": {"type": "string"},
                "ground_truth": {"type": "string"},
            },
            "required": ["query", "response", "ground_truth"],
        },
    )

    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "relevance",
            "evaluator_name": "builtin.relevance",
            "initialization_parameters": {"model": JUDGE_MODEL},
            "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "coherence",
            "evaluator_name": "builtin.coherence",
            "initialization_parameters": {"model": JUDGE_MODEL},
            "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"},
        },
        {
            "type": "azure_ai_evaluator",
            "name": "f1",
            "evaluator_name": "builtin.f1_score",
            "data_mapping": {
                "response": "{{item.response}}",
                "ground_truth": "{{item.ground_truth}}",
            },
        },
    ]

    # 3) Create the evaluation, then start a run against the uploaded dataset.
    print(f"Creating evaluation (judge model: {JUDGE_MODEL}) ...")
    eval_object = openai_client.evals.create(
        name=f"rc-{initials}-dataset-eval",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )
    print("  eval id:", eval_object.id)

    eval_run = openai_client.evals.runs.create(
        eval_id=eval_object.id,
        name=f"rc-{initials}-run",
        data_source=CreateEvalJSONLRunDataSourceParam(
            type="jsonl",
            source=SourceFileID(type="file_id", id=data_id),
        ),
    )
    print("  run id:", eval_run.id)

    # 4) Poll until done (cloud evaluation is asynchronous).
    print("Polling for results (a few minutes) ...")
    while True:
        run = openai_client.evals.runs.retrieve(run_id=eval_run.id, eval_id=eval_object.id)
        if run.status in ("completed", "failed"):
            break
        time.sleep(10)

    print("\nStatus:", run.status)
    counts = getattr(run, "result_counts", None)
    if counts:
        print("Result counts:", counts)
    per_criteria = getattr(run, "per_testing_criteria_results", None)
    if per_criteria:
        print("\nPer-criteria pass rates:")
        for c in per_criteria:
            passed = getattr(c, "passed", "?")
            failed = getattr(c, "failed", "?")
            name = getattr(c, "name", getattr(c, "testing_criteria", "?"))
            print(f"  {name:12}  passed={passed}  failed={failed}")
    report = getattr(run, "report_url", None)
    if report:
        print("\nOpen the full report in the portal:\n ", report)


if __name__ == "__main__":
    main()
