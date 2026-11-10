# CLAUDE.md

Project: FUTURESCOUT AI (semiconductor research platform). **Read `HANDOFF.md` first**, then `PROJECT_STATUS.md`.

Commands (run from `backend/`, Windows PowerShell, venv at `..\.venv`):
- Install: `python -m pip install -e ".[dev]"`
- Test: `python -m pytest` (tests use fixtures and a mock model; no network, no key)
- Live checks: `scripts\demo_science.py`, `scripts\demo_edgar.py`, `scripts\demo_news.py`, `scripts\list_models.py`, `scripts\run_research.py`

Rules that always apply:
- Never fabricate papers, patents, companies, citations, findings or X handles. URLs come only from API clients.
- Label every claim (verified_fact / ai_interpretation / forecast / assumption / unverified_claim). Headlines and social posts are never verified_fact.
- No hardcoded keys; never commit `.env`; never print or log secrets or prompts.
- Not a trading bot: no real trades, no return promises, no wallet access for agents, no automated X actions.
  Owner decision 2026-11-09: topic funds stages 1-2 are approved: PAPER funds per topic with a rule-based decision
  agent that may decide when/how much to invest *in the simulation*, plus NEAR Intents 1Click DRY-RUN quotes (no signing,
  no deposits).
  Owner decision 2026-11-09 (later the same day), stage 3 go-ahead, exactly this scope: a DEDICATED NEAR mainnet
  account holding about 10 USD of USDC + 0.5 NEAR; a trading agent on a strong model proposes ONE buy from the
  price-checked Ondo allowlist; the owner approves each trade in their own terminal
  (`scripts\fund_trade.py approve <id>`, typed confirmation); limits live in `backend/config/funds.yaml` -> `live`
  (10 USD per trade / per day / in total, raised from 5 by the owner on 2026-11-09 because the market refuses smaller swaps; `trading_enabled: false`); a read-only `/trading` page shows it;
  shadow mode (real quotes, nothing sent) may use a larger pretend budget.
  Claude NEVER: runs `approve` or `intents_probe.py --login` (both sign with the owner's key), sets `trading_enabled: true`,
  turns the kill switch off, raises a cap, or reads/types the mainnet key. Real trades got stuck on 2026-11-09 (see
  STAGE3_PLAN.md): no further real trade until those resolve and the owner says so.
  The near.com-style route (signed order from the private balance, `app/fund/signed_exec.py`) is built and OFF:
  `live.signed_route_enabled: false`. Only the owner sets it to true; Claude never does, and never signs. Any cap
  change needs the owner's words in chat first. Selling, auto-approval and more budget each need a new written yes.
  Trading strategy (owner 2026-11-10): `fund_trade.py check` wakes the agent on triggers; shadow fills itself, live only PROPOSES.
  Claude may run `check --shadow`, `check` (live PROPOSALS only) and `watch`; the owner approves each live proposal.
  `live.auto_approve` (funds.yaml): the owner set it to true on 2026-11-10. Claude never changes it. While it is true, a live
  check signs with the owner's key, so Claude does NOT run live `check` or `watch`: the owner runs the loop; Claude may run `check --shadow`.
- Hosting (2026-11-10): Render (API, read-only snapshot `backend/site_data`, no key) + Vercel (website). See HOSTING.md.
- Say "mock-tested" vs "run live" honestly; never call a feature complete without a test.
- Do not push, make the repo public, post on X, submit to the hackathon or spend on mainnet without the owner's explicit yes.
- Update `PROJECT_STATUS.md` after each phase.
- Owner is a beginner: explain plainly and give exact commands.
