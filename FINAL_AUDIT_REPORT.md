# FINAL AUDIT REPORT: FUTURESCOUT AI

Audit date: 2026-11-11. Audited commit: `6b02af5` (main, same as GitHub).
No application code was changed during this audit. Nothing was signed, sealed, traded or pushed.

## How to read this report

Every result says how it was checked:

- **Run live today**: executed during this audit against the real service.
- **Saved live run**: read from a real run stored on disk (date given), not re-executed today.
- **Mock-tested**: covered by the automated tests only (fixtures and a mock model).
- **Not checked**: not verified in this audit; no claim is made.

The audit brief was written without knowledge of this project, so some items do not apply (noted where relevant):
the project has more than 7 agents, covers 9 technology sectors rather than only semiconductors, and uses files plus
an optional PostgreSQL database.

**Scope limits of this audit, stated plainly:**

- The fresh end-to-end run on "UCIe and chiplet architecture" was started and then stopped at the owner's request after
  two model calls (Chief and X). Phase 3 is therefore based on the newest saved chiplet report (2026-11-10), not a new run.
- The browser test (1920 × 1080 and mobile, screenshots) was stopped at the owner's request. Frontend results are HTTP
  checks only. Layout, buttons and mobile view were **not checked** today.
- The video's sound was not listened to. Only the file, the subtitles and the script were inspected.

---

## 1. Overall status

The project runs, is deployed, and its central claims are backed by real data. No critical (P0) issue and no broken core
feature (P1 in the code) was found. The main risks for the submission are presentational: the repository is still
private, the demo video is behind the product, and most reports are locked for a visiting judge.

**Score: 78 / 100** (breakdown in section 10).

---

## 2. Project completeness

| Feature | Status | Evidence | Problem | Recommended fix |
|---|---|---|---|---|
| Frontend (Next.js, 9 pages) | PASS | All 8 hosted pages return 200 (run live today) | Visual and mobile check not done today | Re-run the browser check before submitting |
| Backend (FastAPI, 20 routes) | PASS | All 11 hosted read routes return 200 (run live today) | `/api/runs?limit=200` takes 10–11 s | See P2-3 |
| Automated tests | PASS | 335 passed today (mock-tested, no network) | None | None |
| Agents (chief, science, patent, market, x, risk, investment, plus timing, scout, relevance, topic_review, trader) | PASS | Code and prompt file per agent; 8 agents in the saved chiplet run | Patent agent absent from that run | See P2-2 |
| LangGraph workflow | PASS | `app/graph/workflow.py` builds a `StateGraph`; `langgraph>=1.0` in dependencies | None | None |
| NEAR AI models | PASS | 7 model ids answered today from `cloud-api.near.ai` | None | None |
| External APIs (OpenAlex, arXiv, SEC EDGAR, GDELT, X, EPO, SerpApi, Alpha Vantage) | WARNING | Real records in saved runs; EPO run live today | EPO and Alpha Vantage rate limits cause gaps in some reports | See P2-2 |
| NEAR Protocol (seals, payments, staking) | PASS | Hosted `/verify` returns `match` on mainnet for report `4a2a3eaa…` (run live today) | Older reports are sealed on testnet | State it in the README (it is network-aware already) |
| Database | PASS (optional) | PostgreSQL via SQLAlchemy and migrations; files are the default store | Not exercised today | None |
| Environment variables | PASS | `.env` ignored by git; `.env.example` present (137 lines); `preflight.py` checks them | None | None |
| Deployment | PASS | Render (API), Vercel (site), DigitalOcean (report agent) all live | Trading agent still runs on the laptop | Move it or say so in the README |
| README | PASS | 255 lines, includes "What is real and what is simulated" and "Try it in 10 minutes (no keys needed)" | None found | None |
| Demo video | WARNING | 1920 × 1080 MP4, 4:14 | Content is behind the product | See P2-1 |
| TODO / placeholder code | PASS | None found in app code | One leftover `if True:` in `fund_trade.py:279` | P3 |
| Hardcoded credentials | PASS | Pattern scan of tracked files and git history found none | None | None |
| Stale text | WARNING | `run_research.py` docstring says "Patent and X agents are not built yet" and "NEAR testnet"; `funds.yaml` comment on `auto_approve` says "Keep false for now" while the value is `true` | Contradicts the current state | P3 |

Fake or simulated functionality: the paper funds and the shadow trading budget are simulations and are labelled as
such on the site and in the README. No unlabelled simulation was found.

---

## 3. NEAR AI model audit (run live today)

