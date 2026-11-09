# HANDOFF: FUTURESCOUT AI (for continuing in Claude Code)

Written 2026-11-08 17:59 (Malaysia time). Read this first, then `CLAUDE.md`, `PROJECT_STATUS.md` and `README.md`.

## 1. What this project is

FUTURESCOUT AI is an AI-powered semiconductor intelligence and investment **research** platform. Several agents gather evidence (papers, patents, company filings, news, X posts), a Risk agent argues the other side, and an Investment agent writes a cited report with 1-5 year horizons (0-12 months, 1-3 years, 3-5 years).

It is NOT a trading bot. It never places trades, never promises returns, and every report carries a disclaimer.

The owner is not an experienced Python/AI engineer. Explain things plainly, give exact commands, and say honestly what was tested and what was not.

Models come from the NEAR AI Cloud catalogue (OpenAI-compatible, `https://cloud-api.near.ai/v1`), chosen per agent in `backend/config/model_config.yaml`. No model names in code.

Stack: Python 3.10+, FastAPI (not yet used), LangGraph, Pydantic, PostgreSQL (native, not yet used), Next.js/TypeScript/Tailwind (not yet used), NEAR Protocol testnet (later, kept separate from the research engine).

Machine: the owner uses Windows, Python 3.10.7, venv at `D:\FUTURESCOUT AI\.venv`, project root `D:\FUTURESCOUT AI`, code in `D:\FUTURESCOUT AI\backend`. Run scripts from the `backend` folder.

## 2. Hackathon context (NEAR HACKATHON, from the owner's HACKATHON.md)

