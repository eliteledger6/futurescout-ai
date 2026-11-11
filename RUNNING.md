# Running FUTURESCOUT AI day to day

Everything is double-click. The files are in the main folder `D:\FUTURESCOUT AI`.

## The three parts

| Part | Where it runs | You start it? |
|---|---|---|
| **Website** https://futurescout-ai.vercel.app (and its API on Render) | in the cloud, always on | no, it runs by itself |
| **Report agent**: Agent Market hires, topic proposals, AI reviewer, research, its own reports, the daily radar, NEAR seals, paper funds, publishing to the website | the cloud server since 2026-11-11 (service `futurescout-agent`) | no; on this computer instead: `start_everything.bat` |
| **Trading agent**: buys reports, trades inside your limits, stakes the report agent's earnings | the cloud server since 2026-11-11 (service `futurescout-trader`) | no; on this computer instead: `start_everything.bat` |

Never run an agent in both places at once: two trading agents could pay or trade twice. After you push new code, the
server needs `sudo -u futurescout git -C /home/futurescout/futurescout pull --rebase && systemctl restart futurescout-agent && systemctl try-restart futurescout-trader`
(see `deploy/VPS.md`).

## Every day

| I want to... | Double-click |
|---|---|
| Start everything | `start_everything.bat` (two windows open: report agent, trading agent; leave them open) |
| See what happened | `status.bat` (read-only) |
| Check that everything is set up | `check_setup.bat` (read-only: keys present, data, connections; never shows a key) |
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
| The report agent starts, and then once a day | every paper fund is updated: topics without a fund get one, funds with a newer report or a due weekly review decide again, the rest are revalued at the latest closes; then the website is updated |
| A trade, a report purchase or a stake happens | the website is updated a few minutes later |

## What only you do (on purpose)

- Add money: NEAR to the trading account's near.com balance (for trades and reports).
- Change limits or switches: `backend\config\funds.yaml` (budget caps, auto-approve, selling, the report budget share).
- Keys and tokens: `.env` (never in a chat or a screenshot).
- Withdraw NEAR Agent Market earnings: on market.near.ai.
- The radar refreshes by itself: the report agent recounts it once a day in the background (over an hour at the patent
  office's pace) and publishes it. The setting is `agent_market.radar_refresh_hours` in `backend/config/funds.yaml` (0 = off).
- Reports the agent writes by itself: each of the radar's top 5 topics always has a report from the last 7 days, and
  every report sold on the report market pays for one more (the next topic on the radar below the top 5). At most 2 a
  day, about $0.35-0.45 each. Settings: `agent_market.auto_top_n`, `auto_fresh_days`, `auto_runs_per_day` (0 = off). The
  record is `backend/runs/auto_reports.json`.
- NEAR Agent Market fees ($3 a hire; test hires pay nothing): once the buyer accepts, the fee is recorded in
  `backend/runs/agent_market/income.json` and joins the same split as report sales: 70% staked, 30% kept. The fee sits
  in the agent's marketplace balance until you withdraw it; the 70% is staked once that NEAR is in the report agent's wallet.
- New radar topics: when the report agent has no job, its Science agent (the same model as in a research run) reads
  5 recent papers once an hour and may add ONE new topic, only if paper counts confirm it is growing; at most 3 a day.
  Settings: `agent_market.topic_scout_hours`, `topic_scout_papers`, `topic_scout_max_per_day` (0 hours = off). What it
  read and decided is in `backend/runs/topic_scout.json`. Cost: about $0.05 of NEAR AI credit a day.
- To regenerate the radar by hand: `backend` folder, `..\.venv\Scripts\python.exe scripts\run_radar.py`, then `update_website.bat`.
- Nothing else needs a manual run: reports, seals, paper funds, report purchases, trades, staking and website updates all
  happen inside the two agents started by `start_everything.bat`.

## Costs while it runs

- Research: about $0.40-1.00 per new report (NEAR AI models, X reads); at most 5 proposal runs and 3 Agent Market runs a day.
- Seals: about 0.013 NEAR per report, from the report agent's wallet (keep about 1 NEAR there). Only reports are sealed; paper-fund decisions and trade records are not, unless `SEAL_FUND_DECISIONS=true` or `SEAL_TRADES=true` is set in `.env`.
- Trading agent: model calls only when something triggers it; reports cost $2-3 each, at most 30% of the fund.

## If something looks wrong

- A window shows an error and restarts: that is fine; it tries again by itself. If it repeats, send the last lines to Claude.
- The website shows old data: run `update_website.bat`; on Render, *Manual Deploy -> Deploy latest commit*.
- Stock trades fail ("no quote"): NEAR Intents is not quoting tokenized stocks; nothing is lost, the agent tries again next hour.
- After you change code or `.env`: close both agent windows and start `start_everything.bat` again.
- Before you push code yourself: `git pull --rebase` first (the agents push website data by themselves).

To run the agents in the cloud instead of this computer, see `deploy/VPS.md`.
