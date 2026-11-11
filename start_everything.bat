@echo off
rem FUTURESCOUT AI: start everything that runs on this computer, each in its own window.
rem   1. The report agent: Agent Market hires, topic proposals, AI reviewer, research, NEAR seals, paper funds, publishing.
rem   2. The trading agent: buys reports, trades inside your limits (funds.yaml), stakes the report agent's earnings.
rem Each window restarts its agent if it ever stops. Close a window to stop that agent.
rem The website (Vercel + Render) runs by itself; nothing to start for it.
rem Put a shortcut to this file in the Startup folder (Win+R, shell:startup) to start everything with Windows.
title FUTURESCOUT AI
cd /d "%~dp0"
echo Starting the report agent and the trading agent in two new windows...
start "FUTURESCOUT report agent" cmd /k call "%~dp0start_report_agent.bat"
start "FUTURESCOUT trading agent" cmd /k call "%~dp0start_trading_agent.bat"
echo Done. Check on them any time with status.bat. Pause trading with pause_trading.bat.
timeout /t 8 >nul
