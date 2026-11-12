# FUTURESCOUT AI

An automated research and trading agent for emerging technology, built on NEAR. A team of AI agents (models on **NEAR AI Cloud**) reads research papers, patents, SEC filings and X posts for more than 50 technology topics (the list grows by itself), argues the other side, and writes a report where every claim has a label and a source. Each report's fingerprint is sealed on **NEAR**. The companies the evidence points to go into a paper fund per topic, and a trading agent buys and sells real tokenized stocks through **NEAR Intents**, inside hard limits written in code.

Research information, not financial advice. The trading agent uses a small, capped real-money budget.

## NEAR HACKATHON submission

| | |
|---|---|
| Built | During NEAR HACKATHON (development window 2026-11-01 to 2026-11-14). The first live runs are from 2026-11-08; the git history starts 2026-11-09, when the folder became a repository. No code from before the announcement. |
| Live demo | Website: https://futurescout-ai.vercel.app (read-only copy of the real data; the API behind it: https://futurescout-ai.onrender.com/api/health). The report agent on NEAR Agent Market: https://market.near.ai/a/futurescout |
| Suggested tracks | `agents` (agents that earn, spend, hire and pay: the trading agent buys reports from the report agent in NEAR, the report agent is hired on NEAR Agent Market and stakes its earnings for AI credits), `business` (an AI-run report business: pricing, sales, treasury split 70/30, limits set by the owner), `swarms` (an agent economy between a research team, a report agent and a trading agent), `defi` (a trading agent settling through NEAR Intents), `security` (spending limits, order verification before signing, kill switch), `privacy` (inference on NEAR AI Cloud; orders signed from the Confidential Intents balance) |
| Demo video | `demo/futurescout_hackathon_demo.mp4` (4:14) is built locally by `demo/make_video.py` (not committed: large binary); the public demo post on X links it. Narration: ElevenLabs voice (free plan, credited in the video) |
| AI assistance | Code written with Claude Code (Anthropic). Third-party libraries are listed at the end |

### The problem

Technology investing mixes verifiable facts, rumours and hype, and "AI picks" rarely show their evidence. FUTURESCOUT AI keeps the evidence and the money decisions connected and checkable: every claim is labelled (verified fact, AI interpretation, forecast, assumption, unverified claim) with a source URL from a real API response; the companies come from patents and papers that name them, never from a hand-made list; and every report, fund decision and trade is fingerprinted on NEAR so it cannot be edited afterwards.

### How NEAR is used (concretely)

| NEAR piece | What it does here | Where |
|---|---|---|
| **NEAR AI Cloud** | Every agent (chief, science, risk, market, X, patent, timing, scout, investment, trading) calls a model from the NEAR AI Cloud catalogue through its OpenAI-compatible API; the trading agent runs on Claude Opus 5.5 there | `backend/config/model_config.yaml`, `backend/app/models/` |
| **NEAR Intents (1Click), mainnet** | Real swaps NEAR ⇄ Ondo tokenized stocks. Dry quotes for every candidate; real orders are signed (NEP-413) from the account's **Confidential Intents** balance, the way near.com trades. The order is verified before signing: exactly one transfer, exactly the approved amount, to exactly the quote's deposit address | `backend/app/fund/live.py`, `signed_exec.py`, `intents_signed.py` |
| **NEAR mainnet (SocialDB `social.near`)** | SHA-256 fingerprints, signed by the report agent `grandbread5023.near` (older seals stay on testnet and still verify) of every report; the dashboard re-checks them on each page load. Paper-fund decisions and trade records were sealed too until 2026-11-11; since then only reports are sealed by default, to save NEAR (`SEAL_FUND_DECISIONS=true` / `SEAL_TRADES=true` switch them back on), and the earlier seals still verify ("unchanged since recorded") | `backend/app/chain/near_record.py` |

### What is real and what is simulated