One small call per model to `https://cloud-api.near.ai/v1/chat/completions` with the project's key. All returned HTTP 200.

| Agent(s) | Model asked | Model id returned | Tokens |
|---|---|---|---|
| chief | Qwen/Qwen3.8-27B | Qwen/Qwen3.8-27B | 105 |
| science | deepseek/deepseek-v4.1-flash | deepseek/deepseek-v4.1-flash | 55 |
| patent | Qwen/Qwen3.6-35B-A3B-FP8 | Qwen/Qwen3.6-35B-A3B-FP8 | 211 |
| market | z-ai/glm-5.3 | z-ai/glm-5.3 | 54 |
| x, relevance, topic_review, timing | z-ai/glm-5.3-flash | z-ai/glm-5.3-flash | 75 |
| risk, investment | anthropic/claude-sonnet-5-5 | claude-sonnet-5-5 | 22 |
| trader | anthropic/claude-opus-5-5 | claude-opus-5-5 | 22 |

- All 7 configured ids exist in the live catalogue of 63 models (`list_models.py`, run live today: "Everything matches").
- No agent uses another provider. Every model call goes through one router and one base URL. The Anthropic-named models
  are served by NEAR AI Cloud, not called at Anthropic directly.
- Each agent has a configured fallback model. Fallback behaviour is mock-tested; no fallback was triggered today.
- Token and cost tracking is real: the stopped run logged
  `agent=chief model=Qwen/Qwen3.8-27B tokens=793/1225 cost=$0.00169` and
  `agent=x model=z-ai/glm-5.3-flash tokens=2986/858 cost=$0.00067`.
- Prices in `model_config.yaml` were verified on 2026-11-08 and not re-verified today.

---

## 4. Agent-by-agent results

Source: the saved chiplet report `report_20261110T034939Z` (saved live run, 2026-11-10), total cost $0.373, plus today's
model check. Individual agents were not re-run today.

| Agent | Model in the run | Real data retrieved | Cost | Status |
|---|---|---|---|---|
| Chief | Qwen/Qwen3.8-27B | Plan and gap reviews present | $0.0066 | PASS |
| Science | deepseek/deepseek-v4.1-flash | 8 OpenAlex papers, 8 arXiv preprints | $0.0121 | PASS |
| Patent | (did not run) | None: EPO refused the request that day | – | WARNING |
| Market | z-ai/glm-5.3 | 8 SEC EDGAR filings | $0.0153 | PASS |
| X Intelligence | z-ai/glm-5.3-flash | 15 posts from the X API | $0.0009 + $0.075 X data | PASS |
| Risk | anthropic/claude-sonnet-5-5 | 12 further papers used to challenge the findings | $0.1498 | PASS |
| Investment | anthropic/claude-sonnet-5-5 | Score 72.2 with 8 scored factors | $0.1128 | PASS |
| Timing | z-ai/glm-5.3-flash | 5 Alpha Vantage price series; 1 rate-limit error (CDNS) | $0.0008 | WARNING |

- The Patent agent works in other runs: 31 of the 60 hosted reports include it, among them the newest
  (retrieval-augmented generation, 2026-11-11).
- Error handling is real: the report records the three failures (two EPO, one Alpha Vantage) instead of hiding them,
  and lists the Patent agent under "agents with no analysed evidence".
- Structured output: the report JSON has a fixed section per agent, and claims carry labels.

---

## 5. Research test: chiplet (saved live run, links checked today)

All 55 source links in the report were tested today.

| Source | Count | Result |
|---|---|---|
| Papers with a DOI | 18 | All 18 DOIs resolve. 14 were compared with Crossref: title matches exactly in all 14. 4 could not be compared (2 arXiv DOIs are not in Crossref, 2 were rate-limited) but resolve at doi.org |
| arXiv | 8 | All return 200 |
| SEC EDGAR filings | 8 | All return 200 |
| X posts | 15 | All 15 exist per X's public embed lookup; the author matches the handle in the link |
| Alpha Vantage | 5 | All return 200 |
| Other (one university repository link) | 1 | Returned 418 to the automated check (the server blocks scripts); not confirmed |

- **No fabricated source was found.** Titles are genuine.
- Dates: the report's date and Crossref's year agree, except two papers where the report shows the online date and
  Crossref the journal issue year (2024 vs 2025, 2025 vs 2026). That is normal, not an error.
- Claim labels in the report: 20 verified_fact, 59 ai_interpretation, 17 forecast, 9 unverified_claim, 1 assumption.
  Facts are separated from forecasts.
