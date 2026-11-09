"use client";

// Stage 3: live-trading test (tiny real budget) + shadow mode. READ-ONLY: approval happens only in the owner's terminal.
import "./trading.css";
import { useEffect, useState } from "react";
import { Reveal } from "@/components/motion";
import { ErrorNotice, Loading } from "@/components/ui";
import { api, fmtDate } from "@/lib/api";
import type { TradeProposal, Trading } from "@/lib/types";

const usd = (v: number | null | undefined, d = 2) => (v == null ? "–" : `$${Number(v).toLocaleString(undefined, { minimumFractionDigits: d, maximumFractionDigits: d })}`);
const num = (v: unknown) => (v == null ? null : Number(v));

export default function TradingPage() {
  const [t, setT] = useState<Trading | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    const load = () => api.trading().then((x) => { setT(x); setError(null); }).catch((e: Error) => setError(e.message));
    load();
    const id = setInterval(load, 15_000);
    return () => clearInterval(id);
  }, []);

  const state = !t ? "" : t.kill_switch ? "stopped" : t.trading_enabled ? "armed" : "";
  return (
    <>
      <section className="hero" style={{ padding: "84px 0 56px" }}>
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">Trading · real-money test with a tiny budget · shadow mode</div>
          <h1 className="display" style={{ fontSize: "clamp(38px, 6vw, 72px)" }}>The agent <span className="gradient-text">proposes</span>. The owner approves.</h1>
          <p className="lede">A trading agent on a strong model picks one tokenized stock from the research funds and explains why. Code enforces the limits.
            Nothing is sent until the owner approves that one trade in their own terminal. Shadow mode runs the same steps with real quotes and pretend money.
            <strong> Not investment advice.</strong></p>
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          {error ? <ErrorNotice error={error} /> : !t ? <Loading lines={5} /> : (
            <>
              <div className={`tr-banner ${state}`}>
                <span className="tr-light" />
                <div>
                  <b>{t.kill_switch ? "Stopped: kill switch is on" : t.trading_enabled ? "Armed: an approved trade can be sent" : "Off: no real trade can be sent"}</b>
                  <div className="small muted">
                    {t.network} · {t.account ? <span className="mono">{t.account}</span> : "no fund account connected yet"} · approval: owner&apos;s terminal only
                  </div>
                </div>
              </div>

              <Reveal>
                <div className="stats">
                  <div className="stat"><div className="stat-value">{usd(t.spent.live_total_usd)}<span className="muted" style={{ fontSize: 22 }}> / {usd(t.limits.max_total_usd, 0)}</span></div><div className="stat-label">real money used, of the total cap</div></div>
                  <div className="stat"><div className="stat-value">{t.balances?.usdc != null ? usd(t.balances.usdc) : "–"}</div><div className="stat-label">USDC in the fund account{t.balances?.near != null ? ` · ${t.balances.near} NEAR for fees` : ""}</div></div>
                  <div className="stat"><div className="stat-value">{usd(t.spent.shadow_filled_usd, 0)}<span className="muted" style={{ fontSize: 22 }}> / {usd(t.limits.shadow_budget_usd, 0)}</span></div><div className="stat-label">shadow mode: pretend money placed at real quotes</div></div>
                  <div className="stat"><div className="stat-value">{t.allowlist.length}</div><div className="stat-label">tokenized stocks the agent may choose from</div></div>
                </div>
              </Reveal>

              {t.balances && t.balances.holdings.length > 0 && (
                <div className="notice">
                  <b>Held now (real):</b> {t.balances.holdings.map((h) => `${h.quantity} ${h.symbol}${h.value_usd != null ? ` (about ${usd(h.value_usd)})` : ""}`).join(" · ")}
                </div>
              )}

              <h2 className="h2" style={{ marginBottom: 0 }}>Proposals</h2>
              <p className="sub" style={{ marginTop: 0 }}>Newest first. <span className="pill tr-pill-live">real</span> uses the fund account; <span className="pill tr-pill-shadow">shadow</span> sends nothing.</p>
              {t.proposals.length === 0 ? <div className="notice">No proposals yet. In the backend folder: <span className="mono">python scripts\fund_trade.py propose --shadow</span></div> : (
                <div className="tr-list">{t.proposals.map((p) => <ProposalCard key={p.id} p={p} explorer={t.explorer_tx} />)}</div>
              )}

              <div className="grid grid-2" style={{ background: "transparent", border: 0, gap: 24 }}>
                <div style={{ background: "transparent" }}>
                  <h3 className="h3">Limits, enforced in code</h3>
                  <ul className="small" style={{ color: "var(--text-2)", lineHeight: 1.7 }}>
                    <li>At most {usd(t.limits.max_trade_usd)} per trade, {usd(t.limits.max_day_usd)} per day, {usd(t.limits.max_total_usd)} in total.</li>
                    <li>Buys only, and only tokens on the list below.</li>
                    <li>The quoted price must be within {t.limits.price_band_pct}% of the stock&apos;s last close (a little wider when that close is days old).</li>
                    <li>Quotes costing more than {t.limits.max_cost_pct}% are refused.</li>
                    <li>Each proposal can be sent once. A kill switch stops everything.</li>
                    <li>No button on this site can approve or send a trade.</li>
                  </ul>
                </div>
                <div style={{ background: "transparent" }}>
                  <h3 className="h3">What the agent may choose from</h3>
                  <div className="table-wrap">
                    <table className="table">
                      <thead><tr><th>Token</th><th>Topic</th><th>Report verdict</th><th className="num">Token price</th></tr></thead>
                      <tbody>{t.allowlist.map((a) => (
                        <tr key={a.symbol}><td>{a.symbol} <span className="muted mono small">{a.ticker}</span></td><td className="small">{a.topic}</td>
                          <td className="small" style={{ textTransform: "capitalize" }}>{a.band ?? "–"}{a.score != null ? ` · ${a.score}` : ""}</td><td className="num">{usd(a.price)}</td></tr>
                      ))}</tbody>
                    </table>
                  </div>
                  <p className="small muted">Tokenized stocks are issued by Ondo and bought through NEAR Intents. They track the share price but are not the shares.</p>
                </div>
              </div>
              <p className="small muted">{t.disclaimer}</p>
            </>
          )}
        </div>
      </section>
    </>
  );
}

