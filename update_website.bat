@echo off
rem FUTURESCOUT AI: put the newest data (reports, funds, trading record, radar) on the hosted website now.
rem The agents already do this by themselves after a new report or trade; use this after you ran something by hand.
cd /d "%~dp0"
git pull --rebase --autostash
cd backend
"..\.venv\Scripts\python.exe" scripts\export_site.py
cd ..
git add backend/site_data
git commit -m "Site data update"
git push
echo If it said "nothing to commit", the website was already up to date.
pause
