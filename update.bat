@echo off
TITLE Shortslip Lab Updater
echo ===================================================
echo   Checking GitHub for updates (Shortslip_Lab)...
echo ===================================================
echo.

python -c "import os, hashlib, urllib.request, time; repo='basilalfarooqui-cmyk/Shortslip_Lab'; branch='main'; files=['app.py','clipping.py','reels.py','renderer.py','scheduler.py','youtube_auth.py','requirements.txt','start.bat','templates/index.html']; os.makedirs('templates', exist_ok=True); updated=0; [print(f'Checking {f}...') or (lambda url: (lambda rem: (lambda r_hash, l_hash: (open(f, 'wb').write(rem) and print(f'  -> [UPDATED] {f}') or globals().update(updated=updated+1)) if r_hash != l_hash else print(f'  -> [ALREADY UP TO DATE] {f}'))(hashlib.sha256(rem).hexdigest(), hashlib.sha256(open(f, 'rb').read()).hexdigest() if os.path.exists(f) else ''))(urllib.request.urlopen(urllib.request.Request(url, headers={'Cache-Control': 'no-cache', 'User-Agent': 'Mozilla/5.0'})).read()))(f'https://raw.githubusercontent.com/{repo}/{branch}/{f}?t={int(time.time())}') for f in files]; print('\n==================================================='); print(f'Result: {updated} file(s) updated!' if updated > 0 else 'Result: Everything is already up to date!'); print('==================================================='); exit(2 if updated > 0 else 0)"

if "%ERRORLEVEL%"=="2" (
    echo.
    echo [INFO] Installing/updating Python packages from requirements.txt...
    python -m pip install --upgrade -r requirements.txt --no-warn-script-location
)

echo.
pause