| Real (run live) | Simulated or limited |
|---|---|
| Multi-agent research on real papers (OpenAlex, arXiv), patents, SEC filings and X posts; 16 topics with full reports | Paper funds (one per topic, fully invested) use pretend money at real closing prices |
| Report, fund and trade fingerprints on NEAR mainnet (older ones on testnet) | Shadow trading: pretend money, real NEAR Intents quotes |
| Real-money trades on NEAR mainnet through NEAR Intents. Current record: one buy of INTCon ($43.83, approved by the agent after every code check). Earlier rounds (three buys, and on 2026-11-10 an automatic sale of GOOGLon followed by a buy) were archived (kept on the owner's machine, not in the repository) when the owner restarted the fund | Real-money budget is capped at $60 in total by the owner. The trading loop runs on the cloud server (hourly checks, a daily review of the holding: "hold" on 2026-11-12); NEAR Intents has had no swap route for the INTCon token since 2026-11-10, so that holding cannot be added to or sold for now |
| Agent economy with real NEAR (state on 2026-11-12): the trading agent bought 6 reports (3.599 NEAR) and 1 daily holding brief (0.1385 NEAR, $0.50) from the report agent, which staked 2.5193 NEAR (70%) with NEAR AI (Staking for Inference) and kept the rest | At these amounts the staking rewards cover only a small part of the AI bill; the second trading agent (funded when the kept pot passes $200) is planned, not built |
| NEAR Agent Market listing, live; two free test hires delivered (topic from the brief, change request read from the job thread; the second by the cloud server in under 8 minutes). A visitor's topic proposal ran end to end on 2026-11-11 (AI reviewer approved "retrieval-augmented generation", researched, sealed on mainnet, published by the agent) | No paid Agent Market job yet. For the demo, reports written from 2026-11-11 are unlocked and marked "Unlocked for demo purposes only" |
| Settlement confirmed by reading the private balance | Stock prices: Alpha Vantage free plan (25 lookups a day), NEAR Intents token prices as a labelled fallback |

### Agent economy: agents pay each other and pay for their own AI

The report agent prices each report at what it cost to make (models and X reads, patent searches, the NEAR seal) plus $1.50, kept between $2 and $3 and paid in NEAR at the live price (owner 2026-11-10). The trading agent may only use reports it has bought, pays with a NEAR transfer that the code reads back from the chain, and spends at most 30% of its fund on reports. The report agent stakes 70% of every payment through NEAR AI Cloud's Staking for Inference, so the staking rewards pay for the agents' model usage; it keeps 30%, and once that pot passes $200 it funds a second trading agent (the next step, not built yet). Commands: `fund_trade.py economy status | price | buy | stake`. Owner switch: `economy.enabled` in `backend/config/funds.yaml`. Honest limit: at these amounts the staking rewards cover only a small part of the real AI bill.

### Report market: any trading bot can buy a report

Reports are paid access only: they are never unlocked on the site without payment (owner 2026-11-10; `economy.embargo_hours: null`; one demo report stays free). Any bot can buy it without an account or a key:

1. `GET /api/market`: the newest scored report per topic, its price in NEAR ($2-3 by cost) and the account to pay (the report agent, NEAR mainnet).
2. Send that much NEAR to the report agent with an ordinary NEAR mainnet transfer.
3. `POST /api/market/buy` with `{"run_id", "tx_hash", "buyer"}`: the API reads the transaction from the chain (final, signed by the buyer, paid to the report agent, at least the price; each transaction redeemed once) and returns the full report and an access token for `/api/runs/{run_id}?access=...`.

Until then `/api/runs/{run_id}` answers `402 Payment Required` with the price and these steps. Owner switches: `economy.market_open`, `economy.embargo_hours`.

### Request a report: Agent Market or a free topic proposal

On the site's **Request a report** page a visitor can hire the report agent on NEAR Agent Market, or propose a topic for free
(at most 5 a day). An AI reviewer screens each proposal (is it a real technology worth a research run?); approved topics are
researched by the agent team, sealed on NEAR and listed on the site, and get their paper fund (which also makes the topic tradable for the trading agent). A proposal is only ever used as a short topic name.

### Hire the report agent on NEAR Agent Market

**Live listing: https://market.near.ai/a/futurescout** ($3 per hire, delivery within 12 hours).

The report agent takes paid jobs on NEAR's Agent Market: a buyer gives a technology topic,
the marketplace holds the payment, and the agent delivers a sealed report (reusing a recent one when it exists, otherwise
running the research team, at most 3 new runs a day). The brief is used only as a short topic, never as instructions.
Run it with `python scripts\market_agent.py`; setup and the listing text are in [AGENT_MARKET.md](AGENT_MARKET.md).
Run live on 2026-11-10: a test hire was picked up, a change request was read from the job thread, and the sealed high bandwidth memory report was delivered. Since 2026-11-11 the agent runs on a cloud server, so it answers around the clock (a second test hire was delivered from there in under 8 minutes).

### Safety limits on the trading agent (enforced in code, not by the model)

- Master switch, kill switch file (`fund_trade.py stop`), a total budget cap, and near.com's $20 minimum per trade.
- Buys only from an allowlist built from the paper funds and price-checked tokenized stocks; sells only of what the fund holds, at most 2 a day.
- Only stocks from reports rated strong or building can be bought; quotes that cost more than 2% are refused. Since 2026-11-11 (owner's decision) there is no fixed confidence minimum and no fixed price band: the agent is shown each report's confidence, the quoted price, the stock's last close and the gap between them, and writes its judgement into the decision record.
- The signed order is checked field by field before signing; a proposal is sent at most once; an unclear result is never retried.
- Selling, re-investing sale money and automatic approval are separate owner-only switches in `backend/config/funds.yaml`.
- Every decision (including "hold") is stored with its reasons and fingerprinted.

### Running it day to day (the owner)

The website runs in the cloud by itself. Since 2026-11-11 the two agents (report agent, trading agent) run on a small
cloud server as two services that restart by themselves ([deploy/VPS.md](deploy/VPS.md)); `start_everything.bat` runs
them on the owner's computer instead (never both places at once). Who triggers what, costs and what stays manual:
[RUNNING.md](RUNNING.md).

What the report agent does without anyone asking (all in `backend/config/funds.yaml` -> `agent_market`):
- recounts the Hot-Topic Radar once a day (papers, patents, SEC filers; no model) and publishes it;
- keeps a report from the last 7 days on each of the radar's top 5 topics, and writes one more report for every report
  sold (the next topic down the ranking); at most 2 such reports a day;
- when it has no job, its Science agent reads 5 recent papers an hour and may add ONE new topic to the radar, only if
  paper counts confirm it is growing (at most 3 a day);
- records the fee of every accepted NEAR Agent Market hire, so it joins the 70% staked / 30% kept split.

### Try it in 10 minutes (no keys needed)

The fastest way is the hosted copy: https://futurescout-ai.vercel.app (the first load can take up to a minute while the free API host wakes up). To run it yourself: the repository ships a snapshot of the real data (`backend/site_data`: the reports, the radar, the paper funds, the trading and agent-economy records), and the API serves it by itself when there is no database and no `backend/runs` folder. Windows PowerShell shown; Python 3.10+ and Node.js LTS. On macOS/Linux use `source .venv/bin/activate` and forward slashes.

```powershell
cd backend
python -m venv .venv; .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest                                  # see: all tests pass (fixtures and mocks, no network, no key)
python scripts\serve.py                           # see: API on http://127.0.0.1:8000 (docs at /docs); http://127.0.0.1:8000/api/health says "data":"site_data"
```

In a second terminal:

```powershell
cd frontend
npm install; npm run build; npm run start         # see: the dashboard on http://localhost:3000
```

Then, in the dashboard:

1. Open **Radar**: see more than 50 topics in 9 sectors ranked by paper and patent growth (the list grows: the Science agent added three on 2026-11-11).
2. Open **Reports** and pick *high bandwidth memory*: see the verdict (score 80, confidence 50%), the companies behind the evidence, and "Unchanged since recorded on NEAR mainnet". Switch to **Full report**: every finding with its label, quote and source; the agent trace with model and cost per agent; the company scout table.
3. Open **Funds & trading** → **Paper funds**: one fully invested pretend-money fund per topic with their reasons, compared with the S&P 500.
4. Open **Trading agent**: the pipeline, the agent's latest decisions, the completed real trade with the agent's own reasoning ("Approved by the agent (all checks passed)"), and the **Agent economy** panel: 3 reports bought in NEAR, 1.31 NEAR staked with NEAR AI, the kept pot.
5. Open **How it works**: the agent network, from the topic reviewer to the trading agent, NEAR AI staking and NEAR Agent Market. Tap an agent to see what it does.
6. Open **Reports → Request a report**: the link to hire the report agent on NEAR Agent Market, and the free topic proposal form (5 a day, screened by an AI reviewer; the list below it shows what happened to earlier proposals). The form is live on the hosted site; in a local copy it says proposals are closed, because nobody collects them there. Text that looks like an instruction is refused at once and uses no slot.
7. Back in the backend terminal: `python scripts\fund_trade.py rules` prints the strategy rules; `python scripts\fund_trade.py holdings` prints what the real-money fund holds; `python scripts\tamper_demo.py --run e5d41d1f-fa56-42ce-bf27-9fccb47298a2` reads the report's fingerprint from NEAR mainnet (free read) and shows MATCH, then MISMATCH after changing one word in memory.

To run new research or trade you need your own keys (see `.env.example` and the full commands below); real trading also needs a funded NEAR mainnet account and is off by default.

## Component status (detailed)


Early development. Only the pieces below exist and are tested. Nothing else is claimed.

| Component | State |
|---|---|
| NEAR AI model router (retry, fallback, token and cost tracking) | Built; tested with a mock client and run live against NEAR AI Cloud (2026-11-08) |
| Citation guard (rejects unsupported "verified" claims) | Built and tested |
| OpenAlex and arXiv clients | Built; tested with fixtures; run live (real papers retrieved) |
| SEC EDGAR client (company annual/quarterly reports, verbatim passages) | Built; tested with fixtures; run live |
| GDELT news-headline client | Built; tested with fixtures. Live calls so far refused by GDELT (HTTP 429) from the developer's network |
| Chief, Science, Risk, Market, X, Patent, Company Scout and Investment agents; LangGraph workflow (parallel agents, one bounded gap-review loop); explainable opportunity score; Markdown report | Built; tested with a mock model, and run live end to end with NEAR AI models (2026-11-08: all seven agents produced output, 0 errors, 100% evidence coverage, about $0.23 per run) |
| PostgreSQL storage of runs, sources, findings, usage (SQLAlchemy + Alembic migrations) | Built; tested on SQLite and checked live on PostgreSQL 18 (save + reload) |
| FastAPI backend (saved runs, full reports, start a run) | Built; tested; run live against the saved PostgreSQL runs. Starting runs from the dashboard is off unless `ENABLE_RUN_API=true` (each run spends NEAR AI credit) |
| Next.js dashboard (`frontend/`) | Built and run locally: browse saved reports (score, themes, labelled findings with sources, research activity, filings checked, costs) |
| X Intelligence agent (read-only; about 130 approved company, standards, press and analyst accounts, most approved by the owner and a few added by the agent under the owner's rules; posts are social signals, never facts) | Built and tested with fixtures; first live run 2026-11-08 |
| Patent agent (Google Patents through SerpApi first, EPO Open Patent Services second; patent counts per year, Patent Acceleration, top applicants) | Built and tested with fixtures; run live through SerpApi (the saved reports carry its counts) |
| Hot-topic radar (`scripts/run_radar.py`, dashboard `/radar`): ranks topics by growth in papers (OpenAlex) and patents (Google Patents), counted by code, no model; small-base topics shown but not ranked; 9 technology sectors (`config/sectors.yaml`), sector tabs on the dashboard | Built, tested, run live on 8 topics (2026-11-08) and 37 topics across 9 sectors (2026-11-09) |
| Topic discovery: the X watch proposes topics from real posts; the paper scout (`scripts/discover_topics.py`, weekly in watch mode) finds fast-growing keywords in recent papers per sector and verifies each with a real per-year count before adding it | Built, tested; first live dry run 2026-11-09 |
| Company discovery: SEC full-text search finds every filer whose reports mention the topic, including small companies not on the configured list; marked "discovered" and read like the others | Built, tested, run live (HBM: 34 companies found) |
| Company fundamentals from SEC XBRL (revenue, growth, R&D intensity, size class by revenue) and 8-K press-release exhibits | Built, tested, run live |
| Paper portfolio (simulation, dashboard `/portfolio`): each sealed report "buys" its top scout candidates with pretend money at the first close after the report date and tracks them against the SOXX ETF; derived from NEAR-fingerprinted reports so it cannot be backdated; no money moves, not advice | Built and tested (2026-11-09); positions recorded live, pricing needs a free Alpha Vantage key |
| Company Scout: every company behind the evidence (patent assignees, paper authors' employers, SEC filers), matched to the SEC ticker file, sized from XBRL, ranked by a transparent "next-runner" heuristic that favours smaller, growing, R&D-heavy names; incumbents listed separately; a forecast label, not a recommendation | Built and tested (2026-11-09); first live run 2026-11-09 |
| Retraction flags (OpenAlex) honoured by the citation guard; X post engagement recorded | Built, tested |
| Price & timing risk (part of the Risk agent): run-up, distance from 50-day average, volatility and drawdown over ~100 trading days for the companies whose filings mention the topic; rule-based level elevated / moderate / subdued. A risk input, never a buy/sell signal | Built and tested with fixtures; needs a free Alpha Vantage key; not yet run live |
| Watch mode (`scripts/watch.py --loop`): scans the approved X accounts every 2 hours, spots rising topics, refreshes the radar, and starts a full research run when a topic is hot and has no fresh report (capped per day); each run is sealed on NEAR; every decision is logged and shown on the dashboard | Built and tested with fakes; first live cycle 2026-11-09 |
| NEAR Protocol record: each report's SHA-256 fingerprint is stored in SocialDB (mainnet `social.near` since 2026-11-10, signed by the report agent; testnet before), and the dashboard re-checks it on the record's own network ("unchanged since recorded") | Built, tested; written live on testnet (2026-11-08) and on mainnet (2026-11-10) |

## Problem

Technology investment research mixes verifiable facts, rumours and hype. FUTURESCOUT AI keeps them apart: every claim carries a label (verified fact, AI interpretation, forecast, assumption, unverified claim), a confidence level and source URLs that come from real API responses, never from a model's memory.

## How NEAR is used (detail)

- All agents call models from the **NEAR AI Cloud** catalogue through its OpenAI-compatible API (`https://cloud-api.near.ai/v1`). Each agent has its own configurable model in `backend/config/model_config.yaml`.
- After each run, the report's SHA-256 fingerprint is stored on **NEAR mainnet** (SocialDB contract `social.near`, signed by the report agent's account when `SEAL_NETWORK=mainnet`; testnet `v1.social08.testnet` otherwise). Each record names its network, and the website re-checks it on that network. Anyone can recompute a report's fingerprint and compare it with the on-chain value, so a report cannot be quietly edited after publication. The research agents never touch a key; real-money trading is a separate, capped part (see the hackathon section above).

## Full commands (with your own keys)

Requires Python 3.10+ (tested on 3.13). Windows PowerShell shown; adapt paths on other systems. Run everything from the `backend` folder.

```powershell
cd "D:\FUTURESCOUT AI\backend"
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
copy ..\.env.example ..\.env      # then edit .env and add your keys

pytest                            # do this: expect all tests to pass (they use fixtures, no network)
python scripts\list_models.py     # see: config vs the live NEAR AI model catalogue
python scripts\demo_science.py --topic "high bandwidth memory" --no-llm   # see: real OpenAlex + arXiv papers
python scripts\demo_market.py --topic "high bandwidth memory" --keywords "HBM" --no-news   # see: real SEC filing passages
python scripts\demo_science.py --topic "high bandwidth memory" --from-year 2023   # see: cited analysis + model cost
python scripts\run_research.py --topic "high bandwidth memory"   # see: full multi-agent report in backend\runs\report_*.md
python scripts\run_radar.py       # see: topics ranked by paper + patent growth (backend\runs\radar.json, dashboard /radar)
# dashboard (two terminals):
python scripts\serve.py           # terminal 1, backend folder: API on http://127.0.0.1:8000 (docs at /docs)
#   terminal 2, frontend folder (needs Node.js LTS): npm install  then  npm run dev
#   see: the dashboard at http://localhost:3000 (saved reports, scores, evidence with sources)
python scripts\watch.py --once          # see: one autonomous cycle (X scan -> radar -> research trigger), logged to runs\watch_state.json
# NEAR testnet seal (needs the testnet account from .env.example):
python scripts\near_record_report.py --latest   # the newest report's fingerprint sealed on the SEAL_NETWORK network
python scripts\near_record_report.py --all --dry-run   # list reports not yet sealed there; drop --dry-run to seal them
python scripts\tamper_demo.py                   # see: a sealed report verifies MATCH; change one word in memory -> MISMATCH (nothing saved)
python scripts\discover_topics.py --dry-run     # see: the paper scout propose new fast-growing topics per sector (nothing added)
# no keys at all? `python scripts\serve.py` + the dashboard still work: with no runs and no database the API serves
# the three real, sealed sample reports and the radar in backend\samples (exported with scripts\export_samples.py)
# optional database (needs PostgreSQL and DATABASE_URL in .env):
python -m alembic upgrade head    # create the tables
python scripts\db_check.py        # see: connection status and saved runs
# (these scripts are in backend\scripts, so run them from the backend folder)
```

Keys (see `.env.example`): `NEAR_AI_API_KEY` from https://cloud.near.ai, `OPENALEX_API_KEY` from a free account at https://openalex.org/settings/api. arXiv and GDELT need no key. `EDGAR_USER_AGENT` must be your name and a real contact email (the SEC requires it; it is sent only to sec.gov). The Market agent checks the companies that the papers and patents point to (no hand-made list).

## Launch it and share it

The dashboard talks to the API through its own origin (`/api/*` is proxied by Next.js to `API_INTERNAL_URL`, default `http://127.0.0.1:8000`), so one address is enough to show the site to other people.

| How | Command / steps | Who can see it |
|---|---|---|
| **On your laptop** | backend: `python scripts\serve.py` · frontend: `npm run dev` → http://localhost:3000 | you |
| **Same Wi-Fi** (phone, a friend next to you) | `python scripts\serve.py --host 0.0.0.0` and `npm run dev -- -H 0.0.0.0`, then open `http://<your-PC-IP>:3000` | people on your network |
| **Temporary public link, nothing to install** | keep both servers running and, in a new terminal, run `ssh -R 80:localhost:3000 nokey@localhost.run` (type `yes` the first time). It prints an `https://….lhr.life` address; share it. Works while that terminal stays open; the address changes each time | anyone with the link |
| **Temporary public link, steadier** | `winget install Cloudflare.cloudflared`, then `cloudflared tunnel --url http://localhost:3000`; it prints an `https://….trycloudflare.com` address that works while the command runs | anyone with the link |
| **One command with Docker** | `docker compose up --build` (reads keys from `.env`; without a database it serves `backend/runs`, or the sample reports when there are none) → http://localhost:3000 | you, or a server you own |
| **Always-on hosting (set up: see HOSTING.md)** | frontend on Vercel (import the repo, root `frontend`, set `API_INTERNAL_URL` to your API's URL); API on Render/Railway/Fly (Python service, start command `python scripts/serve.py --host 0.0.0.0 --port $PORT`, env vars from `.env.example`). Keys live in the host's environment settings, never in the repo | the public |

What to keep private: `.env` (keys, tokens, the proposals secret), your NEAR private keys. Sharing the site shares the reports; it never exposes keys. Watch mode (`scripts\watch.py --loop`) only runs where you start it.

## Layout

```
backend/config/model_config.yaml   model per agent, prices, fallbacks
backend/app/models/                NEAR AI client and router
backend/app/sources/               OpenAlex, arXiv, SEC EDGAR, GDELT clients
backend/app/agents/{chief,science,risk,market,investment}/   one agent each (+ prompts)
backend/app/graph/citation_guard.py, workflow.py      evidence checks; LangGraph pipeline
backend/app/scoring/ + config/scoring.yaml            explainable opportunity score
backend/app/report/                                   Markdown report
backend/app/db/ + migrations/                         PostgreSQL tables and Alembic migrations
backend/scripts/                   demo and verification scripts
demo/                              demo video script (DEMO_SCRIPT.md) and build_demo.py (automatic narrated MP4)
backend/tests/                     tests (fixtures are synthetic and labelled)
PROJECT_STATUS.md                  detailed phase status
```

## What is unfinished (honest list, 2026-11-11)

- **Two machines share data through git.** The agents run on a cloud server; the hosted website is a read-only snapshot (`backend/site_data`) that the agents commit and push. It shows the data, takes topic proposals and has no key. Proposals stored on the hosted API are lost if it restarts before the loop collects them, and so is the record of reports bought through `/api/market/buy`.
- **Seen live on the cloud server (2026-11-11/12)**: the daily radar refresh; two own reports for top-5 radar topics ('mixture of experts', 'supervised fine-tuning'), then the stop at 2 a day; three topics added by the Science agent while idle ('assertion generation', 'quantum annealing', 'movable antenna'); the hourly live price of the holding; the first daily holding brief, written for $0.05 and paid with 0.1385 NEAR; the daily review ("hold"). **Built and mock-tested, not yet seen live**: a report sale paying for the next report, an Agent Market fee joining the 70/30 split (both hires were free tests), a purchase by an outside bot.
- **Radar numbers are in transition**: the refresh of 2026-11-11 14:18 UTC counted papers by each topic's name alone; the checked search phrases are now shared between machines, and the next daily refresh uses them and adds the three new topics.
- **A report payment is proven by a transaction hash and the buyer's name.** Hashes are public, so the proof does not show that the requester is the payer; a signed message from the buyer would. The seal is a SocialDB entry the report agent's key could overwrite: it protects against outsiders, not against the key holder.
- **One real holding only**: the trading agent runs (hourly checks, real orders inside the caps), but NEAR Intents has had no route for the INTCon token since 2026-11-10, so it cannot add to or sell that holding; it is valued at the live token price.
- **NEAR Agent Market**: listed ($3 a hire) and tested with two free test hires (the second handled by the cloud server in under 8 minutes); no paid job yet, so no fee has been recorded.
- **The second trading agent** (funded when the report agent's kept 30% passes $200) is planned, not built. Staking rewards at today's amounts cover only a small part of the AI bill.
- **Reports written from 2026-11-11 are unlocked for the demo** (`economy.demo_free_from`); the paid lock, payment check and access token are built and tested, and one outside purchase through `/api/market/buy` has not happened yet.
- **Patent counts come from the European Patent Office's free database** (EPO OPS) since 2026-11-11 for all radar topics; paid Google Patents searches stay off (`SERPAPI_CACHE_ONLY=true`). EPO allows about 5 searches a minute when busy, so a full radar count takes over an hour, and a topic it cannot count keeps its earlier numbers with their date.
- **X signals depend on the approved accounts** (about 130 on 2026-11-11): a topic none of them posts about gets no X signals, and posts are never treated as facts.
- **GDELT news** has refused requests from the development network (HTTP 429); the Market agent runs without headlines.
- **No custom NEAR contract**: fingerprints use SocialDB (`social.near` on mainnet since 2026-11-10; older seals stay on testnet and still verify).
- **Score weights are initial assumptions**, not fitted to outcomes; the Company Scout's next-runner score is a transparent heuristic.
- The dashboard has been checked in a browser at desktop and phone widths, not by a designer.

## Limits

- The Science agent reads titles, metadata and abstracts only, never full text, and says so.
- arXiv items are preprints and are not peer reviewed.
- Paper counts and "research acceleration" show research activity, not commercial success.
- The Market agent reads short verbatim passages from the latest SEC annual/quarterly reports of a fixed company list. 8-K press releases (exhibit files) are not read yet, and companies that do not file with the SEC (for example SK hynix, Samsung) are not covered.
- News items are headlines only. A headline is never treated as a verified fact.
- Without Patent and X agents some scoring dimensions have no evidence. The opportunity score is then shown as "not reportable" instead of a misleading number.
- The report is research information, not investment advice.
- Third-party content (paper metadata, later X posts) stays subject to its own terms; arXiv PDFs are never stored.

## License

MIT, see [LICENSE](LICENSE). This covers the code in this repository only; retrieved data (paper metadata, SEC filings, news headlines) remains under its sources' own terms.

## Third-party libraries

openai (Python SDK), httpx, pydantic, py-near, PyNaCl, base58, pydantic-settings, PyYAML, LangGraph, SQLAlchemy, Alembic, psycopg, FastAPI, Uvicorn, pytest. Dashboard: Next.js, React, TypeScript; fonts Space Grotesk and Inter (Google Fonts). Visual style inspired by near.org; FUTURESCOUT uses its own name and logo. Optional: a local PostgreSQL server (not needed to run the demo; without `DATABASE_URL` reports are written to files only). Code in this repository was written with AI assistance (Claude).
