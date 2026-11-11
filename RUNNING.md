# Running FUTURESCOUT AI day to day

Everything is double-click. The files are in the main folder `D:\FUTURESCOUT AI`.

## The three parts

| Part | Where it runs | You start it? |
|---|---|---|
| **Website** https://futurescout-ai.vercel.app (and its API on Render) | in the cloud, always on | no, it runs by itself |
| **Report agent**: Agent Market hires, topic proposals, AI reviewer, research, NEAR seals, paper funds, publishing to the website | this computer | `start_everything.bat` |
| **Trading agent**: buys reports, trades inside your limits, stakes the report agent's earnings | this computer | `start_everything.bat` |

## Every day

| I want to... | Double-click |
|---|---|
| Start everything | `start_everything.bat` (two windows open: report agent, trading agent; leave them open) |
| See what happened | `status.bat` (read-only) |
| Pause real trading at once | `pause_trading.bat` (the kill switch; the loops keep running) |
| Resume real trading | `resume_trading.bat` |
| Put the newest data on the website now | `update_website.bat` (the agents do this by themselves after a new report or trade) |
| Stop everything | close the two agent windows |

**Start with Windows:** press Win+R, type `shell:startup`, press Enter, and put a shortcut to `start_everything.bat` in the
folder that opens. Keep the laptop plugged in and set *Settings -> System -> Power -> Screen and sleep -> When plugged in,
put my device to sleep after* to **Never**.

## What triggers what (nobody has to click)

| When | What happens |
|---|---|
| A visitor proposes a topic on the website (max 5 a day) | within a minute the report agent collects it; the AI reviewer approves or rejects it with a reason |
| A topic is approved, or someone hires the agent on NEAR Agent Market and no recent report exists | the research team writes the report (5-15 min) -> sealed on NEAR mainnet -> its paper fund is built -> the website is updated (a few minutes later) |
| Someone hires the agent and a report on that topic is less than 7 days old | that report is delivered at once (no new research) |
| Every 60 minutes | the trading agent checks for a new report, a sharp price move or its daily review; if one is found it buys the report and decides to buy, sell or hold, inside your limits |
| The report agent has been paid enough (70% of payments reaches 1 NEAR) | it stakes that NEAR with NEAR AI; the rewards pay for the agents' AI |
| A trade, a report purchase or a stake happens | the website is updated a few minutes later |

## What only you do (on purpose)

- Add money: NEAR to the trading account's near.com balance (for trades and reports).
- Change limits or switches: `backend\config\funds.yaml` (budget caps, auto-approve, selling, the report budget share).
- Keys and tokens: `.env` (never in a chat or a screenshot).
- Withdraw NEAR Agent Market earnings: on market.near.ai.
- Regenerate the radar: `backend` folder, `..\.venv\Scripts\python.exe scripts\run_radar.py`, then `update_website.bat`.

## Costs while it runs

- Research: about $0.40-1.00 per new report (NEAR AI models, X reads); at most 5 proposal runs and 3 Agent Market runs a day.
- Seals: about 0.013 NEAR per report or fund decision, from the report agent's wallet (keep about 1 NEAR there).
- Trading agent: model calls only when something triggers it; reports cost $2-3 each, at most 30% of the fund.

## If something looks wrong

- A window shows an error and restarts: that is fine; it tries again by itself. If it repeats, send the last lines to Claude.
- The website shows old data: run `update_website.bat`; on Render, *Manual Deploy -> Deploy latest commit*.
- Stock trades fail ("no quote"): NEAR Intents is not quoting tokenized stocks; nothing is lost, the agent tries again next hour.
- After you change code or `.env`: close both agent windows and start `start_everything.bat` again.
- Before you push code yourself: `git pull --rebase` first (the agents push website data by themselves).

To run the agents in the cloud instead of this computer, see `deploy/VPS.md`.
