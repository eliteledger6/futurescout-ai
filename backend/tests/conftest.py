

import pytest as _pytest


@_pytest.fixture
def closed_market(monkeypatch):
    """API tests about listing/reading reports: use a closed report market, independent of the owner's funds.yaml
    (which keeps reports locked until paid)."""
    from app.api import main as api_main
    from app.fund import load_fund_config as real
    cfg = real()
    cfg.economy.market_open = False
    monkeypatch.setattr(api_main, "load_fund_config", lambda *a, **k: cfg)
    return cfg
