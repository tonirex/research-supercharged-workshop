"""Lab 1 (Build rail) — Search the literature with a hosted Web Search tool.

The current Foundry API ships a hosted `WebSearchTool` that needs NO Bing connection.
The agent searches live public pages server-side and returns an answer with citations.

Run from the assets/ folder (after `az login` and filling .env):
    python lab01_websearch.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from common.research_common import (  # noqa: E402
    WEBSEARCH_MODEL,
    citations_of,
    cleanup,
    research_agent,
    run_response,
    text_of,
    web_search_tool,
)


def main():
    # search_context_size: "low" | "medium" | "high" (how much page context to pull in)
    # Web Search runs on the default model-router. WEBSEARCH_MODEL lets you pin a fallback
    # model (e.g. gpt-5.4) via FOUNDRY_WEBSEARCH_MODEL, but it's not required.
    agent = research_agent("websearch", tools=[web_search_tool("high")], model=WEBSEARCH_MODEL)
    try:
        question = text_of("search_recent")
        print(f"Q: {question}\n")
        resp = run_response(agent, question)
        print(resp.output_text, "\n")
        print("Sources the agent cited:")
        for c in citations_of(resp) or [("(none captured — see the reply text)", None)]:
            if isinstance(c, dict):
                print(f"  - {c.get('title')}  {c.get('url')}")
            else:
                print(f"  - {c[0]}")
    finally:
        cleanup(agent)


if __name__ == "__main__":
    main()
