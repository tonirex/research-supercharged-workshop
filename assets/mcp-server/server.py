"""Research Tools MCP server — the remote tool endpoint for Lab 4.

The admin deploys this to Azure Container Apps (see admin/03-deploy-mcp-server.md) so
that on the day, workshop participants only need to paste one HTTPS URL into their agent:

    Foundry portal  ->  agent  ->  Tools  ->  MCP  ->  server URL = https://<app-fqdn>/mcp

It speaks the MCP **Streamable HTTP** transport (single endpoint, default path ``/mcp``),
which is what Microsoft Foundry's hosted MCP tool connects to.

Tools exposed
-------------
* ``convert_units`` — exact unit conversions in real Python (no hallucinated math). The
  logic is copied verbatim from ``assets/lab04_tool.py`` so the portal (MCP) rail and the
  SDK (function-tool) rail return identical numbers.
* ``search_arxiv``  — live search of the public arXiv preprint API (open access, no key).
  This is the "wow": the agent reaches a real external research service it otherwise
  cannot see.

Design notes
------------
* **Public + unauthenticated by design.** It only serves public data and stateless math,
  so there is nothing to protect and participants can connect with zero setup. Do NOT add
  secrets or private data to this server. (To lock it down later, put it behind APIM / an
  API key and pass headers via the Foundry MCP tool.)
* **Stateless** (``stateless_http=True``) so Azure Container Apps can scale it to more than
  one replica without sticky sessions.
"""
from __future__ import annotations

import os
import urllib.parse
import xml.etree.ElementTree as ET

import httpx
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import PlainTextResponse

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))

mcp = FastMCP(
    "research-tools",
    host=HOST,
    port=PORT,
    stateless_http=True,  # no session affinity -> safe to scale across ACA replicas
)

# ---------------------------------------------------------------- convert_units
# Copied verbatim from assets/lab04_tool.py so the MCP (portal) rail and the
# function-tool (SDK) rail give identical answers for the Lab 4 question.
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


@mcp.tool()
def convert_units(value: float, from_unit: str, to_unit: str) -> dict:
    """Convert a physical quantity between units.

    Supported: eV<->J, nm<->m, angstrom<->m, kPa<->atm, and C<->K.
    Returns ``{"value": <number>, "unit": <str>}`` or ``{"error": <str>}``.
    """
    f, t = str(from_unit).lower().strip(), str(to_unit).lower().strip()
    if (f, t) == ("c", "k"):
        return {"value": value + 273.15, "unit": "K"}
    if (f, t) == ("k", "c"):
        return {"value": value - 273.15, "unit": "C"}
    if (f, t) in _FACTORS:
        return {"value": value * _FACTORS[(f, t)], "unit": to_unit}
    return {"error": f"no conversion from {from_unit} to {to_unit}"}


# ----------------------------------------------------------------- search_arxiv
@mcp.tool()
def search_arxiv(query: str, max_results: int = 5) -> dict:
    """Search the public arXiv preprint API and return the most relevant papers.

    ``query`` is free text, e.g. "solid-state battery electrolytes". Returns a list of
    papers with title, authors, link, and a short summary. Open access, no API key.
    """
    max_results = max(1, min(int(max_results), 10))
    url = (
        "https://export.arxiv.org/api/query?search_query="
        + urllib.parse.quote(f"all:{query}")
        + f"&start=0&max_results={max_results}&sortBy=relevance"
    )
    try:
        resp = httpx.get(
            url,
            timeout=30.0,
            follow_redirects=True,
            headers={"User-Agent": "research-workshop-mcp/1.0"},
        )
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001 - report failure to the agent, don't crash
        return {"error": f"arxiv request failed: {exc}"}

    ns = {"a": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError as exc:
        return {"error": f"could not parse arxiv response: {exc}"}

    papers = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
        summary = (entry.findtext("a:summary", default="", namespaces=ns) or "").strip()
        link = (entry.findtext("a:id", default="", namespaces=ns) or "").strip()
        authors = [
            (a.findtext("a:name", default="", namespaces=ns) or "").strip()
            for a in entry.findall("a:author", ns)
        ]
        papers.append(
            {
                "title": " ".join(title.split()),
                "authors": ", ".join(x for x in authors if x)[:200],
                "link": link,
                "summary": " ".join(summary.split())[:400],
            }
        )
    return {"query": query, "count": len(papers), "papers": papers}


# ------------------------------------------------------------------- health check
@mcp.custom_route("/healthz", methods=["GET"])
async def healthz(_request: Request) -> PlainTextResponse:
    """Cheap liveness probe for ACA / curl (the MCP endpoint itself is /mcp)."""
    return PlainTextResponse("ok")


if __name__ == "__main__":
    # Streamable HTTP transport -> serves the MCP endpoint at http://HOST:PORT/mcp
    mcp.run(transport="streamable-http")