- Time horizon: the report uses forecasts and a horizon field, but the explicit "1–5 years" framing of the audit brief
  was not tested because the fresh run with that question was stopped.
- Weakness: this report has **no patent evidence** and is sealed on **testnet** (it predates the move to mainnet).

---

## 6. X Intelligence audit

| Check | Status | Evidence |
|---|---|---|
| Read-only | PASS | `app/sources/x.py` has only read methods (user lookup, recent search); no post, like, follow or message method exists |
| Real posts | PASS | 15 of 15 post links confirmed today |
| Post URLs and attribution | PASS | Links are built from the author's handle and the post id; authors match |
| Cost tracking | PASS | $0.005 per post read; $0.075 recorded for the run (15 posts) |
| Does not pretend | PASS | Without `X_BEARER_TOKEN` the agent is skipped and the report says so (mock-tested) |
| Posts never labelled verified fact | PASS | Project rule; enforced in code and tests (mock-tested) |
| Watchlist | PASS | `config/x_watchlist.yaml` exists; not re-resolved against X today |
| Authentication, rate-limit handling, duplicate prevention | Not checked live today | The stopped run made the X model call but the data step was not confirmed. Mock-tested only |

---

## 7. Security findings

| Area | Status | Finding |
|---|---|---|
| Secrets in the repository | PASS | No key pattern in tracked files or in git history; `.env` never committed |
| Secrets in logs | PASS | No print or log of a key, token or prompt found; `preflight.py` prints only "set / missing" |
| CORS | PASS | Only localhost origins; the public site reaches the API through Vercel's proxy |
| Starting research from the web | PASS | Hosted `POST /api/runs` answers 403 (run live today) |
| Proposal sync | PASS | Needs a secret header, compared in constant time; without it 401 (run live today) |
| Input validation | PASS | Topic too short is rejected with 422 (run live today); visitor text is treated as a topic name only |
| SQL injection | PASS | No raw SQL strings; the database layer uses the ORM |
| Hosted API holds no keys | PASS | Render serves a read-only snapshot; signing happens only where the owner put the keys |
| Report paywall | WARNING | The full text of paid reports is in `backend/site_data` in git. Once the repository is public, anyone can read them without paying (P2-4) |
| Proposal limit | WARNING | 5 a day in total, not per visitor: one person can use up the day's proposals (P3) |
| Trading authority | WARNING | `live.auto_approve: true`: the trading agent sends real orders without a per-trade approval. This is the owner's standing decision. Code limits remain: $60 total budget, allowlist, 2% cost cap, kill switch. A judge may still ask about it, so the README should state it in one clear sentence |
| NEAR private keys | PASS | Read from `.env` only; never in the repository, the snapshot or the logs. Key values were not opened in this audit |

---

## 8. Frontend findings

Run live today (HTTP only):

- All pages return 200: `/`, `/research`, `/radar`, `/trading`, `/funds`, `/portfolio`, `/about`, `/runs/<id>`.
- All read API routes return 200 with data: 60 reports over 16 topics, the Radar (54 topics, computed today), trading,
  funds, economy, proposals (open, 4 of 5 left today), market.
- `/runs/<unknown id>` returns HTTP 200 instead of 404 (the page then shows an error). Minor.
- `/api/runs?limit=200` takes 10–11 seconds on the hosted API (measured three times). The home page waits on it.
- 58 of the 60 hosted reports are locked; 2 are open for the demo. A judge can read very few full reports.

Not checked today: layout at 1920 × 1080, mobile view, buttons, loading and empty states, screenshots.

---

## 9. Demo video findings

File: `demo/futurescout_hackathon_demo.mp4` (not in git; a 22 MB copy also exists).

| Check | Status | Evidence |
|---|---|---|
| Resolution | PASS | 1920 × 1080, 30 fps, H.264 |
| Format | PASS | MP4, AAC stereo 48 kHz |
| Length | PASS | 4:13.87 |
| Black scenes | PASS | No black segment of 1 second or longer |
| Subtitles | PASS | 44 subtitle entries, ending at 4:11 |
| Voice | Not checked by ear | ElevenLabs voice "Chris", approved by the owner from a sample; credit shown on the end card |
| Exposed keys | Not re-checked frame by frame today | Frames were reviewed when the video was made |
| Content up to date | FAIL | See below |

The video no longer matches the product:

