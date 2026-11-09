# FUTURESCOUT AI

AI-assisted research on emerging technologies across the whole technology sector (semiconductors, AI software, robotics, quantum, energy, space, biotech tools, cybersecurity, XR). Specialist agents gather evidence from papers, patents, company sources and X posts, a separate risk agent argues the other side, and a final agent writes an evidence-backed report with sources, uncertainty and 1-5 year horizons.

It produces research, not trading signals. It never places trades and never promises returns.

## Status (read this first)

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
| X Intelligence agent (read-only; 17 owner-approved company, standards and press accounts; posts are social signals, never facts) | Built and tested with fixtures; first live run 2026-11-08 |
| Patent agent (EPO Open Patent Services, worldwide; patent counts per year, Patent Acceleration, top applicants) | Built and tested with fixtures; needs a free EPO OPS key; not yet run live |
| Hot-topic radar (`scripts/run_radar.py`, dashboard `/radar`): ranks topics by growth in papers (OpenAlex) and patents (Google Patents), counted by code, no model; small-base topics shown but not ranked; 9 technology sectors (`config/sectors.yaml`), sector tabs on the dashboard | Built, tested, run live on 8 topics (2026-11-08) and 37 topics across 9 sectors (2026-11-09) |
| Topic discovery: the X watch proposes topics from real posts; the paper scout (`scripts/discover_topics.py`, weekly in watch mode) finds fast-growing keywords in recent papers per sector and verifies each with a real per-year count before adding it | Built, tested; first live dry run 2026-11-09 |
| Company discovery: SEC full-text search finds every filer whose reports mention the topic, including small companies not on the configured list; marked "discovered" and read like the others | Built, tested, run live (HBM: 34 companies found) |
| Company fundamentals from SEC XBRL (revenue, growth, R&D intensity, size class by revenue) and 8-K press-release exhibits | Built, tested, run live |
| Paper portfolio (simulation, dashboard `/portfolio`): each sealed report "buys" its top scout candidates with pretend money at the first close after the report date and tracks them against the SOXX ETF; derived from NEAR-fingerprinted reports so it cannot be backdated; no money moves, not advice | Built and tested (2026-11-09); positions recorded live, pricing needs a free Alpha Vantage key |
| Treasury (`/api/treasury`, panel on `/market`): testnet NEAR earned from report sales and the seller's on-chain balance against what the runs cost in models and X data | Built, tested, live (2026-11-09) |
| Company Scout: every company behind the evidence (patent assignees, paper authors' employers, SEC filers), matched to the SEC ticker file, sized from XBRL, ranked by a transparent "next-runner" heuristic that favours smaller, growing, R&D-heavy names; incumbents listed separately; a forecast label, not a recommendation | Built and tested (2026-11-09); first live run 2026-11-09 |
| Retraction flags (OpenAlex) honoured by the citation guard; X post engagement recorded | Built, tested |
| Price & timing risk (part of the Risk agent): run-up, distance from 50-day average, volatility and drawdown over ~100 trading days for the companies whose filings mention the topic; rule-based level elevated / moderate / subdued. A risk input, never a buy/sell signal | Built and tested with fixtures; needs a free Alpha Vantage key; not yet run live |
| Watch mode (`scripts/watch.py --loop`): scans the approved X accounts every 2 hours, spots rising topics, refreshes the radar, and starts a full research run when a topic is hot and has no fresh report (capped per day); each run is sealed on NEAR and listed for sale; every decision is logged and shown on the dashboard | Built and tested with fakes; first live cycle 2026-11-09 |
| Report marketplace on NEAR testnet: summaries free, full reports unlock after a NEAR payment to the platform's account, verified on-chain; demo buyer bot pays and verifies the report fingerprint | Built, tested, and run live on testnet (2026-11-08: payment, verification, sale note and fingerprint match, 3 real transactions) |
| NEAR Protocol testnet record: each report's SHA-256 fingerprint is stored in SocialDB on testnet, and the dashboard re-checks it ("unchanged since recorded") | Built, tested and written live on testnet |

## Problem

Technology investment research mixes verifiable facts, rumours and hype. FUTURESCOUT AI keeps them apart: every claim carries a label (verified fact, AI interpretation, forecast, assumption, unverified claim), a confidence level and source URLs that come from real API responses, never from a model's memory.

## How NEAR is used

- All agents call models from the **NEAR AI Cloud** catalogue through its OpenAI-compatible API (`https://cloud-api.near.ai/v1`). Each agent has its own configurable model in `backend/config/model_config.yaml`.
- FUTURESCOUT is an agent that **earns**: other agents (or people) pay it NEAR for full research reports. The payment is a native NEAR transfer on testnet; the API reads the transaction from the chain before unlocking the report (`scripts/buyer_bot.py` is a demo buyer).
- After each run, the report's SHA-256 fingerprint is stored on **NEAR testnet** (SocialDB contract `v1.social08.testnet`). Anyone can recompute a report's fingerprint and compare it with the on-chain value, so a report cannot be quietly edited after publication. Testnet only; no trading, no transfers, and the research agents never touch the key.

## Try it

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
# report market on NEAR testnet (needs the seller and buyer testnet accounts from .env.example):
python scripts\near_record_report.py --latest   # see: the newest report's fingerprint recorded on NEAR testnet
python scripts\buyer_bot.py --dry-run           # see: which report a buyer bot would buy and the price
python scripts\buyer_bot.py                     # see: the bot pays 0.1 testnet NEAR, the API verifies it on-chain, report unlocks
# optional database (needs PostgreSQL and DATABASE_URL in .env):
python -m alembic upgrade head    # create the tables
python scripts\db_check.py        # see: connection status and saved runs
# (these scripts are in backend\scripts, so run them from the backend folder)
```

Keys (see `.env.example`): `NEAR_AI_API_KEY` from https://cloud.near.ai, `OPENALEX_API_KEY` from a free account at https://openalex.org/settings/api. arXiv and GDELT need no key. `EDGAR_USER_AGENT` must be your name and a real contact email (the SEC requires it; it is sent only to sec.gov). Companies checked by the Market agent are listed in `backend/config/companies.yaml`.

## Layout

```
backend/config/model_config.yaml   model per agent, prices, fallbacks
backend/app/models/                NEAR AI client and router
backend/config/companies.yaml      companies the Market agent checks (tickers; CIKs resolved live)
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

openai (Python SDK), httpx, pydantic, pydantic-settings, PyYAML, LangGraph, SQLAlchemy, Alembic, psycopg, FastAPI, Uvicorn, pytest. Dashboard: Next.js, React, TypeScript; fonts Space Grotesk and Inter (Google Fonts). Visual style inspired by near.org; FUTURESCOUT uses its own name and logo. Optional: a local PostgreSQL server (not needed to run the demo; without `DATABASE_URL` reports are written to files only). Code in this repository was written with AI assistance (Claude).
