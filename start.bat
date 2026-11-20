@echo off
cd /d "%~dp0"
where node >nul 2>nul
if %errorlevel%==0 (
    start "" "http://localhost:8000/"
    node server.mjs
) else (
    start "" "http://localhost:8000/"
    python -m http.server 8000
)
