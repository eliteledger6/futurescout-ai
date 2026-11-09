# Stage 3 plan: small real trades through NEAR Intents (BUILT, SWITCHED OFF, no trade made)

Status 2026-11-09 evening: the owner gave the go-ahead for a first proof trade (about 5 USD + 0.5 NEAR, agent on a
strong model, visible UI). Step C is built and mock-tested; shadow mode has run (real quotes, nothing sent).
`trading_enabled` is false and no fund account is connected, so nothing can be sent yet. See "Where it stands" below.

This is engineering planning, not investment advice. Real money can be lost through price moves, bugs, fees or the
token issuer. Start with an amount you could lose completely without it mattering.

## Where it stands (2026-11-09 evening)

- Built: `app/fund/live.py` (limits, executor, shadow fill), `app/agents/trader` (Claude Opus 5.5 on NEAR AI Cloud),
  `scripts/fund_trade.py` (status / propose / approve / reject / resume / stop / start), `/api/trading` and the
  read-only `/trading` page. 14 tests with a fake chain and a fake 1Click.
- Shadow run: Opus proposed MRVLon; the real dry quote passed every check ("would receive 0.70 MRVLon for $100").
  An earlier GOOGLon proposal was refused by the price check (quote 3.0% above a 3-day-old close); the band now
  widens with the age of the close (3% + 1.5% per extra day, max 8%).
- **Blocker for the 5 USD budget: the market refuses swaps that small ("No liquidity available").** Dry quotes on
  2026-11-09: 8 USD works for INTCon, NVDAon, GOOGLon, QQQon; MSFTon, MRVLon, SPYon need about 30 USD. So the first
  real trade needs a cap of about 10 USD. **The owner raised the cap to 10 USD on 2026-11-09** (per trade, per day and in total).
- Still not verified: the owner's eligibility for Ondo tokens, and how a holding is sold again.

## Live test result (2026-11-09 night): the wallet route got stuck

- Two real buys of GOOGLon were approved by the owner and sent: 10 USD (2.82 NEAR, 13:58 UTC) and 25 USD (6.93 NEAR,
  14:55 UTC), paid from the wallet to 1Click deposit addresses (depositType ORIGIN_CHAIN, recipientType INTENTS).
- Both stayed PROCESSING. The NEAR sits, wrapped, in the swap service's per-swap holding accounts inside intents.near
  (checked on chain). The service replaced the requested 30-minute deadline with its own, 2026-11-12. Kill switch ON.
  References for support (https://t.me/near_intents): deposit addresses dbd82b56...a8a6 and 8db1fe33...931f.
- The owner's manual swaps inside near.com were instant. They are not on the public chain or the public explorer,
  and the near.com balance was never visible on intents.near: near.com appears to use the private "Confidential
  Intents" layer with a signed order from an internal balance.
- Built since, QUOTES ONLY (`app/fund/intents_signed.py`, `scripts/intents_probe.py`): dry quotes on the internal
  route, a real quote + the unsigned order the service generates, and an owner-run login (signs an EMPTY order) that
  reads private balances and quotes the confidential route. There is no submit function.
- Lesson: check the deadline the service RETURNS, and never send a second trade while one is unresolved.
- Also found: rpc.mainnet.near.org and rpc.testnet.near.org are deprecated (HTTP 429); both replaced with FastNEAR.

## What was verified (2026-11-09)

- NEAR Intents lists 28 Ondo tokens on BNB Chain (`GET /v0/tokens?ondoTokens=true`, also the bridge list):
  stocks NVDA, MSFT, GOOGL, META, AMZN, AAPL, TSLA, INTC, MRVL, HOOD, CRCL; the rest are ETFs and funds.
- Dry-run quotes from USDC on NEAR work; quoted cost 0.4-1.4% per trade.
- 10 of the 52 paper-fund holdings have a token (MSFT, GOOGL, META, INTC, MRVL). The other 42 do not, including
  every small company, and Micron, AMD, KLA, Cisco.
- From the 1Click docs: a real swap is `POST /v0/quote` with `dry: false` -> send the pay asset to the returned
  `depositAddress` -> `GET /v0/status` until `SUCCESS` or `REFUNDED`. There is **no testnet**; the docs say to test
  with small amounts. Without an API key every real quote pays an extra 0.25% fee.
- **Not verified:** whether the owner's account is eligible to hold Ondo tokens (Ondo is for eligible non-US
  holders), and exactly how a balance held inside NEAR Intents is sold again (the docs describe a signed-intent flow).

