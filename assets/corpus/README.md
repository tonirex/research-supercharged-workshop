# Corpus — drop your own documents here (Lab 2)

Lab 2 builds a **vector store** from everything in this folder so the agent can answer
**grounded in your documents** and cite them.

## ⚠️ Data posture — read first
Use **public / unclassified** material only. Do **not** place sensitive, classified, or
personal documents here, or upload them to any agent, vector store, or code-interpreter
session during this workshop.

## What to add
A handful of files is plenty for the lab (3–10 is ideal):

- `.pdf`, `.md`, `.txt`, `.docx` all work.
- Good public choices: open-access papers (e.g. arXiv PDFs), public technical reports,
  standards, datasheets, Wikipedia article exports, or your own published/non-sensitive notes.

## Where it's used
- **🟢 Explore (portal):** on your agent, use **Tools → Upload files** to add these same files.
- **🔵 Build (SDK):** `python lab02_filesearch.py` indexes this folder via
  `build_vector_store()` and queries it.

> The facilitator provides a small open-access starter pack on the day if you don't bring
> your own — see [STARTER-CORPUS.md](./STARTER-CORPUS.md) for the curated manifest. This folder
> ships empty by design.
