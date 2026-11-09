"use client";

// Earned (report sales on NEAR testnet) against spent (model + X costs): the agent funding its own research.
import Link from "next/link";
import { useEffect, useState } from "react";
import { api, fmtUsd } from "@/lib/api";
import type { Treasury } from "@/lib/types";
import { CountUp } from "./motion";

export function TreasuryPanel() {
  const [t, setT] = useState<Treasury | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { api.treasury().then(setT).catch((e: Error) => setError(e.message)); }, []);
  if (error) return <div className="notice small">Treasury unavailable: {error}</div>;
  if (!t) return <div className="panel small muted">Loading treasury…</div>;
  const ratio = t.spent_usd > 0 ? t.earned_near / t.spent_usd : null;
  return (
    <div className="panel stack treasury" style={{ gap: 18 }}>
      <div className="row" style={{ justifyContent: "space-between", alignItems: "baseline", flexWrap: "wrap", gap: 8 }}>
        <div>
          <div className="eyebrow">Treasury · an agent that pays for its own research</div>
          <h3 className="h3" style={{ margin: "8px 0 0" }}>Earned on NEAR testnet vs spent on research</h3>
        </div>
        <span className="small muted">{t.seller_account ?? "seller not configured"} · testnet</span>
      </div>
      <div className="stats">
        <div className="stat"><div className="stat-value"><CountUp value={t.earned_near} decimals={2} /><span style={{ fontSize: 22 }}> Ⓝ</span></div><div className="stat-label">earned from {t.sales} report sale{t.sales === 1 ? "" : "s"}</div></div>
        <div className="stat"><div className="stat-value">{t.balance ? <><CountUp value={t.balance.available_near} decimals={2} /><span style={{ fontSize: 22 }}> Ⓝ</span></> : "–"}</div><div className="stat-label">{t.balance ? "account balance now (on-chain view)" : t.balance_error ? "balance unavailable" : "balance not read"}</div></div>
        <div className="stat"><div className="stat-value">{fmtUsd(t.spent_usd)}</div><div className="stat-label">spent on {t.runs} research run{t.runs === 1 ? "" : "s"} (models + X data)</div></div>
        <div className="stat"><div className="stat-value">{t.avg_cost_per_run_usd != null ? fmtUsd(t.avg_cost_per_run_usd) : "–"}</div><div className="stat-label">average cost of one report</div></div>
      </div>
      <p className="small" style={{ color: "var(--text-2)", margin: 0 }}>
        Each report costs about {t.avg_cost_per_run_usd != null ? fmtUsd(t.avg_cost_per_run_usd) : "–"} to produce and sells for {t.price_near} Ⓝ.
        {ratio != null && t.sales > 0 ? ` So far ${t.earned_near} Ⓝ has come in against ${fmtUsd(t.spent_usd)} out.` : ""} {t.note}
      </p>
      {t.recent_sales.length > 0 && (
        <div className="table-wrap">
          <table className="table">
            <thead><tr><th>When</th><th>Report</th><th>Buyer</th><th className="num">Paid</th><th>Transaction</th></tr></thead>
            <tbody>{t.recent_sales.map((s) => (
              <tr key={s.tx_hash}>
                <td className="small muted">{s.purchased_at ? new Date(s.purchased_at).toLocaleString() : "–"}</td>
                <td><Link href={`/runs/${s.run_id}`}>{s.topic}</Link></td>
                <td className="mono small">{s.buyer}</td>
                <td className="num">{s.amount_near} Ⓝ</td>
                <td><a className="mono small" href={s.explorer_url} target="_blank" rel="noopener noreferrer">{s.tx_hash.slice(0, 10)}… ↗</a></td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      )}
    </div>
  );
}
