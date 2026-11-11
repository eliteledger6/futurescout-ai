# Hosting the site (laptop can be off)

- **API** (the data): Render, free plan. It serves a snapshot of the reports, funds and trading record in `backend/site_data`.
- **Website**: Vercel, free plan. It forwards `/api/...` calls to the Render API.

Hosted copy is read-only: no database, no model calls, no new runs and **no private key**, so it can never trade.
Your laptop keeps doing the research and trading; you publish fresh data with three commands (bottom of this page).

## 0. Push the code to GitHub (once)
The repo must be on GitHub first (private is fine): `git push -u origin main`.

## 1. API on Render (about 10 minutes)
1. Go to https://render.com, click **Get Started**, sign up **with GitHub**.
2. When Render asks for GitHub access, allow it for the `futurescout-ai` repository (private repos are fine).
3. In the Render dashboard click **New +** -> **Blueprint**.
4. Pick the `futurescout-ai` repository. Render finds `render.yaml` and shows one service: `futurescout-api`.
5. It asks for one value, `FUND_MAINNET_ACCOUNT_ID`: type your trading account's public name (the `.near` / long hex account
   name, the same as in your `.env`). This only shows balances. **Never paste a private key into Render.**
6. Click **Apply**. The first build takes 5-10 minutes. When it says **Live**, copy the address at the top,
   like `https://futurescout-api-xxxx.onrender.com`.
7. Check it: open `<that address>/api/health` in the browser. You should see `{"ok":true,"store":"files"}`.

Free plan note: Render puts the API to sleep after 15 minutes without visitors; the next visit waits about a minute while
it wakes up. To keep it awake, make a free monitor at https://uptimerobot.com (HTTP, every 5 minutes) on
`<Render address>/api/health`.

## 2. Website on Vercel (about 5 minutes)
1. Go to https://vercel.com, sign up **with GitHub**, allow access to the `futurescout-ai` repository.
2. **Add New...** -> **Project** -> **Import** `futurescout-ai`.
3. **Root Directory**: click **Edit** and choose `frontend`. Framework is detected as **Next.js**.
4. Open **Environment Variables** and add: Name `API_INTERNAL_URL`, Value = the Render address from step 1.6
   (no slash at the end).
5. Click **Deploy**. After 2-3 minutes you get an address like `https://futurescout-ai.vercel.app`. That is the link for judges.
   It stays the same; every push to GitHub updates it.

## 3. Publishing fresh data (after new reports or trades)
From the `backend` folder:

```
..\.venv\Scripts\python.exe scripts\export_site.py
git add site_data
git commit -m "Site data update"
git push
```

Render and Vercel redeploy by themselves within a few minutes.

## If something is wrong
- Website shows "Could not reach the API": the Render API is asleep (wait a minute and refresh) or `API_INTERNAL_URL` is wrong
  (Vercel -> Project -> Settings -> Environment Variables; after changing it, Deployments -> ... -> **Redeploy**).
- Render build failed: open the service -> **Logs**, copy the last lines into the chat.

## Notes from the first deploy (2026-11-10)
- Live: API https://futurescout-ai.onrender.com (Render, built with `backend/Dockerfile`), website https://futurescout-ai.vercel.app.
- Render builds the Docker image, so anything the hosted API needs must be copied in `backend/Dockerfile` (it ships `site_data`).
- `/api/health` shows which data folder is served and how many reports it holds (`"data":"site_data","reports":59`).
- A manually created Render service may not redeploy on push: use **Manual Deploy -> Deploy latest commit**, or turn Auto-Deploy on.

## Topic proposals on the hosted site (2026-11-11)
Visitors can propose a topic on `/research`. The hosted API only stores proposals; the report agent on the owner's laptop
collects them, lets the AI reviewer screen them, researches the approved ones and (with `--publish`) puts the reports online.

1. Make a secret (any long random text). From the `backend` folder: `..\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))"`
2. Render -> the API service -> **Environment** -> add `PROPOSALS_TOKEN` = that secret -> save (it redeploys).
3. In the laptop's `.env` add the same `PROPOSALS_TOKEN=...` and `PUBLIC_API_URL=https://futurescout-ai.onrender.com`.
4. Run the report agent: `..\.venv\Scripts\python.exe scripts\market_agent.py --publish`

Without `PROPOSALS_TOKEN` on Render the hosted page says proposals are closed. Proposals stored on Render since the last
collection are lost when it redeploys or restarts, so keep the report agent running when you expect visitors.

## Keeping everything alive (2026-11-11)
- The website (Vercel + Render) runs by itself. The agents run on the owner's laptop while `start_report_agent.bat` is open:
  double-click it (it restarts the report agent if it ever stops). To start it with Windows: press Win+R, type
  `shell:startup`, and put a shortcut to `start_report_agent.bat` in the folder that opens.
- Keep the laptop plugged in and stop it from sleeping (Settings -> System -> Power -> Screen and sleep -> "When plugged in,
  put my device to sleep after": Never). A sleeping laptop answers nothing.
- While the agent runs it contacts the hosted API every minute, which also keeps the free Render service awake.
- The trading loop (`scriptsund_trade.py watch`) is separate and started by hand, only when NEAR Intents works.
