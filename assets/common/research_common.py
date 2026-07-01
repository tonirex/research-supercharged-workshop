"""Research Supercharged — shared helpers for the Build (SDK) rail.

One place that talks to Microsoft Foundry Agent Service (the *current* agents API,
``azure-ai-projects >= 2.0``) so each lab script stays short. Standardises on the
current Foundry flow — the same backend the Foundry **portal** drives, so a
participant's portal agent and an SDK agent are the *same* object:

    project.agents.create_version(definition=PromptAgentDefinition(...))      # define + version
    openai = project.get_openai_client()                                     # OpenAI-compatible client
    openai.responses.create(input=..., extra_body={"agent_reference": ...})  # run, read .output_text

Env (.env or shell):
    FOUNDRY_PROJECT_ENDPOINT   https://<account>.services.ai.azure.com/api/projects/<project>
    FOUNDRY_MODEL_NAME         model deployment name (default: model-router)
    INITIALS                   your initials -> agents named rc-<initials>
Auth: run `az login` first (DefaultAzureCredential).

Data posture (read me): this workshop uses ONLY public / unclassified information.
Do not upload sensitive, classified, or personal data to any agent, vector store,
or code-interpreter session.
"""
from __future__ import annotations

import functools
import json
import os
import pathlib
import re
from dataclasses import dataclass, field

try:  # optional: load a local .env if python-dotenv is installed
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover
    pass

# --------------------------------------------------------------------------- paths
HERE = pathlib.Path(__file__).resolve()
ASSETS = HERE.parents[1]          # .../assets
ROOT = HERE.parents[2]            # repo root
CORPUS = ASSETS / "corpus"        # drop-your-own (unclassified) PDFs / text here
DATA = ASSETS / "data"            # sample datasets for the code-interpreter lab

# --------------------------------------------------------------------------- config
# Accept the current FOUNDRY_* names (official samples) and older names for resilience.
MODEL = os.environ.get("FOUNDRY_MODEL_NAME") or os.environ.get("MODEL_DEPLOYMENT", "model-router")
# Web Search works on the default model-router (verified). Optionally pin a specific Azure
# OpenAI model (e.g. gpt-4.1) as a fallback via FOUNDRY_WEBSEARCH_MODEL.
WEBSEARCH_MODEL = os.environ.get("FOUNDRY_WEBSEARCH_MODEL") or MODEL
INITIALS = os.environ.get("INITIALS", "xx")


def _endpoint() -> str:
    ep = os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or os.environ.get("PROJECT_ENDPOINT")
    if not ep:
        raise RuntimeError(
            "Set FOUNDRY_PROJECT_ENDPOINT in your environment or .env (see .env.example)."
        )
    return ep


def agent_name(suffix: str = "") -> str:
    """Shared-project naming convention: rc-<initials>[-suffix] (avoids collisions in one project)."""
    base = f"rc-{INITIALS}"
    return f"{base}-{suffix}" if suffix else base


