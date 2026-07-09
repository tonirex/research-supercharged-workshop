"""Lab 0 (Build rail) — Hello, Research Copilot (create + chat with an agent).

Creates the SAME kind of governed agent you build in the portal — a Prompt agent on the
current Microsoft Foundry agents API (azure-ai-projects >= 2.0) — and chats with it once,
before adding any tools. Every later lab gives this agent a new superpower.

The portal agent and this SDK agent are the *same* object type in Foundry: the portal is
just a UI over the `project.agents.create_version(...)` call `research_agent()` makes here.

Run from the assets/ folder (after `az login` and filling .env):
    python lab00_hello.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from common.research_common import (  # noqa: E402
    cleanup,
    research_agent,
    run_text,
)


def main():
    # research_agent() creates rc-<initials>-hello in the shared project with the Research
    # Copilot persona (public/unclassified guardrails baked in) and no tools yet.
    agent = research_agent("hello")
    try:
        question = "In one sentence, what can you help me research?"
        print(f"Q: {question}\n")
        print(run_text(agent, question))
    finally:
        cleanup(agent)  # tidy up the shared project when you're done


if __name__ == "__main__":
    main()