- Development ends **2026-11-14T23:59Z = 2026-11-15 07:59 Malaysia time**.
- Need a public repo, a README judges can follow, a demo with a real working run, and a LICENSE (owner's choice, not added).
- **Nothing below has been done, and each needs the owner's explicit yes:** make the repo public, `git push`, post the demo on X, sign or spend on mainnet, submit the single application (print the full JSON payload first and wait for a yes). Never invent values for human-decided fields (project name, lead name, email, team size, tracks, mainnet NEAR payout account, repo URL, demo post URL, description, consent).
- Re-read https://nearhackathon.com/HACKATHON.md before submitting.

## 3. Non-negotiable rules

- Never fabricate papers, patents, companies, citations or findings. Source URLs come only from API clients, never from a model.
- Every important claim has a label: `verified_fact`, `ai_interpretation`, `forecast`, `assumption`, `unverified_claim`, plus a confidence level and source ids.
- No hardcoded keys. Env vars + `.env.example`; `.env` is gitignored. Never commit secrets. Tell the owner never to paste keys into chat.
- No unrestricted wallet access for agents. No real trades.
- X agent: read-only, official X API only, never post/like/follow/DM. Never invent X handles; proposed accounts need owner approval. Mock data only in clearly labelled tests.
- Do not claim a feature is complete unless it was tested. Distinguish "mock-tested" from "run live".
- Never log prompts, responses or keys.
- After each phase: list files, run tests, say what was demonstrated live, update `PROJECT_STATUS.md`, say what is next.

## 4. Environment limits that shaped the work

- The previous (cloud) sandbox could not reach OpenAlex, arXiv, X, NEAR, SEC or GDELT. All sandbox tests use synthetic fixtures labelled FIXTURE and a mock model. Only the owner's laptop produced live results. In Claude Code on the laptop, live checks become possible.
- **The owner has no NEAR AI credit right now**, so the model path has never run live. Anything that needs a model is mock-tested only.

## 5. Architecture (what exists)

```
backend/config/model_config.yaml   model per agent, prices, fallbacks (verified against live catalogue: 64 models)
backend/config/scoring.yaml        8 weighted dimensions + risk penalty (initial assumptions)
backend/app/config.py              Settings (env vars)
backend/app/models/                NEAR AI client + ModelRouter (retry, fallback, pydantic validation + 1 repair retry, cost tracking)
backend/app/schemas/               common.py (SourceRecord, Finding, labels), science.py, research.py
backend/app/sources/               base.py, openalex.py, arxiv.py, edgar.py, gdelt.py
backend/app/graph/citation_guard.py  verified_fact needs a valid source id AND an excerpt found in the cited title/abstract, else downgraded
backend/app/graph/workflow.py      LangGraph pipeline
backend/app/agents/{chief,science,risk,investment}/   agent.py + prompt .md files
backend/app/agents/retrieval.py, formatting.py        shared helpers
backend/app/scoring/engine.py      explainable score
backend/app/report/markdown.py     report renderer
backend/scripts/                   list_models, demo_science, check_counts, run_research, demo_edgar, demo_news
backend/tests/                     84 tests (fixtures in tests/fixtures, helpers in tests/helpers.py)
```

Pipeline (`workflow.py`): chief_plan -> (science || risk_independent) -> chief_review -> optional ONE extra science round (MAX_EXTRA_ROUNDS=1) -> risk_challenge -> investment. A crashing node is recorded as an error and the run continues; missing credentials (`ConfigError`) stop the run loudly. `AGENTS_NOT_RUN = ["patent","market","x"]` appears in every report.

Key design decisions:
- Source ids = `"src_" + sha1(canonical url)[:10]`. Models may only reference ids.
- An agent counts as "run" only if its model analysis succeeded (plan.source=="model", science.llm_alias set, risk.analyzed, investment.draft present). Retrieval alone is not "run".
- Finding ids: S1.. (science), R1.. (risk), C1.. (challenges). Investment cites finding ids; code strips unknown ids, relabels unsupported statements as `assumption`, drops companies without evidence, guarantees all three horizons.
- Score: a dimension without cited evidence is "missing", never zero. Base = sum(weight x rating/5) / sum(evidenced weights) x 100; risk penalty up to 30%; **not reportable below 50% weight coverage**. With only Science + Risk evidence, the score will normally be "not reportable". This is intentional until Patent/Market/X exist.
- Router structured-output modes: json_schema, json_object, prompt_only (per-model flags); falls back if `response_format` is rejected.
- `TextDepth` values: `metadata_only`, `abstract_only`, `excerpt_only`, `full_text`. Never claim more depth than was retrieved.

## 6. What was done and how it was verified

| Item | Verified how |
|---|---|
| Foundation: config, schemas, citation guard, router | Tests (mock client). Catalogue check ran live on the laptop: all 7 configured models exist with matching prices/flags |
| OpenAlex + arXiv clients, Science agent retrieval | Live on laptop: real papers, from-year filter works. Counts use exact phrase in title/abstract (plain `search=` was ~50x too broad: measured) |
| Science agent model analysis | Mock only |
| Chief, Risk (2 passes), Investment, scoring, workflow, Markdown report, `run_research.py` | Mock-tested (70 tests passed on the laptop, 2026-11-08) |
| EDGAR client (`sources/edgar.py`, `scripts/demo_edgar.py`) | Tests + **live on laptop** (Micron filings and HBM excerpts returned correctly). Table-fragment filter fixed afterwards: not re-run live yet |
| GDELT news client (`sources/gdelt.py`, `scripts/demo_news.py`) | Tests only. **Never run live** |

Test count: 84 passed in the build sandbox. The laptop last confirmed 70; the 14 added EDGAR/GDELT tests have not been run there.

Bugs found by tests/live runs and fixed (do not regress): model failure lost from ScienceResult; arXiv ignored `from_year`; research-acceleration inflated by loose search; reports claiming agents "ran" when only retrieval happened; `UsageRecord.timestamp` evaluated at import.

## 7. NOT done / pending (priority order)

**Update 2026-11-08 evening (Claude Code on the laptop):** laptop checks done (tests pass; EDGAR live OK; GDELT returns HTTP 429 to every request from this network, so it was never run live). **Market agent built** (`agents/market/`, `config/companies.yaml`, `schemas/market.py`, `scripts/demo_market.py`): retrieval run live, model analysis mock-tested only. 95 tests pass. Still open from item 2: 8-K exhibit (EX-99) reading, non-SEC companies via approved IR pages. See `PROJECT_STATUS.md`.

1. ~~Run the pending laptop checks~~ (done; GDELT still blocked, retry later)
2. ~~**Market agent**~~ (built; remaining gaps below) (decision made: SEC EDGAR + company investor-relations pages + news search):
   - Build `agents/market/` (agent.py + prompt.md), same pattern as the Science agent: retrieve with `EdgarClient`, `GdeltClient`, then model analysis, citation guard, fids `M1..`.
   - News (GDELT) is headline-only: findings from it must be `unverified_claim` or `ai_interpretation`, never `verified_fact`.
   - Filings give `excerpt_only` text. Known gap: 8-K press releases live in exhibit files (EX-99), not the main document, so 8-K excerpts are usually empty. Consider reading the exhibit.
   - SK hynix and Samsung do not file with the SEC; TSMC and ASML file 20-F/6-K. Cover non-SEC companies via official IR pages only if the owner approves a short list of URLs. This part is not built.
   - Add `market` to the workflow (parallel with science/risk), a `config/companies.yaml` with tickers (resolve CIKs at runtime from `company_tickers.json`, never hardcode), model config entry, schemas, report section, tests. Remove "market" from `AGENTS_NOT_RUN` only once it runs.
   - Add Market dimensions to scoring evidence (commercial_readiness, customer_adoption, industry_investment, competitive_position, supply_chain_readiness).
3. ~~**PostgreSQL**~~ **Code built 2026-11-08** (`app/db/`, `alembic.ini`, `migrations/`, `scripts/db_check.py`; SQLAlchemy 2 + Alembic + psycopg 3 in the venv). PostgreSQL 18.6 installed by the owner; tables created; save/reload verified live (rolled back, database empty). pgvector not added. Original note: **PostgreSQL (native, Windows)**: store runs, sources, findings, reports, usage. pgvector later. Needs `DATABASE_URL` in `.env`. Use SQLAlchemy/psycopg or similar, with migrations (Alembic). Ask the owner before installing anything outside the venv.
4. **Patent agent: BUILT 2026-11-08 on EPO OPS, mock-tested only** (`app/sources/epo.py`, `app/agents/patent/`). Waiting for the owner's EPO_OPS_CONSUMER_KEY/SECRET; the first live call must confirm the JSON parser. Owner decisions 2026-11-08 for what follows: (a) NEAR = testnet record of report hashes only (no trading, no wallet agent); (b) price data goes into the Risk agent as "price/timing risk" (run-up, volatility, drawdown), never buy signals; (c) later: more paper sources, more X accounts (lookup + approval), small-cap discovery and a hot-topic radar. Original note: start with a feasibility check. PatentsView API was announced to pause from 2026-03-20 during migration to the USPTO Open Data Portal (replacement unconfirmed); EPO OPS needs free registration (~2.5 GB/week non-paying quota). Confirm which source works before building.
5. **FastAPI backend + Next.js dashboard** (2026-11-08: API built, tested, live-checked; Next.js dashboard in `frontend/` built and run locally with Node 26; start both with `.claude/launch.json` configs "api" and "dashboard", or `python scripts\serve.py` + `npm run dev`. Gotcha: inside Claude Code's sandbox npm's default cache is not writable (ENOENT); use `npm install --cache <scratchpad>\npm-cache`. Never run `next build` while `next dev` is running (they share `.next/`; it broke the dev server once). X API credit is now available, so item 7 is no longer on hold): dashboard must show label, confidence, sources and gaps; no fake buttons.
6. **NEAR Protocol (testnet)**: optional, only if it serves a real purpose (e.g., anchoring a report hash). Restricted key, no agent wallet access.
7. **X Intelligence agent: BUILT 2026-11-08** (`app/sources/x.py`, `app/agents/x/`, `config/x_watchlist.yaml`, `scripts/x_lookup.py`). Owner approved all 17 accounts found by the lookup; round 2 (2026-11-08 late) added 20 more (companies incl. small suppliers, SEMI, Hot Chips, press/research houses, two analyst accounts): 37 approved in total. `scripts/x_lookup.py` now looks up only candidates not yet approved. X API details checked on docs.x.com 2026-11-08: recent search `GET /2/tweets/search/recent` (7 days, 10-100 per request), user lookup `GET /2/users/by`; pay-per-use $0.005/post read, $0.010/user read, failed requests not billed, same resource within 24 h billed once. Storage/display terms of X still not reviewed. Original note: **X Intelligence agent: was ON HOLD by the owner's choice.** Needs paid X API credits (pay-per-usage; $0.005 per post read, $0.010 per user lookup, 3M reads/month cap per X's pricing page; per-endpoint limits and storage/display terms are still unverified). Watchlist not decided: recommended categories are ~12 official company accounts, 3 standards bodies (JEDEC, SEMI, imec), ~3 specialist press, 2-3 named analysts. **Handles must be verified through an X API lookup script and approved by the owner; none are recorded.** Posts are "social signals", never `verified_fact`.
8. **First live model run** (needs NEAR AI credit): `python scripts\demo_science.py --topic "high bandwidth memory"` then `python scripts\run_research.py --topic "high bandwidth memory" -v`. Expect to tune prompts and structured-output handling; record real token cost.
9. **Housekeeping**: update `PROJECT_STATUS.md` (it does not yet mention EDGAR/GDELT or 84 tests) and `README.md` (status table, Market sources); add `EDGAR_USER_AGENT` mention; add LICENSE only when the owner chooses one; keep README honest about unfinished parts for judges.

