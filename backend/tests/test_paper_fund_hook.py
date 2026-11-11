"""Every new report gets its paper fund: funds.py is started for the report's topic, and a failure never breaks the run.
The subprocess is faked (no prices, no seal)."""
import subprocess
from types import SimpleNamespace

from app.paper_fund_hook import MAX_PRICE_REQUESTS, build_paper_fund


def test_builds_the_fund_for_the_reports_topic():
    seen, logs = [], []

    def run(cmd, **kw):
        seen.append((cmd, kw["cwd"]))
        return SimpleNamespace(returncode=0, stdout="retrieval-augmented generation: invested in 4 companies\n", stderr="")
    assert build_paper_fund("retrieval-augmented generation", log=logs.append, run=run) is True
    cmd, cwd = seen[0]
    assert cmd[1:] == ["scripts/funds.py", "--topic", "retrieval-augmented generation", "--max-price-requests", str(MAX_PRICE_REQUESTS)]
    assert cwd.endswith("backend") and "invested in 4 companies" in logs[0]


def test_a_fund_problem_never_breaks_the_report():
    logs = []
    assert build_paper_fund("x", log=logs.append, run=lambda *a, **k: SimpleNamespace(returncode=1, stdout="", stderr="boom\n")) is False
    assert "failed (boom)" in logs[-1]

    def slow(*a, **k):
        raise subprocess.TimeoutExpired(cmd="funds", timeout=1)
    assert build_paper_fund("x", log=logs.append, run=slow) is False and "did not finish" in logs[-1]
    assert build_paper_fund("  ", log=logs.append, run=slow) is False                 # no topic: nothing started
