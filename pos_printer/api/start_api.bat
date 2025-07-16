@echo off
echo Starting Custom Printer API...
cd /d "%~dp0"
python -m pip install -r requirements.txt
echo API starting on http://127.0.0.1:8765
python printer_api.py
pause