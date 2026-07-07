# Screenshots for Lab 1 (Portal Walkthrough)

These images are referenced by [`../../lab-01-portal.md`](../../lab-01-portal.md). Each was captured
from the **main content pane** of the Foundry portal ([ai.azure.com](https://ai.azure.com)) with the
browser chrome and left navigation cropped out.

| File | Step | What it shows |
|------|------|---------------|
| `01-web-search-dialog.png` | 1 | The **Add/Edit the Web Search Tool** dialog with **Search type = "Search the web with Bing Search"** selected (not Bing Custom Search). |
| `02-grounded-answer.png` | 2 | A grounded reply: a structured **top-3** with **inline numbered citations**, the Web Search tool attached in the left panel, and a **Web search** badge under the answer. |
| `03-inspect-citations.png` | 3 | The **expanded source list** — each numbered citation as a clickable source card (news-science, industry analysis, university), all recent. |
| `04-web-search-off.png` | 4 | The **A/B contrast**: with Web Search **removed** (empty Tools panel), the same question is capped at the training cutoff, cites from memory with "please verify" hedges, and shows **no** source cards or Web search badge. |

> Capture tip: to reproduce these crops, screenshot the portal's main content region (the `<main>`
> element) rather than the full window, so the top bar and left nav are excluded. For the dialog in
> step 1, screenshot just the modal so it reads as a tight, focused crop.
