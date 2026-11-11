@echo off
rem FUTURESCOUT AI: start the trading agent and keep it running (restarts itself if it stops).
rem It checks every 60 minutes: wakes on a new report, a sharp price move or its daily review; buys reports from the
rem report agent, trades tokenized stocks inside your limits (backend\config\funds.yaml) and stakes the report agent's
rem earnings with NEAR AI. Real money: run it in ONE place only (this computer OR the cloud server, never both).
rem Pause trading without closing this window: pause_trading.bat (resume: resume_trading.bat).
title FUTURESCOUT trading agent
cd /d "%~dp0backend"
:loop
echo [%date% %time%] starting the trading agent
"..\.venv\Scripts\python.exe" scripts\fund_trade.py watch --publish
echo [%date% %time%] the trading agent stopped (exit code %errorlevel%); starting again in 60 seconds. Close this window to stop for good.
timeout /t 60 /nobreak >nul
goto loop
