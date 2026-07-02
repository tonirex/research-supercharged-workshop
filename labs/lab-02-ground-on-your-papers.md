---
lab: 2
title: "Ground on Your Papers"
duration: "40 min (≈ 0:55–1:35)"
foundry_feature: "File Search / RAG (vector store)"
rails: ["🟢 Explore (portal)", "🔵 Build (SDK) — optional"]
---

# Lab 2 — Ground on Your Papers 📚

**Goal:** point Research Copilot at **your own** documents so it answers from *them* — and
cites the exact file — instead of the open web. This is Retrieval-Augmented Generation (RAG).

> **Why it matters for research:** your most valuable context (papers you're reading, reports,
> notes) isn't on the public web. RAG lets the agent read *your* corpus and ground every claim
> in a specific source you can open.

> ### ⚠️ Reminder: unclassified / public documents only
> Anything you index here is uploaded to the shared project. Use open-access papers, public
> reports, or your own non-sensitive notes. **No classified or personal material.**

---

## 🟢 Explore (portal) — everyone

> ### ⚠️ First, switch this agent to **`gpt-5.4`**
> The **File Search** tool is **not** supported on `model-router` in the portal — you'll get
> *"File search tool doesn't work with the model you selected. Please use another model."* On your
> `rc-<initials>` agent, open the **model** selector, pick **`gpt-5.4`**, and Save. *(Keep it on
> `gpt-5.4` for the rest of the portal labs — it supports every tool. Web Search from Lab 1 works
> on it too.)*

1. Gather **3–10 public documents** (PDF / MD / TXT / DOCX). No materials of your own? Use the
   facilitator's **open-access starter pack**.
2. On your `rc-<initials>` agent, open **Knowledge → add files** (or **Tools → Add → Files**). In
   the **Attach files** dialog, keep **Create a new index**, then **replace the auto-generated
   Vector index name with one you'll recognise — include your initials**, e.g.
   **`<initials>-papers`** (`jd-papers`). Upload your documents and wait for indexing.
   > **Why rename it?** Everyone shares one project, so the vector indexes are listed together.
   > Your initials make *yours* easy to find and avoid confusion with a neighbour's.
3. Ask a grounding question:
   > *"Using only the documents I uploaded, summarise the key findings and methods. Cite the
   > specific source file for each point. If something isn't in the documents, say so."*
4. **Test its honesty:** ask something you *know* isn't in the corpus. A good RAG agent says
   *"that's not covered in the provided documents"* rather than making it up.

### ✅ Checkpoint
Answers are **grounded in your files with per-claim citations**, and the agent **declines**
to answer what isn't in the corpus.

---

## 🔵 Build (SDK) — optional

Drop your files into **`assets/corpus/`**, then run:

```bash
python lab02_filesearch.py
```

It indexes the folder into a vector store and attaches a `FileSearchTool`:

```python
from common.research_common import research_agent, file_search_tool, build_vector_store, run_response, citations_of, cleanup, text_of

vector_store_id = build_vector_store()                       # uploads + indexes assets/corpus
agent = research_agent("rag", tools=[file_search_tool(vector_store_id)])
resp = run_response(agent, text_of("summarize_corpus"))
print(resp.output_text)
print(citations_of(resp))                                    # which files were cited
cleanup(agent)
```

> Unlike the portal, the **SDK** File Search runs fine on the default **`model-router`** — no model
> switch needed on this rail (verified). `build_vector_store()` auto-names the index; pass
> `name="<initials>-papers"` to label yours in the shared project.

---

## 💡 Go further
- **Combine rails:** give one agent *both* tools — `tools=[file_search_tool(vs), web_search_tool()]`
  (on the default `model-router`) — so it grounds on your papers **and** can check the live web.
  Ask a question that needs both.
- Ask for a **literature-review table** (method · dataset · result · source file) across the corpus.

➡️ **Next:** *Break (10 min)*, then [Lab 3 — Analyse the data](./lab-03-analyse-the-data.md)
