# Running the report agent on a cloud server (laptop off)

The website already runs in the cloud (Vercel + Render). This moves the **report agent** there too: the one program that
takes NEAR Agent Market hires, collects topic proposals, runs the AI reviewer and the research team, seals reports on NEAR
and publishes them to the website. After this the laptop can be off.

The **trading agent** can run there too (owner's decision, 2026-11-11). It is installed switched off, because its key
controls real money: read "Trading agent" below before you turn it on.

Built 2026-11-11. The setup script was syntax-checked and the publishing step was tested on the owner's laptop; the
script itself has **not been run on a real server yet**: the first run is the test.

## What you need
- A small Linux server ("VPS") with **Ubuntu 24.04**, 1 CPU and 2 GB memory is enough (about $5-6 a month at Hetzner,
  DigitalOcean, Vultr and similar). You get an IP address and a root password or SSH key from the provider.
- About 30 minutes.

## Steps

**0. On your laptop, publish the latest records first**, so the server starts from today's data (from `backend`):

```
..\.venv\Scripts\python.exe scripts\export_site.py
```

then, from the main folder: `git pull --rebase`, `git add backend/site_data`, `git commit -m "Site data update"`, `git push`
(if it says "nothing to commit", that is fine).

**1. Connect to the server** from PowerShell on your laptop (use the IP the provider gave you):

```
ssh root@YOUR.SERVER.IP
```

**2. Download and run the setup script** (on the server). The repository is private, so copy the script over first.
On your laptop, in a second PowerShell window, from `D:\FUTURESCOUT AI`:

```
scp deploy\setup_vps.sh root@YOUR.SERVER.IP:/root/
```

Then on the server:

```
bash /root/setup_vps.sh git@github.com:eliteledger6/futurescout-ai.git
```

It stops once and prints a line starting with `ssh-ed25519`. Copy that line, open GitHub -> the repository ->
**Settings -> Deploy keys -> Add deploy key**, paste it, tick **Allow write access**, save. Then press Enter on the server.
(That line is a public key. It only lets this server read and push to this one repository.)

**3. Put your keys on the server.** Open the server's settings file:

```
sudo -u futurescout nano /home/futurescout/futurescout/.env
```

Copy these values from your laptop's `.env` (open it in Notepad next to the terminal). Type or paste them only into this
file, never into a chat:

| Line | Needed for |
|---|---|
| `NEAR_AI_API_KEY` | every agent's model calls |
| `OPENALEX_API_KEY`, `EDGAR_USER_AGENT` | papers, SEC filings |
| `X_BEARER_TOKEN` | X signals |
| `SERPAPI_API_KEY`, `SERPAPI_CACHE_ONLY`, `EPO_OPS_CONSUMER_KEY`, `EPO_OPS_CONSUMER_SECRET` | patents |
| `ALPHA_VANTAGE_API_KEY` | price and timing check |
| `REPORT_AGENT_ACCOUNT_ID`, `REPORT_AGENT_PRIVATE_KEY`, `SEAL_NETWORK=mainnet` | sealing reports on NEAR mainnet |
| `AGENT_MARKET_TOKEN` | NEAR Agent Market jobs |
| `PROPOSALS_TOKEN`, `PUBLIC_API_URL` | topic proposals from the hosted site |

Leave `DATABASE_URL` **empty** (the server keeps reports as files). Leave `FUND_MAINNET_ACCOUNT_ID`,
`FUND_MAINNET_PRIVATE_KEY` and `ONECLICK_API_KEY` empty unless you turn the trading agent on (see below). Save with Ctrl+O, Enter, then Ctrl+X.

**4. Stop the report agent on your laptop** (close the `start_report_agent.bat` window, and remove its shortcut from the
Startup folder). Two agents would both take the same jobs.

**5. Start the agent on the server and watch it:**

```
systemctl start futurescout-agent
journalctl -u futurescout-agent -f
```

It should print `report agent: checking for Agent Market jobs and topic proposals every 60s ...`. Press Ctrl+C to stop
watching (the agent keeps running). Type `exit` to leave the server.

**6. In Render**, open the API service -> **Settings -> Build & Deploy -> Auto-Deploy: On Commit**, so every report the
server publishes appears on the website by itself.

## Trading agent (optional, real money)

The trading agent buys reports from the report agent, trades tokenized stocks through NEAR Intents inside your limits and
stakes the report agent's earnings. On the server it runs as a second service, `futurescout-trader`.

**Before you turn it on**
- Its key signs real orders by itself (`live.auto_approve` is on). Anyone who gets into the server gets that key. Keep
  only the money you are willing to lose in the trading account and its near.com balance; the code's own cap is the
  `live` block in `backend/config/funds.yaml` ($60 in total today).
- Run it in **one place only**. Stop any `fund_trade.py watch` window on your laptop first.
- On 2026-11-10/11 NEAR Intents refused the fund's orders. While that lasts the loop only tries, fails and reports it.

**Turn it on**
1. Add to the server's `.env` (same file as above): `FUND_MAINNET_ACCOUNT_ID`, `FUND_MAINNET_PRIVATE_KEY`, `ONECLICK_API_KEY`.
2. Start it and make it start after reboots:

```
systemctl enable --now futurescout-trader
journalctl -u futurescout-trader -f
```

**Stop it**
- Pause trading but keep the loop: `sudo -u futurescout bash -c "cd ~/futurescout/backend && ../.venv/bin/python scripts/fund_trade.py stop"`
  (the kill switch; `start` instead of `stop` switches it back).
- Stop the loop for good: `systemctl disable --now futurescout-trader`, then delete the three trading lines from `.env`.

**Change a limit** (budget, caps, switches): edit `backend/config/funds.yaml` on your laptop, commit, `git push`, then on the
server run the "Get new code" command below. The server never changes limits by itself.

The website shows a new trade, report purchase or stake a few minutes after it happens (the loop publishes only then,
not after every hourly check).

## Everyday commands (on the server)

| What | Command |
|---|---|
| Is it running? | `systemctl status futurescout-agent` |
| What is it doing? | `journalctl -u futurescout-agent -n 50` |
| What has it done? | `sudo -u futurescout bash -c "cd ~/futurescout/backend && ../.venv/bin/python scripts/market_agent.py --status"` |
| Stop / start | `systemctl stop futurescout-agent` / `systemctl start futurescout-agent` |
| Get new code you pushed | `sudo -u futurescout git -C /home/futurescout/futurescout pull --rebase && systemctl restart futurescout-agent && systemctl try-restart futurescout-trader` |
| Trading agent: running? what is it doing? | `systemctl status futurescout-trader` · `journalctl -u futurescout-trader -n 50` |

## Things to know
- **Keys on a server are a risk.** Use a provider login with two-factor sign-in, log in with an SSH key rather than a
  password if the provider offers it, and keep the server for this one job. Keep only a small balance in the report agent's NEAR wallet (it needs about 0.013 NEAR
  per seal). Move larger amounts, such as NEAR returning from unstaking, to another wallet. If you ever suspect the server,
  make new keys (NEAR AI, X, Agent Market token, a new access key for the report agent account) and delete the old ones.
- **The server becomes the place where new reports are made.** Your laptop's local database stops getting new reports.
  To see the newest data on the laptop, `git pull` and start the API with `FUTURESCOUT_DATA_DIR=site_data`.
- **Before you push code from the laptop, run `git pull --rebase`**: the server pushes site data by itself.
- **Costs keep running while you are away**: at most 5 proposal runs and 3 Agent Market runs a day (about $0.60-1.00 each).
- To move back to the laptop: `systemctl disable --now futurescout-agent` on the server, `git pull` on the laptop, and
  start `start_report_agent.bat` again.