## 7b. Added 2026-11-08 (late): radar and discovery

- **Hot-topic radar** (`app/radar/`, `config/topics.yaml`, `scripts/run_radar.py`, API `/api/radar`, dashboard `/radar`): heat = average of paper and patent YoY growth between the two most recent complete years, code only. Topics with < 20 documents in the earlier year are shown but not ranked. Gotchas found live: Google Patents inflates counts for hyphenated phrases combined with OR (write phrases with spaces: fixed in `build_query`); "in-memory computing" / "processing-in-memory" match tens of thousands of patents (terms narrowed).
- **Company discovery** (`app/sources/edgar_fulltext.py`, `MarketAgent(discovery=...)`): SEC full-text search (efts.sec.gov, free, needs EDGAR_USER_AGENT) finds all filers mentioning the topic; up to 8 extra companies with tickers are read (newest filing) and marked `discovered`. Price/timing then covers them too. Prompts tell the models discovered companies are small/unknown and never "opportunities".
- SerpApi budget: ~57 of 100 searches used by 2026-11-08 evening (radar 35+10, patent runs 13, probes 4). Cache: 24 h.

## 7c. Added 2026-11-08 (later): enrichment

`app/sources/sec_facts.py` (XBRL company facts, 24 h cache, size class USD-only), `EdgarClient.press_releases` (EX-99 via index.json), `SourceRecord.is_retracted` + guard rule, X `public_metrics` -> `cited_by_count`. Semantic Scholar rejected anonymously (429): not added. Full 7-agent live report exists (see PROJECT_STATUS). Still owner-gated: ALPHA_VANTAGE_API_KEY (price/timing), NEAR testnet account (on-chain record), extra X accounts (lookup + approval), API restart for the dashboard to show /radar and new fields.

