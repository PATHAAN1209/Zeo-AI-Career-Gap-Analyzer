@echo off
title SkillGraph Platform
cd /d "%~dp0backend"
echo ============================================================
echo   SKILLGRAPH PLATFORM
echo   Scan your skills. Engineer your future.
echo ============================================================
echo.
echo [INFO] Starting SkillGraph Web Server on http://127.0.0.1:8000
echo [INFO] Hosting 250 Career Roles + Resume AI Scanner
echo.
echo Website URL: http://127.0.0.1:8000/
echo.
python -m uvicorn main:app --host 127.0.0.1 --port 8000
pause
