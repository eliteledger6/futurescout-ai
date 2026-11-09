# FUTURESCOUT AI — demo video script and shot list

Target length: 2 min 30 s – 3 min. Record at 1920×1080 (or 1280×720), browser zoom 100%, dark theme.
Before recording: API running (`python scripts\serve.py` in `backend/`), dashboard running (`npm run dev` in `frontend/`),
open `http://localhost:3000` and let it load once so the data is cached. Close other tabs. Mute notifications.

Windows screen recorder: `Win + G` → Capture → Record (saves to `Videos\Captures`). OBS also works.

Say the lines in your own words if you prefer; the facts in them are all true for the current build.
Numbers (score 63.1, 69 sources, 37 accounts, 0.1 NEAR) match the saved high bandwidth memory report; check them on screen before you speak.

| # | Time | Screen / action | Say |
|---|------|-----------------|-----|
| 1 | 0:00–0:15 | Home page, hero. Don't scroll yet. | "FUTURESCOUT AI is a team of eight AI agents that finds the next hot semiconductor technology and shows the evidence. It reads papers, patents, SEC filings and X posts. Every claim carries a label and its sources, and every report is sealed on NEAR." |
| 2 | 0:15–0:30 | Click **Radar** in the nav. Hover a row so it highlights; click **co-packaged optics** to open the detail charts. | "The radar ranks topics by how fast papers and patent filings are growing year over year. It is pure counting — no model, no opinion. Co-packaged optics and high bandwidth memory are the hottest right now." |
| 3 | 0:30–0:55 | Back to home, scroll to **How the agents work together**. Hover **Chief**, then **Risk challenge**, then **NEAR record** so the detail card changes. | "A research run is twelve steps. The Chief plans the searches. Science, Risk, Market, X and Patent agents work in parallel. The Chief reviews, the Risk agent argues against the findings and checks how far prices have already run, and the Investment agent writes the report. Every agent runs on a model from NEAR AI Cloud." |
| 4 | 0:55–1:15 | Scroll up to the **Autonomous watch** panel. Point at "Research it started" and the decision log. | "It also runs on its own. Every two hours the X agent reads the approved accounts, counts which topics are rising, and may propose new ones tied to real posts. When a topic is hot and has no fresh report, a full research run starts automatically, within a daily budget. Every decision is logged with its reason." |
| 5 | 1:15–1:30 | Scroll to **Research reports**, click the **high bandwidth memory** report with score 63. Pause on the hero: agent pills and the green NEAR badge. | "Here is a report on high bandwidth memory. Seven agents ran: forty-nine findings, sixty-nine sources. The green badge says the report is unchanged since it was recorded on NEAR testnet." |
| 6 | 1:30–1:45 | Click **Score** in the sticky navigator. Let the gauge animate. | "The score is built dimension by dimension, and its confidence can never be higher than the confidence of the evidence it cites. Headlines and social posts never count as verified facts." |
| 7 | 1:45–2:00 | Click **Evidence**. Hover one finding so the label and excerpt are visible. | "Every finding carries a label — verified fact, interpretation, forecast, assumption or unverified claim — and the exact excerpt it came from. A verified fact must point to a real source and quote it exactly; a citation guard checks this in code, not in a prompt." |
| 8 | 2:00–2:15 | Click the green **Unchanged since recorded on NEAR testnet** badge; the NEAR explorer opens in a new tab. Show the transaction, then close the tab. | "Sealing means the report's SHA-256 fingerprint is written to NEAR SocialDB on testnet. Anyone can recompute it and compare it with the chain, so a report cannot be quietly edited after the fact." |
| 8b | 2:15–2:35 | Open the newest **co-packaged optics** report, click **Emerging companies** in the navigator. Click the top row (FormFactor) so the reasons and sources unfold. | "Instead of only naming the giants everyone knows, the Company Scout collects every company behind the evidence: patent assignees, paper authors' employers and SEC filers. It matches them to the SEC ticker file, pulls their financials, and scores smaller, growing, R&D-heavy names as possible next runners. A heuristic, labelled forecast, never a recommendation." |
| 9 | 2:35–2:50 | Click **Market** in the nav. Show the price, "purchases recorded", and the **How a bot buys a report** steps. | "FUTURESCOUT is an agent that earns. Summaries and scores are free; the full evidence unlocks after a payment of 0.1 NEAR to its account. The API reads the transfer from the chain before unlocking." |
| 10 | 2:50–3:05 | Switch to a terminal in `backend/`. Run `python scripts\buyer_bot.py --dry-run` (free, sends nothing) — or, if you want a live purchase on camera, `python scripts\buyer_bot.py` (0.1 testnet NEAR, needs the buyer key in `.env`). | "A separate buyer bot picks the hottest topic, pays on testnet, downloads the report and checks the fingerprint against NEAR. This is a real testnet purchase, not a mock." |
| 10b | 3:05–3:20 | Back on **Market**, scroll to the **Treasury** panel (earned Ⓝ, balance read from chain, spent on research). | "The agent pays for its own work. Each report costs about twenty cents of model and data; buyers pay 0.1 NEAR on testnet. The treasury shows what came in, what went out, and the account balance read live from the chain." |
| 10c | 3:20–3:40 | Click **Portfolio** in the nav. Point at the "simulation" wording and the benchmark column. | "Does the research point at winners? The paper portfolio is a simulation: every sealed report buys its top scout candidates with pretend money at the first close after the report date, and tracks them against the SOXX ETF. Nothing is traded, and the positions come from reports fingerprinted on NEAR, so they cannot be backdated." |
| 11 | 3:40–3:50 | Back to the dashboard home. | "FUTURESCOUT AI: models on NEAR AI Cloud, reports sealed and sold on NEAR, and an agent that funds its own research. Testnet only, and not financial advice. Thank you." |

If you need to stay under 3 minutes, drop scenes 4 (watch) and 10c (portfolio) and shorten 3.

## NEAR points to make sure the judges hear
1. All agent models are called through **NEAR AI Cloud** (`cloud-api.near.ai`), one model per agent, configurable.
2. Every report is **sealed on NEAR testnet** (SocialDB `v1.social08.testnet`): fingerprint on chain, verified live by the API.
3. The agent **earns**: reports are sold for NEAR; payment verified on chain; a demo buyer bot completes the loop.
4. Autonomy: watch mode triggers research by itself, with a daily budget and a public decision log.

## Honesty rules for the recording
- Say "testnet" every time money is mentioned. Never say or imply returns.
- Do not call the X posts or news facts; the UI labels them "unverified claim" for a reason.
- If a live call fails on camera (X rate limit, SEC slow), say so and move on; the saved report still works offline.

## Automatic version
`demo/build_demo.py` builds a narrated MP4 from headless screenshots of the running dashboard
(see the top of that file for the command). It uses the same lines as this table.
