@echo off
rem FUTURESCOUT AI: read-only check that the keys, data and connections the agents need are in place. Never shows a key.
title FUTURESCOUT setup check
cd /d "%~dp0backend"
"..\.venv\Scripts\python.exe" scripts\preflight.py
echo.
pause
