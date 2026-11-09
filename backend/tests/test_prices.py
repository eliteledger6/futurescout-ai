

def test_alpha_vantage_notice_never_carries_the_api_key():
    import pytest
    from app.sources.base import SourceError
    from app.sources.prices import parse_daily
    with pytest.raises(SourceError) as e:
        parse_daily({"Information": "We have detected your API key as ABCD1234EFGH5678 and our standard API rate limit is 25 requests per day."}, "TER")
    assert "ABCD1234EFGH5678" not in e.value.message and "***" in e.value.message
