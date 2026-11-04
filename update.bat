@echo off
TITLE Shortslip Lab Updater
echo ===================================================
echo   Checking GitHub for updates (Shortslip_Lab)...
echo ===================================================
echo.

:: Backup local schedule state so your booked slots are never lost
if exist "schedule_tracker.json" (
    copy /Y "schedule_tracker.json" "schedule_tracker.json.bak" >nul
)

:: Method 1: If this folder is a Git repository, use git pull
if exist ".git" (
    git fetch origin main
    for /f "delims=" %%i in ('git rev-list HEAD...origin/main --count') do set DIFF=%%i
    if "%DIFF%"=="0" (
        echo [OK] Everything is already up to date!
    ) else (
        echo [UPDATE] Found new changes on GitHub. Updating files...
        git reset --hard origin/main
        if exist "schedule_tracker.json.bak" (
            copy /Y "schedule_tracker.json.bak" "schedule_tracker.json" >nul
        )
        echo.
        echo [INFO] Updating Python libraries...
        python -m pip install --upgrade -r requirements.txt --no-warn-script-location
        echo.
        echo [SUCCESS] All files updated to the latest GitHub version!
    )
    if exist "schedule_tracker.json.bak" del "schedule_tracker.json.bak"
    echo.
    pause
    exit /b
)

:: Method 2: If downloaded as a ZIP (no .git folder), compare raw files via PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$repo = 'basilalfarooqui-cmyk/Shortslip_Lab';" ^
    "$branch = 'main';" ^
    "$files = @('app.py', 'clipping.py', 'reels.py', 'renderer.py', 'scheduler.py', 'youtube_auth.py', 'requirements.txt', 'start.bat', 'templates/index.html');" ^
    "$updatedCount = 0;" ^
    "if (!(Test-Path 'templates')) { New-Item -ItemType Directory -Path 'templates' | Out-Null };" ^
    "foreach ($f in $files) {" ^
    "    $url = \"https://raw.githubusercontent.com/$repo/$branch/$f?t=\" + [DateTimeOffset]::Now.ToUnixTimeSeconds();" ^
    "    try {" ^
    "        $remoteBytes = (Invoke-WebRequest -Uri $url -UseBasicParsing -Headers @{'Cache-Control'='no-cache'}).Content;" ^
    "        if ($remoteBytes -is [string]) { $remoteBytes = [System.Text.Encoding]::UTF8.GetBytes($remoteBytes) }" ^
    "        $remoteHash = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($remoteBytes));" ^
    "        $localHash = '';" ^
    "        if (Test-Path $f) {" ^
    "            $localBytes = [System.IO.File]::ReadAllBytes((Resolve-Path $f));" ^
    "            $localHash = [System.BitConverter]::ToString([System.Security.Cryptography.SHA256]::Create().ComputeHash($localBytes));" ^
    "        }" ^
    "        if ($remoteHash -ne $localHash) {" ^
    "            [System.IO.File]::WriteAllBytes((Join-Path $PWD $f), $remoteBytes);" ^
    "            Write-Host \"[UPDATED] $f\" -ForegroundColor Green;" ^
    "            $updatedCount++;" ^
    "        } else {" ^
    "            Write-Host \"[ALREADY UP TO DATE] $f\" -ForegroundColor DarkGray;" ^
    "        }" ^
    "    } catch {" ^
    "        Write-Host \"[SKIPPED] Could not fetch $f (check if repo is public or file exists)\" -ForegroundColor Yellow;" ^
    "    }" ^
    "}" ^
    "Write-Host '';" ^
    "if ($updatedCount -eq 0) {" ^
    "    Write-Host '==> All files are already up to date! No changes needed.' -ForegroundColor Cyan;" ^
    "} else {" ^
    "    Write-Host \"==> Successfully updated $updatedCount file(s) from GitHub!\" -ForegroundColor Green;" ^
    "    exit 2;" ^
    "}"

:: If files were updated (exit code 2), also refresh requirements.txt packages
if "%ERRORLEVEL%"=="2" (
    echo.
    echo [INFO] Refreshing Python packages from requirements.txt...
    python -m pip install --upgrade -r requirements.txt --no-warn-script-location
)

:: Restore local schedule state
if exist "schedule_tracker.json.bak" (
    copy /Y "schedule_tracker.json.bak" "schedule_tracker.json" >nul
    del "schedule_tracker.json.bak"
)

echo.
pause
