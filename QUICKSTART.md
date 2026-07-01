# Quick Start — Research Supercharged (1 page)

You'll build **Research Copilot**, an agent that gains a superpower each lab:
🔎 **Search** the web · 📚 **Ground** on your docs · 📊 **Analyse** data · 🛠️ **Act** with tools.

> ## ⚠️ One rule, all day: **public / unclassified data only**
> Shared project, shared infra. No classified, sensitive, or personal material in any agent,
> upload, or prompt.

---

## Pick a rail (switch anytime)
- 🟢 **Explore** — do everything in the **portal**. No install. *Everyone can finish on this rail.*
- 🔵 **Build** — same agent from **Python**. Optional, goes deeper.

**Name your agent `rc-<your-initials>`** on the shared project (e.g. `rc-acw`), then paste the
Research Copilot persona from **[Lab 0](./labs/lab-00-hello-research-copilot.md)** — no typing from scratch.

---

## 🟢 Explore — get going in 4 steps
1. Open the shared **Foundry project** (link from facilitator) → **Agents** → **New agent**.
2. Name it `rc-<initials>`, paste the **persona** (from Lab 0), pick **`model-router`**.
3. **Chat** to confirm it replies — and that it **declines** a sensitive ask.
4. Each lab, add one tool: **Web Search** → **Knowledge/Files** → **Code Interpreter** → **MCP**.

## 🔵 Build — get going in 4 steps
```bash
cd research-supercharged-workshop/assets
pip install --prefer-binary -r requirements.txt
copy .env.example .env        # fill FOUNDRY_PROJECT_ENDPOINT + INITIALS, then: az login
python lab01_websearch.py     # then lab02_filesearch / lab03_codeinterpreter / lab04_tool
```
> Run scripts **from the `assets/` folder** so `from common.research_common import ...` resolves.

---

## The four labs at a glance
| Lab | You'll do | Portal (🟢) | Code (🔵) |
|-----|-----------|------------|-----------|
| 1 · Search | Cited answer from the live web | Tools → Web Search → *Search the web with Bing Search* (no setup, on `model-router`) | `lab01_websearch.py` |
| 2 · Ground | Cited answer from your **public** docs | Switch model → **`gpt-4.1`**, then Knowledge → add files (name the index with your initials) | `lab02_filesearch.py` |
| 3 · Analyse | Stats + chart; find the outlier | Tools → Code Interpreter | `lab03_codeinterpreter.py` |
| 4 · Act | Agent calls a tool, you approve | Tools → MCP | `lab04_tool.py` |

> **Model:** Labs 0–1 run on **`model-router`** (Web Search included). **From Lab 2 on, switch your
> agent to `gpt-4.1`** — the portal's File Search tool doesn't accept `model-router` — and keep it
> there for the rest of the portal labs. *(The `🔵` SDK scripts all work on `model-router`.)*

For Lab 2, use your **own public PDFs** or the facilitator's **starter corpus pack**.

---

## Stuck? (Build rail)
- `ModuleNotFoundError: common` → you're not in `assets/`. `cd` there.
- Auth / endpoint error → fill `.env` and run `az login`.
- `pip` wheel errors → `pip install --upgrade pip setuptools wheel`, then re-run with `--prefer-binary`.
- Lab 2 "no files" → add public docs to `assets/corpus/` first.

## When you finish
✅ You have a research agent with four superpowers. **Delete your `rc-<initials>` agent** to keep
the shared project tidy. Want to go further? See **Lab 5** and the repo `README`.
