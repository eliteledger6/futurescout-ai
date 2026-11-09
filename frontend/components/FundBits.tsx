"use client";

// Small shared pieces for the topic-fund pages (simulation).
import type { FundValuePoint } from "@/lib/types";

export const TIERS = [
  { key: "low", label: "Low risk · large companies" },
  { key: "medium", label: "Medium risk · mid-size" },
  { key: "high", label: "High risk · small companies" },
] as const;

export const pct = (v: number | null | undefined, d = 1) => (v == null ? "–" : `${v > 0 ? "+" : ""}${v.toFixed(d)}%`);
export const usd = (v: number | null | undefined, d = 0) =>
  v == null ? "–" : `$${v.toLocaleString(undefined, { minimumFractionDigits: d, maximumFractionDigits: d })}`;
export const tone = (v: number | null | undefined) => (v == null || Math.abs(v) < 0.005 ? "var(--text-2)" : v > 0 ? "var(--accent)" : "var(--l-danger)");

/** Stacked bar: how the fund's money is split between the three tiers and cash. */
export function TierBar({ tiers, cash, total }: { tiers: Record<string, number>; cash: number; total: number }) {
  const parts = [...TIERS.map((t) => ({ key: t.key, label: t.label, v: tiers[t.key] ?? 0 })), { key: "cash", label: "Cash", v: cash }];
  return (
    <div className="tier-bar" role="img" aria-label={parts.map((p) => `${p.label}: $${Math.round(p.v)}`).join(", ")}>
      {parts.map((p) => p.v > 0 && <span key={p.key} className={`tier-${p.key}`} style={{ width: `${(p.v / (total || 1)) * 100}%` }} title={`${p.label}: $${Math.round(p.v).toLocaleString()}`} />)}
    </div>
  );
}

export function TierLegend() {
  return (
    <div className="tier-legend">
      {TIERS.map((t) => <span key={t.key}><i className={`tier-dot tier-${t.key}`} />{t.label}</span>)}
      <span><i className="tier-dot tier-cash" style={{ border: "1px solid var(--line-strong)" }} />Cash</span>
    </div>
  );
}

/** Fund value vs the benchmark (both start at the fund's starting cash). Dashed = benchmark. */
export function ValueLine({ points, start, height = 44, className = "fund-spark" }: { points: FundValuePoint[]; start: number; height?: number; className?: string }) {
  const pts = [{ day: "start", value_usd: start, benchmark_value_usd: start }, ...points];
  if (pts.length < 2) return <svg className={className} viewBox={`0 0 100 ${height}`} aria-hidden="true"><line x1="0" x2="100" y1={height / 2} y2={height / 2} className="bench-line" /></svg>;
  const vals = pts.flatMap((p) => [p.value_usd, p.benchmark_value_usd ?? p.value_usd]);
  const lo = Math.min(...vals), hi = Math.max(...vals), span = hi - lo || 1;
  const x = (i: number) => (i / (pts.length - 1)) * 100;
  const y = (v: number) => height - 3 - ((v - lo) / span) * (height - 6);
  const path = (get: (p: FundValuePoint) => number | null) => pts.map((p, i) => { const v = get(p); return v == null ? "" : `${i ? "L" : "M"}${x(i).toFixed(2)},${y(v).toFixed(2)}`; }).join(" ");
  return (
    <svg className={className} viewBox={`0 0 100 ${height}`} preserveAspectRatio="none" role="img"
      aria-label={`Fund value from $${Math.round(start)} to $${Math.round(pts[pts.length - 1].value_usd)}`}>
      <path className="bench-line" d={path((p) => p.benchmark_value_usd)} vectorEffect="non-scaling-stroke" />
      <path className="fund-line" d={path((p) => p.value_usd)} vectorEffect="non-scaling-stroke" />
    </svg>
  );
}