## 7d. Added 2026-11-08 (late): X discovery, patent pause

- X discovery: `discover_accounts` (one relevancy search over all of X, authors from the response), `watchlist.py` (suggested/approved/changes, `auto_manage`), `scripts/x_discover.py`. Lesson from the first live run: topic searches on X surface stock-tip accounts first; keep `auto_manage: false` unless the owner accepts that risk, and keep the flag words current.
- Patents: `SERPAPI_CACHE_ONLY=true` is set in the owner's `.env` (I added the line at the owner's request); remove it to resume live patent searches. Radar and full runs for cached topics keep working.

## 7f. Added 2026-11-09: watch mode + UI pass

- Watch mode: `app/watch/`, `scripts/watch.py --once|--loop`, `/api/watch`, dashboard panel. Settings `WATCH_*` in `.env.example`. Owner wants X scans and research frequent, patents rare (live patent counts only for new topics, 2/week) and the patent cadence NOT shown on the web. Lesson: X queries are limited to ~512 chars; `account_chunks()` splits account lists (both scan and topic search). The Chief model adds topics to `config/topics.yaml` (`found_by: x watch`, with post ids); review them occasionally.
- UI pass: `components/motion.tsx` (Reveal, CountUp, ScoreGauge), `RadarStrip`, `ReportToc`, `LivePanel`; aurora hero; glass cards. Screenshots are black while the Browser pane is hidden: verify visually with the pane shown. For a second dev server use `NEXT_PUBLIC_API_URL` + `serve.py --port`; the API now allows any localhost port (CORS).

## 7g. Added 2026-11-09: demo video kit

- `demo/DEMO_SCRIPT.md`: shot list and narration for a human-recorded 3-minute video (Win+G or OBS).
- `demo/build_demo.py`: automatic narrated MP4 (`demo/futurescout_demo.mp4`) from headless Chrome screenshots of the running dashboard + Windows TTS + bundled ffmpeg (`pip install pillow imageio-ffmpeg`). Needs API :8000 and dashboard :3000 running. The NEAR explorer cannot be screenshotted headless (Cloudflare check), so that scene is a card drawn from the live `/verify` result. `demo/build/` and `*.mp4` are git-ignored. `next.config.mjs` has `devIndicators: false` (hides the dev "N" badge; restart `npm run dev` after changing it).
- UI fixes found with the pane visible: nav no longer wraps (<900px scrolls sideways), grid columns use `minmax(0,1fr)` + `min-width:0`, radar error text is shortened in the UI (`friendlyError`) so the SerpApi quota message is never shown.

## 7h. Added 2026-11-09: Company Scout (emerging companies)

