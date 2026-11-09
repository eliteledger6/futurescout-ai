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
  no deposits). Stage 3 (small real trades, owner approves each, per-trade/daily caps, kill switch, owner-held key in
  `.env`) needs the owner's explicit written go-ahead first; Claude never places trades or handles that key.
- Say "mock-tested" vs "run live" honestly; never call a feature complete without a test.
- Do not push, make the repo public, post on X, submit to the hackathon or spend on mainnet without the owner's explicit yes.
- Update `PROJECT_STATUS.md` after each phase.
- Owner is a beginner: explain plainly and give exact commands.