## What stage 3 is, and is not

- IS: a **separate, small, dedicated mainnet account** that buys a few Ondo stock tokens for the topics that have
  them, only after the owner approves each trade, within hard caps.
- IS NOT: an autonomous trading bot, a copy of the full paper funds (only ~20% of holdings can be bought), or
  anything that touches the owner's main wallet.

## Steps

### A. Owner checks, no code (do these first; any "no" stops the plan)
1. On near.com, confirm your country and account are allowed to buy Ondo stocks, and read their terms.
2. Buy about $5 of one token (e.g. SPYon) by hand in near.com, then sell it. This proves eligibility and shows
   the real costs and how selling works, before any code exists.
3. Decide the test budget (suggested: $50 total) and which 1-2 topics to start with (suggested: AI agents, chiplet).

### B. Wallet set-up (owner does it; Claude never sees the key)
4. Create a NEW mainnet account used for nothing else (example name: `futurescout-fund.near`).
5. Fund it with the test budget in USDC plus about 1 NEAR for fees. The account balance is the maximum loss.
6. Put its key in `backend\.env` yourself (`FUND_MAINNET_ACCOUNT_ID`, `FUND_MAINNET_PRIVATE_KEY`). Never in chat,
   never in git. Optional: get a free 1Click partner API key to avoid the 0.25% fee.

### C. Code (Claude builds, mock-tested first; no live call until D)
7. `app/fund/executor.py`: the only module allowed to send funds. Flow per trade: fresh quote -> safety checks ->
   send USDC to the deposit address -> poll status -> record the result.
8. Hard limits, checked in code before every send, all configurable in `config/funds.yaml`:
   - `trading_enabled: false` by default, plus a kill-switch file that stops everything at once;
   - allowlist: only Ondo tokens that pass the symbol + price check;
   - max per trade (suggested $10), max per day ($25), max total ever deposited ($50);
   - quote price within 3% of the stock's last close, max slippage 1%, quote not older than 60 seconds;
   - buys only at first; selling added after step A2 shows how it works.
9. Approval queue: the decision agent only *proposes* trades. Each proposal waits until the owner runs
   `python scripts\fund_trade.py approve <id>` on this laptop. No approval through the website (the site can be
   shared by link; a web button could be clicked by anyone).
10. Records: every proposal, approval, quote, transaction hash and final status is stored and fingerprinted on
    NEAR (same sealing as reports). Refunds and failures are recorded too.
11. Dashboard: a "Live (real money)" section on the fund page, clearly separate from the paper fund, read-only.
12. Tests: executor fully mock-tested (limits, kill switch, refund, failed status, double-send protection).
    One week of "shadow mode": real quotes, proposals and approvals, but the send step is skipped and logged.

### D. First live trade (owner runs every command)
13. Owner sets `trading_enabled: true`, approves ONE $5 buy, and watches it complete or refund.
14. Review together: cost vs quote, time taken, records. Fix anything odd before a second trade.
15. Only then: allow the remaining budget, still one approval per trade.

### E. Later, only if D went well (each needs a new yes)
- Selling and rebalancing; small auto-approved trades under a low cap; one account per topic.

## What Claude will and will not do

- Will: write and test the code, explain each command, review results with you.
- Will not: place, approve or trigger any trade; type, read or handle the wallet key; move funds; raise a limit
  without your instruction; tell you which stocks to buy or when.

## Open risks to accept before starting

- Eligibility or terms may rule this out entirely (step A1).
- Tokens depend on Ondo as issuer and on BNB Chain; they are not the shares themselves.
- Selling is unverified until step A2. Do not buy more than you are willing to leave stuck.
- Costs of 0.4-1.4% each way mean small trades lose money to fees.
- Tax and reporting duties are yours; ask a professional if unsure.

## Go-ahead

To start step C, the owner writes in chat: which topics, the total budget, the per-trade and per-day caps, and that
steps A1-A2 are done. Claude then updates `CLAUDE.md` with exactly those limits and builds C. Step D needs a second
explicit yes.
