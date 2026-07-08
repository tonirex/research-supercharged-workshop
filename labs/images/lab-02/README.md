# Screenshots for Lab 2 (Portal Walkthrough)

These images are referenced by [`../../lab-02-portal.md`](../../lab-02-portal.md). Each was captured
from the **main content pane** of the Foundry portal ([ai.azure.com](https://ai.azure.com)) with the
browser chrome and left navigation cropped out.

| File | Step | What it shows |
|------|------|---------------|
| `01-switch-model-gpt-5.4.png` | 1 | The **Model** dropdown open with **`gpt-5.4`** selected (check mark) among the project deployments, and the **Upload files** button under **Tools** now **enabled** (it is greyed out on `model-router`). |
| `02-attach-files-index-name.png` | 2 | The **Attach files** dialog: **Create a new index**, the **Vector index name** renamed to **`ac-papers`**, and five open-access PDFs each showing **Success**, so **Attach** is enabled. |
| `03-file-search-indexed.png` | 3 | The **Tools** panel after attaching: **File search** listing the **`ac-papers`** vector store (size + `vs_…` ID) alongside the **Web search** tool from Lab 1. |
| `04-grounded-answer.png` | 4 | A **grounded reply** organised per source, with the exact file name (`gpt3-few-shot-learners.pdf`) in the section heading and an inline **citation chip** `[1]`. |
| `05-honesty-decline.png` | 5 | The **honesty test**: asked about GPT-4 (not in the corpus), the agent states it is **not stated** in the documents and points to what they *do* cover (GPT-3) with citations. |

> Capture tip: to reproduce these crops, screenshot the portal's main content region (the `<main>`
> element) rather than the full window, so the top bar and left nav are excluded. For the **Attach
> files** dialog in step 2, screenshot just the modal so it reads as a tight, focused crop; for the
> chat answers in steps 4–5, screenshot the **Chat** panel so the reply and its citations fill the frame.
