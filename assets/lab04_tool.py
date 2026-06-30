"""Lab 4 (Build rail) — Give the agent a tool it can call (function calling).

We expose a Python `convert_units` function as a tool. When the question needs a
conversion, the model calls the tool, we run the real Python, hand the result back, and
it finishes the answer. `run_with_trace` records which tools fired so we can assert it.

Stretch: swap the function tool for an MCP server with `mcp_tool(...)` (see README).

Run from the assets/ folder:
    python lab04_tool.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from common.research_common import (  # noqa: E402
    cleanup,
    function_tool,
    research_agent,
    run_with_trace,
    text_of,
)

# A few conversions a researcher actually reaches for. Real Python = no hallucinated math.
_FACTORS = {
    ("ev", "j"): 1.602176634e-19,
    ("j", "ev"): 1.0 / 1.602176634e-19,
    ("nm", "m"): 1e-9,
    ("m", "nm"): 1e9,
    ("angstrom", "m"): 1e-10,
    ("m", "angstrom"): 1e10,
    ("kpa", "atm"): 1.0 / 101.325,
    ("atm", "kpa"): 101.325,
}


def convert_units(value, from_unit, to_unit):
    """Convert a physical quantity between units. Returns {value, unit} or {error}."""
    f, t = str(from_unit).lower().strip(), str(to_unit).lower().strip()
    if (f, t) == ("c", "k"):
        return {"value": value + 273.15, "unit": "K"}
    if (f, t) == ("k", "c"):
        return {"value": value - 273.15, "unit": "C"}
    if (f, t) in _FACTORS:
        return {"value": value * _FACTORS[(f, t)], "unit": to_unit}
    return {"error": f"no conversion from {from_unit} to {to_unit}"}


CONVERT_SCHEMA = {
    "type": "object",
    "properties": {
        "value": {"type": "number", "description": "The quantity to convert"},
        "from_unit": {"type": "string", "description": "Source unit, e.g. eV, nm, kPa, C"},
        "to_unit": {"type": "string", "description": "Target unit, e.g. J, m, atm, K"},
    },
    "required": ["value", "from_unit", "to_unit"],
    "additionalProperties": False,
}


def main():
    tool = function_tool(
        "convert_units", "Convert a physical quantity between units.", CONVERT_SCHEMA
    )
    agent = research_agent("tools", tools=[tool])
    try:
        question = text_of("convert_question")
        print(f"Q: {question}\n")
        out, trace = run_with_trace(
            agent, question, functions={"convert_units": convert_units}
        )
        print(out, "\n")
        fired = [c.name for c in trace.tool_calls]
        print("Tools the agent called:", fired)
        assert "convert_units" in fired, f"expected convert_units to be called, got {fired}"
        print("PASS — the agent used the tool instead of guessing.")
    finally:
        cleanup(agent)


if __name__ == "__main__":
    main()
