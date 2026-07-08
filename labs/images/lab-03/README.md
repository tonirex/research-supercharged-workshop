# Screenshots for Lab 3 (Portal Walkthrough)

These images are referenced by [`../../lab-03-portal.md`](../../lab-03-portal.md). Each was captured
from the **main content pane** of the Foundry portal ([ai.azure.com](https://ai.azure.com)) with the
browser chrome and left navigation cropped out.

| File | Step | What it shows |
|------|------|---------------|
| `01-add-code-interpreter.png` | 1 | The **Tools → Add** menu open, toggling **Code interpreter** on below the already-enabled **Web search** — tools stack up across labs. |
| `02-upload-csv.png` | 2 | The **Code interpreter → Upload files** dialog with **`sample_experiments.csv`** at **Success**, and the supported-types tooltip listing `.csv`, `.xlsx`, and more. This is how a CSV gets in — **not** the chat composer. |
| `03-code-and-run.png` | 3 | The chat showing **generated Python** running in the sandbox: `pandas.read_csv`, then `df.head()`, `df.columns`, `df.shape`, `df.dtypes`. |
| `04-analysis-summary.png` | 4 | The computed answer: energy density is **improving** (+90.5 %), **trial 12 (`S012`)** flagged, a **Download the energy density plot** link (the chart is a downloadable file, not inline), and a **Dataset description**. |
| `05-outlier-flagged.png` | 5 | The **Row that breaks the upward trend** section: **trial 12 / `S012`** at **120.4 Wh/kg**, between neighbours at **214.9** and **229.6** — a contextual outlier ~**101.85 Wh/kg** below local expectation. |

> Capture tip: to reproduce these crops, screenshot the portal's main content region (the `<main>`
> element) for the tool-config shots (steps 1). For the **Upload files** dialog in step 2, screenshot
> just the modal so it reads as a tight crop; for the chat in steps 3–5, screenshot the **Chat** panel so
> the code and reply fill the frame. Note: in the current portal the Code Interpreter chart is delivered
> via a **download link**, not rendered inline, so there is no separate chart screenshot.
