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