function steps(p: TradeProposal): { label: string; state: "done" | "now" | "bad" | "" }[] {
  const s = p.status;
  if (p.side === "hold") return [{ label: "Agent proposed to hold", state: "done" }];
  if (p.mode === "shadow") {
    return [{ label: "Proposed by the agent", state: "done" }, { label: "Real quote checked", state: p.quote ? (s === "failed" ? "bad" : "done") : s === "failed" ? "bad" : "" },
            { label: s === "failed" ? "Refused by a safety check" : "Shadow filled (nothing sent)", state: s === "shadow_filled" ? "done" : s === "failed" ? "bad" : "" }];
  }
  const order = ["proposed", "approved", "executing", "deposited", "success"];
  const at = order.indexOf(s);
  const done = (i: number) => (at >= i ? "done" : "") as "done" | "";
  const end = s === "refunded" ? "Refunded" : s === "failed" ? "Failed (see log)" : s === "rejected" ? "Rejected by the owner" : "Filled";
  const bad = s === "refunded" || s === "failed" || s === "rejected";
  return [{ label: "Proposed by the agent", state: "done" }, { label: "Approved by the owner", state: s === "rejected" ? "bad" : s === "proposed" ? "now" : (p.history.some((e) => e.status === "approved") ? "done" : "") },
          { label: "USDC sent", state: p.deposit_tx ? "done" : s === "executing" ? "now" : done(3) }, { label: end, state: s === "success" ? "done" : bad ? "bad" : s === "deposited" ? "now" : "" }];
}

function ProposalCard({ p, explorer }: { p: TradeProposal; explorer: string }) {
  const q = p.quote ?? p.dry_quote;
  const inUsd = num(q?.amountInUsd), outUsd = num(q?.amountOutUsd);
  const cost = inUsd && outUsd ? ((inUsd - outUsd) / inUsd) * 100 : null;
  return (
    <div className={`tr-card ${p.mode}`}>
      <div className="tr-head">
        <h3 className="tr-title">{p.side === "hold" ? "Hold: no trade proposed" : <>Buy {usd(p.usd)} of {p.symbol} <span className="muted small">{p.ticker} · {p.topic}</span></>}</h3>
        <div className="pills">
          <span className={`pill ${p.mode === "live" ? "tr-pill-live" : "tr-pill-shadow"}`}>{p.mode === "live" ? "real" : "shadow"}</span>
          <span className="pill">{p.status.replace("_", " ")}</span>
        </div>
      </div>
      <div className="tr-steps">{steps(p).map((s) => <span key={s.label} className={`tr-step ${s.state}`}><i className="dot" />{s.label}</span>)}</div>
      {p.rationale && <p className="tr-why"><b>Agent&apos;s reason:</b> {p.rationale}</p>}
      {p.risks.length > 0 && <ul className="tr-risks">{p.risks.map((r) => <li key={r}>{r}</li>)}</ul>}
      {p.side !== "hold" && (
        <div className="tr-kv">
          <div><div className="k">Pays</div><div className="v">{usd(inUsd ?? p.usd)} USDC</div></div>
          <div><div className="k">{p.status === "success" ? "Received" : "Would receive"}</div><div className="v">{p.result?.amountOutFormatted ?? q?.amountOutFormatted ? `${Number(p.result?.amountOutFormatted ?? q?.amountOutFormatted).toFixed(5)} ${p.symbol}` : "–"}</div></div>
          <div><div className="k">Quoted cost</div><div className="v">{cost != null ? `${cost.toFixed(2)}%` : "–"}</div></div>
          <div><div className="k">Stock&apos;s last close</div><div className="v">{p.ref_close != null ? `${usd(p.ref_close)}` : "–"}<span className="muted small"> {p.ref_close_date ?? ""}</span></div></div>
        </div>
      )}
      {p.error && <div className="notice notice-warn small">{p.error}</div>}
      <div className="small muted">
        {fmtDate(p.created_at)} · model {p.model ?? "none"}{p.model_cost_usd ? ` (${usd(p.model_cost_usd, 3)})` : ""}
        {p.deposit_tx && <> · <a href={explorer.replace("{tx}", p.deposit_tx)} target="_blank" rel="noopener noreferrer">deposit transaction ↗</a></>}
        {p.chain?.explorer_url && <> · <a href={p.chain.explorer_url} target="_blank" rel="noopener noreferrer">record sealed on NEAR testnet ↗</a></>}
      </div>
      <details>
        <summary className="small muted" style={{ cursor: "pointer" }}>Step log</summary>
        <ol className="tr-log">{p.history.map((e, i) => <li key={i}>{fmtDate(e.at)} · {e.status.replace("_", " ")}{e.note ? `: ${e.note}` : ""}</li>)}</ol>
        {p.sha256 && <div className="small muted mono" style={{ wordBreak: "break-all", marginTop: 6 }}>sha256 {p.sha256}</div>}
      </details>
    </div>
  );
}
