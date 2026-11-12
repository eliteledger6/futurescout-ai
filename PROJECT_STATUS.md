# PROJECT_STATUS

Last updated: 2026-11-08 evening (Phases 0, 1 verified on live data; Phases 5-7 built and mock-tested only; EDGAR client live-verified; GDELT client blocked by GDELT, never run live)

## Phase status

| Phase | State | Notes |
|---|---|---|
| 0 Architecture and feasibility | Done | |
| 0b Foundation (config, schemas, citation guard, model router) | Built; live-verified (NEAR AI chat calls, 2026-11-08) | Two router bugs found live and fixed (see Verified live) |
| 1 Science Agent (OpenAlex + arXiv) | Live-verified (retrieval + model) | |
| 2 Patent | **Paused by the owner 2026-11-08 to save quota for the demo**: `SERPAPI_CACHE_ONLY=true` in `.env` serves cached patent data (HBM and the 8 radar topics, any age) and spends nothing; uncached topics report "patent search paused". About 66 of 100 searches used. Live-verified 2026-11-08 via SerpApi. First live run exposed full-text matching ("HBM" = 28,702 patents in 2025 incl. biology); fixed to title/abstract (`TI=`/`AB=`, 263 in 2025, all on topic). HBM counts 2022-2026: 112, 108, 150, 263, 329 (partial); Patent Acceleration 2024→2025 +75%. Model (Qwen 3.6) works live ($0.013); invented source ids were removed by the citation guard; prompt now forbids model-computed growth claims. EPO registration still under manual validation (ref 49638) | Sources: Google Patents via SerpApi (owner's account, 100 free searches; ≤6 searches per run, 24-h local cache) or EPO OPS. | Feasibility check 2026-11-08: PatentsView API retired 2026-03-20 (moved to USPTO Open Data Portal; key reportedly needs a USPTO.gov account with ID.me verification, unconfirmed); EPO OPS chosen: worldwide (incl. KR/CN/JP), free up to 4 GB/week, needs registration (anonymous request refused with HTTP 403, checked live). Computes Patent Acceleration and top applicants in code; findings P1... The OPS JSON layout follows the known format because the official docs could not be read: **verify against the first live response** |
| 3 X | **Account discovery built** (`XClient.discover_accounts`, `app/agents/x/watchlist.py`, `scripts/x_discover.py`): the agent reads ~50 recent topic posts from all of X and ranks the AUTHORS (real handles only) into `suggested`; `auto_manage: false` by default (owner approves); when true it adds clean high scorers and removes agent-added accounts silent for 90 days, never owner-approved ones; every change is logged. First live run (HBM, $0.245): the top hits were stock-tip influencers and a parody account, so the caution filter was widened and flags now subtract from the score; the 10 suggestions sit in `suggested` with flags for the owner to review. Live-verified 2026-11-08; watchlist expanded to **37 approved accounts** (round 2: 20 of 24 candidates found by lookup, $0.20, all approved by the owner; TSMC, Onto Innovation, Kulicke & Soffa not found on X). Per-run cap stays 30 posts | Full run: X search found 5 real posts (est. $0.025) but the X model step ran out of tokens (same reasoning issue as DeepSeek; X had no `reasoning_effort` and only 4000 tokens). Fixed (low effort, 12000 tokens); X-only re-run: 5 findings, all `unverified_claim`, attributed to the posting account, model cost $0.0006 | Read-only client (no post/like/follow methods). Searches ONLY the 17 owner-approved accounts in `config/x_watchlist.yaml` (confirmed by X API lookup 2026-11-08, $0.17; TSMC and SEMIconnects not found, excluded). Recent search (7 days), max 30 posts/run (~$0.15). Posts are `social_post`: never `verified_fact`; findings resting only on posts are `unverified_claim`/`ai_interpretation`. X cost shown as a "x (data)" usage row |
| 4 Market | Live-verified (retrieval + model) | SEC EDGAR latest 10-K/20-F + 10-Q per company in `config/companies.yaml`, plus GDELT headlines (GDELT refuses this network so far). Runs in parallel with Science/Risk. Needs NEAR AI credit for a live model run |
| 5 Risk (independent pass + challenge pass) | Live-verified | Claude Sonnet 5.5: 77% of run cost |
| 4b Company discovery (Market agent) | Live-verified 2026-11-08 | SEC full-text search (efts.sec.gov, free). HBM, last 15 months: 71 filings, 34 distinct companies; the 8 most-mentioning with tickers are read (newest filing each) and marked `discovered`: FormFactor, Veeco, KLA, Micron, Ultra Clean, Netlist, Teradyne, Alpha Compute (no excerpt). Excerpts spot-checked: on topic (e.g. FormFactor: DRAM revenue up on HBM demand). Bug found live and fixed: hits are in relevance order, so the newest filing is now chosen by date |
| 4c Hot-topic radar | Live-verified 2026-11-08 (8 topics, 45 SerpApi searches incl. re-runs); **2026-11-09: 37 topics across 9 sectors** (see HANDOFF 7k) | Code-only ranking by paper + patent growth; see "Radar results" below |
| 4f Cross-sector radar, live 2026-11-09 13:45 | 37 topics, 30 ranked, 0 SerpApi searches | Top: vision-language-action model +1077% (22→259 papers), AI agents +316%, RAG +254%, speculative decoding +217%, mixture of experts +205%, end-to-end autonomous driving +135%, quantum error correction +127%, post-quantum cryptography +126%, zero-knowledge proof +89%, co-packaged optics +83% (papers+patents). Small-base (not ranked): direct-to-cell satellite +400% (base < 20), glass core substrate, neutral atom QC, optical inter-satellite link, AI drug discovery. Paper-scout dry run proposed e.g. supervised fine-tuning +230%, inference efficiency +191%, world models +113%, robotic manipulation +93%, grid-scale energy storage +59%; nothing added automatically yet |
| 4g Paper scout, first live add (owner's yes, 2026-11-09) | 17 topics added (54 total): large language model inference, vision-language models, model compression, mathematical reasoning, data curation, inference efficiency, supervised fine-tuning, robotic manipulation, world models, robot control, green hydrogen, hydrogen storage, grid-scale energy storage, flexible antenna, artificial intelligence in healthcare, data poisoning, oled displays | 5 bad proposals removed by hand and the rules tightened: cosmology terms in quantum (hubble/neutrino/CMB stems now excluded), "multi-agent systems" in biotech (excluded), and a hyphenated plural duplicate of a seed ("vision-language-action models"; duplicate check now splits hyphens). Radar recomputed with 54 topics |
| 4e Radar heat without patents | Fixed 2026-11-09 | Heat now averages the growth signals that exist ("papers only" when patents are paused, marked * on the dashboard), so new-sector topics can be ranked and auto-researched while the SerpApi quota is saved |
| 4d Whole technology sector + paper scout | Built and mock-tested 2026-11-09 (205 tests); live radar + paper-scout dry run 2026-11-09 (results below) | Owner: "don't focus on semicon". 9 sectors in `config/sectors.yaml`; topics/companies tagged by sector; research runs pick up the topic's sector (Chief hints, sector-filtered Market companies); new topics come from seeds, the X scout (now with sector) and the new paper scout (growing OpenAlex keywords, verified counts, ≥20 base, ≥25% growth, weekly in watch mode). X signals for non-semiconductor sectors need owner-approved accounts first |
| 5b Price & timing risk (Risk agent) | Built and mock-tested (7 tests); **not run live** (needs ALPHA_VANTAGE_API_KEY) | Owner decision 2026-11-08: price/timing as a risk input, never buy signals. Source check: Stooq now blocks bots (not bypassed); Twelve Data free plan is "internal non-display" only (unusable for a public dashboard); Alpha Vantage free = 25 requests/day, last 100 trading days (no 52-week/200-day view). Metrics and the elevated/moderate/subdued level are computed by code from fixed rules; model explains only (forecast labels are rewritten). Findings T1... |
| 5c Company Scout (`app/scout/`) | Built and mock-tested (8 tests) 2026-11-09; **live run on co-packaged optics 2026-11-09 12:42 (run 0bc26a1c, $0.218)**: 23 names from 10 company-affiliated papers + 10 SEC filers (no patents: cache-only), 12 matched to the SEC file, 9 candidates outside the big-name list: FormFactor (small, 4 filings), Coherent (mid), Veeco (small), Lumentum, Aeluma (micro), Jabil, Amkor, ASE, Canon; incumbents Marvell/AMD/Broadcom listed separately; 10 unlisted (Corning, Huawei, MediaTek, Ericsson, DuPont, Furukawa…). The Investment agent's themes now name Coherent, Lumentum, Aeluma, Amkor, ASE, FormFactor, Veeco, Jabil. Bug found live and fixed: OpenAlex affiliations carry a country suffix ("Corning (United States)"), now stripped before matching | Owner's ask: name the companies actually behind the topic, not only the big names everyone knows. Code only, no model. Collects patent assignees (Patent agent sources), company-type author affiliations (new `SourceRecord.affiliations` from OpenAlex institution type "company") and SEC filers (Market agent); matches names to the SEC ticker file (`EdgarClient.ticker_map()`, never guessed; unmatched names are listed as "not SEC-listed"); pulls XBRL fundamentals (≤15 lookups/run); computes a transparent 0-100 **next-runner score** (patents ≤25, papers ≤15, filings ≤20, micro/small +15 or mid +10, revenue growth ≤10, R&D intensity ≤10). Candidates = SEC-listed companies NOT on `companies.yaml`; incumbents listed separately. Writes K1.. findings (label `ai_interpretation`, code-computed) that the Investment agent may cite; prompt rule 5c tells it to prefer evidenced emerging names over incumbents, never as a recommendation. Report section "Emerging companies", dashboard section + agent-flow node |
| 5d Paper portfolio (`app/portfolio/`, `scripts/portfolio.py`, `/api/portfolio`, dashboard `/portfolio`) | Built and mock-tested 2026-11-09; live: 3 pending positions from the CPO report (FORM, COHR, VECO); **prices not run** (needs ALPHA_VANTAGE_API_KEY) | A SIMULATION, labelled as such everywhere: each sealed report "buys" its top scout candidates with a $10k pretend notional at the first close on/after the report date; price-only returns vs the SOXX ETF over the same dates; ≤20 Alpha Vantage requests per update (free plan 25/day); positions derive from NEAR-fingerprinted reports so they cannot be backdated. Owner decision 2026-11-09: no real trading, no key to agents |
| 5f Topic funds (`app/fund/`, `config/funds.yaml`, `scripts/funds.py`, `/api/funds`, dashboard `/funds`) | Built and mock-tested 2026-11-09 (9 tests); **live 2026-11-09: 15 funds, every decision sealed on NEAR testnet** (OLED 100% invested; AI agents, HBM, chiplet, silicon photonics, PQC, LLM inference, grid storage 75%; others 40%; VLA 0%) | Owner approved stages 1-2 (2026-11-09). One $10k PAPER fund per topic: low (large, 60%) / medium (mid, 30%) / high (small/micro, 10%) tiers from the latest report's companies; decision agent = code rules (invested share by verdict band, halved on an 8-point score drop, staged entry for stretched tiers, review after 7 days or when price data arrives); fills at the latest close, assumed 0.3% cost; every decision sha256-fingerprinted on NEAR testnet (`futurescout/funds/<key>`). Stage 2: 1Click token list + dry-run quotes; a token counts only if symbol AND price match the stock. Live 2026-11-09: the public 1Click list (216 tokens) has no tokenized stock, but the **NEAR Intents bridge list (`supported_tokens`, 250 tokens) has 28 Ondo tokens on BNB Chain** (NVDAon, MRVLon, INTCon, MSFTon, GOOGLon, METAon, TSLAon, SPYon...) and 1Click quotes them by `intents_token_id`. Funds now read both lists; a bridge token counts only if the price implied by a $100 dry quote is within 15% of the stock's close. **10 of 52 holdings have a real dry quote** (MSFT/GOOGL/META in AI agents, INTC, MRVL in five funds; quoted cost 0.4-1.2%). Ondo limits holders (non-US, eligibility); a quote does not prove eligibility. Still no trades (stage 3 needs the owner's written go-ahead). Alpha Vantage free plan (25/day) limits how many holdings get a price per day |
| 5g Patent year-to-date + EPO default + safety fixes (2026-11-09) | Live | Patents compare 1 Jan -> today-30d vs the same dates last year (EPO, free); radar heat includes it; all 15 saved reports backfilled and re-sealed. EPO OPS live-verified and now the default patent source. Fixes found live: (1) **Alpha Vantage quotes the API key in its rate-limit notice; it had been saved in 9 reports** -> masked at the source, DB/files scrubbed (0 left), reports re-sealed; owner advised to rotate the key; (2) NUL bytes in a SEC excerpt made PostgreSQL drop the 6G report -> stripped before sealing/saving; (3) seals now pay only gas while prepaid SocialDB storage lasts; a network-error retry no longer pays a deposit; `scripts/near_storage.py --withdraw` returned 3.17 unused testnet NEAR |
| 5h Live-trading test (stage 3) + shadow mode (`app/fund/live.py`, `app/agents/trader`, `scripts/fund_trade.py`, `/api/trading`, `/trading`) | Built and mock-tested 2026-11-09 (14 tests, fake chain + fake 1Click); **shadow mode run live** (Opus proposal, real dry quote, nothing sent); **no real trade made; `trading_enabled: false`; no fund account connected** | Owner go-ahead for a ~5 USD proof trade. Agent proposes, owner approves in the terminal with a typed confirmation, code enforces caps / allowlist / price band / single send / kill switch. Live finding: swaps under ~8 USD are refused by the market, so the 5 USD cap cannot trade until the owner raises it (see STAGE3_PLAN.md). The real send path (ft_transfer to the 1Click deposit address on mainnet) is untested until the first live trade; there is no testnet |
| 5e Treasury (`app/treasury.py`, `/api/treasury`, panel on `/market`) | Built, mock-tested, **live 2026-11-09**: earned 0.1 Ⓝ (1 sale), balance 2.19 Ⓝ read via RPC view_account, spent $1.37 over 7 runs ($0.195 avg) | Earned (ledger) vs spent (saved runs' usage); on-chain balance cached 2 min; testnet only, "tokens have no value" shown |
| 6 Chief + LangGraph orchestration | Live-verified | Parallel Science/Risk, one bounded gap-review loop; 2026-11-09: Company Scout runs in the challenge stage, before Investment |
| 7 Investment + scoring engine + Markdown report | Live-verified | Score weights are still initial assumptions |
| 8 Database | Built; live-verified on PostgreSQL 18.6 (owner's laptop) | Tables: runs, sources, findings, usage, errors (+ full report JSON and Markdown). Alembic migration `0001_initial`. `run_research.py` saves each run when DATABASE_URL is set; files in backend/runs/ are always written too |
| 9 Dashboard | 2026-11-09 UI pass: animated aurora hero, glass cards with cursor glow, scroll-reveal sections, counting stat numbers, an animated score gauge, a sticky section navigator on reports, a live radar strip of the hottest topics in the hero, an "Autonomous watch" panel (scan status, rising topics, research started, decision log), Radar and Market pages. All motion stops under prefers-reduced-motion. DOM-checked at desktop width on 2026-11-09 (data loads, gauge 63.1, 11 TOC targets resolve, no overflow); screenshots were unavailable because the browser pane was hidden, so the look is not yet confirmed by eye. 2026-11-08 later: added an animated agent-network diagram (home + How it works) and a per-report "agent trace" (which agents ran, findings, sources, model, cost; amber = data without analysis, dashed = not run), phone layout as a numbered step list; new hero, source strip, score rings. Checked in the browser at desktop and 375 px (no overflow, no console errors except /verify 404 from an API process started before that endpoint existed). Built and run locally (2026-11-08): API tested (8 tests + live check); Next.js type-checks and builds cleanly; all 4 pages load real data from PostgreSQL with no console errors; tabs, label filters and finding links checked in the browser; phone width (375 px) fits. Not yet looked at visually by a person | `backend/app/api/`, `scripts/serve.py`, `frontend/`. Style inspired by near.org (black, light grotesk type, hairline dividers, mint accent) with FUTURESCOUT's own logo. Plain CSS instead of Tailwind (fewer packages). Run button off unless `ENABLE_RUN_API=true` |
| 10 NEAR Protocol | **Live on testnet 2026-11-08**: report fingerprint record, buyer payment verified on-chain, seller sale note (3 real transactions, see "Report marketplace"). Dashboard badge verifies against the chain | Owner decision 2026-11-08: testnet record only (no trading/wallet agent; NEAR Intents has no testnet). Report SHA-256 stored in SocialDB `v1.social08.testnet` (contract existence and code hash checked live via RPC). Mainnet accounts/RPCs refused in code. Dashboard badge re-verifies via free RPC read. Library: py-near |
| 10b NEAR verification across schema changes | Bug found 2026-11-09 and fixed: new report fields (`scout`, `affiliations`) changed the digest of already-sealed reports (red "Changed after recording" badge). Digest now ignores later-added fields at their defaults (`ADDED_*` lists in `near_record.py`); HBM report verifies `match` again | See HANDOFF 7j for the rule |
| 4h First non-semiconductor live run: post-quantum cryptography (cybersecurity) 2026-11-09 14:04, run 548cc3ff, $0.185, sealed tx 26B7TQ… | Sector picked up automatically: Market read CRWD, PANW, ZS, NET, FTNT, OKTA; score 43.1 (coverage 90%); X produced nothing (accounts are semiconductor-only, as expected). **Quality issue found:** SEC full-text discovery surfaced filers that mention PQC only in risk-factor boilerplate (two banks, an insurer, a cavitation-equipment micro-cap) and the scout ranked them as candidates → fix: SIC industry lookup, finance/insurance/real-estate filers demoted and labelled | Themes still named F5, Cisco, Fortinet correctly |
| 9b Report readability (2026-11-09 night) | Built, mock-tested (210 tests), type-checked; looked at in the pane | Verdict card first (code-computed read of the technology: band, plain words, why / watch out / what would change it; labelled forecast, no buy/sell/timing), Simple view vs Full report toggle, price sparkline + stretch meter (needs Alpha Vantage key to have data), one-origin `/api` proxy, Docker files (untested: no Docker here), README launch/share guide |
| 11a Hackathon readiness (2026-11-09 evening) | git repository initialised, first commit made (not pushed, not public); `backend/samples` with 3 sealed reports + radar for key-less clones; README "What is unfinished"; `scripts/tamper_demo.py` (live: MATCH → MISMATCH); `next build` clean; live run on post-quantum cryptography started (cybersecurity sector) | Owner-only: push, make public, choose track, submit |
| 11 Deploy / demo | Demo kit 2026-11-09: `demo/DEMO_SCRIPT.md` (14-scene shot list, ~3:50) + `demo/build_demo.py` v2 (still frames, burned-in subtitles + .srt, title bar; no zoom after the owner said v1 looked shaky and had no captions) → `demo/futurescout_demo.mp4` (~4.4 min, 1080p) | Owner-only: record the human version, publish, submit |

## Test results

- Owner's laptop (Windows, Python 3.10), 2026-11-08 evening: **136 passed**, 0 failed (run by Claude Code). The dashboard (TypeScript) type-checks and builds; it has no automated tests yet. Includes 7 database tests on a throwaway in-memory SQLite database: the real Alembic migration is applied and compared with the code's table definitions (no differences), a full mocked run is saved and reloaded identically, no prompt text or key is stored, an unreachable database fails in ~5 s without printing the password and without losing the report files.
- Live on PostgreSQL 18.6 (owner's laptop, 2026-11-08): `alembic upgrade head` created the tables (schema 0001_initial); `db_check.py` connects. A synthetic fixture run was saved and reloaded identically inside a transaction that was then rolled back (6 findings, 6 sources; `report_json` is JSONB and a JSONB query works); the database was left empty. No real research run has been saved yet (that needs NEAR AI credit).
- Test count is now 103 (added: clear error for an unescaped '@' in the database password).
- Bug found by the tests and fixed: with the database down, saving hung ~130 s on Windows; a 5 s connection timeout was added. All use synthetic fixtures and a scripted mock model; no network, no key.

Bugs found by tests so far (all fixed): model failure lost from the Science result; arXiv ignored the year filter (found from live output); report claimed agents had "produced output" when only retrieval had happened or a default plan was used (an agent now counts as run only if its model analysis succeeded).

## Verified live (owner's laptop, 2026-11-08)

**First live end-to-end run with NEAR AI models (2026-11-08 evening, `run_research.py --topic "high bandwidth memory" --no-news`):** all five agents produced output (chief, science, risk, market, investment), 0 errors, 37 findings, 34 real sources, score 63.3 at 90% coverage, saved to PostgreSQL. **Real cost $0.170** (measured from token counts): Risk/Claude Sonnet 5.5 $0.131 (77%), Market/GLM-5.3 $0.019, Investment/DeepSeek $0.013, Chief/Qwen $0.004, Science/DeepSeek $0.004. About 3-4 minutes.

Problems the live runs exposed, all fixed with tests (none were visible with the mock model):
1. DeepSeek V4.1 Flash spent all 8000 output tokens on hidden reasoning and returned an empty answer. Fix: per-agent `reasoning_effort` in `model_config.yaml` (low: 36k -> 5k reasoning characters, 12 findings, $0.0055) and larger token budgets; a clear "ran out of output tokens" error; the setting is dropped automatically if a model rejects it.
2. Qwen rejected every structured request: "System message must be at the beginning" (the router sent two system messages). Fix: exactly one system message. Provider error reasons are now kept in error messages.
3. **Security: `-v` printed full request URLs, which contain the OpenAlex API key.** Fix: network-library logs are always kept at WARNING (test added). The key appeared in a local log and in the Claude Code chat; the log was deleted; **the owner should rotate the OpenAlex key**.
4. Score showed "confidence: high" from coverage alone, although most ratings were low/medium. Fix: confidence is now capped by the cited ratings' own confidence.
5. Risk challenges were labelled `verified_fact` although they are judgements. Fix: relabelled `ai_interpretation` (the quote is still checked).
6. The keyword "memory bandwidth" (proposed by the Chief) matched NVIDIA export-control passages, which the report then used as HBM evidence. Fix: broad phrases are no longer used as filing keywords.
7. Filing passages could start mid-sentence and lose their subject (KLA "increased 66%" was really Korea revenue). Fix: passages start at the sentence containing the keyword.

**Second live run after the fixes (same topic, 2026-11-08):** 0 errors, $0.166, score 55.7 with confidence now "low" (note explains why), no NVIDIA export-control finding (keyword fix), KLA finding now correctly says Korea revenue +33% QoQ / +66% YoY, all 9 Risk challenges labelled `ai_interpretation`, Applied Materials' forward-looking statement labelled `unverified_claim`; no API key in the verbose log. Saved to PostgreSQL (run 78439685-…). Use this report (`backend/runs/report_20261108T111301Z.md`) for the demo; the first run is kept in the database as history.

Known limit that remains: the citation guard checks that a quote exists in the source, not that the claim around it says the same thing. Claims were spot-checked by hand (Micron/Netlist and KLA correct; NVIDIA finding off-topic, see 6).

- `list_models.py`: NEAR AI catalogue has 64 models; the 7 models in `config/model_config.yaml` exist and their prices and advertised features match. No key needed.
- `demo_science.py --no-llm` for "high bandwidth memory": 12 real papers from OpenAlex + arXiv with real URLs, all from 2023 or later.
- `demo_edgar.py --ticker MU --keywords "high bandwidth memory,HBM"` (re-run 2026-11-08 evening): 3 real Micron filings (10-K 2026-10-09, two 8-Ks). The 10-K gave 4 HBM excerpts; the cover-page fragment is gone. One excerpt started mid-word ("reign AI"); fixed (cuts now snap to word boundaries, still verbatim), test added, re-checked live. The 8-Ks are still `metadata_only` (press releases sit in EX-99 exhibits, not read yet).
- `demo_news.py` (GDELT): **failed live.** GDELT answered HTTP 429 ("limit requests to one every 5 seconds") even to a single request after a 75-second pause, so it is refusing this network, not reacting to our pace. The response shape is still unverified. Try again later or from another network; if it keeps failing, a different news source is needed (your decision).
- `demo_market.py --topic "high bandwidth memory" --keywords "HBM" --no-news` (retrieval only, no model): all 12 tickers in `config/companies.yaml` resolved against the live SEC ticker file; 22 reports read; 9 mention the keywords (Micron x2, AMD, Broadcom, Marvell, Applied Materials, Lam Research, KLA x2). Passages spot-checked: verbatim and on topic. NVIDIA, Intel, Qualcomm, TSMC, ASML: no mention found in their latest reports (checked by hand for NVIDIA/Intel/Broadcom/TSMC full documents; this says nothing about their actual HBM business).
  - Two bugs found by this live run and fixed (tests added): filings were cut at 4 MB, but TSMC's 20-F is 10.4 MB (cap now 16 MB); "high-bandwidth memory" (hyphen) did not match "high bandwidth memory" (hyphens now match spaces; passages stay verbatim).
- Counting method measured with `check_counts.py`: plain `search=` matched ~50-200x too many works. Counts now use the exact phrase in title/abstract (2024: 167, 2025: 277, +65.9%). Synonyms such as "HBM3" are missed, so it is a rough activity indicator only.

## Full live report with every agent (2026-11-08 22:08 MYT, `backend/runs/report_20261108T140823Z.md`, DB run 295751e8-…)

All 7 agents produced output (chief, science, risk, market, x, patent, investment), 0 errors, **evidence coverage 100%**, score 63.1 with confidence medium (capped by the ratings' own confidence), **$0.233** model cost (Risk/Claude Sonnet $0.15 = 65%) + $0.025 X data; patents and X posts served from cache. Discovery added 8 companies (FormFactor, Veeco, Ultra Clean, Netlist, Teradyne, Alpha Compute, Qnity, Alpha & Omega) and the model produced cited findings from them (Veeco "production tool of record at a Tier 1 HBM customer"; FormFactor probe-card revenue up on HBM; Netlist ITC actions; Alpha & Omega on concentrated HBM capacity raising DRAM prices). Not run: price/timing (no ALPHA_VANTAGE_API_KEY) and the NEAR record (no testnet account). This is the demo report candidate.

## Data-source enrichment (2026-11-08, after the report above; mock-tested, live-checked where noted)

- **SEC XBRL company facts** (`app/sources/sec_facts.py`): revenue, growth, R&D intensity, net income per company, size class by revenue (micro/small/mid/large, USD reporters only). Live: Micron FY2026 revenue $133.2B (large), FormFactor $785M (small, R&D 14.7%), Ultra Clean $2.1B (mid), TSMC in TWD (no class). Shown in the report table, the dashboard and the Market model prompt.
- **8-K press releases** (`EdgarClient.press_releases`): EX-99 exhibits found via each filing's index.json; 2 per configured company, last 120 days. Live: Micron's two latest found; neither mentions HBM (checked: 0 occurrences in 18k chars), so no excerpt: correct behaviour.
- **Retractions**: OpenAlex `is_retracted` is stored; the citation guard refuses a retracted paper as verification and the model is told the paper is retracted.
- **X engagement** (likes+reposts+replies+quotes) is stored per post and shown to the model as attention, not truth.
- **Semantic Scholar**: NOT added. Anonymous requests return HTTP 429 (checked live); a key needs an approval form.
- Tests: 168 passed.

## Watch mode (2026-11-09; owner: frequent X + research, patents rarely)

`app/watch/`, `scripts/watch.py --once|--loop`, API `/api/watch`, dashboard "Autonomous watch" panel. Each cycle (default every 2 h, `WATCH_X_INTERVAL_MINUTES`): X scan of all approved accounts since the last seen post (no topic filter, ≤50 posts); code counts mentions of radar topics; the Chief model may propose ≤3 NEW technology topics, each tied to real post ids (dropped otherwise), which join `config/topics.yaml`; radar refresh with papers live and patents from cache (a new topic gets one live patent count, ≤`WATCH_NEW_PATENT_TOPICS_PER_WEEK`=2 per week); trigger rule: heat ≥ 40% or ≥ 3 mentions in the scan, no report younger than 7 days, ≤ 2 runs/day; triggered runs are saved, sealed on NEAR and listed. Every decision is logged with its reason in `runs/watch_state.json`. Runs only while the laptop and the script are running. 5 tests.

Live cycles 2026-11-09 (00:08 and 00:16 MYT): cycle 1's X scan failed with HTTP 400 because a 37-account `from:` query exceeds X's ~512-character limit; fixed by chunking account lists (topic searches too; no account dropped; tests added). The rules still ran: skipped HBM (fresh report), triggered **co-packaged optics** (heat +83%) and **backside power delivery** (+62%), held chiplet and compute-in-memory under the 2/day cap; both reports were produced and saved (scores 42.3 and 44.5, $0.21 and $0.18; X/patent not run for them: X failed, patents paused). Cycle 2 (scan only): 50 posts from 37 accounts, mentions HBM 2 / chiplet 1, Chief proposed 3 new topics from real posts (3D DRAM, high bandwidth compute (HBC), diamond wafer for chip cooling), added to the radar (11 topics), all research skipped as fresh or capped. Watcher total so far: ~$0.65 (X $0.25, two runs).

**2026-11-10 re-run with evidence-based companies:** batch of 15 started 03:10 UTC; high bandwidth memory (score 80, confidence 49.6%) and AI agents (70.8) completed with companies from patents/papers (HBM: MU 7 patents, INTC, MRVL, SK hynix, SanDisk; AI agents: MSFT, NOW, PANW, NTNX...). Then NEAR AI Cloud answered HTTP 402 (credit used up): 13 topics produced empty, unscored runs (scout only; each still cost X data and a testnet seal). The batch now stops on 402. Lists lead with the newest SCORED run, so the empty runs sit among the older ones. Funds re-decided for the two new reports (filing-only names gone). TO DO once the owner tops up NEAR AI credit: rerun the 13 topics, re-decide all funds, re-record the video.

**2026-11-10 trading strategy (owner request):** the trading agent no longer waits for `propose`. `python scriptsund_trade.py check [--shadow] [--loop]` wakes it on triggers (new sealed report for a traded topic; one-day fall >= 7% or rise >= 10% in a held/allowed stock; routine review every 24 h), gives it the report's verdict/confidence and dated X + filing findings as the only 'news', and applies fixed rules in code (`app/fund/strategy.py`: no buy below 45% confidence or outside strong/building, max 2 dip-buys per company, 25% share cap in shadow, only buys). Shadow fills automatically; live makes a proposal for the owner. Every wake-up is recorded (`checks` in trading state, fingerprinted) and shown on the Trading page, which now lists every real-money decision with the agent's reasoning. First live shadow check 2026-11-10 03:00 UTC: 5 new reports + review -> hold (AI-agents confidence 38.7% < 45%). 269 tests.

**2026-11-10 companies from the evidence (owner decision):** `config/companies.yaml` is gone. The Market agent now runs after Science and Patent and reads the SEC filings of the companies they point to (patent assignees, paper authors' employers, matched to the SEC ticker file; `app.scout.evidence_companies`), plus full-text filers marked "filing mention only". Paper funds buy only companies with patents or papers (filing-only names such as Figma are shown, never bought). 267 tests. Existing reports still show the old company sets until re-run.

**2026-11-10 signed route run live:** third real buy ($25 MRVLon) from the near.com private balance via the signed order; signed and submitted in a second, stock visible in near.com minutes later (owner-confirmed; `fund_trade.py confirm`). See STAGE3_PLAN.md.

**2026-11-10 trades resolved:** both real GOOGLon orders completed (SUCCESS; 0.0345 + 0.0846 GOOGLon for $35 of NEAR, ~10 h each); records updated and sealed via `fund_trade.py resume`. See STAGE3_PLAN.md.

**2026-11-10 (later):** Funds and Trading share one menu tab ("Funds & trading", sub-tabs Paper funds / Trading agent); the agent diagram ends with Topic fund and Trading agent and scrolls sideways on phones; demo video (2:21) has transparent captions and one funds-and-trading scene. The video describes how trading works and shows shadow mode; it does NOT claim a completed real trade (the two real orders are still stuck).

**Removed 2026-11-10 (owner decision): report selling.** The report market, treasury panel, payment check, buyer bot, `/api/market*` and `/api/treasury` routes, the Market tab and the `purchases` table model are gone (migration `0003_drop_purchases`; an existing database keeps the old table until `python -m alembic upgrade head` is run). Sections below that describe them are history. Also 2026-11-10: the agent diagram shows ONE Risk agent (it still does both passes: independent search, then challenging findings; its challenges are listed under Risk), and the "counted by code / no model" wording was removed from the pages and the video. 264 tests pass.

## (REMOVED 2026-11-10) Report marketplace (2026-11-08, late; owner decision: agents BUY reports, no trading)

**Run live on NEAR testnet 2026-11-08 (end to end):** seller `futurescoutai.testnet`, buyer `futurescoutaibuyer.testnet` (owner's dedicated test accounts, 2.5 testnet NEAR each). (1) Report fingerprint recorded: tx `C71fhHKJNqxvbhVUMV56zXeXQ29Ciusrk7ATqxWTBHyk` (first attempt failed: SocialDB needs a 0.1 NEAR initial storage deposit, fixed). (2) Buyer bot chose the HBM report via the radar, paid 0.1 testnet NEAR: tx `FrAfuoF5o7LAG9ftzcX9dKnZarxhSvT6yFVJtQnc8zSt`; the API verified it on-chain and unlocked the report. (3) Seller's sale note on-chain: tx `5fc7Ec3RfLYAcHjpGY1jbxJ6ZTX3s29F5Cq5nMrM8nnX`. (4) Buyer recomputed the SHA-256: MATCH. Purchase stored in PostgreSQL; access is per buyer account. Details: `app/chain/payments.py` verifies a native NEAR transfer by reading the `tx` from testnet RPC (final, signer = buyer, receiver = seller, Transfer deposit >= price, hash unused); `app/api/market.py`: `GET /api/market` (free teasers: summary, score, themes, fingerprint, price), `GET /api/market/{id}?buyer=` (full report once paid), `POST /api/market/{id}/purchase`, `GET /api/market/{id}/purchases`; purchases in PostgreSQL (`purchases` table, migration 0002) or `runs/purchases.json`; seller notes each sale on-chain (SocialDB) when its key is set. `scripts/buyer_bot.py` = a separate agent: picks the hottest radar topic's report, pays on testnet, buys, verifies the fingerprint. Dashboard `/market`. No custom contract: near-sdk-js refuses Windows and Rust is not installed (Q-011: not required). Testnet only; mainnet refused in code.

## NEAR Intents asset check (2026-11-08, live, free)

`GET https://1click.chaindefuser.com/v0/tokens` lists 216 supported assets across 39 chains (NEAR 35, Ethereum 29, Solana 22, Base 18, Robinhood chain 6, ...). **No tokenized stock or equity token is listed**: the Solana set is SOL, stablecoins, xBTC and memecoins; the Robinhood-chain set is USDG, ETH, USDe and two small tokens; the only "x" tokens are USDCx stablecoins. So "buy Micron/NVIDIA through NEAR Intents" is not possible today; a research-to-trade bridge can only report "no tradeable on-chain asset for this company" or trade unrelated crypto. Owner raised making the product an autonomous trading bot; Claude will write such code with hard limits but will not operate it with the owner's funds. Decision pending.

## Radar results (2026-11-08, `scripts\run_radar.py`, 2024 -> 2025 growth)

Two bugs the first run exposed, both fixed with tests: (1) hyphenated phrases combined with OR made Google Patents return ~25,000-38,000 "compute-in-memory" patents for 2025 (each phrase alone: under 80); phrases are now written with spaces (167 combined). (2) "glass core substrate" topped the list at +171% from only 7 -> 30 papers; topics with fewer than 20 documents in the earlier year are now shown but not ranked. Final ranking (papers / patents, 2024 -> 2025): 1 co-packaged optics +82% / +84% (heat +83); 2 high bandwidth memory +66% / +75% (+71); 3 backside power delivery +100% / +23% (+62); 4 chiplet +50% / +45% (+48); 5 compute-in-memory +45% / +44% (+45); 6 silicon photonics +12% / +39% (+26); 7 gallium nitride +18% / +8% (+13); unranked: glass core substrate (7 -> 30 papers, small base). SEC filer counts per topic are also stored. Heat is an activity indicator, not an investment signal.

## What the full pipeline does (`scripts\run_research.py`)

1. **Chief** plans: topic summary, science queries, risk queries, filing/news keywords, key questions (falls back to a plain plan if the model fails).
2. **Science**, **Risk (independent pass)** and **Market** run in parallel. Science/Risk use real OpenAlex/arXiv data; Market uses SEC filing passages and GDELT headlines. All findings go through the citation guard. Market rules enforced in code: a headline can never be `verified_fact`, a finding resting only on headlines becomes `unverified_claim` unless it is an `ai_interpretation`, and a company is kept on a finding only if a cited source names it. Market finding ids are M1, M2...
3. **Chief** reviews gaps; may request ONE extra Science round (bounded).
4. **Risk (challenge pass)** challenges specific Science findings.
5. **Investment** writes themes (three horizons, bull/base/bear, catalysts, risks, invalidation conditions) citing finding ids; code removes invalid ids, relabels unsupported statements as `assumption`, drops companies without evidence, and computes the opportunity score from cited ratings.
6. A Markdown + JSON report is written to `backend/runs/`, with sources, errors, gaps and per-agent token/cost usage.

Design choices that matter:
- The score shows "not reportable" when under 50% of the scoring weight has cited evidence. With Market findings the commercial dimensions can now have evidence, so a reportable score becomes possible; patent momentum stays missing until the Patent agent exists.
- Agents with no analysed evidence (patent, x, and market if its model analysis did not succeed) are listed in every report.
- Market gaps (stated in every report): 8-K press releases (EX-99 exhibits) are not read; SK hynix, Samsung and other non-SEC filers are not covered (needs your approved list of official IR pages).
- Weights in `config/scoring.yaml` are initial assumptions, not fitted to data.

## NOT verified yet

- Any live model call: whether each assigned model returns valid structured output for the Chief, Risk and Investment schemas, how good the analyses are, latency, and real cost. Needs NEAR AI credit.
- Quality of the prompts with real models. Expect to tune them after the first real run.
- Whether the Chief's narrower queries really improve paper relevance (some retrieved papers are only tangential, e.g. a 6G radio chip paper that mentions an HBM link).
- The new tests on Windows / Python 3.10.
- My rough cost estimate (not measured): a full run makes about 7-9 model calls and likely costs well under $1, with the Risk agent (Claude Sonnet 5.5, $2/$10 per million tokens) the largest part. Real figures come from the first run's usage table.

## Exactly what to do next

1. ~~Install PostgreSQL~~ Done 2026-11-08. Reference steps, in case you set it up again elsewhere:
   - Download the Windows installer from https://www.postgresql.org/download/windows/ (latest version) and run it. Keep port 5432. It asks for a password for the `postgres` admin user: choose one and keep it private.
   - Open "SQL Shell (psql)" from the Start menu (press Enter for the defaults, then type the admin password) and run, with your own password (letters and digits only, so it needs no escaping in the URL):
     `CREATE USER futurescout WITH PASSWORD 'choose-a-password';` then `CREATE DATABASE futurescout OWNER futurescout;` then `\q`
   - In `D:\FUTURESCOUT AI\.env` set `DATABASE_URL=postgresql://futurescout:choose-a-password@localhost:5432/futurescout` (type it in the file yourself; never paste passwords into chat).
   - From `backend`: `python -m alembic upgrade head` (creates the tables), then `python scripts\db_check.py` (should say Connected, schema version 0001_initial, 0 runs).
   - Mistakes seen during setup: a password containing '@' must be written %40 in DATABASE_URL; in SQL Shell the password needs single quotes; to change an existing user's password use ALTER USER, not CREATE USER.
2. ~~Get NEAR AI credit and do the first live run~~ Done 2026-11-08 (see "Verified live"). ~~Rotate the OpenAlex API key~~ Done by the owner 2026-11-08.
   **Next: X Intelligence agent.** The owner has X API credit (2026-11-08). Before building: the owner puts `X_BEARER_TOKEN` in `.env`; candidate accounts are looked up through the X API (never invented) and the owner approves the watchlist. Posts stay "social signals", never `verified_fact`; read-only, no posting/liking/following.
   Remaining human-only hackathon steps: record the demo video (script: `demo/DEMO_SCRIPT.md`; automatic fallback: `demo/futurescout_demo.mp4` built by `python demo\build_demo.py` on 2026-11-09), make the repo public, post on X, submit (each needs your explicit yes). LICENSE (MIT, "FUTURESCOUT AI contributors") added 2026-11-08.
   Demo video part 1 built 2026-11-10: `demo/futurescout_hackathon_demo.mp4` (2:25, 1920x1080, 30 fps, real screen recording of the running app, Windows text-to-speech narration, captions in `.srt`, script in `demo/NARRATION.md`), made by `python demo/make_video.py`. Rebuilt later the same day without the report-market scene: it covers research, reports, seal and paper funds with scoring v2. The real-trading scene is deliberately NOT in it (owner decision: record it after the stuck swaps are resolved, then join the two).
3. Retry GDELT later: `python scripts\demo_news.py --query "high bandwidth memory" --timespan 1month`.

When you have NEAR AI credit and `NEAR_AI_API_KEY` in `.env`:

3. `python scripts\demo_science.py --topic "high bandwidth memory"`: first live model call (Science only, cheapest check).
4. `python scripts\demo_market.py --topic "high bandwidth memory" --keywords "HBM" --no-news --llm`: first live Market model call.
5. Next build step after the database: Patent feasibility check, or FastAPI backend + dashboard (reads runs from the database).
6. `python scripts\run_research.py --topic "high bandwidth memory" -v`: full pipeline. Paste the console output; open the `.md` report in `backend\runs`.

## Open decisions (yours)

- X: will you buy X API credits (pay-per-usage)? Which accounts go in the watchlist (I will not invent handles)?
- Decided: Market sources = SEC EDGAR + company IR pages + news search; database = native PostgreSQL; X agent on hold.
- Which official IR/press-release pages may the Market agent read (for SK hynix, Samsung and others that do not file with the SEC)?
- If GDELT keeps refusing this network: try again later, or choose another news source (e.g. a paid search API; terms not yet checked)?
- Model choices: OK to compare Market on `glm_5_3` vs `glm_5_3_flash`, and Investment on `deepseek_v4_1_flash` vs `claude_opus_5_5`?

## Risks (current)

1. Patent data access is unresolved: PatentsView APIs were announced to pause from 2026-03-20 during migration to the USPTO Open Data Portal; EPO OPS needs registration and has a weekly free quota. Phase 2 starts with a feasibility check.
2. X API costs money (pay-per-usage, about $0.005 per post read per X's pricing page). Per-endpoint rate limits and X's rules for storing/displaying posts are still unchecked.
3. Structured output is unproven per model on the live API.
4. A real URL does not prove a source supports a claim. The guard checks quoted excerpts against abstracts, which reduces but does not remove this risk. The Investment agent's statements are only checked for citing real finding ids, not for whether the finding really supports them.
5. No credit means nothing in the model path has run live; a hackathon demo needs at least one real run.
6. Time: see hackathon section.

## Hackathon (NEAR HACKATHON) notes

Source: `HACKATHON.md` you provided (live copy: https://nearhackathon.com/HACKATHON.md; re-read before submitting).

- Development ends **2026-11-14T23:59Z (= 2026-11-15 07:59 Malaysia time)**.
- The repository must be public by then and needs a README judges can follow (draft exists) and a LICENSE (not added: you choose the license).
- Only the NEAR integration built during the window is judged. Using NEAR AI Cloud for inference is real NEAR usage. NEAR Protocol payments/records are optional and only worthwhile if they serve a real purpose.
- Track(s): your choice. Possible fits: `privacy` (NEAR AI Cloud), `agents`, `open`. None selected.
- The demo needs a real working run (video). A local-only demo is allowed, but screenshots alone are not enough when judges cannot open it.
- Human-only steps (not done without your explicit yes): make the repo public, push, publish the X demo post with video, create your mainnet NEAR payout account, provide team lead name/email/team size, consent to the contact notice, and confirm the exact JSON payload before the single submission.
- Everything unfinished must be described as unfinished in the README.


## 2026-11-10: selling, hosting
- Selling built (owner's written yes): the agent may sell (part of) a holding for NEAR on the private signed route. Code rules: held >= 24 h, report weakened / fall explained by evidence / rotation into a better-supported company; at most 2 sales a day; sale price not far below the last close; cost cap; a too-small sale is sized up to the $20 market minimum. After a sale the agent is woken once more and may buy. Orders on the private route are now settled by watching the private balance (no manual `confirm` needed when the coins arrive).
- Switches (owner-only, OFF): `live.sells_enabled`, `live.budget_mode: net` (cap counts buys minus sale proceeds). `live.auto_approve` was set true by the owner.
- Mock-tested (278 tests). Run live: dry sale quotes for GOOGLon and MRVLon on the INTENTS route pass every sale check (cost ~0.6%). No real sale yet.
- Hosting prepared: Render (API reading the exported snapshot backend/site_data) + Vercel (website). See HOSTING.md. Not deployed yet.
- RUN LIVE 2026-11-10 08:08 UTC, first full automatic round (auto_approve on, `check --review` run by the owner): the agent sold ALL GOOGLon (0.1191 -> 9.5406 NEAR, about $34.63; reason: its report weakened, no topic fund names Google, AI agents confidence 38.6%), then on the after-sale wake-up bought INTCon with the proceeds (9.5399 NEAR -> 0.5814 INTCon, about $34.23; HBM report strong, 49.6%). Both settled in seconds, confirmed from the private balance; both records sealed on NEAR testnet. Bug found and fixed first: holdings were valued from the public token list, which has no stock prices, so the first sale was refused as $0.
- Owner limits 2026-11-10: per-trade and daily caps removed (set equal to the $60 total), no minimum holding time; $20 near.com minimum kept.
- RUN LIVE 2026-11-10 (agent economy): the trading agent bought two reports from the report agent with real NEAR, both confirmed on mainnet: high bandwidth memory 0.295 NEAR (tx EK87dsDBo3y7sXsBryx3j9pM5zsNSZT6r7ceE3MbmPch), 6G 0.127 NEAR (tx E36EnCVocVTXv7rm1efJgf6BiC6iTmDrTuxfYgvBomiz). The report agent (grandbread5023.near) staked 5 NEAR through NEAR AI's stake.dao (product 'NEAR AI Cloud Credits', validator nearai.pool.near, '100 NEAR x 1 month = $1 credit'); the position is Active and accruing. Further stakes by the agent use the same call; mock-tested, not yet run by the agent.
- 2026-11-10: report payments can come from the trading agent's near.com (private) balance (`economy.pay_from: private`): signed order NEAR -> report agent's wallet (recipientType DESTINATION_CHAIN), checked before signing like trades, saved before signing, arrival seen on chain (native NEAR or wNEAR; the report agent unwraps wNEAR before staking). Dry quote run live (4.3 NEAR in, 4.3 NEAR out, ~10 s); the signed payment is mock-tested, not yet run live. Prices 3-5 NEAR (owner); report budget 30% of the fund (owner).
- 2026-11-10 RESTART (owner): the owner sold MRVLon and INTCon by hand in near.com; the trading and economy records were ARCHIVED (backend/runs/*/archive_2026-11-10_before_restart, not deleted; their NEAR fingerprints stay on chain) and the trading agent starts from zero with a fresh $60 budget (owner's yes). The near.com balance is read by the owner's loop (`fund_trade.py balance`, or each live check with auto-approve) and shown on the site; it counts in the fund's value.
- 2026-11-10 report market (owner): any trading bot can buy early access to a fresh report for its first 24 h (GET /api/market, pay the report agent in NEAR, POST /api/market/buy with the tx hash; checked on chain, redeemed once; 402 until paid; free after 24 h). Mock-tested and live-checked read-only (catalog of 15 reports at 3.8-4.6 NEAR; locked report answers 402); no outside purchase yet.

## 2026-11-10: seals move to NEAR mainnet

- `SEAL_NETWORK=mainnet` (in `.env`, set by the owner) seals every new report, paper-fund decision and trade record in
  SocialDB `social.near`, signed by the report agent `grandbread5023.near`. Default stays testnet. A mainnet recorder
  refuses a `.testnet` account or RPC. Mock-tested (301 tests); not yet run live.
- Old records keep their testnet seal and still verify: the website reads each record from its own network and the badge
  says which ("Unchanged since recorded on NEAR mainnet / testnet").
- Moving old reports: `python scripts\near_record_report.py --all --dry-run`, then without `--dry-run` (owner runs it;
  first seal locks 0.1 NEAR storage, about 0.004 NEAR per seal after that).

- 2026-11-10 (owner): reports are never unlocked without payment. `economy.embargo_hours: null` keeps every report locked
  (402 with the price) until a buyer pays; a number brings back "free after N hours". The demo report (high bandwidth
  memory) stays free via `always_free`. Mock-tested.
- 2026-11-10 (owner): reports cost $2-3 by what they cost to make (models and X reads, patent searches at $0.025, NEAR seal
  $0.05, plus $1.50), paid in NEAR at the live price; buyers get 3% leeway for NEAR price moves. Agent Market hire: $3.
  Mock-tested (307 tests).
- 2026-11-10 (owner): economy restarted at $2-3 reports (old records in runs/economy/archive_2026-11-10_before_2usd_restart/;
  INTC and the trading records kept, NEAR Intents could not trade). The report agent now stakes 70% of report PAYMENTS
  received minus earlier stakes (never other NEAR in its wallet, e.g. the owner's unstaked NEAR coming back), keeps
  0.3 NEAR for gas and seals, minimum stake 0.25 NEAR. `economy buy --max N` limits new reports per run. Mock-tested.
- 2026-11-10: hosting live (API https://futurescout-ai.onrender.com via backend/Dockerfile, site https://futurescout-ai.vercel.app).
  NEAR Agent Market listing live: https://market.near.ai/a/futurescout ($3 per hire, 12 h, self-hosted on the owner's laptop);
  one free test hire run live (topic taken from the brief, change request read from the thread, HBM report reused).
- 2026-11-11 (owner): /research is open again with two routes: hire the report agent on NEAR Agent Market ($3), or propose a
  topic for free (5 a day). `app/proposals.py`: short-topic filter, daily limit, AI reviewer (`topic_review`, run live on three
  sample topics: approved sodium-ion batteries, rejected "dogecoin price" and "the future"), queue worked by
  `scripts/market_agent.py` (reuses a recent report, else one research run, sealed), `--publish` exports and pushes the
  snapshot. Hosted proposals need PROPOSALS_TOKEN on Render and in `.env`. Mock-tested (316 tests); no real proposal
  researched yet; not deployed until the owner pushes.
- 2026-11-11 (owner): the first visitor proposal ran live end to end (retrieval-augmented generation: reviewer approved,
  researched, score 75.4, sealed on mainnet, published by the agent). For the demo, every report written from 2026-11-11 on
  is unlocked (`economy.demo_free_from` in funds.yaml) and the site marks it "Unlocked for demo purposes only" (card pill and
  a notice on the report); the two `always_free` reports carry the same mark. Delete `demo_free_from` to sell new reports again.
- 2026-11-11 (owner chose a small cloud server for the report agent): `deploy/setup_vps.sh` + `deploy/VPS.md` put
  `market_agent.py --publish` on an Ubuntu server as a self-restarting service (file-based data seeded from the snapshot,
  GitHub deploy key, keys entered by the owner). `publish()` now pulls before it exports and pushes. Checked: script syntax,
  the file-based data path on a scratch clone (60 reports, export round trip changes nothing). NOT yet run on a real server.
  The trading agent and its key stay on the owner's computer.
- 2026-11-11: hosted Radar fixed (the API served the old sample radar instead of the snapshot; now snapshot first; checked
  live: "this year so far" filled, heat 818 for the top topic). Server setup now also installs the trading agent as a second,
  switched-off service (`futurescout-trader`, `fund_trade.py watch --publish`); both loops publish through one lock, the
  trading loop only after a trade, report purchase or stake. Mock-tested (321 tests); not yet run on a real server.
- 2026-11-11 (owner): every new report gets its paper fund. `app/paper_fund_hook.py` runs `scripts/funds.py --topic <topic>`
  right after each research run in the report agent (proposals, Agent Market) and in `scripts/run_research.py` (`--no-fund`
  to skip); 6 fresh price lookups per fund; a fund problem never breaks the report. That fund is what makes a topic tradable,
  so the trading agent then sees a "new report" trigger. Mock-tested (323 tests); not yet run live.
- 2026-11-11 (owner: "I hope I can run everything easily"): one-click files in the main folder: `start_everything.bat`
  (report agent + trading agent, each in a self-restarting window), `start_trading_agent.bat`, `status.bat` (read-only;
  run and checked), `pause_trading.bat` / `resume_trading.bat` (kill switch), `update_website.bat`. Guide: RUNNING.md.
- 2026-11-11 (owner: everything inside "run everything", no manual steps): the report agent updates every paper fund when
  it starts and then once a day (`update_all_funds`: missing funds created, newer reports or due reviews decided, the rest
  revalued; 10 fresh price lookups), then publishes. Shadow trading stays at real NEAR Intents quotes only (no fallback).
  Mock-tested (324 tests).
- 2026-11-11 (owner: "remove the confidence level, the AI agent should think itself"): `strategy.min_confidence_pct: 0`
  for shadow and live. The agent is told to weigh each report's confidence and size smaller on thinner evidence; code still
  enforces the verdict rule (strong/building), the caps, the allowlist, the price band and the cost cap.
- 2026-11-11 (owner: "let the agent decide ... clearly aware of the last close and the current price"): `live.price_band_pct: 0`
  for shadow and live. Each candidate now shows the agent `quoted_price_per_token` and `gap_vs_last_close_pct`, and the
  agent is told it carries that risk. Still in code: verdict rule, budget caps, allowlist, cost cap, kill switch.
  Shadow review run live: NVDA quoted 3.49% above its close + 0.53% cost; the agent chose to hold (thin evidence).
- 2026-11-11 (owner): the trading agent buys a report only when it could act on it now: one of its stocks is rated
  'strong' or 'building' AND NEAR Intents quotes it (the 6G report, rated 'early', had been bought for nothing). Reports
  already bought stay usable. The trading page also shows refused buys with the reason and every bought report. Mock-tested.
- 2026-11-11 (owner: "make sure all your wordings are correct"): an extra review is now named "extra review, outside the
  hourly schedule" (never "the owner asked"); refused orders say "refused by the code's safety checks". The four shadow
  reviews Claude ran for testing (4:11-4:35 PM) keep the agent's original words, with a visible correction (field
  `correction`, not part of the record's fingerprint): started by the developer, not the owner; the NVDA refusal came
  from the price band that the owner removed minutes later; the 4:26 "no fund includes INTC" came from a bug since fixed.
- 2026-11-11 (owner: "just remove them"): the four shadow test reviews Claude ran were removed from the public record and
  kept in backend/runs/trading/archive_test_reviews_2026-11-11.json (local only; nothing had been bought or sold). The
  `correction` field stays available for future use but no record carries one.
- 2026-11-11: trading page splits decisions into "Real money" and "Shadow" lists. The shadow side's memory of the
  retrieval-augmented generation and chiplet reports (set only by the removed test reviews) was cleared, so the shadow side
  reacts to them at its next hourly check like the real side did.
- 2026-11-11 (owner: "show how much it earns, by % only"): `/api/trading` returns `performance` (live_pct, shadow_pct,
  per holding), valued at each stock's latest daily close from the topic funds; report purchases not included. The trading
  page shows "x% since bought" next to "Real money" and "Shadow". Today: real -1.96%, shadow -1.83% (INTC at the 2026-11-10 close).
- 2026-11-11 (owner spotted it on near.com): performance and the agent's own valuation use the LIVE NEAR Intents price of
  the tokenized stock (public token list, the price near.com shows; cached 10 min); the latest daily close only when missing.
  INTCon $60.76 -> real +2.47%, shadow +2.62% (near.com showed $44.91 for the holding). The swap quote still fails ("No liquidity").
- 2026-11-11 audit (owner: "make sure nothing is hidden or hardcoded"): no key or token in tracked files or git history;
  `.env`, `runs/`, caches and media are not tracked; no account name hardcoded in code (config only); `hidden` list empty;
  every app module imports; 332 tests; hosted endpoints answer and both checked seals match on mainnet. Fixed: the site
  export no longer copies `economy/sales.json` (buyers' access tokens). Known leftovers, harmless: one `if True:` block in
  `fund_trade.run_check`; ESLint is not configured for the frontend (TypeScript check and build pass).
- 2026-11-11 consistency pass (owner): site text and docs brought in line with the current rules (no price band, no
  confidence minimum, agent decides; `start_everything.bat`; 16 topics; research page says new reports are free for the demo;
  HANDOFF.md marked historical; home page uses the radar's sector names). Every page clicked through on the local build:
  home (16 cards, sector filter), radar (54 rows, tabs, detail), free and paid report, 16 fund pages, trading, how it works
  (18 agents), request a report (form, injection refused). Cloud kit: `scripts/preflight.py` + `check_setup.bat`
  (read-only readiness check, run on the laptop: READY) and the VPS guide step 4b.
- 2026-11-11 radar patents (owner: "yes go ahead"): EPO OPS (free) is the fallback for topics Google Patents (SerpApi,
  paused) cannot count; each topic records `patent_source`. First run: EPO counted 6 topics, then blocked the key for about
  12 minutes (`search=black`, their service was "overloaded"; our 1.5 s pace was too fast), and the 8 saved Google results
  had expired. The previous radar (2026-11-09) was restored. Now: the EPO client follows the rate EPO states in each reply,
  a refused source is not asked again in the same run, and a run that cannot count a topic's patents keeps the earlier
  numbers with their date (`carry_over_patents`). Mock-tested (335 tests). The full recompute is still to do.

## 2026-11-11 (evening): Radar patents counted for all 54 topics (run live)
- `scripts/run_radar.py` ran at EPO's allowed pace (about 5 searches a minute while their service is overloaded): 51 topics
  counted by EPO OPS; the last 3 (mixture of experts, post-quantum cryptography, confidential computing) failed on a passing
  EPO error during the run and were counted afterwards and merged in. All 54 topics now have patent numbers from one source
  (EPO OPS); none says "not counted yet". Papers run to 12 October 2026.
- Effect on the ranking: 34 topics ranked, 20 marked "small base" (fewer than 20 papers or patents in the earlier year).
  Some topics that were ranked on papers alone are now unranked because their patent base is tiny, e.g.
  vision-language-action model (0 patents in 2024, 32 in 2025).
- A topic's error now lists every patent source that was asked (before, a failed fallback was hidden behind the first
  source's message). Mock-tested: 335 tests pass.
- Backups kept locally: `runs/radar_backup_2026-11-09.json`, `runs/radar_epo_51_2026-11-11.json`.

## 2026-11-11 (night): final audit and its code fixes
- `FINAL_AUDIT_REPORT.md`: audit of the whole project (78/100, no critical issue). Run live: one call to each of the 7
  NEAR AI models, all 55 source links of the newest chiplet report (all genuine), every hosted page and read route, the
  mainnet seal check, the write routes' refusals, a secrets scan. Not done: a fresh end-to-end research run and the
  browser test (both stopped by the owner), listening to the video.
- Fixes from the audit (mock-tested, 335 tests pass; timing measured locally against the site snapshot):
  the report list and the report market no longer open every locked report and re-read `funds.yaml` per report
  (`/api/runs?limit=200`: about 1.9 s -> 0.7 s locally; it took 10-11 s on the hosted API); `run_research.py` help text
  matches the current agents and seal network; the comment on `live.auto_approve` matches its value (value untouched);
  leftover `if True:` removed from `fund_trade.run_check` (indentation only); `cp -n` warning in `deploy/setup_vps.sh`.
- Still open from the audit: video behind the product, patent evidence missing in 29 of 60 reports, paid reports readable
  in the snapshot once the repository is public, only 2 of 60 reports open to a visitor, unknown report address returns 200.

## 2026-11-11 (night): Agent Market hire handled by the server; publishing from two machines made safe
- Run live: a test hire on NEAR Agent Market (brief "confidential computing", created 12:39:30 UTC) was picked up by the
  report agent on the cloud server at 12:40:24, researched with all 9 agents (cost $0.32, one GDELT rate-limit note),
  sealed on NEAR mainnet (tx 5QvRePUW...), given a paper fund, submitted at 12:47:14 and published (commit 3813744).
- Problem found: the export rebuilt the whole snapshot from the publishing machine's own files. The server's publish
  therefore replaced the new Radar (EPO, 11 Nov) with its own older copy (9 Nov) and set the trading record back by four
  checks; a publish from the laptop would have deleted the server's new report.
- Fix (mock-tested, 336 tests pass; the export itself run live on the laptop): `export_site.py` now adds to the snapshot
  and never takes away. Reports only the other machine has are kept (`--prune` removes them on purpose), and a shared
  file (radar, portfolio, trading record, economy, proposals, each paper fund) is replaced only when this machine's copy
  is not older than the snapshot's (`site_publish.copy_unless_older`, by the latest time written inside the file).
  The Radar and the trading record in the snapshot are restored.
- Known limit: the trading agent on the laptop does not see reports made on the server (they are not in its own data),
  so it cannot buy them until trading runs on the server as well.

## 2026-11-11 (night): the Radar refreshes by itself
- The report agent's loop (`scripts/market_agent.py`) now recounts the Hot-Topic Radar every
  `agent_market.radar_refresh_hours` (24; 0 = off) with `scripts/run_radar.py` as a background process
  (`app/radar_refresh.py`), so jobs and proposals are still served while it counts, and publishes it when it ends well.
  It first takes the newest published radar as its base (a refresh keeps earlier patent numbers for topics it cannot
  count) and is started with SERPAPI_CACHE_ONLY=true, so it never buys a Google Patents search.
- Mock-tested (339 tests pass). Not run live: Claude does not run the report-agent loop while seals are on mainnet. It
  starts on the server at the first loop after the code arrives and the service restarts.
- Topics: the 54 radar topics are 34 written by hand plus 20 added by the paper scout (`scripts/discover_topics.py`,
  code that reads recent paper keywords; not the Chief agent, which plans one research run). Discovery is still started
  by hand; reports from Agent Market jobs and visitor proposals are not added to the radar's topic list.

## 2026-11-11 (night): the Science agent scouts new radar topics while idle (owner: "reuse our current research agent")
- `app/agents/science/topic_scout.py`: when the report agent's loop has no job, once every
  `agent_market.topic_scout_hours` (1) the Science agent reads `topic_scout_papers` (5) papers of the last six months
  from the next sector (a random sample of papers carrying the sector's phrase in title or abstract; never the same
  paper twice) and may name ONE technology the radar does not track. It is the same agent as in a research run: the
  `science` model and settings, no second agent.
- The model only names a candidate. Code decides: the name must point at papers it was really shown, must not be a
  variant of a tracked topic, and OpenAlex must count at least 20 papers in the earlier year, at most 5000, and 25%
  growth. At most `topic_scout_max_per_day` (3) topics a day. A new topic is appended to `config/topics.yaml`
  (`found_by: science agent`, evidence = the paper ids) and counted at the next radar refresh; `topics.yaml` is now
  published together with the website data. Every turn is recorded in `runs/topic_scout.json`.
- Mock-tested (343 tests pass). Run live as a dry run that wrote nothing to the topic list (4 turns, real papers, the
  real Science model, $0.001-0.0025 a turn): it rejected 'nitride ferroelectrics' (9 papers in 2024, too few) and
  'uav battery-swap' (no counts), and would have added 'quantum annealing' (525 -> 734 papers, +40%) and
  'assertion generation' (20 -> 33, +65%). Not run inside the report-agent loop by Claude (seals are on mainnet).

## 2026-11-11 (night): only reports are sealed on NEAR (owner: "only seal report")
- Radar topics were never sealed. What was sealed besides reports: every paper-fund decision (one fund per topic,
  reviewed daily, about 0.013 NEAR per seal) and every trade record (real and shadow).
- Now only reports are sealed. `scripts/funds.py` seals a decision and `fund_trade.py` seals a trade record only when
  `SEAL_FUND_DECISIONS=true` / `SEAL_TRADES=true` is set in `.env` (default off; `funds.py --seal-missing` still seals on
  request). Decisions and trade records keep their own fingerprint; earlier seals stay and still verify.
- Site and docs say so (home, about, trading page heading, README, RUNNING.md, .env.example, CLAUDE.md).
- Mock-tested (346 tests pass). Takes effect on each machine when its agents restart with this code.

## 2026-11-11 (night): how reports get written by themselves; Agent Market fees join the 70/30 split (owner's decision)
- `app/report_queue.py`, in the report agent's loop: one queue = the radar's ranking without topics that have a report
  from the last `auto_fresh_days` (7). (1) Each of the top `auto_top_n` (5) topics gets a report when it has no fresh
  one. (2) Every report sold on the report market (a paid purchase in the economy record, read from this machine and
  from the published snapshot) pays for one more: the next topic in the queue below the top 5. At most
  `auto_runs_per_day` (2) a day, one per pass, only when no job is waiting; sales made before the first start fund
  nothing; a failed run is retried after a day and does not use up a sale. Record: `runs/report_queue.json`.
- `app/market_income.py`: the fee of every accepted, paid NEAR Agent Market hire (`escrowAmount` in USD; test hires
  are 0 and are not income) is recorded once with its value in NEAR at the live price, published with the site data,
  and counted by the staking step as received (`extra_received_near`): 70% staked, 30% kept. The listing shows $3.00
  (checked on the public page today). The fee stays in the marketplace balance until the owner withdraws it, so the
  70% is staked only once that NEAR is in the report agent's wallet. `/api/economy` shows `market_income`.
- Mock-tested (352 tests pass). Not run live: the loop seals and spends, so the owner runs it. Both test hires so far
  paid 0, so no fee has been recorded yet.

## 2026-11-11 (night): second bug hunt (after the purchase-route fix)
- Checked: every Python file for names used but never defined (none); every API route with odd and hostile input on a
  copy of the site data; the report queue against the real radar and reports (it would write 'mixture of experts',
  then 'supervised fine-tuning', then 'zero-knowledge proof' for a sale); adding a scouted topic to a copy of
  `topics.yaml` (earlier topics unchanged, duplicate refused); the website's type check (passes).
- Fixed: (1) the server's services never fetched new code: a restart ran whatever was last pulled. Both systemd units
  now pull before starting (`deploy/setup_vps.sh`; an already installed server still needs the manual pull-and-restart
  line from `deploy/VPS.md` once). (2) The report queue ranked by this machine's own radar copy, which on the server is
  older than the published one until its first refresh ends: it now takes the newest radar first. (3) A NUL character
  in the `/api/runs?topic=` filter gave HTTP 500 with the database store (PostgreSQL refuses it); it is stripped.
- Mock-tested (353 tests pass); the API fuzz now reports no server error.

## 2026-11-11 (late): both agents run on the cloud server; agent network and content brought up to date
- Run live (owner's server): the report agent restarted on today's code at 13:53 UTC and at once began its first own
  report, 'mixture of experts' (a top-5 radar topic without a fresh report). The trading agent was enabled on the server
  at 13:56 UTC with the laptop's trading and purchase records copied over first; it recognised them (3.599 NEAR received
  for reports, 2.5193 NEAR staked) and ran a shadow and a live check with no trigger. No agent runs on the laptop any more.
- Agent network (`AgentFlow.tsx`, `lib/agents.ts`): new first column "Find topics" with a Hot-Topic Radar node (daily
  recount, top 5 kept fresh, a sale pays for the next report, idle scouting adds topics) next to the Topic reviewer;
  descriptions of Science (idle scouting), Report agent (runs on a server, own reports), Agent Market and staking (fees
  join the 70/30 split) and Topic fund (decisions no longer sealed) updated. A single report's trace is unchanged.
- The agent network is now also on the home page, between the hero and the reports (owner's suggestion), with a link to
  the rules on How it works. Radar page: one line on the daily recount and idle scouting.
- README ("Running it day to day", "What is unfinished") and RUNNING.md say where the agents run now, what the report
  agent does by itself, and state the known limits (payment proof by public hash, seal not write-once, data shared
  through git). Checked in the browser on this computer: home page diagram and one report's agent trace.

## 2026-11-11 (late): the agent network says which boxes are AI agents (owner: "it seems many agents but in fact it is not")
- Every box now carries a tag and the diagram has a legend with counts: **AI** (calls a model on NEAR AI Cloud): Topic
  reviewer, Chief, Science, Patent, Risk, X signals, Market, Price & timing, Investment, Trading agent = 10 agents
  (Chief review is the Chief's second pass and is tagged AI but not counted again); **CODE** (fixed rules and counts,
  no model): Hot-Topic Radar, Company scout, NEAR record, Topic fund, Report agent (the program and account, no model of
  its own) = 5; **SERVICE** (outside NEAR services): NEAR AI staking, Agent Market = 2; **PLANNED**: Trading agent 2.
  The kind is derived from whether the box has a model assigned (`kindOf` in `frontend/lib/agents.ts`), so it cannot
  drift from the configuration. The detail panel and the phone list show the same tag.
- Checked in the browser on this computer (home page); the website builds.

## 2026-11-11 (late): the Report agent is the framed AI team (owner: "report agent is an AI agent that generates the report")
- The earlier tagging called the "Report agent" box CODE, which read as if the report agent were not an AI agent. The
  diagram now draws a dashed frame around everything the Report agent is ("REPORT AGENT · one NEAR account · 9 AI agents
  working as a team": Topic reviewer, Chief, Science, Patent, Risk, X signals, Market, Price & timing, Investment, plus
  its code steps), and the small box is renamed "Sales & wallet" (its NEAR account and selling step, code).
- The legend opens with the plain statement: two agents, each with its own NEAR account, do business with each other:
  the Report agent (the framed team) and the Trading agent (1 AI agent). Then the box tags as before.
- Company scout stays tagged CODE: `app/scout` makes no model call (it merges company names from patents, papers and
  filings, matches SEC tickers and scores with a fixed heuristic); its K-findings are written by code.
- Checked in the browser on this computer (home page); the website builds.

## 2026-11-11 (late): Report agent drawn as the box all the work flows into (owner: "all the output go to him and report it out")
- The frame is gone. The box in the last research column is "Report agent" again (tag AI TEAM, highlighted), under the
  stage label "Report out": Investment (the written report), NEAR record (the seal), Topic fund and NEAR Agent Market
  (hires) all lead into it, and it reports out to the Trading agent (report for NEAR) and to staking. This matches the
  program: `scripts/market_agent.py` takes the topic, runs the research team, collects the finished report, seals it,
  builds the fund, publishes, delivers and sells.
- Legend lead: "The Report agent runs the research: it takes a topic, hands it to its team of 9 AI agents, collects all
  their work into one report, and reports it out: sealed on NEAR, published here, and sold. The Trading agent buys the
  report and trades on it. Each of the two has its own NEAR account." Box tags unchanged otherwise (10 AI, 4 code,
  2 services, 1 planned).
- Checked in the browser on this computer (home page, narrow window: the diagram scrolls sideways); the website builds.

## 2026-11-11 (late): last check of the claims in the agent network and on the site, against what the server did
- **Confirmed live (owner's server, from the published data and the hosted API):** the report agent wrote its own reports
  'mixture of experts' (13:58 UTC) and 'supervised fine-tuning' (14:06 UTC) because they were top-5 radar topics without
  a fresh report, each with all 9 AI agents, sealed on NEAR mainnet (hosted /verify: match), then stopped at the cap of
  2 a day; the daily radar refresh ran and was published at 14:18 UTC without overwriting anything; the new paper-fund
  decisions are not sealed (only reports are); the trading agent ran its checks on the server with the copied record;
  3.599 NEAR received, 2.5193 NEAR staked = 70.0%; the listing price is $3; proposals are open (5 a day).
- **Built and mock-tested, not yet seen live:** a sale paying for the next report (no sale since), a scouted topic being
  added (no topic added yet), an Agent Market fee joining the split (both hires were free test runs), an outside purchase.
- **Corrected wording that said more than is true:** "NEAR AI credits from staking pay every agent's model calls" ->
  "staking earns NEAR AI credits, which go toward the agents' model calls" (they cover a small part of the bill);
  "never unlocked without payment" -> opened only by a payment, with new reports open for the demo; "every report is
  sealed" -> each topic's report (the first day's three test runs are not sealed; every topic's latest report is);
  the two service boxes are "NEAR ecosystem services the agents use" (owner), not "outside" services.
- **Bugs found by the check and fixed:** (1) the radar's paper counts used search phrases cached only on the machine
  that researched a topic, so the server counted 'AI agents' by its name alone (1082 -> 4494 papers; the laptop, with the
  checked phrases, 1691 -> 8204). The checked phrases are now published (`site_data/phrases`) and used by any machine,
  and the radar no longer drops them after 7 days. The published radar still has the server's numbers until its next
  refresh. (2) Newest-wins compared the latest time inside two files, and a quote deadline two days ahead sat in both
  copies of the trading record, so the laptop's older copy replaced the server's newer one in an export here (caught
  before any commit). Future times are now ignored and, when equal, the copy with more history is kept; `--mine` forces
  this machine's copy. (3) The queue record was named `report_queue.json`, which matches the pattern of report files
  (the hosted health count was one too high); it is `auto_reports.json` now, and the loop renames an existing one.
- Radar page (owner): the heat bar is gone, heat is a coloured number; the table fits without a sideways scroll bar at
  375, 1100, 1270 and 1440 px (the detail panel moves below the table under 1240 px; on phones two columns the detail
  panel repeats are left out). The small charts no longer show a year that has not started.
- 354 tests pass; the website builds; home page and radar checked in the browser on this computer.

## 2026-11-11 (late): demo video v10 (4:48)
- `demo/make_video.py` re-recorded and re-rendered against the hosted site (DEMO_DASHBOARD_URL / DEMO_API_URL), which now
  shows the server's live data. 1920x1080, 30 fps, H.264 + AAC 48 kHz, 48 subtitle entries, no black scene, no silence
  longer than 2.5 s; a 26 MB copy is `demo/futurescout_hackathon_demo_small.mp4` (neither file is in git).
- Changed from v9: the Report agent is introduced as the one that runs the research, hands the topic to its 9 AI
  agents, collects their work and reports it out; 6 reports bought and 2.5 NEAR staked (were 3 and 1.3); the radar is
  recounted daily and the Science agent adds topics when idle; staking "earns credits toward the agents' models" (was
  "pays for every agent's models"); "anyone can check a report against its seal" replaces "fund decisions and trades
  get sealed the same way"; code checks budget, allowed stocks and cost, the agent weighs the price; a new scene "Runs
  by itself" (Request a report page, both agents on a cloud server, top 5 radar topics kept covered, a sale pays for
  the next report); the closing card says two free test hires and that both agents run on a cloud server.
- 15 narration lines were generated new with ElevenLabs (voice Chris, free plan, about 1,650 characters); the rest came
  from the cache. Checked by still frames at nine points and by sound level; not listened to.

## 2026-11-12: the trading agent always knows the live price of what it holds (owner)
- Before: the agent reviewed its holdings once a day (`review_hours: 24`) and was woken by a sharp move between two
  daily closes (Alpha Vantage). The live token price was used only to value the fund on the website.
- Now, on every check (hourly): the live NEAR Intents price of each holding is read and saved
  (`TradingState.holding_prices`: price, time, cost per share, gain since bought, move since the agent's last look). A
  move of `drop_pct` (7%) down or `jump_pct` (10%) up since the agent last looked wakes it (`strategy.watch_holdings`),
  so a slow slide over several checks adds up; after the agent has looked, the count restarts (`mark_seen`). When woken
  for any reason the agent is given, per holding, `price_now`, `price_read_at`, `cost_per_share`,
  `gain_pct_since_bought` and `move_pct_since_your_last_look`, and is told to state each holding's current price.
- The loop prints the price of each holding at every check, and the Trading page shows the last price the agent read.
- Mock-tested (355 tests pass). Run live read-only on this computer: INTC read at $61.00, +2.9% against its cost of
  $59.29 a share. Not run in the trading loop by Claude (it signs); it takes effect when the server's trader restarts.
- Not built yet (needs the owner's numbers): a daily "holding brief" bought from the report agent (X signals and a
  risk note on each holding), paid in NEAR.

## 2026-11-12: daily holding briefs, bought from the report agent for $0.50 (owner: "$0.50 a day")
- `app/fund/holding_brief.py` + `fund_trade.cmd_briefs`, first step of every pass of the trading loop: for each share
  the live fund holds whose brief is older than `economy.brief_hours` (24), the report agent's X signals agent reads the
  newest posts of the company's own account, press and analysts (one search of at most 14 accounts; 10 posts is the X
  API's minimum) and its Risk agent in brief mode (`risk_brief`, a small model) writes a short note: summary starting
  with the live price and gain, what changed against the risks the latest report named, up to three risks, and an
  urgency. Posts stay labelled as unverified claims. A brief marked "high" wakes the trading agent; whenever the agent
  is woken it reads the newest brief of each holding.
- Payment: `economy.brief_usd` (0.5) per brief in NEAR at the live price, one payment for everything owed, from the
  near.com balance through `pay_from_private` and the same checks as a report purchase (economy switch, trading switch,
  kill switch, price cap, report budget). It is recorded as a purchase, so it joins the 70% staked / 30% kept split,
  but it is not counted as a report sale (it does not pay for a new report). A payment that cannot be sent leaves the
  briefs owed; after `brief_max_owed` (3) unpaid briefs no new one is written; a payment that may be under way is
  never repeated. Written and paid only in the owner's loop (`live.auto_approve`).
- Site: the Trading page shows the briefs (summary, what changed, risks, urgency, post links, price, paid or owed) and
  the last price the agent read for each holding; the Trading agent's description says both.
- Mock-tested (361 tests pass). Run live as a dry run on this computer, with nothing saved and nothing paid: a real
  brief on INTC read 10 posts (TrendForce, Jon Peddie Research, Intel's own account), cost $0.05 to make (X reads
  $0.05, models $0.0008), is priced $0.50 = 0.139 NEAR, urgency "low". The first test with the whole watchlist read 26
  posts ($0.13), which is why a brief now reads a short account list. The payment itself has not run: it signs with
  the owner's key, and near.com may refuse so small an amount (then briefs add up until one payment goes through).

## 2026-11-12: the daily review of holdings never came due (bug found in the server's log, fixed)
- The server's trading log showed "no review due" at every hourly check since the loop started. Cause: the 24-hour
  review counted from the last CHECK, and the hourly loop renewed that time every hour. The published record confirms
  it: the only "review" wake-ups are the first ones on 2026-11-10; the agent had not looked at its INTC holding since.
- Fix: the review counts from when the agent last actually looked (`TradingState.last_review_at` /
  `last_live_review_at`, set whenever the agent is called). A record from before the fix has no such time, so the
  review comes due at the next check. Mock-tested (362 tests pass). Takes effect when the server's trader restarts.
- Run live on the owner's server at 01:00 UTC: the trader restarted on the code with the live price watch and the
  daily holding briefs; its first pass was still running when the log was pasted.

## 2026-11-12: everything brought up to date and checked against the live data
- Run live on the owner's server (log of 01:00-01:15 UTC): the first daily holding brief on INTC (10 posts, $0.051 to
  make) was paid with 0.1385 NEAR from the near.com balance and arrived in the report agent's account after about 15 s;
  the live price is printed at every check; after the review fix the daily review fired: real money "hold" on INTC
  (price $60.91 stated, the brief read), shadow "buy" of $600 MSFT (pretend). Each review cost about $0.05.
- Agent network: a "daily brief · $0.50" badge between the Trading agent and the Report agent; the legend says the
  Trading agent reads the price of what it holds every hour and buys a daily brief. Trading page: "urgent holding
  brief" as a wake-up reason. README: opening line, the "runs live" rows (6 reports and 1 brief bought, 2.5193 NEAR
  staked, two test hires, trading loop on the server), the demo walk-through, and the "what is unfinished" list now
  separates what was seen live from what is only mock-tested. RUNNING.md: the server's everyday commands come first.
- Claims check against the hosted API (script, run live): 9 AI agents in the report team plus the trading agent, all
  on NEAR AI Cloud model ids; proposals 5 a day and open; Agent Market price $3.00; 14 reports on sale at $2.00-2.31;
  each of the radar's top 5 topics has a report from the last 2 days; the radar is under 24 hours old; the 4 newest
  reports match their seal on NEAR; the brief costs $0.50 and the latest is paid; the holding's live price is under 90
  minutes old; trading enabled, kill switch off; 67.4% of 3.7375 NEAR received is staked (0.097 NEAR of the 70% waits
  for the 1 NEAR minimum); all six pages load. All held.
- 362 tests pass; the website builds; the diagram's badges do not overlap (checked in the browser at 1440 px).
