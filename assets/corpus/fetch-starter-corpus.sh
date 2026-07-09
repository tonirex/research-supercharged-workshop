#!/usr/bin/env bash
# Fetch the open-access starter corpus for Lab 2 (RAG) into this folder.
# These files are downloaded LOCALLY (git-ignored) — we do NOT commit them, because the
# arXiv papers are under arXiv's non-exclusive license (not free to redistribute). The NIST
# doc is US-Gov public domain. Each participant fetches their own copy for the workshop.
#
# Usage:  bash assets/corpus/fetch-starter-corpus.sh
set -euo pipefail
cd "$(dirname "$0")"

# filename|url  (open-access / public-domain sources only)
FILES=(
  "attention-is-all-you-need.pdf|https://arxiv.org/pdf/1706.03762"
  "bert.pdf|https://arxiv.org/pdf/1810.04805"
  "resnet-deep-residual-learning.pdf|https://arxiv.org/pdf/1512.03385"
  "gpt3-few-shot-learners.pdf|https://arxiv.org/pdf/2005.14165"
  "nist-csf-2.0.pdf|https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf"
)

echo "Fetching starter corpus into $(pwd) ..."
for entry in "${FILES[@]}"; do
  name="${entry%%|*}"
  url="${entry##*|}"
  if [ -s "$name" ]; then
    echo "  skip  $name (already present)"
    continue
  fi
  if curl -fsSL --max-time 120 -o "$name" "$url"; then
    echo "  ok    $name ($(wc -c < "$name") bytes)"
  else
    echo "  FAIL  $name — download it manually from $url" >&2
    rm -f "$name"
  fi
done
echo "Done. (These PDFs are git-ignored and stay local.)"
