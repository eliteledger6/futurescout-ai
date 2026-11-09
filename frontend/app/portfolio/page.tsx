"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { CountUp, Reveal } from "@/components/motion";
import { ErrorNotice, Loading } from "@/components/ui";
import { api, fmtDate } from "@/lib/api";
import type { Portfolio, Position } from "@/lib/types";

const pct = (v: number | null | undefined, d = 1) => (v == null ? "–" : `${v > 0 ? "+" : ""}${v.toFixed(d)}%`);
const usd = (v: number | null | undefined) => (v == null ? "–" : `$${v.toLocaleString(undefined, { maximumFractionDigits: 0 })}`);
const tone = (v: number | null | undefined) => (v == null ? "var(--text-2)" : v >= 0 ? "var(--accent)" : "var(--l-danger)");

export default function PortfolioPage() {
  const [pf, setPf] = useState<Portfolio | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { api.portfolio().then(setPf).catch((e: Error) => setError(e.message)); }, []);

  const s = pf?.summary;
  return (
    <>
      <section className="hero" style={{ padding: "84px 0 60px" }}>
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">Paper portfolio · simulation · no money moves</div>
          <h1 className="display" style={{ fontSize: "clamp(40px, 6vw, 76px)" }}>What if someone had <span className="gradient-text">acted on the reports?</span></h1>
          <p className="lede">Each sealed report &quot;buys&quot; its top Company Scout candidates with a fixed pretend amount at the first close after the report date.
            The positions are derived from reports fingerprinted on NEAR, so nothing can be backdated. A way to check whether the research points at companies
            that later did well; <strong>not</strong> advice, not a track record to invest on.</p>
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          {error ? <ErrorNotice error={error} /> : !pf || !s ? <Loading lines={4} /> : (
            <>
              <Reveal>
                <div className="stats">
                  <div className="stat"><div className="stat-value" style={{ color: tone(s.return_pct) }}>{s.return_pct == null ? "–" : <><CountUp value={Math.abs(s.return_pct)} decimals={1} prefix={s.return_pct >= 0 ? "+" : "−"} suffix="%" /></>}</div><div className="stat-label">simulated return, price only</div></div>
                  <div className="stat"><div className="stat-value" style={{ color: tone(s.benchmark_return_pct) }}>{pct(s.benchmark_return_pct)}</div><div className="stat-label">{pf.benchmark?.ticker ?? "benchmark"} over the same dates</div></div>
                  <div className="stat"><div className="stat-value">{usd(s.value_usd)}</div><div className="stat-label">pretend value of {usd(s.invested_usd)} invested</div></div>
                  <div className="stat"><div className="stat-value">{s.open}<span className="muted" style={{ fontSize: 22 }}> / {s.positions}</span></div><div className="stat-label">positions priced, from {s.reports} report{s.reports === 1 ? "" : "s"}</div></div>
                </div>
              </Reveal>

              {!pf.prices_configured && (
                <div className="notice notice-warn">Prices are not configured (<span className="mono">ALPHA_VANTAGE_API_KEY</span>, free key). Positions are recorded as
                  &quot;pending&quot; and will be priced from the first close after each report date once <span className="mono">python scripts\portfolio.py</span> runs.</div>
              )}
              {pf.prices_configured && s.pending > 0 && (
                <div className="notice small">{s.pending} position{s.pending === 1 ? "" : "s"} still pending: run <span className="mono">python scripts\portfolio.py</span> in the backend folder to price them
                  (Alpha Vantage free plan: 25 requests a day).</div>
              )}

              <div className="table-wrap">
                <table className="table radar-table">
                  <thead><tr><th>Report</th><th>Company</th><th className="num">Scout score</th><th className="num">Entry</th><th className="num">Last</th><th className="num">Pretend value</th><th className="num">Return</th><th>Status</th></tr></thead>
                  <tbody>{pf.positions.map((p) => <Row key={`${p.run_id}-${p.ticker}`} p={p} />)}</tbody>
                </table>
              </div>
              {pf.positions.length === 0 && <div className="notice small">No positions yet: the Company Scout has not named an SEC-listed candidate in any saved report.</div>}

              <div className="panel stack" style={{ gap: 8 }}>
                <h3 className="h3" style={{ margin: 0 }}>How this simulation works</h3>
                <ul className="small" style={{ color: "var(--text-2)", margin: 0, paddingLeft: 18 }}>
                  {pf.notes.map((n) => <li key={n}>{n}</li>)}
                  <li>Pretend notional per position: {usd(pf.notional_usd)}; up to {pf.positions_per_report} candidates per report (highest next-runner score first).</li>
                  <li>Prices: Alpha Vantage daily closes (last ~100 trading days){pf.prices_updated_at ? `, last refreshed ${fmtDate(pf.prices_updated_at)}` : ""}.</li>
                </ul>
                <p className="small muted" style={{ margin: 0 }}>{pf.disclaimer}</p>
              </div>
            </>
          )}
        </div>
      </section>
    </>
  );
}

function Row({ p }: { p: Position }) {
  const badge = p.status === "open" ? <span className="pill pill-on">priced</span>
    : p.status === "error" ? <span className="pill" style={{ color: "var(--l-danger)", borderColor: "var(--l-danger)" }}>error</span>
    : <span className="pill">pending</span>;
  return (
    <tr>
      <td><Link href={`/runs/${p.run_id}`}>{p.topic}</Link><div className="small muted">{p.report_date}</div></td>
      <td><strong>{p.company}</strong> <span className="muted mono small">{p.ticker}</span></td>
      <td className="num">{p.next_runner_score != null ? p.next_runner_score.toFixed(0) : "–"}</td>
      <td className="num">{p.entry_close != null ? <>{p.entry_close.toFixed(2)}<div className="small muted">{p.entry_date}</div></> : "–"}</td>
      <td className="num">{p.last_close != null ? <>{p.last_close.toFixed(2)}<div className="small muted">{p.last_date}</div></> : "–"}</td>
      <td className="num">{usd(p.value_usd)}</td>
      <td className="num" style={{ color: tone(p.return_pct), fontWeight: 600 }}>{pct(p.return_pct, 2)}</td>
      <td>{badge}{p.note && <div className="small muted" style={{ maxWidth: 260 }}>{p.note}</div>}</td>
    </tr>
  );
}