- Why: the owner pointed out that reports only named well-known incumbents (Micron etc.), which nobody needs to pay for. The scout answers "which companies are really working on this, and could a smaller one be the next runner?"
- Where: `app/scout/__init__.py` (CompanyScout, SecMatcher, next_runner_score), `app/schemas/scout.py`, workflow node in `risk_challenge`, `InvestmentAgent.run(scout=...)` + prompt rule 5c, `report/markdown.py` section, frontend `ScoutSection` + `scout` agent key (AgentFlow node, agents.ts, types.ts). Tests: `tests/test_scout.py`.
- Rules kept: names only from retrieved sources; SEC matching needs every identity token of the SEC title present in the found name (legal forms stripped); a single short token ("ON") never matches; universities/institutes are excluded; unmatched names are shown as "not SEC-listed", never guessed; the score is a heuristic labelled forecast in the UI and the K findings are `ai_interpretation` (code-computed). Not advice.
- Limits: counts cover only the documents the run retrieved; patent assignees come from the cached SerpApi results while `SERPAPI_CACHE_ONLY=true`; companies that do not file with the SEC (Samsung, SK hynix, most Japanese/European names) have no financials.

## 7o. Added 2026-11-09 (night): the X read list grows by itself (owner: "follow more, no approval, verified, followed by CEOs/VPs")

