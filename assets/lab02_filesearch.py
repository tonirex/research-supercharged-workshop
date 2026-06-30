"""Lab 2 (Build rail) — Ground answers in YOUR documents (File Search / RAG).

Builds a vector store from everything in assets/corpus, attaches a FileSearchTool, and
asks a grounded question. The agent answers from your documents and cites them.

Reminder: put only PUBLIC / UNCLASSIFIED documents in assets/corpus.

Run from the assets/ folder:
    python lab02_filesearch.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from common.research_common import (  # noqa: E402
    build_vector_store,
    citations_of,
    cleanup,
    delete_vector_store,
    file_search_tool,
    research_agent,
    run_response,
    text_of,
)


def main():
    print("Indexing assets/corpus into a vector store ...")
    vector_store_id = build_vector_store()  # uploads + indexes assets/corpus
    agent = research_agent("rag", tools=[file_search_tool(vector_store_id)])
    try:
        question = text_of("summarize_corpus")
        print(f"\nQ: {question}\n")
        resp = run_response(agent, question)
        print(resp.output_text, "\n")
        print("Documents the agent cited:")
        for c in citations_of(resp):
            print(f"  - {c.get('title')}")
    finally:
        cleanup(agent)
        delete_vector_store(vector_store_id)  # tidy up the shared project


if __name__ == "__main__":
    main()
