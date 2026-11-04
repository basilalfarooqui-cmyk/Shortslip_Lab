@echo off
TITLE Unified Viral Studio
echo [INFO] Updating yt-dlp and dependencies...
python -m pip install --upgrade -r requirements.txt --no-warn-script-location
echo [INFO] Launching Flask server...
start python app.py
timeout /t 2 >nul
echo [INFO] Opening browser interface...
start http://127.0.0.1:5000
exit
