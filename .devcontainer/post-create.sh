#!/usr/bin/env bash
# Devcontainer bootstrap for the Research Supercharged Build (SDK) rail.
# Installs the Python dependencies and seeds a local .env so participants can start fast.
set -euo pipefail

echo "==> Upgrading pip / setuptools / wheel"
python -m pip install --upgrade pip setuptools wheel

echo "==> Installing Build-rail dependencies (assets/requirements.txt)"
pip install --prefer-binary -r assets/requirements.txt

if [ ! -f assets/.env ]; then
  cp assets/.env.example assets/.env
  echo "==> Created assets/.env from .env.example — fill in FOUNDRY_PROJECT_ENDPOINT and INITIALS."
else
  echo "==> assets/.env already exists — leaving it as-is."
fi

echo "==> Fetching open-access starter corpus for Lab 2 (git-ignored, local only)"
bash assets/corpus/fetch-starter-corpus.sh || echo "   (skipped — you can re-run assets/corpus/fetch-starter-corpus.sh later, or add your own docs)"

cat <<'EOF'

============================================================
 Build (SDK) rail ready. Next steps:
   1) az login --use-device-code
   2) Edit assets/.env   (FOUNDRY_PROJECT_ENDPOINT + INITIALS)
   3) cd assets
   4) python lab01_websearch.py   (then lab02 / lab03 / lab04)

 Data rule: PUBLIC / UNCLASSIFIED material only.
============================================================
EOF
