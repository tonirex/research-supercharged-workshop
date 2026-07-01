# Starter Corpus — open-access pack for Lab 2

A **curated, public / open-access** document set the facilitator hands out so anyone who
didn't bring their own papers can still do **Lab 2 (RAG)**. Spans several research domains
so a mixed DSO room all has something relevant.

> ### ⚠️ Everything here is public by design
> These are open-access / public-domain sources only. This pack exists *precisely* so nobody
> needs to reach for internal material. Keep it that way.

---

## How the facilitator assembles it (day before)
1. Download 6–10 of the items below into a folder.
2. **Verify each link resolves** during the dry-run (URLs drift) and that each opens as a real
   PDF/HTML, not a paywall.
3. Zip as `starter-corpus.zip` and share (USB / network share / download link).
4. Participants unzip into **`assets/corpus/`** (🔵 Build) or upload via **Knowledge** (🟢 Explore).

Aim for **diversity over volume** — 6–10 files across a few domains is ideal for the lab.

### Quick download (verified open-access links)

Grabs a solid **5-file starter set** (4 ML classics + a public cyber framework) into
`assets/corpus/`. Run from the repo root (PowerShell shown — on macOS/Linux use `curl` instead of
`curl.exe`):

```powershell
cd assets/corpus
curl.exe -sSL -o attention-is-all-you-need.pdf     https://arxiv.org/pdf/1706.03762
curl.exe -sSL -o bert.pdf                          https://arxiv.org/pdf/1810.04805
curl.exe -sSL -o resnet-deep-residual-learning.pdf https://arxiv.org/pdf/1512.03385
curl.exe -sSL -o gpt3-few-shot-learners.pdf        https://arxiv.org/pdf/2005.14165
curl.exe -sSL -o nist-csf-2.0.pdf                  https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
```

All sources are arXiv (open access) or NIST (US-Gov public domain). The corpus PDFs are
**git-ignored**, so they stay on your machine and are never committed. Add more from the manifest
below for extra domains.

---

## Manifest

| # | Title | Domain | Source / where to get it | Why it's good for the lab |
|---|-------|--------|--------------------------|---------------------------|
| 1 | *Attention Is All You Need* | ML / AI | arXiv `1706.03762` (PDF) | Famous, self-contained; great for "summarise the method" |
| 2 | *BERT: Pre-training of Deep Bidirectional Transformers* | ML / NLP | arXiv `1810.04805` (PDF) | Pairs with #1 for "compare these two methods" |
| 3 | NIST Cybersecurity Framework (CSF) 2.0 | Cyber / policy | csrc.nist.gov (public-domain PDF) | Structured, factual; good for "what does it recommend?" |
| 4 | NIST Post-Quantum Cryptography overview (FIPS 203/204/205 intro) | Cryptography | csrc.nist.gov (public domain) | Current, technical; tests precise citation |
| 5 | IPCC AR6 *Summary for Policymakers* | Climate / environment | ipcc.ch (public PDF) | Dense facts + figures; good honesty test |
| 6 | An open-access **materials science** review (e.g. a *Nature Communications* or MDPI article) | Materials | doaj.org / the journal (CC-BY PDF) | Ties to the Lab 3 battery/energy theme |
| 7 | An arXiv **physics** review in your area (cond-mat / quant-ph) | Physics | arXiv (PDF) | Lets domain folks ask real questions |
| 8 | A **signal processing / radar** open-access paper or public tech report | Sensing | arXiv `eess.SP` / public report | Relatable for a defence-science audience (still public) |
| 9 | Wikipedia export — pick one topic (e.g. *Kalman filter*) | General reference | en.wikipedia.org → *Download as PDF* | Reliable baseline; easy "is X in the docs?" check |
| 10 | A public **standard / datasheet** (e.g. an IETF RFC, a component datasheet) | Engineering | ietf.org / vendor site | Structured facts; good for precise retrieval |

> Items #6–#8 are intentionally "pick one from this source" — choose current, **CC-licensed /
> open-access** articles close to your room's disciplines during prep. The
> [DOAJ](https://doaj.org) and [arXiv](https://arxiv.org) are reliable open-access starting points.

---

## Suggested demo questions (work across most of the pack)
- *"Using only the uploaded documents, summarise the key findings and methods. Cite the source file for each point."*
- *"Compare the approaches in [doc A] and [doc B]. Where do they agree or differ?"*
- *"Build a table: method · dataset · result · source file, across the corpus."*
- **Honesty check:** *"What do these documents say about [an unrelated topic]?"* → expect a decline.

## Licensing note
Only include materials that are **open access or public domain** and redistributable
(arXiv, NIST/US-Gov public domain, CC-BY journals, IPCC public reports, Wikipedia CC-BY-SA).
When in doubt, link to the source instead of redistributing the file.
