@echo off
rem FUTURESCOUT AI: what the agents have done and the state of the money. Read-only: nothing is sent or signed.
title FUTURESCOUT status
cd /d "%~dp0backend"
echo ===== Report agent: Agent Market jobs and topic proposals =====
"..\.venv\Scripts\python.exe" scripts\market_agent.py --status
echo.
echo ===== Trading agent: switches, limits, holdings =====
"..\.venv\Scripts\python.exe" scripts\fund_trade.py status
echo.
echo ===== Agent economy: reports bought, staking =====
"..\.venv\Scripts\python.exe" scripts\fund_trade.py economy status
echo.
pause