# --------------------------------------------------------------------- canned prompts
def _load_json(path: pathlib.Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _prompts() -> dict:
    try:
        return _load_json(ROOT / "prompts" / "demo-prompts.json")["prompts"]
    except Exception:
        return {}


PROMPTS: dict = _prompts()


def text_of(prompt_id: str) -> str:
    """The verbatim user message for a canned demo prompt id (see prompts/demo-prompts.json)."""
    return PROMPTS[prompt_id]["text"]


# The Research Copilot persona — responsible-AI + unclassified-data guardrails baked in.
DEFAULT_INSTRUCTIONS = """\
You are Research Copilot, an assistant that helps a researcher explore a topic faster:
searching public sources, grounding answers in documents the user provides, analysing data,
and summarising findings clearly.

Rules:
- Use ONLY public, unclassified information. Never request, store, or reason over sensitive,
  classified, or personal data. If asked to, decline and explain why.
- Ground your claims. When you use a web result or a provided document, cite it. If you are
  unsure or have no source, say so plainly — never invent citations, numbers, or quotations.
- Be concise and structured: lead with the answer, then the supporting evidence.
- You are a research aid, not an authority. Flag clearly when a human expert should verify.
"""


# --------------------------------------------------------------------- SDK plumbing (current API)
@functools.lru_cache(maxsize=1)
def get_project():
    """Authenticated AIProjectClient for the shared workshop project (cached).

    `allow_preview=True` enables preview surfaces (harmless for the GA features the labs use).
    """
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    try:
        return AIProjectClient(
            endpoint=_endpoint(), credential=DefaultAzureCredential(), allow_preview=True
        )
    except TypeError:  # older 2.x without allow_preview kwarg
        return AIProjectClient(endpoint=_endpoint(), credential=DefaultAzureCredential())


@functools.lru_cache(maxsize=1)
def get_openai():
    """OpenAI-compatible client for conversations + responses (current API)."""
    return get_project().get_openai_client()


def _models():
    """The current agents model classes (azure-ai-projects >= 2.0)."""
    import azure.ai.projects.models as m

    return m


# --------------------------------------------------------------------- agents
def json_text_format(name: str, schema: dict):
    """A `PromptAgentDefinition.text` that pins a JSON schema (optional structured output)."""
    m = _models()
    return m.PromptAgentDefinitionTextOptions(
        format=m.TextResponseFormatJsonSchema(name=name, schema=schema)
    )


def create_agent(name, instructions, tools=None, text_format=None, description=None, model=None):
    """Create (version) a Prompt agent in the shared project; returns the agent version object.

    `model` overrides the default deployment (FOUNDRY_MODEL_NAME / model-router) for this agent.
    All labs (including Web Search) run on model-router; pass `model` only to pin a specific
    deployment as a fallback (e.g. gpt-4.1).
    """
    m = _models()
    kwargs = dict(model=model or MODEL, instructions=instructions)
    if tools:
        kwargs["tools"] = list(tools)
    if text_format is not None:
        kwargs["text"] = text_format
    definition = m.PromptAgentDefinition(**kwargs)
    create_kwargs = dict(agent_name=name, definition=definition)
    if description:
        create_kwargs["description"] = description
    return get_project().agents.create_version(**create_kwargs)


def research_agent(suffix="", instructions=None, tools=None, text_format=None, model=None):
    """Create a Research Copilot agent (named rc-<initials>[-suffix]) with the default persona.

    Pass `model` to override the default deployment — e.g. to pin a specific Azure OpenAI model
    such as gpt-4.1 as a fallback (all labs, including Web Search, work on model-router).
    """
    return create_agent(
        name=agent_name(suffix),
        instructions=instructions or DEFAULT_INSTRUCTIONS,
        tools=tools,
        text_format=text_format,
        model=model,
    )


def agent_reference(agent) -> dict:
    """The `agent_reference` payload that binds a response to an agent (goes in extra_body)."""
    return {"name": agent.name, "type": "agent_reference"}


# --------------------------------------------------------------------- run
def run_response(agent, text: str):
    """Single-turn: send `text` to `agent`, return the full response object (inspect .output)."""
    return get_openai().responses.create(
        input=text,
        extra_body={"agent_reference": agent_reference(agent)},
    )


def run_text(agent, text: str) -> str:
    """Single-turn: send `text` to `agent`, return the assistant's output text.

    Works directly for hosted tools (Web Search, File Search, Code Interpreter) — the
    service runs them server-side, so no client-side tool loop is needed here.
    """
    return run_response(agent, text).output_text


def citations_of(response) -> list:
    """Best-effort: pull cited URLs/titles from a response (Web/File Search), de-duplicated.

    Prefers structured ``url_citation`` annotations. Falls back to markdown ``[title](url)``
    links in the answer text, because the web search tool sometimes inlines citations that
    way instead of emitting annotations.
    """
    cites: list = []
    seen: set = set()

    def _add(title, url):
        key = url or title
        if key and key not in seen:
            seen.add(key)
            cites.append({"title": title, "url": url})

    for item in getattr(response, "output", None) or []:
        for part in getattr(item, "content", None) or []:
            for ann in getattr(part, "annotations", None) or []:
                url = getattr(ann, "url", None)
                title = getattr(ann, "title", None) or getattr(ann, "filename", None)
                if url or title:
                    _add(title, url)
    if not cites:  # fallback: scrape [title](url) markdown links from the answer text
        text = getattr(response, "output_text", "") or ""
        for m in re.finditer(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", text):
            _add(m.group(1), m.group(2))
    return cites


_JSON_RE = re.compile(r"\{.*\}", re.S)


def extract_json(text: str) -> dict:
    """Parse a JSON object from an assistant reply (tolerates stray prose)."""
    try:
        return json.loads(text)
    except Exception:
        match = _JSON_RE.search(text or "")
        if not match:
            raise ValueError(f"No JSON object found in reply: {text!r}")
        return json.loads(match.group(0))


@dataclass
class ToolCall:
    name: str


@dataclass
class Trace:
    tool_calls: list = field(default_factory=list)
    response: object = None


def run_with_trace(agent, text: str, functions=None):
    """Run with a manual function-tool loop and capture which tools fired.

    `functions` maps a FunctionTool name -> a Python callable. Hosted tools (Web/File
    Search, Code Interpreter, or MCP with require_approval="never") run automatically and
    need no handler. Returns (output_text, Trace) where Trace.tool_calls lists the function
    tools the agent invoked.
    """
    functions = functions or {}
    openai = get_openai()
    ref = {"agent_reference": agent_reference(agent)}
    response = openai.responses.create(input=text, extra_body=ref)
    calls: list = []
    for _ in range(6):  # cap the tool-call loop
        fcalls = [it for it in response.output if getattr(it, "type", None) == "function_call"]
        if not fcalls:
            break
        outputs = []
        for it in fcalls:
            calls.append(ToolCall(name=it.name))
            handler = functions.get(it.name)
            try:
                args = json.loads(it.arguments or "{}")
            except Exception:
                args = {}
            result = handler(**args) if handler else {"error": f"no handler for {it.name}"}
            if not isinstance(result, str):
                result = json.dumps(result)
            outputs.append(
                {"type": "function_call_output", "call_id": it.call_id, "output": result}
            )
        response = openai.responses.create(
            input=outputs, previous_response_id=response.id, extra_body=ref
        )
    return response.output_text, Trace(tool_calls=calls, response=response)


# --------------------------------------------------------------------- tools (current API)
def web_search_tool(search_context_size: str = "medium"):
    """A hosted WebSearchTool — grounds answers on live public web pages. No connection needed.

    `search_context_size`: "low" | "medium" | "high" (how much context to retrieve).
    """
    return _models().WebSearchTool(search_context_size=search_context_size)


def file_search_tool(vector_store_id):
    """A FileSearchTool bound to one vector store (pass directly in `tools=[...]`)."""
    return _models().FileSearchTool(vector_store_ids=[vector_store_id])


def code_interpreter_tool(container=None):
    """A hosted CodeInterpreterTool — runs Python to analyse uploaded data and make charts."""
    m = _models()
    return m.CodeInterpreterTool(container=container) if container else m.CodeInterpreterTool()


def function_tool(name, description, parameters, strict=True):
    """A FunctionTool the model can call; you execute it in run_with_trace's `functions`."""
    return _models().FunctionTool(
        name=name, description=description, parameters=parameters, strict=strict
    )


def mcp_tool(server_label, server_url, require_approval="never", allowed_tools=None):
    """An MCPTool the agent can call (Lab 4 stretch). `require_approval` is "never" | "always"."""
    m = _models()
    kwargs = dict(server_label=server_label, server_url=server_url, require_approval=require_approval)
    if allowed_tools:
        kwargs["allowed_tools"] = allowed_tools
    return m.MCPTool(**kwargs)


# --------------------------------------------------------------------- file search (RAG)
def build_vector_store(folder=None, name=None) -> str:
    """Upload every file under `folder` into a new vector store; return its id.

    Defaults to assets/corpus (drop your own unclassified PDFs/text there).
    Uses the OpenAI-compatible client (current API): openai.vector_stores.*
    """
    openai = get_openai()
    path = pathlib.Path(folder) if folder else CORPUS
    if not path.is_absolute() and not path.exists():
        path = CORPUS / str(folder)
    skip = {"readme.md", "starter-corpus.md"}  # meta-docs in the corpus folder, not research content
    files = sorted(
        p for p in path.rglob("*")
        if p.is_file() and not p.name.startswith(".") and p.name.lower() not in skip
    )
    if not files:
        raise RuntimeError(
            f"No files to index under {path}. Add a few public/unclassified docs to assets/corpus first."
        )
    vs = openai.vector_stores.create(name=name or agent_name("corpus"))
    for fp in files:
        with open(fp, "rb") as fh:
            openai.vector_stores.files.upload_and_poll(vector_store_id=vs.id, file=fh)
    return vs.id


def upload_file(path):
    """Upload a single file (e.g. a CSV for code interpreter); return the file id."""
    with open(path, "rb") as fh:
        return get_openai().files.create(file=fh, purpose="assistants").id


def delete_vector_store(vector_store_id) -> None:
    """Best-effort delete of a vector store created during a lab (keeps the shared project tidy)."""
    if not vector_store_id:
        return
    try:
        get_openai().vector_stores.delete(vector_store_id)
    except Exception:
        pass


# --------------------------------------------------------------------- housekeeping
def cleanup(*agents):
    """Best-effort delete of the agent versions created during a lab run."""
    api = get_project().agents
    for a in agents:
        if a is None:
            continue
        try:
            api.delete_version(agent_name=a.name, agent_version=a.version)
        except Exception:
            pass
