"""Application settings, read from environment variables / .env (never hardcoded)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent
CONFIG_DIR = BACKEND_DIR / "config"


class ConfigError(RuntimeError):
    """A required setting (usually an API key) is missing."""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(str(PROJECT_ROOT / ".env"), str(BACKEND_DIR / ".env")),
        env_file_encoding="utf-8",
        extra="ignore",  # .env may already list variables for later phases
    )

    near_ai_api_key: Optional[SecretStr] = None
    near_ai_base_url: str = "https://cloud-api.near.ai/v1"
    openalex_api_key: Optional[SecretStr] = None
    http_user_agent: str = "FuturescoutAI/0.1 (research prototype)"
    # The SEC requires a User-Agent with a real contact email, e.g. "YourName you@example.com"
    edgar_user_agent: Optional[str] = None
    # e.g. postgresql://futurescout:PASSWORD@localhost:5432/futurescout (contains a password: never print it)
    database_url: Optional[SecretStr] = None
    # Alpha Vantage daily prices (free key: 25 requests/day, last 100 trading days)
    alpha_vantage_api_key: Optional[SecretStr] = None

    def alpha_vantage_key_value(self) -> Optional[str]:
        return (self.alpha_vantage_api_key.get_secret_value().strip() or None) if self.alpha_vantage_api_key else None

    # SerpApi Google Patents (owner's account; each request = 1 search of the plan's monthly quota)
    serpapi_api_key: Optional[SecretStr] = None
    # True = spend no SerpApi searches: serve patent data from backend/cache/serpapi only (any age) and
    # report "patent search paused" for topics that are not cached. For saving quota before a demo.
    serpapi_cache_only: bool = False
    # Which patent source a run uses when both are configured: "serpapi" (Google Patents, paid quota) or "epo"
    # (EPO OPS, free ~4 GB/week; live-verified 2026-11-09).
    patent_source: str = "epo"     # owner 2026-11-09: EPO first (free); falls back to SerpApi when EPO keys are missing

    def serpapi_key_value(self) -> Optional[str]:
        return self.serpapi_api_key.get_secret_value().strip() or None if self.serpapi_api_key else None

    # EPO Open Patent Services (free registration at developers.epo.org; free up to 4 GB/week)
    epo_ops_consumer_key: Optional[SecretStr] = None
    epo_ops_consumer_secret: Optional[SecretStr] = None

    def epo_credentials(self) -> Optional[tuple[str, str]]:
        k = self.epo_ops_consumer_key.get_secret_value().strip() if self.epo_ops_consumer_key else ""
        s = self.epo_ops_consumer_secret.get_secret_value().strip() if self.epo_ops_consumer_secret else ""
        return (k, s) if k and s else None

    # NEAR testnet record of report hashes. A DEDICATED testnet account only; mainnet is refused in code.
    near_testnet_account_id: Optional[str] = None
    near_testnet_private_key: Optional[SecretStr] = None

    def near_testnet_credentials(self) -> Optional[tuple[str, str]]:
        acc = (self.near_testnet_account_id or "").strip()
        key = self.near_testnet_private_key.get_secret_value().strip() if self.near_testnet_private_key else ""
        return (acc, key) if acc and key else None

    # Stage 3 live-trading test (owner go-ahead 2026-11-09): a DEDICATED, tiny NEAR MAINNET account. The key is used
    # only by scripts/fund_trade.py approve (run by the owner) and is never logged, stored or returned by the API.
    fund_mainnet_account_id: Optional[str] = None
    fund_mainnet_private_key: Optional[SecretStr] = None
    oneclick_api_key: Optional[SecretStr] = None      # optional NEAR Intents partner key (avoids the extra 0.25% fee)

    # NEAR Agent Market (market.near.ai): the report agent's API token (aat_...), made by the owner on the listing page
    agent_market_token: Optional[SecretStr] = None
    seal_network: str = "testnet"                  # owner 2026-11-10: "mainnet" = seals signed by the report agent's account on NEAR mainnet
    # owner 2026-11-11: "only seal report". Every seal costs NEAR (about 0.013 each on mainnet), and paper-fund decisions
    # are made for every topic every day. Reports are always sealed; these two are off unless set to true in .env.
    seal_fund_decisions: bool = False              # SEAL_FUND_DECISIONS=true: also seal each paper-fund decision
    seal_trades: bool = False                      # SEAL_TRADES=true: also seal each trade record (real and shadow)
    proposals_token: Optional[SecretStr] = None    # shared secret between the hosted API and the owner's report-agent loop
    public_api_url: Optional[str] = None           # the hosted API (e.g. https://futurescout-ai.onrender.com) the loop collects proposals from
    public_site_url: Optional[str] = None          # e.g. the hosted website; put in deliverables as "online: <url>/runs/<id>"

    # Agent economy (owner 2026-11-10): the report agent's own mainnet account; it is paid for reports and stakes for AI credits
    report_agent_account_id: Optional[str] = None
    report_agent_private_key: Optional[SecretStr] = None

    def report_agent_credentials(self) -> Optional[tuple[str, str]]:
        acc = (self.report_agent_account_id or "").strip()
        key = self.report_agent_private_key.get_secret_value().strip() if self.report_agent_private_key else ""
        return (acc, key) if acc and key else None

    def fund_mainnet_credentials(self) -> Optional[tuple[str, str]]:
        acc = (self.fund_mainnet_account_id or "").strip()
        key = self.fund_mainnet_private_key.get_secret_value().strip() if self.fund_mainnet_private_key else ""
        return (acc, key) if acc and key else None

    # Paper portfolio (a SIMULATION: no money moves). Each sealed report "buys" its top Company Scout candidates
    # with a fixed pretend notional, priced at the first close on/after the report date (Alpha Vantage daily data).
    portfolio_notional_usd: float = 10_000.0
    portfolio_positions_per_report: int = 3
    portfolio_benchmark: str = "SOXX"          # ETF ticker compared over the same dates ("" = none)
    portfolio_max_price_requests: int = 20     # Alpha Vantage free plan: 25 requests/day
    # Watch mode (scripts/watch.py): how often the X accounts are scanned and how much may be spent.
    watch_x_interval_minutes: int = 120
    watch_max_runs_per_day: int = 2             # full research runs the watcher may start per day
    watch_report_max_age_days: int = 7          # a topic with a younger report is not researched again
    watch_heat_threshold: float = 40.0          # radar heat (%) that makes a topic worth a run
    watch_x_mentions_threshold: int = 3         # or this many posts about it in one scan
    watch_new_patent_topics_per_week: int = 2   # new topics allowed a live patent count per week (quota)
    watch_paper_discovery_days: int = 7         # how often the paper scout looks for new growing topics per sector (0 = off)
    # X reading (owner 2026-11-09: read more, grow the account list automatically). Every post read costs ~$0.005.
    watch_x_max_posts: int = 100                # newest posts read per scan from the watched accounts
    watch_x_daily_budget_usd: float = 3.0       # stop X reading for the day once this much was spent (0 = no X calls)
    watch_x_discovery_topics_per_day: int = 3   # new topics per day that get an account search on X (~$0.25 each)
    watch_x_endorse_lookups_per_scan: int = 10  # profiles looked up for handles that watched accounts keep @mentioning ($0.01 each)

    # X API (read-only). Pay-per-use: billed per post / user returned.
    x_bearer_token: Optional[SecretStr] = None

    def x_token_value(self) -> Optional[str]:
        if self.x_bearer_token is None:
            return None
        return self.x_bearer_token.get_secret_value().strip() or None
    # Starting a run from the dashboard spends NEAR AI credit (~$0.17 per run, measured), so it is off
    # unless the owner sets ENABLE_RUN_API=true. Browsing saved reports always works.
    enable_run_api: bool = False

    def database_url_value(self) -> Optional[str]:
        if self.database_url is None:
            return None
        return self.database_url.get_secret_value().strip() or None

    def require_near_key(self) -> str:
        if self.near_ai_api_key is None or not self.near_ai_api_key.get_secret_value().strip():
            raise ConfigError(
                "NEAR_AI_API_KEY is not set. Copy .env.example to .env and add your "
                "key from https://cloud.near.ai"
            )
        return self.near_ai_api_key.get_secret_value().strip()

    def openalex_key_value(self) -> Optional[str]:
        if self.openalex_api_key is None:
            return None
        value = self.openalex_api_key.get_secret_value().strip()
        return value or None


def quiet_network_logs() -> None:
    """HTTP libraries log full request URLs at INFO level, and some APIs (OpenAlex) carry the API key
    in the URL. Keep them at WARNING always, even in verbose mode, so keys are never logged.
    (A verbose run on 2026-11-08 printed the OpenAlex key this way; this function is the fix.)"""
    import logging

    for name in ("httpx", "httpx2", "httpcore", "openai", "urllib3"):
        logging.getLogger(name).setLevel(logging.WARNING)


def get_settings() -> Settings:
    return Settings()
