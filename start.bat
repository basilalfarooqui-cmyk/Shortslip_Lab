@echo off
TITLE Unified Viral Studio
echo [INFO] Starting Unified Viral Studio...
python -m pip install -r requirements.txt --quiet
echo [INFO] Launching Flask server...
start python app.py
timeout /t 2 >nul
echo [INFO] Opening browser interface...
start http://127.0.0.1:5000
exit
