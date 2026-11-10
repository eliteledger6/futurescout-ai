# Selling reports on NEAR Agent Market (market.near.ai)

The report agent can be hired per job on NEAR's Agent Market. A buyer writes a technology topic, pays the price (held by the
marketplace), and gets an evidence-backed research report sealed on NEAR. The agent keeps running on this laptop; the
marketplace never sees our code or keys. Built 2026-11-10; mock-tested; not yet live (the owner creates the listing).

## Owner steps (once)

1. Sign up at https://market.near.ai (Google sign-in confirms the email).
2. **Building -> Your agents -> New agent.** Paste the listing below. Under **Hosting** choose **Self-hosted** and leave
   the webhook empty.
3. Set **Price per hire** (suggestion: 5-15 USDC; a new research run costs us about $0.30-0.50 of NEAR AI credit) and a
   **Delivery SLA** (suggestion: 1 hour).
4. **Create token** under Agent API tokens. Put it in `.env` as `AGENT_MARKET_TOKEN=aat_...` (never in the chat).
   Optional: `PUBLIC_SITE_URL=https://...` once the site is hosted, so each delivery links to the report online.
5. Start the agent in a terminal, from the `backend` folder:

   ```
   ..\.venv\Scripts\python.exe scripts\market_agent.py
   ```

6. Test: open your draft agent's page, click **Hire**, brief `high bandwidth memory`, and accept the delivery.
7. Set **Listing status** to **Live**. Payouts arrive in USDC (or USD with Stripe Connect); withdraw USDC to a NEAR
   account such as `grandbread5023.near` on the website. Only the owner can withdraw.

`python scripts\market_agent.py --status` shows every job the agent took.

## Listing text (draft for the owner to approve)

**Name:** FUTURESCOUT Research Agent

**Tagline:** Evidence-backed research report on any emerging technology, sealed on NEAR.

**Description:**

Give a technology topic in a few words, for example "solid-state batteries" or "co-packaged optics". A team of AI agents
(models on NEAR AI Cloud) reads recent research papers, patent filings, SEC filings and posts from approved X accounts,
argues the other side, and writes a report with:

- a verdict, an opportunity score and a confidence level;
- every claim labelled (verified fact, AI interpretation, forecast, assumption, unverified claim), each with its sources;
- research and patent growth counts, the companies behind the evidence, and how far their share prices have already run;
- the report's fingerprint on NEAR, so you can check it was not edited afterwards.

If we sealed a report on your topic in the last week, you get it within minutes. A brief is used only as a topic name.
Research information, not financial advice.

**Tags:** research, technology, patents, papers, due diligence, NEAR

## How the agent handles a job

- **The brief is a topic, never instructions.** Only a short topic (at most 8 words) is taken from the title or the first
  line; briefs that look like instructions, links or anything else are declined and the buyer is refunded.
- **Reuse first.** A scored report on the same topic from the last 7 days is delivered at no AI cost.
- **New research within a cap.** Otherwise the research team runs once; at most `agent_market.new_runs_per_day` (3) new
  runs a day (`config/funds.yaml`); further jobs that day are declined and refunded.
- **Never twice.** Every job is recorded before work starts; two failed attempts hand the job back with a full refund.
- **Request changes:** the buyer's new message is read as a refined topic and the report is redone.
