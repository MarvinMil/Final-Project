#!/bin/bash
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
source .venv/bin/activate
python -m pip install --upgrade pip wheel >/dev/null 2>&1
pip install -r requirements.txt
python app.py
