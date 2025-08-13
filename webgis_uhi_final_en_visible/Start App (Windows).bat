@echo off
cd /d %~dp0
if not exist .venv (
  py -3 -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip wheel >nul 2>&1
pip install -r requirements.txt
python app.py