- It says the agent bought three reports and staked 1.3 NEAR. Now: 6 reports bought, 2.52 NEAR staked.
- It does not show the "Request a report" page (Agent Market link and free topic proposals with an AI reviewer).
- It presents reports as paid only; new reports are now open "for demo purpose only".
- The trading rules changed (no fixed confidence minimum, no fixed price band).
- The Radar shown predates today's patent counts for all 54 topics.

---

## 10. NEAR Hackathon readiness and score

| Question | Answer |
|---|---|
| Genuinely uses NEAR AI? | Yes. Every model call goes to NEAR AI Cloud; verified live today |
| Real multi-agent architecture? | Yes. A LangGraph workflow, separate prompts, separate models, separate cost lines |
| Meaningful role per agent? | Yes. Risk deliberately uses a different model family to challenge the others |
| NEAR integration functional and meaningful? | Yes. Mainnet seals verifiable from the site, agent-to-agent payments in NEAR, staking with NEAR AI, an Agent Market listing |
| Can a judge reproduce the demo? | Not yet: the repository is private. The live site works without setup |
| README clear? | Yes, including a no-keys quick start and an honest "what is unfinished" list |
| API dependencies documented? | Yes (`.env.example`, README) |
| Real research results? | Yes. 55 of 55 links in the audited report are genuine |
| Clear reason for multiple agents? | Yes: separate evidence types, an independent challenger, and two agents that trade with each other |
| Differentiated? | Yes: the agent economy and the on-chain audit trail. The research-agent idea alone is common |

| Category | Points | Reason |
|---|---|---|
| Product functionality (20) | 16 | Everything deployed and answering; slow report list; real swaps limited by an outside liquidity problem |
| AI and multi-agent (20) | 16 | Real and verified; patent evidence missing in part of the reports; agents not re-run individually today |
| NEAR integration (20) | 17 | Mainnet seals, payments, staking, Agent Market; only one real holding and older seals on testnet |
| Research quality and evidence (15) | 12 | Sources genuine and labelled; gaps from rate limits; confidence often low |
| User experience (10) | 7 | Not visually re-tested today; most reports locked for a visitor |
| Technical quality and security (10) | 7 | 335 tests, no leaked secrets; paywall bypass once public; some stale text |
| Presentation and documentation (5) | 3 | Good README; video outdated; repository private |
| **Total** | **78** | |

---

## 11. Issues by priority

**P0 (critical): none.**

**P1 (high) — submission blockers, not code defects**

- P1-1. The repository is private. Judges cannot inspect or reproduce it. Making it public is the owner's decision
  (and see P2-4).
- P1-2. The X demo post and the single submission are not done yet (owner's actions; deadline 2026-11-14 23:59 UTC).

**P2 (medium)**

- P2-1. The demo video is behind the product (section 9). Fix: re-render with current numbers and the new page.
- P2-2. Patent evidence is missing in 29 of 60 reports, including the newest chiplet report, because of EPO or SerpApi
  limits on the day. Fix: re-run the flagship topics when EPO allows, or state the gap on the report page.
- P2-3. `/api/runs?limit=200` takes 10–11 s on the hosted API. Fix: cache the NEAR price used for the lock information
  instead of computing it per report.
- P2-4. Paid reports are readable in the public repository's `backend/site_data`. Fix options: accept and state it
  (demo), or publish only summaries of locked reports in the snapshot.
- P2-5. A judge can open only 2 of 60 reports. Fix: unlock a few more flagship reports for the judging period.
- P2-6. The fresh UCIe / chiplet run and the browser test were not completed in this audit.

**P3 (low)**

- Stale docstring in `backend/scripts/run_research.py` ("Patent and X agents are not built yet", "NEAR testnet").
- Stale comment on `auto_approve` in `backend/config/funds.yaml`.
- Leftover `if True:` in `backend/scripts/fund_trade.py:279`.
- `/runs/<unknown id>` returns HTTP 200.
- Proposal limit is global, not per visitor.
- Alpha Vantage rate-limit errors appear in some reports.
- `cp -n` warning in `deploy/setup_vps.sh`.

---

## 12. Recommended order before submission

1. Decide on making the repository public and how to treat the paid reports in the snapshot (P1-1, P2-4).
2. Unlock a few flagship reports for judges (P2-5).
3. Re-render the video (P2-1).
4. Speed up the report list (P2-3) and fix the stale text (P3).
5. Re-run the browser check at desktop and mobile size, then the X post and the single submission.

Left on disk by this audit: `backend/runs/_audit/` (a copied old report, the partial log of the stopped run and the
link-check results). It is outside git and outside the website data, and can be deleted.
