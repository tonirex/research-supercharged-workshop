# Screenshots for Lab 4 (Portal Walkthrough)

These images are referenced by [`../../lab-04-portal.md`](../../lab-04-portal.md), captured from the
Foundry portal ([ai.azure.com](https://ai.azure.com)). The navigation shots (steps 1–2) keep the
**left navigation** visible — because "go to **Tools** on the left" *is* the workaround — while the
agent/chat shots (steps 3–6) are cropped to the content pane.

| File | Step | What it shows |
|------|------|---------------|
| `01-tools-list.png` | 1 | The **Tools** area (left nav) listing **`research-tools`** typed as **Model Context Protocol (MCP)** — the one shared server an admin pre-registered. **Connect a tool** is greyed out for a Foundry User. |
| `02-use-in-agent.png` | 2 | The **`research-tools`** detail page with **Use in an agent** open, listing recent agents (`rc-ac`, …). Shows the remote **`…/mcp`** endpoint and **Unauthenticated** access. |
| `03-tool-attached.png` | 3 | The agent build page **Tools** section with **`research-tools`** (and its `…/mcp` endpoint) attached below **Web search** — tools stack up across labs. |
| `04-approval-prompt.png` | 4 | The human-in-the-loop **approval prompt**: `convert_units({ value: 1.8, from_unit: "eV", to_unit: "J" })` with **Approve** (Approve once / Always approve this tool / Always approve all tools) and **Deny**. |
| `05-convert-result.png` | 5 | **Request has been approved** and the computed answer **`1.8 eV = 2.8839179412 × 10⁻¹⁹ J`** — the tool's exact result, not a guess. |
| `06-arxiv-result.png` | 6 | An approved **`search_arxiv`** call summarising **real, live arXiv papers with links** — and honestly flagging a tangential hit. |
| `blocked-01-select-tool.png` | — | *(Reference for the "Note on the main lab".)* The **Tools → Add → Custom** dialog where the main lab sends you: the **Model Context Protocol (MCP)** tile alongside OpenAPI and A2A. |
| `blocked-02-connect-disabled.png` | — | *(Reference for the "Note on the main lab".)* A fully valid **Add MCP tool** config (URL + Unauthenticated) with the **Connect** button **greyed out** — the Foundry Owner gate that blocks participants from self-adding the server. |

> Capture tip: for the **Tools list** and **Use in an agent** shots, screenshot with the left nav in
> frame so the navigation path is obvious. For the chat (steps 4–6), screenshot the **Chat** panel so
> the approval prompt and grounded result fill the frame. The two `blocked-*` images document *why*
> the shared-connection workaround exists — they're not part of the numbered participant flow.