- "Follow" = add to FUTURESCOUT's read list (`config/x_watchlist.yaml`). The agent never follows, likes or posts on X (CLAUDE.md). `auto_manage: true`, `require_verified: true`, `auto_add_min_score: 8.0`, `max_accounts: 200` (owner decision 2026-11-09).
- Add rule `watchlist.qualifies()`: verified_type in {blue, business, government} (X sends the string "none" for unverified: that bug let unverified accounts in on the first live seed and was fixed), no caution flags, score ≥ 8 incl. endorsement bonus, AND substance: 2+ on-topic posts, a senior role in the bio, an @mention by a watched account, or a business badge. A government badge alone does not count (politicians posting about 6G got in on the first seed).
- "Followed by famous people" is approximated by **@mentions from watched accounts** (`mentioned_handles`, free: the posts are already read; +2 per distinct watched mentioner, max +6, 60-day window). Reading execs' follow lists was rejected on cost (X bills per user returned). Handles mentioned by ≥2 watched accounts are looked up (≤10 per scan, $0.01 each) and run through the same rule. Senior roles: `EXEC_ROLE_RE` in `app/sources/x.py`, +2 (≥5k followers) or +1.
- Watch mode: reads `WATCH_X_MAX_POSTS` (100) per scan, reloads the account list each cycle, records spend per day in `watch_state.json` and stops X calls at `WATCH_X_DAILY_BUDGET_USD` ($3). Every new topic (X scout or paper scout) triggers an X account search, ≤ `WATCH_X_DISCOVERY_TOPICS_PER_DAY` (3). Research runs read 50 posts instead of 30.
- Scripts: `x_seed_sectors.py [--dry-run]` (one search per sector on its hottest topic; run once 2026-11-09, $1.84, 8 sectors), `x_recheck.py [--dry-run]` (re-applies the rules to agent-added accounts from stored facts or the change log; failing ones go back to `suggested` with the reason; never touches owner accounts). Result after the seed + re-check: 37 owner + 14 agent-added = 51 watched; 79 back in `suggested` with reasons. Tests: `tests/test_x_growth.py`.
- Then the owner approved those 79 (group `owner-added`, `approved_by: owner`, a `note` keeps the re-check reason; the agent never removes them): **130 watched**. Adding cost $0 (ids already known). Cost bug found before it bit: `recent_from_accounts` / `search_watchlist` gave EACH query chunk the full post cap, so 6 chunks could bill 600 posts ($3) per scan; the cap is now shared across chunks (≥10 per request, X's minimum). Owner's limit "no more than $4": watch mode stops X calls at `WATCH_X_DAILY_BUDGET_USD` = $3/day; research runs add about $0.25 each (≤ 2 automatic per day), so the worst case is about $3.50/day. If the owner means $4 in total, a total cap still has to be added.

## 7n. Added 2026-11-09 (night): year-to-date momentum (owner: "if 2025 had 1000 papers and 2026 only 100, isn't that outdated?")

- Full-year growth compares the last two COMPLETE years only, so a topic collapsing in the current year was invisible until January. Added a same-period comparison: papers 1 Jan → (today − 30 days) this year vs the same dates last year (`app/agents/science/metrics.py`: `ytd_window`, `compute_ytd`, `ytd_from_client`; `OpenAlexClient.count_between`; 2 requests per topic). The 30-day lag is cut from BOTH years because OpenAlex indexes new papers late. Trend label: rising > +10%, cooling < −10%, else flat; no label when last year's window had < 20 papers.
- Used in: radar heat (now the average of papers last full year + papers YTD + patents last full year, `heat_basis` lists the parts; `TopicSignal.paper_ytd`, `trend`), the Science result (`ScienceResult.ytd`, in `ADDED_ANYWHERE_IF_EMPTY`), the Investment prompt metrics, the verdict (why line + "research is cooling this year" qualifier), the Markdown report, radar column "This year so far" with a trend chip, and the report's research-activity block. Tests: `tests/test_ytd.py`.
- Live radar 2026-11-09 (cutoff 10 Oct): 45 rising, 1 flat, 2 cooling (microLED display −41%, AR glasses −16%), 6 too small to call. Sanity check passed: last year's window holds 62–79% of the full 2025 count, as expected for Jan–10 Oct.

## 7m. Added 2026-11-09 (night): verdict, simple view, price chart, one-origin proxy, Docker

- Owner asked for "a final AI that decides" but "no investment suggestions": resolved as a **verdict on the technology**, computed by code (`app/report/verdict.py`) from the stored report: band (strong / building / early / weak / insufficient from the score), qualifiers (risk ≥4, commercialisation gap, stretched stocks, low confidence), plain words (`draft.plain_summary`, which the Investment prompt now asks for, else the summary's first sentences), why / watch out / what would change it (from dimensions, acceleration, scout, theme risks, hype flags, catalysts, invalidation conditions). No model call; labelled forecast; disclaimer "names no entry point". Served as `verdict` in `GET /api/runs/{id}` and printed at the top of the Markdown.
- Report page: **Simple view** (default, remembered in localStorage): verdict → score → emerging companies → price & timing (or an empty-state note explaining the Alpha Vantage key). **Full report** = everything as before, with the TOC.
- Price & timing: `PriceMetrics.closes` (last ~100 closes; in `ADDED_ANYWHERE_IF_EMPTY`) feeds a sparkline and a "how stretched" meter (position = % vs 50-day average). Wording kept as a risk input; the owner's request for "buy-in time" was declined and explained.
- Dashboard → API now same-origin: `NEXT_PUBLIC_API_URL` defaults to "" and `next.config.mjs` rewrites `/api/*` to `API_INTERNAL_URL` (default `http://127.0.0.1:8000`). For a second dev pair set `NEXT_PUBLIC_API_URL=http://127.0.0.1:8001` as before. `serve.py --host 0.0.0.0` for LAN/containers.
- `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml` (API 8000 + web 3000, `.env` for keys, runs/cache mounted). Not built here (Docker not installed on the dev laptop): **untested**. README "Launch it and share it" lists laptop / LAN / cloudflared quick tunnel / Docker / Vercel+Render.

## 7l. Added 2026-11-09 (evening): hackathon readiness

- **Git**: the folder was never a repository. `git init -b main` + first commit `c3e0147` (183 files; `.env`, `runs/`, `cache/`, `node_modules`, `.next`, demo build excluded; `.gitattributes` normalises line endings). Repo-local git identity set to the project account (eliteledger6). Pushing / making it public is the owner's call.
- **Samples for fresh clones**: `backend/samples/` holds three real sealed reports (HBM 295751e8, CPO 0bc26a1c, backside power 77fc7104) + `radar.json`, exported by `scripts/export_samples.py`. `_default_store` serves them when there is no DB and `runs/` has no reports; `load_radar` falls back to `samples/radar.json`. Test `tests/test_samples.py` also checks every shipped sample is sealed. Re-export after notable runs.
- **Tamper demo**: `scripts/tamper_demo.py [--run id]` reads the on-chain fingerprint, shows MATCH, edits one word in memory, shows MISMATCH; writes nothing.
- README gained "What is unfinished"; `next build` passes (9 routes); dashboard shows the sector on report cards and report pages.
- **Scout industry rule** (found on the first non-semiconductor live run, post-quantum cryptography, run 548cc3ff): SEC full-text discovery returns banks/insurers whose filings mention the topic in risk factors, and the scout ranked them. Now `EdgarClient.industry(cik)` reads the SIC code from the submissions record; `NON_TECH_SIC_PREFIXES` (finance 60-67, retail, agriculture, transport, services…) marks `off_sector`, −25 points, listed last, no K finding, labelled "outside tech" in the UI. `scripts/rescout.py --run <id> [--reseal]` re-runs the scout on a saved report (no model cost) and re-seals it; used on 548cc3ff (banks → 0, F5/Cisco now lead; new tx BtoVpk…). Note: the Investment text is not regenerated by rescout, so its themes may still name demoted companies.
- Samples now also include the post-quantum report (4 sealed reports).

## 7k. Added 2026-11-09: whole technology sector + paper scout (owner: "don't focus on semicon")

- `config/sectors.yaml` (9 sectors: semiconductors, ai_software, robotics_autonomy, quantum, energy, space_comms, biotech_tools, cybersecurity, xr_devices) with `discovery_queries` (paper scout) and `hints` (given to the Chief). `topics.yaml` entries carry `sector` (37 seed topics, 3–4 per new sector); `companies.yaml` carries `sector` (64 SEC filers; tickers resolve against the SEC file at run time, never guessed).
- Run flow: `run_research(sector=None)` looks the sector up from topics.yaml (`sector_of_topic`), passes `Sector: … (hints)` to the Chief plan and makes the Market agent read only that sector's configured companies (`MarketAgent.run(sector=)`; SEC full-text discovery still finds anyone). `scripts\run_research.py --sector <key>` overrides. `ResearchReport.sector` added (in `ADDED_TOP_LEVEL_IF_NONE` for the digest). Prompts' first line now says "the whole technology sector".
- How topics get on the radar (owner's question): (1) seeds; (2) X watch: the Chief model proposes ≤3 per scan tied to real post ids, now also picking the sector key; (3) **paper scout** `app/radar/discovery.py`: per sector, OpenAlex keywords of the most-cited recent works (`OpenAlexClient.recent_keywords`), minus known/generic/near-duplicate phrases, each verified with a real per-year count; proposed only if ≥20 papers in the earlier year and ≥25% YoY growth; evidence = work ids; `found_by: paper scout`. Runs every `WATCH_PAPER_DISCOVERY_DAYS` (7) inside the watcher (`Watcher.paper_discovery`, state `last_paper_discovery_at`) or by hand: `scripts\discover_topics.py [--sector key] [--dry-run]`. Once on the radar, heat (paper+patent growth) and X mentions decide research as before.
- API: `GET /api/sectors`; `POST /api/runs` accepts `sector`; run summaries include `sector`. Dashboard: sector tabs on /radar, copy generalised. X accounts are still the 37 semiconductor ones: other sectors get X signals only after the owner approves accounts (`scripts\x_discover.py --topic ...`).
- Paper-scout rules tightened after the first live dry run surfaced whole fields and off-sector phrases ("large language models" 35k papers, "food security", "baryon acoustic oscillations"): a keyword must come from ≥2 of the sector's queries (`MIN_QUERIES_HIT`), the earlier-year count must be ≤ `MAX_BASE` 5000, and society/policy phrases are in `GENERIC`.
- Radar heat: with patents paused, new-sector topics had no heat (both signals were required) and could never be ranked or auto-researched. `heat_of` now averages the signals that exist and `TopicSignal.heat_basis` says "papers+patents" / "papers only" (dashboard marks papers-only with *). Re-run `scripts\run_radar.py` after changing topics.
- First live add (2026-11-09, owner approved): 17 paper-scout topics joined the radar (54 topics). Review `found_by: paper scout` entries after each weekly pass; the scout is good at technologies and still occasionally lets a neighbouring field through (fixed cases: cosmology stems in quantum, "multi-agent systems" in biotech, hyphenated plurals of seeds). Delete a bad entry from topics.yaml by hand and, if it is a pattern, add a stem to that sector's `exclude`.
- Costs: radar now counts 54 topics (OpenAlex free with key; patents cache-only → "patents: not counted yet" for new topics; SEC filer counts ~4 requests/topic).

## 7j. GOTCHA found 2026-11-09: adding schema fields silently breaks NEAR verification of old reports

- `report_digest()` hashes the full report JSON. Adding `scout` and `SourceRecord.affiliations` made every previously sealed report show **"Changed after recording"** (red badge) because the dump now contained `"scout": null` / `"affiliations": []`.
- Fix in `app/chain/near_record.py`: `ADDED_TOP_LEVEL_IF_NONE` and `ADDED_ANYWHERE_IF_EMPTY` list the fields added after the first seal; they are stripped from the digest when at their default, kept when they carry data. Test: `test_fingerprint_is_stable_across_schema_additions`.
- RULE: whenever you add an optional field to `ResearchReport` or anything inside it, add its name to those lists (never remove entries), run the tests, and check `/api/runs/<old id>/verify` says `match` for the HBM report `295751e8-…`.

## 7i. Added 2026-11-09: paper portfolio + treasury (owner chose these INSTEAD of a trading bot)

- The owner asked twice for an autonomous trading bot with a real NEAR key; refused (CLAUDE.md: not a trading bot; no wallet access for agents). Agreed replacement: a SIMULATION portfolio and a treasury view.
- Portfolio: `app/portfolio/__init__.py` (Position/Portfolio models, `add_positions_from_report`, `sync_from_store`, `price_position`, `update_prices`), state file `backend/runs/portfolio.json`, `scripts/portfolio.py [--no-prices]`, `GET /api/portfolio` (syncs positions from saved reports on read; prices only via the script because of the 25/day Alpha Vantage limit), dashboard `/portfolio`. Settings `PORTFOLIO_*` in `app/config.py`. Positions = top `positions_per_report` scout candidates with tickers; entry = first close on/after the report date; `pending` until a bar exists; `error` when the ticker is unknown to Alpha Vantage. Always say "simulation".
- Treasury: `app/treasury.py` (`read_balance` = RPC `view_account`, testnet only; `treasury_report`), `GET /api/treasury` (balance cached 120 s), `components/TreasuryPanel.tsx` on `/market`.
- Demo video v2 (`demo/build_demo.py`): still frames (no zoom; the zoompan jitter looked like camera shake), narration burned in as subtitles chunk by chunk plus a `.srt`, title bar on top, new scenes for the scout, treasury and portfolio. Point it at other ports with `DEMO_API_URL` / `DEMO_DASHBOARD_URL`. Section offsets for crops were measured in the browser pane at 1280 px (`#scout` 9613 on the post-quantum report 548cc3ff, `.treasury` 697, portfolio `.stats` 619 on 2026-11-09); the scout scene follows the newest report with candidates, so re-measure `#scout` whenever that report changes (a wrong offset shows the wrong section, as happened once).

## 7e. Added 2026-11-08 (late): report marketplace

Owner decision: FUTURESCOUT sells reports to other agents (Agent Economy track), no trading. Code: `app/chain/payments.py` (verify native NEAR transfer via RPC `tx`), `app/api/market.py` (teaser/full/purchase/purchases; FileLedger or DbLedger), `db/models.Purchase` + migration `0002_purchases`, `scripts/buyer_bot.py` (separate buyer account; `--dry-run` sends nothing), dashboard `/market`. **Live on testnet 2026-11-08**: seller futurescoutai.testnet, buyer futurescoutaibuyer.testnet (owner's dedicated test accounts); fingerprint record, 0.1 NEAR payment, on-chain verification, sale note and fingerprint match all worked (tx hashes in PROJECT_STATUS). `scripts/near_record_report.py` seals existing reports. For the demo: start the API (`python scripts\serve.py`), then `python scripts\buyer_bot.py`. Testnet tokens only; mainnet refused in code. NEAR Intents was checked live: no tokenized stocks (216 assets), so "buy the company through Intents" is not possible today. near-sdk-js does not build on Windows; a Rust contract is a possible later upgrade (Q-011: not required).

## 8. Owner decisions on record

- Market sources: SEC EDGAR + company IR pages + news search.
- Database: native PostgreSQL.
- X agent: on hold; do other agents first.
- News source: GDELT chosen by Claude (free, no key, headlines only); paid APIs (Brave, Tavily) not evaluated beyond third-party blog comparisons: terms unconfirmed. Owner may overrule.
- Python >=3.10.

## 9. Open questions for the owner

- When will NEAR AI credit be available? (Blocks every live model check.)
- Which official IR/press-release pages may the Market agent read?
- Which hackathon track(s), project name, license? (Human-only.)
- Does the owner want X credits before the deadline?

## 10. Gotchas

- `EDGAR_USER_AGENT` must contain a real contact email (SEC rule). Put it in `.env`, never invent one. It is sent only to sec.gov.
- SEC limit: 10 requests/second (client uses ~6/s). GDELT: ~1 request / 5 s. arXiv: 1 request / 3 s, never store PDFs. OpenAlex needs `OPENALEX_API_KEY` (100k credits/day).
- `pip` on Windows needs `python -m pip install -e ".[dev]"` from `backend`.
- Windows paths: tell the owner paths in plain words; use `\` in PowerShell commands.
- Keep test fixtures clearly labelled FIXTURE / synthetic (`.invalid` domains). Mock sources must not be able to produce `verified_fact`.
