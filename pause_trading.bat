@echo off
rem FUTURESCOUT AI: kill switch ON. No real trade can run until resume_trading.bat. The loops keep running.
cd /d "%~dp0backend"
"..\.venv\Scripts\python.exe" scripts\fund_trade.py stop
pause
