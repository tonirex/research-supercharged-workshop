"""Lab 3 (Build rail) — Analyse data with a hosted Code Interpreter.

The current Foundry API ships a hosted `CodeInterpreterTool` — a real Python sandbox the
agent uses to compute (so numbers are calculated, not guessed). Here we hand it a small
public dataset and ask for stats + a trend read. In the *portal* you'd also see any chart
rendered inline; from the SDK we print the agent's analysis.

Run from the assets/ folder:
    python lab03_codeinterpreter.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from common.research_common import (  # noqa: E402
    DATA,
    cleanup,
    code_interpreter_tool,
    research_agent,
    run_text,
)


def main():
    csv_text = (DATA / "sample_experiments.csv").read_text(encoding="utf-8")
    agent = research_agent("data", tools=[code_interpreter_tool()])
    try:
        prompt = (
            "You have a Python sandbox. Analyse this experiment dataset (CSV below).\n\n"
            f"{csv_text}\n\n"
            "1) Report summary statistics for each numeric column.\n"
            "2) Is `energy_density_whkg` improving across trials? Fit a simple trend and quantify it.\n"
            "3) Identify any row that breaks that upward trend (a contextual outlier vs. its\n"
            "   neighbouring trials), name its sample_id, and explain why. Show the key numbers."
        )
        print(run_text(agent, prompt))
    finally:
        cleanup(agent)


if __name__ == "__main__":
    main()
