#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install --no-deps kaggle-environments==1.32.7
if [[ "${1:-}" == "--distributed" ]]; then
  .venv/bin/python -m pip install -r requirements-ray.lock
fi
.venv/bin/python -c 'from arena.engine import fingerprint; print(fingerprint())'
