@echo off
rem FUTURESCOUT AI: kill switch OFF. Real trades can run again, inside the limits in backend\config\funds.yaml.
cd /d "%~dp0backend"
"..\.venv\Scripts\python.exe" scripts\fund_trade.py start
pause
