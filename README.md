# Research Supercharged: Azure AI for the Curious Mind 🔬✨

A **hands-on, 3-hour** workshop that takes a curious researcher from *"what's an AI agent?"* to
*"I built one that searches the literature, reads my papers, crunches my data, and calls tools"* —
all on **Microsoft Foundry**.

- **Audience:** researchers, scientists & engineers (built for **DSO**) — curious minds, mixed
  coding experience.
- **Format:** ~3 hours, hands-on, on a single shared Foundry project.
- **Anchor:** you build one agent — **"Research Copilot"** — and give it a new superpower each lab.
  Bring your own research topic; the labs adapt to any field.

> ## ⚠️ Data posture — public / unclassified only
> This workshop runs on shared cloud infrastructure with **public or synthetic data only**.
> Do **not** type, upload, or ground on anything sensitive, classified, or personal — in chats,
> documents, or datasets. The Research Copilot persona is instructed to refuse such requests,
> but **you** are the real guardrail. When in doubt, use a public example.

---

## What you'll build

| Lab | Superpower | Foundry feature |
|-----|------------|-----------------|
| **0** | A governed chat agent (your *Research Copilot*) | Agents |
| **1** | **Search** the live literature, with citations | Web Search |
| **2** | **Ground** answers in your own documents | File Search / RAG |
| **3** | **Compute** real statistics & charts on data | Code Interpreter |
| **4** | **Act** by calling tools / services | Function calling · MCP |
| **5** | Take it home — Responsible AI & next steps | — |

## Agenda (3 hours)

| Time | Segment | Lab |
|------|---------|-----|
| 0:00 – 0:20 | Welcome + your first agent | [Lab 0](./labs/lab-00-hello-research-copilot.md) |
| 0:20 – 0:55 | Search the literature | [Lab 1](./labs/lab-01-search-the-literature.md) |
| 0:55 – 1:35 | Ground on your papers | [Lab 2](./labs/lab-02-ground-on-your-papers.md) |
| 1:35 – 1:45 | ☕ Break | — |
| 1:45 – 2:25 | Analyse the data | [Lab 3](./labs/lab-03-analyse-the-data.md) |
| 2:25 – 2:50 | Add a tool | [Lab 4](./labs/lab-04-add-a-tool.md) |
| 2:50 – 3:00 | Take it home | [Lab 5](./labs/lab-05-take-it-home.md) |

## Two rails — follow either, switch anytime

- **🟢 Explore (portal)** — *everyone.* Point-and-click in the Foundry portal. No install, no code.
- **🔵 Build (SDK)** — *optional, for the code-curious.* The same agent in ~10 lines of Python.

Each lab has both. Not a coder? Stay on 🟢 the whole way and you'll still build everything.

---

## Get started

> **New here? Grab the one-page [QUICKSTART.md](./QUICKSTART.md)** — both rails, the data rule,
> and the four labs at a glance.
>
> **Facilitator?** Provision the shared project + grant participant access with the
> **[SETUP.md](./SETUP.md)** runbook (Basic Foundry account, model deployments, and least-privilege
> **Foundry User** RBAC).

### 🟢 Explore rail
1. Open the **shared workshop project** in the Foundry portal (link from your facilitator).
2. Go to **[Lab 0](./labs/lab-00-hello-research-copilot.md)** and follow the green steps.

### 🔵 Build rail
```bash
cd assets
az login                         # auth (DefaultAzureCredential)
copy .env.example .env           # fill FOUNDRY_PROJECT_ENDPOINT + your INITIALS
pip install -r requirements.txt
python lab01_websearch.py        # first agent with web search
```
Full SDK setup & troubleshooting: **[assets/README.md](./assets/README.md)**.

## Repo layout
```
research-supercharged-workshop/
├── README.md                  ← you are here
├── QUICKSTART.md              one-page participant handout (both rails)
├── SETUP.md                   facilitator setup & RBAC runbook (provision the shared project)
├── workshop-plan.md           design rationale & run-of-show
├── facilitator-guide.md       minute-by-minute facilitator script
├── slides-outline.md          deck skeleton (~40 slides) for the session
├── labs/                      the 6 hands-on labs (start at Lab 0)
├── prompts/demo-prompts.json  canned prompts the scripts use
└── assets/                    Build (SDK) rail
    ├── README.md              SDK setup + how to run
    ├── requirements.txt · .env.example
    ├── common/research_common.py   shared helper (all SDK calls live here)
    ├── lab01_websearch.py … lab04_tool.py
    ├── corpus/                ← drop your own unclassified docs (Lab 2)
    │   └── STARTER-CORPUS.md   curated open-access pack for Lab 2
    └── data/sample_experiments.csv   synthetic dataset (Lab 3)
```

## Tech stack
Built on the **current Microsoft Foundry agents API** — `azure-ai-projects` **2.x**
(`create_version` + the Responses API) with the OpenAI-compatible client. **Not** the classic
Assistants / `azure-ai-agents` API. All starter code is verified against `azure-ai-projects`
**2.2.0** / `openai` **2.43.0** (Python 3.10+).

> **Inspiration:** the demo flow follows the modular structure of the
> [`microsoft-foundry/Foundry-Agent-Lab`](https://github.com/microsoft-foundry/Foundry-Agent-Lab)
> (hello → web search → RAG → code → MCP), re-themed for research and rebuilt on the current API.
