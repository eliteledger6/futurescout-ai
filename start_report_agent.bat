@echo off
rem FUTURESCOUT AI: start the report agent and keep it running.
rem It takes NEAR Agent Market hires, collects topic proposals from the website, lets the AI reviewer screen them,
rem researches approved topics, seals them on NEAR and publishes new reports to the hosted site (git push).
rem Double-click this file, or put a shortcut to it in the Windows Startup folder. Close the window (or Ctrl+C) to stop.
rem It never trades: the trading agent is a separate loop (scripts\fund_trade.py watch) that the owner starts by hand.
title FUTURESCOUT report agent
cd /d "%~dp0backend"
:loop
echo [%date% %time%] starting the report agent
"..\.venv\Scripts\python.exe" scripts\market_agent.py --publish
echo [%date% %time%] the report agent stopped (exit code %errorlevel%); starting again in 30 seconds. Close this window to stop for good.
timeout /t 30 /nobreak >nul
goto loop
