"use client";

import "../funds.css";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { TIERS, TierBar, TierLegend, ValueLine, pct, tone, usd } from "@/components/FundBits";
import { CountUp, Reveal } from "@/components/motion";
import { ErrorNotice, Loading } from "@/components/ui";
import { api, fmtDate } from "@/lib/api";
import type { FundDecision, FundHolding, TopicFund } from "@/lib/types";

const TIER_LABEL: Record<string, string> = Object.fromEntries(TIERS.map((t) => [t.key, t.label]));

export default function FundPage() {
  const { slug } = useParams<{ slug: string }>();
  const [f, setF] = useState<TopicFund | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { api.fund(slug).then(setF).catch((e: Error) => setError(e.message)); }, [slug]);

  if (error) return <section className="section"><div className="container"><ErrorNotice error={error} /></div></section>;
  if (!f) return <section className="section"><div className="container"><Loading lines={6} /></div></section>;
  const s = f.summary;
  const last = f.decisions[f.decisions.length - 1];
  return (
    <>
      <section className="section" style={{ paddingTop: 48 }}>
        <div className="container stack">
          <div className="small"><Link href="/funds">← All topic funds</Link></div>
          <div className="eyebrow">Topic fund · simulation · pretend money, real prices</div>
          <h1 className="display" style={{ margin: 0, fontSize: "clamp(32px, 5vw, 56px)" }}>{f.topic}</h1>

          <Reveal>
            <div className="stats">
              <div className="stat"><div className="stat-value">{usd(s.value_usd)}</div><div className="stat-label">pretend value (started at {usd(f.start_cash_usd)})</div></div>
              <div className="stat"><div className="stat-value" style={{ color: tone(s.return_pct) }}><CountUp value={Math.abs(s.return_pct)} decimals={2} prefix={s.return_pct >= 0 ? "+" : "−"} suffix="%" /></div><div className="stat-label">fund return, after assumed costs</div></div>
              <div className="stat"><div className="stat-value" style={{ color: tone(s.benchmark_return_pct) }}>{pct(s.benchmark_return_pct, 2)}</div><div className="stat-label">S&amp;P 500 ({f.benchmark}) over the same dates</div></div>
              <div className="stat"><div className="stat-value">{s.invested_pct.toFixed(0)}%</div><div className="stat-label">invested now · {s.holdings} holdings</div></div>
            </div>
          </Reveal>

          <div>
            <TierBar tiers={s.tiers_usd} cash={s.cash_usd} total={s.value_usd} />
            <div style={{ marginTop: 8 }}><TierLegend /></div>
          </div>

          {f.history.length > 0 && (
            <div>
              <ValueLine points={f.history} start={f.start_cash_usd} height={120} className="fund-chart" />
              <p className="small muted" style={{ marginTop: 4 }}>Solid = fund, dashed = S&amp;P 500, both from {usd(f.start_cash_usd)}. One point per update.</p>
            </div>
          )}

          {last && (
            <div className="notice">
              <b>Latest decision ({fmtDate(last.at)}):</b> report verdict <span className="pill band-pill">{last.band}</span>
              {last.score != null && <> score {last.score}</>} → target <b>{last.target_invested_pct}%</b> invested.
              {last.staged_tiers.length > 0 && <> Staged entry for the {last.staged_tiers.join(", ")}-risk tier (stocks look stretched).</>}
              {" "}<Link href={`/runs/${last.run_id}`}>Open the report →</Link>
            </div>
          )}
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          <h2 className="h2">Holdings</h2>
          <p className="sub">Companies from the latest report, grouped by size. &quot;NEAR Intents&quot; shows whether a tokenized version can be swapped
            through the public NEAR Intents API today and, if so, a real dry-run quote for the holding&apos;s value (nothing is sent).</p>
          <div className="table-wrap">
            <table className="table">
              <thead><tr><th>Company</th><th>Tier</th><th className="num">Pretend value</th><th className="num">Return</th><th>Price stretch</th><th>NEAR Intents</th></tr></thead>
              <tbody>{f.holdings.map((h) => <HoldingRow key={h.ticker} h={h} />)}
                {f.holdings.length === 0 && <tr><td colSpan={6} className="muted">Holding cash only.</td></tr>}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          <h2 className="h2">Decision log</h2>
          <p className="sub">The decision agent follows fixed rules (backend <span className="mono">config/funds.yaml</span>): the fund stays fully invested in the companies the
            report&apos;s patents and papers name, split into low, medium and high risk; the verdict and confidence are recorded with every decision. Each decision&apos;s fingerprint is stored on NEAR testnet.</p>
          <ol className="timeline">{[...f.decisions].reverse().map((d, i) => <DecisionItem key={i} d={d} />)}</ol>
          <ul className="small muted">{f.notes.map((n) => <li key={n}>{n}</li>)}</ul>
        </div>
      </section>
    </>
  );
}

function HoldingRow({ h }: { h: FundHolding }) {
  return (
    <tr>
      <td>{h.company} <span className="muted mono small">{h.ticker}</span><div className="small muted">{h.why}</div></td>
      <td className="small"><i className={`tier-dot tier-${h.tier}`} />{TIER_LABEL[h.tier] ?? h.tier}</td>
      <td className="num">{usd(h.value_usd)}<div className="small muted">{h.last_close != null ? `$${h.last_close.toFixed(2)} · ${h.last_date}` : ""}</div></td>
      <td className="num" style={{ color: tone(h.return_pct) }}>{pct(h.return_pct, 2)}</td>
      <td className="small">{h.timing_risk ?? "–"}</td>
      <td className="small">
        {!h.route ? <span className="muted">not checked</span>
          : h.route.available ? (
            <span className="route-yes" title={h.route.asset_id ?? ""}>{h.route.symbol} on {h.route.blockchain}
              {h.quote && (h.quote.error ? <div className="muted">quote: {h.quote.error}</div>
                : <div className="muted">dry quote: {usd(h.quote.amount_in_usd, 2)} → {usd(h.quote.amount_out_usd, 2)} ({h.quote.cost_pct?.toFixed(2)}% cost)</div>)}
            </span>
          ) : <span className="route-no" title={h.route.note}>no tokenized route yet</span>}
      </td>
    </tr>
  );
}

function DecisionItem({ d }: { d: FundDecision }) {
  const buys = d.trades.filter((t) => t.side === "buy"), sells = d.trades.filter((t) => t.side === "sell");
  return (
    <li>
      <div className="fund-row">
        <b>{fmtDate(d.at)} · <span className="band-pill">{d.band}</span>{d.score != null && ` (${d.score})`} → {d.target_invested_pct}% invested</b>
        {d.chain?.explorer_url ? <a className="small" href={d.chain.explorer_url} target="_blank" rel="noreferrer">sealed on NEAR testnet ↗</a>
          : <span className="small muted">not sealed</span>}
      </div>
      <div className="small" style={{ marginTop: 6 }}>
        {buys.length > 0 && <span className="trade-buy">Bought {buys.map((t) => `${t.ticker} ${usd(t.usd)}`).join(", ")}. </span>}
        {sells.length > 0 && <span className="trade-sell">Sold {sells.map((t) => `${t.ticker} ${usd(t.usd)}`).join(", ")}. </span>}
        {d.trades.length === 0 && <span className="muted">No trades.</span>}
      </div>
      <ul className="reasons">{d.reasons.map((r, i) => <li key={i}>{r}</li>)}</ul>
      {d.sha256 && <div className="small muted mono" style={{ marginTop: 8, wordBreak: "break-all" }}>sha256 {d.sha256}</div>}
    </li>
  );
}
