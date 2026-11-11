"use client";

// Trading: an agent pipeline you can watch. READ-ONLY: a trade is approved only in the owner's terminal.
import { FundTabs } from "@/components/FundTabs";
import "./trading.css";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { CountUp, Reveal } from "@/components/motion";
import { ErrorNotice, Loading } from "@/components/ui";
import { api, fmtDate } from "@/lib/api";
import type { Economy, TradeProposal, Trading } from "@/lib/types";

const usd = (v: number | null | undefined, d = 2) => (v == null ? "–" : `$${Number(v).toLocaleString(undefined, { minimumFractionDigits: d, maximumFractionDigits: d })}`);
const num = (v: unknown) => (v == null ? null : Number(v));
const IN_FLIGHT = ["approved", "executing", "deposited"];
const COLOURS = ["#3987e6", "#00ec97", "#c98a1f", "#d4486a", "#8ea3ff", "#7fd1c8", "#e0a030"];

export default function TradingPage() {
  const [t, setT] = useState<Trading | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [eco, setEco] = useState<Economy | null>(null);
  const busy = useRef(false);
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;
    const load = () => api.trading()
      .then((x) => { setT(x); setError(null); busy.current = x.proposals.some((p) => p.mode === "live" && IN_FLIGHT.includes(p.status)); })
      .then(() => api.economy().then(setEco).catch(() => undefined))          // the economy panel refreshes with the rest
      .catch((e: Error) => setError(e.message))
      .finally(() => { timer = setTimeout(load, busy.current ? 4_000 : 15_000); });   // faster while a real trade is in flight
    load();
    return () => clearTimeout(timer);
  }, []);

  const live = t?.proposals.filter((p) => p.mode === "live" && (p.status === "success" || IN_FLIGHT.includes(p.status))) ?? [];   // completed (or running) real trades, newest first
  const current = live.find((p) => p.side !== "hold");
  const shadowOrders = t?.proposals.filter((p) => p.mode === "shadow") ?? [];
  const state = !t ? "" : t.kill_switch ? "stopped" : t.trading_enabled ? "armed" : "";
  return (
    <>
      <section className="hero tp-hero">
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">Trading · {t?.auto_approve ? "an AI agent that trades on its own, inside hard limits" : "an AI agent with a human on the switch"}</div>
          {t?.auto_approve
            ? <h1 className="display" style={{ fontSize: "clamp(36px, 5.4vw, 66px)" }}>The agent <span className="gradient-text">decides</span>. Code checks. The order runs.</h1>
            : <h1 className="display" style={{ fontSize: "clamp(36px, 5.4vw, 66px)" }}>The agent <span className="gradient-text">proposes</span>. Code checks. The owner approves.</h1>}
          {t && (
            <div className={`tp-status ${state}`} style={{ marginTop: 18 }}>
              <span className="lamp" />
              {t.kill_switch ? "Stopped: kill switch on" : !t.trading_enabled ? "Off: no real trade can be sent"
                : t.auto_approve ? "Armed: the agent's orders run when every check passes" : "Armed: an approved trade can be sent"}
              <span className="muted">· {t.account ?? "no account connected"} · NEAR mainnet</span>
            </div>
          )}
        </div>
      </section>

      <section className="section" style={{ paddingTop: 28 }}>
        <div className="container stack">
          <FundTabs active="trading" />
          {error ? <ErrorNotice error={error} /> : !t ? <Loading lines={5} /> : (
            <>
              <Pipeline p={current} auto={t.auto_approve} />

              <Reveal>
                <div className="stats">
                  <div className="stat"><div className="stat-value"><CountUp value={t.spent.live_counted_usd ?? t.spent.live_total_usd} decimals={2} prefix="$" /><span className="muted" style={{ fontSize: 22 }}> / {usd(t.limits.max_total_usd, 0)}</span></div><div className="stat-label">{t.selling?.budget_mode === "net" ? "real money invested (buys minus sales), of the cap" : "real money used, of the total cap"}</div></div>
                  <div className="stat"><div className="stat-value">{t.private_near != null ? <><CountUp value={t.private_near} decimals={2} /> Ⓝ</> : "–"}</div><div className="stat-label">NEAR in the fund&apos;s near.com balance{t.private_checked_at ? ` (as of ${fmtDate(t.private_checked_at)})` : " (not read yet)"}; wallet {t.balances?.near != null ? `${t.balances.near.toFixed(2)} NEAR` : "–"}</div></div>
                  <div className="stat"><div className="stat-value"><CountUp value={t.shadow_portfolio.invested_usd} prefix="$" /><span className="muted" style={{ fontSize: 22 }}> / {usd(t.shadow_portfolio.budget_usd, 0)}</span></div><div className="stat-label">shadow mode: pretend money placed at real quotes</div></div>
                  <div className="stat"><div className="stat-value"><CountUp value={t.allowlist.length} /></div><div className="stat-label">tokenized stocks the agent may choose from</div></div>
                </div>
              </Reveal>

              {(t.live_holdings?.length ?? 0) > 0 && (
                <div className="notice"><b>Held now (real money, from the fund&apos;s records):</b>{" "}
                  {t.live_holdings!.map((h) => `${h.quantity.toFixed(5)} ${h.symbol} (cost ${usd(h.cost_usd)})`).join(" · ")}
                  {(t.spent.live_proceeds_usd ?? 0) > 0 && <> · sales so far returned {usd(t.spent.live_proceeds_usd!)}</>}</div>
              )}

              {t.pending_live.length > 0 && !t.auto_approve && (
                <div className="notice notice-warn"><b>{t.pending_live.length} real-money proposal{t.pending_live.length > 1 ? "s" : ""} waiting for the owner&apos;s approval.</b>{" "}
                  The agent decided; only the owner can send it: <span className="mono">python scripts\fund_trade.py approve {t.pending_live[0]}</span> in the backend folder (or <span className="mono">reject</span>).</div>
              )}
              <AgentLog t={t} />
              {eco && <EconomyPanel e={eco} />}

              <h2 className="h2" style={{ margin: "8px 0 0" }}>Real-money trades <span className="muted small">· {live.length} completed, newest first · each record sealed on NEAR</span></h2>
              {live.length === 0 && <div className="notice">No real trade completed yet.</div>}
              {(t.owner_sales?.length ?? 0) > 0 && (
                <p className="small muted" style={{ margin: 0 }}>
                  {t.owner_sales!.map((o) => `${o.symbol} (bought for ${usd(o.bought_usd)} on ${fmtDate(o.bought_at)})`).join(", ")}: sold by the owner in near.com to pay for research reports; not an agent trade, so not listed here.
                </p>
              )}
              {live.map((p, i) => <LiveTrade key={p.id} p={p} explorer={t.explorer_tx} animate={i === 0} />)}

              <ShadowPortfolio t={t} orders={shadowOrders} />

              <details>
                <summary style={{ cursor: "pointer" }}><b>Rules and allowed tokens</b> <span className="muted small">· limits enforced in code</span></summary>
                <div className="grid grid-2" style={{ background: "transparent", border: 0, gap: 24, marginTop: 12 }}>
                  <ul className="small" style={{ color: "var(--text-2)", lineHeight: 1.7, background: "transparent", margin: 0 }}>
                    <li>At most {usd(t.limits.max_trade_usd)} per trade, {usd(t.limits.max_day_usd)} per day, {usd(t.limits.max_total_usd)} in total.</li>
                    <li>{t.selling?.enabled ? `Buys of the tokens listed here; sales only of what the fund holds (at most ${t.selling.max_sells_per_day} a day, never far below the last close).` : "Buys only, and only the tokens listed here."}</li>
                    <li>The quoted price must be within {t.limits.price_band_pct}% of the stock&apos;s last close (a little wider when that close is days old).</li>
                    <li>Real quotes costing more than {t.limits.max_cost_pct}% are refused.</li>
                    <li>Each proposal can be sent once. A kill switch stops everything.</li>
                    <li>No control on this site can approve or send a trade.</li>
                    <li>The agent runs on its own (<span className="mono">fund_trade.py watch</span>): shadow orders fill themselves; {t.auto_approve
                      ? "live orders run automatically once every check passes (the owner switched on auto-approve; the kill switch still stops everything)"
                      : "a live order is a proposal until the owner approves it"}.</li>
                  </ul>
                  <div className="table-wrap" style={{ background: "transparent" }}>
                    <table className="table">
                      <thead><tr><th>Token</th><th>Topic</th><th>Report</th><th className="num">Price</th></tr></thead>
                      <tbody>{t.allowlist.map((a) => (
                        <tr key={a.symbol}><td>{a.symbol}</td><td className="small">{a.topic}</td>
                          <td className="small" style={{ textTransform: "capitalize" }}>{a.band ?? "–"}{a.score != null ? ` · ${a.score}` : ""}</td><td className="num">{usd(a.price)}</td></tr>
                      ))}</tbody>
                    </table>
                  </div>
                </div>
              </details>
              <p className="small muted">{t.disclaimer}</p>
            </>
          )}
        </div>
      </section>
    </>
  );
}

/* ------------------------------------------------------------------ the pipeline */
const ICON: Record<string, ReactNode> = {
  research: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"><path d="M5 4h10l4 4v12H5z" /><path d="M9 12h6M9 16h6M9 8h3" /></svg>,
  agent: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"><rect x="5" y="8" width="14" height="11" rx="3" /><path d="M12 8V4M9.5 13h.01M14.5 13h.01M9.5 16.2c1.6 1 3.4 1 5 0" /><circle cx="12" cy="3.4" r="1" /></svg>,
  checks: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.500-7-10V6z" /><path d="M9 12l2.200 2.200L15.200 10" /></svg>,
  owner: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"><circle cx="12" cy="8" r="3.500" /><path d="M5 20c.8-3.600 3.600-5.500 7-5.500s6.200 1.900 7 5.500" /></svg>,
  swap: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"><path d="M4 8h14l-3-3M20 16H6l3 3" /></svg>,
  hold: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19V9l8-5 8 5v10z" /><path d="M9 19v-6h6v6" /></svg>,
};
const NODES = [
  { key: "research", name: "Research", sub: "sealed reports, topic funds" },
  { key: "agent", name: "Trading agent", sub: "Claude Opus picks and explains" },
  { key: "checks", name: "Safety checks", sub: "caps, allowlist, cost" },
  { key: "owner", name: "Owner", sub: "approves in their terminal" },
  { key: "swap", name: "NEAR Intents", sub: "NEAR ⇄ tokenized stock" },
  { key: "hold", name: "Holding", sub: "in the fund account" },
];

function Pipeline({ p, auto = false }: { p?: TradeProposal; auto?: boolean }) {
  const nodes = NODES.map((n) => (n.key === "owner" && auto ? { ...n, name: "Auto-approve", sub: "runs when every check passes" } : n));
  const selling = p?.side === "sell";
  // active = index of the stage the newest real proposal is at; done = stages before it
  let active = -1, bad = -1, allDone = false, caption: ReactNode = <>Idle. The agent wakes on a new report, a sharp price move or its daily review.</>;
  if (p) {
    const s = p.status;
    if (s === "proposed") { active = 3; caption = auto ? <>The agent decided to {selling ? "sell" : "buy"} {usd(p.usd)} of {p.symbol}; <b>checks running</b>.</>
      : <>Waiting for the <b>owner&apos;s approval</b> to {selling ? "sell" : "buy"} {usd(p.usd)} of {p.symbol}.</>; }
    else if (s === "approved" || s === "executing") { active = 4; caption = <>Approved. Getting a real quote and <b>sending the payment</b>.</>; }
    else if (s === "deposited") { active = 4; caption = selling ? <>Order sent. <b>NEAR Intents is swapping</b> {p.symbol} into NEAR.</> : <>Payment sent. <b>NEAR Intents is swapping</b> it into {p.symbol}.</>; }
    else if (s === "success") { allDone = true; caption = selling
      ? <><b>Sold.</b> {p.result?.amountInFormatted ? `${Number(p.result.amountInFormatted).toFixed(5)} ` : ""}{p.symbol} for about {usd(Number(p.result?.amountOutUsd ?? 0))} of NEAR.</>
      : <><b>Filled.</b> The fund account holds {p.result?.amountOutFormatted ? `${Number(p.result.amountOutFormatted).toFixed(5)} ` : ""}{p.symbol}.</>; }
    else if (s === "refunded") { bad = 4; caption = <><b>Refunded.</b> The swap did not complete and the payment came back.</>; }
    else if (s === "rejected") { bad = 3; caption = <>The owner <b>rejected</b> this proposal.</>; }
    else { bad = p.deposit_tx ? 4 : 2; caption = <><b>Stopped by a check.</b> {p.error ?? "See the step log."}</>; }
  }
  return (
    <div className="tp-pipe" role="img" aria-label={`Trading pipeline: research, trading agent, safety checks, ${auto ? "automatic approval" : "owner approval"}, NEAR Intents swap, holding`}>
      {nodes.map((n, i) => {
        const done = allDone || (active >= 0 ? i < active : bad >= 0 ? i < bad : false);
        const cls = [done ? "done" : "", i === active ? "active" : "", i === bad ? "bad" : "",
          allDone || (active >= 0 && i < active) ? "flow" : !p ? "idle" : ""].join(" ");
        return (
          <div key={n.key} className={`tp-node ${cls}`}>
            <div className="tp-orb">{ICON[n.key]}</div>
            <div className="tp-name">{n.name}</div>
            <div className="tp-sub">{n.sub}</div>
          </div>
        );
      })}
      <div className="tp-caption">{caption}</div>
    </div>
  );
}

/* ------------------------------------------------------------------ the real trade */
function useTyped(text: string, on: boolean): string {
  const [n, setN] = useState(on ? 0 : text.length);
  useEffect(() => {
    if (!on || typeof window === "undefined" || window.matchMedia("(prefers-reduced-motion: reduce)").matches) { setN(text.length); return; }
    setN(0);
    const id = setInterval(() => setN((k) => { if (k >= text.length) { clearInterval(id); return k; } return k + 3; }), 16);
    return () => clearInterval(id);
  }, [text, on]);
  return text.slice(0, n);
}

function Elapsed({ since }: { since: string }) {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => { const id = setInterval(() => setNow(Date.now()), 1000); return () => clearInterval(id); }, []);
  const s = Math.max(0, Math.round((now - new Date(since).getTime()) / 1000));
  return <span className="mono">{Math.floor(s / 60)}:{String(s % 60).padStart(2, "0")}</span>;
}

const TRIGGER_WORDS: Record<string, string> = { new_report: "new report", price_drop: "sharp fall", price_jump: "sharp rise", review: "daily review", manual: "review on request", after_sale: "after a sale" };

function EconomyPanel({ e }: { e: Economy }) {
  const link = (tx: string | null) => (tx ? <a href={e.explorer_tx.replace("{tx}", tx)} target="_blank" rel="noopener noreferrer">tx ↗</a> : null);
  const bought = (rid: string) => e.purchases.find((x) => x.run_id === rid && x.status !== "failed");
  return (
    <div className="tr-card">
      <div className="tr-head">
        <h2 className="tr-title" style={{ minWidth: 0, overflowWrap: "anywhere" }}>Agent economy <span className="muted small">· reports bought in NEAR</span></h2>
        <div className="pills"><span className="pill">{e.enabled ? "on: real NEAR" : "off"}</span></div>
      </div>
      <p className="small" style={{ color: "var(--text-2)", margin: 0 }}>
        {e.limits.max_price_usd
          ? <>The report agent prices every report at what it cost to make (AI models, X reads, patent searches, the NEAR seal) plus ${e.limits.margin_usd?.toFixed(2)}, kept between ${e.limits.min_price_usd} and ${e.limits.max_price_usd}, and paid in NEAR at the live price. The trading agent may only use </>
          : <>The report agent prices every report in NEAR by its quality (score and confidence), at most {e.limits.max_price_near} NEAR and never below what it cost to make. The trading agent may only use </>}
        reports it has bought, and spends at most {Math.round(e.limits.budget_share_of_fund * 100)}% of its fund on them. Each payment is a signed order from the trading agent's near.com balance, checked before signing, and confirmed when it arrives.
        The report agent stakes {Math.round(e.limits.stake_share * 100)}% of every payment through NEAR AI&apos;s Staking for Inference (NEAR AI accepts at least {e.limits.min_stake_near} NEAR at a time, so it waits until enough payments add up); the rewards pay for the agents&apos; AI.
        It keeps the other {100 - Math.round(e.limits.stake_share * 100)}%; once that pot passes ${e.second_trader_at_usd ?? 200} it funds a second trading agent (the next step).
      </p>
      <div className="stats" style={{ marginTop: 4, gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 140px), 1fr))", overflowWrap: "anywhere" }}>
        <div className="stat"><div className="stat-value">{e.spent_near.toFixed(3)} Ⓝ</div><div className="stat-label">paid for reports by the trading agent</div></div>
        <div className="stat"><div className="stat-value">{e.report_agent_wallet_near != null ? `${e.report_agent_wallet_near.toFixed(2)} Ⓝ` : "–"}</div><div className="stat-label">report agent wallet ({e.seller_account})</div></div>
        <div className="stat"><div className="stat-value">{e.report_agent_staked_near != null ? `${e.report_agent_staked_near.toFixed(2)} Ⓝ` : "–"}</div><div className="stat-label">staked for NEAR AI credits</div></div>
        <div className="stat"><div className="stat-value">{(e.kept_near ?? 0).toFixed(2)} Ⓝ</div><div className="stat-label">kept pot: at ${e.second_trader_at_usd ?? 200} it funds a second trading agent</div></div>
      </div>
      {e.prices.length > 0 && (
        <div className="tr-mini">{[...e.prices].sort((a, b) => Number(!!bought(b.run_id)) - Number(!!bought(a.run_id))).slice(0, Math.max(6, e.purchases.filter((x) => x.status === "paid").length + 2)).map((p) => {
          const b = e.purchases.find((x) => x.run_id === p.run_id && x.status !== "failed");
          return <div key={p.run_id}><b>{p.price_near} Ⓝ</b><span>{p.topic} <span className="why">· ${p.price_usd.toFixed(2)} · {b ? (b.status === "paid" ? "bought" : "payment sent") : "not bought"} {b && link(b.tx_hash)}</span></span></div>;
        })}</div>
      )}
      {e.stakes.length > 0 && <div className="small muted">
        {e.stakes.filter((s) => s.status === "staked").map((s) => <div key={s.id}>{fmtDate(s.at)} · staked {s.amount_near} NEAR with NEAR AI {link(s.tx_hash)}</div>)}
        {e.stakes.some((s) => s.status !== "staked") && <div>{e.stakes.filter((s) => s.status !== "staked").length} stake attempt(s) were refused (under NEAR AI&apos;s {e.limits.min_stake_near} NEAR minimum, or not enough balance); nothing was lost.</div>}
      </div>}
    </div>
  );
}

function whyWoke(triggers: { kind: string }[]): string {
  const kinds = Array.from(new Set(triggers.map((x) => TRIGGER_WORDS[x.kind] ?? x.kind)));
  return kinds.length ? kinds.join(", ") : "check";
}

function firstSentence(text: string): string {
  const m = text.match(/^.{20,}?[.!?](\s|$)/);
  const one = (m ? m[0] : text).trim();
  return one.length > 180 ? one.slice(0, 177).trimEnd() + "…" : one;
}

// What a decision led to: a decided buy or sale that the code refused (or that failed) is not shown as done.
function outcome(c: { action: string; usd: number; ticker: string; proposal_id: string | null }, proposals: { id: string; status: string; history: { note: string }[] }[]): string {
  if (c.action !== "buy" && c.action !== "sell") return "held";
  const what = c.action === "buy" ? `${usd(c.usd)} of ${c.ticker}` : `about ${usd(c.usd)} of ${c.ticker}`;
  const p = proposals.find((x) => x.id === c.proposal_id);
  const done = !p || ["success", "shadow_filled", "deposited", "executing", "approved"].includes(p.status);
  if (done) return c.action === "buy" ? `bought ${what}` : `sold ${what}`;
  const why = p.history.length ? p.history[p.history.length - 1].note.replace(/^shadow: /, "") : p.status;
  return `decided to ${c.action} ${what}; not done: ${why}`;
}

function AgentLog({ t }: { t: Trading }) {
  const woke = (t.checks ?? []).filter((c) => c.action !== "none" && !c.summary.startsWith("No budget left"));   // the agent was actually called
  const cfg = t.strategy?.config;
  return (
    <div className="tr-card">
      <div className="tr-head">
        <h2 className="tr-title">Latest decisions <span className="muted small">· by the trading agent</span></h2>
        <div className="pills"><span className="pill">{t.strategy?.last_check_at ? `last check ${fmtDate(t.strategy.last_check_at)}` : "no check yet"}</span></div>
      </div>
      <p className="small" style={{ color: "var(--text-2)", margin: 0 }}>
        It checks every {cfg?.check_minutes ?? 60} min and wakes on a new report, a sharp price move or a daily review{t.selling?.enabled ? "; it can buy, sell or hold" : "; it can buy or hold"}.
      </p>
      {woke.length === 0 ? <div className="small muted">No decision recorded yet.</div> : (
        <ol className="tr-log" style={{ margin: 0 }}>
          {woke.slice(0, 5).map((c) => (
            <li key={c.id}>
              <b>{fmtDate(c.at)}</b> · <span className="pill" style={{ marginRight: 6 }}>{c.mode === "live" ? "real" : "shadow"}</span>
              {whyWoke(c.triggers)}{" → "}
              <b>{outcome(c, t.proposals)}</b>
              {c.summary && <div className="small muted">{firstSentence(c.summary)}</div>}
            </li>
          ))}
        </ol>
      )}
      {(t.strategy?.rules || cfg) && (
        <details><summary className="small muted" style={{ cursor: "pointer" }}>How it decides</summary>
          {t.strategy?.rules && <ul className="small" style={{ color: "var(--text-2)", lineHeight: 1.6 }}>{t.strategy.rules.map((r) => <li key={r}>{r}</li>)}</ul>}
        </details>
      )}
    </div>
  );
}

function LiveTrade({ p, explorer, animate = true }: { p: TradeProposal; explorer: string; animate?: boolean }) {
  const typed = useTyped(p.rationale, animate);
  const q = p.quote ?? p.dry_quote;
  const inUsd = num(q?.amountInUsd), outUsd = num(q?.amountOutUsd);
  const cost = inUsd && outUsd ? ((inUsd - outUsd) / inUsd) * 100 : null;
  const s = p.status;
  const working = IN_FLIGHT.includes(s);
  const sentAt = p.history.find((e) => e.status === "deposited")?.at;
  const endBad = s === "refunded" || s === "failed" || s === "rejected";
  const idx = s === "proposed" ? 0 : s === "approved" || s === "executing" ? 1 : s === "deposited" ? 2 : s === "success" ? 3 : p.deposit_tx ? 2 : p.history.some((e) => e.status === "approved") ? 1 : 0;
  const autoApproved = p.history.some((e) => e.status === "approved" && /AUTOMATICALLY/.test(e.note));
  const manual = p.quote?.route === "manual";                         // the owner's own sale in near.com, recorded by hand
  const stops = manual ? ["Sold by the owner in near.com", "No agent decision", "Recorded by hand", "Done"] : ["Decided by the agent", autoApproved ? "Approved by the agent (all checks passed)" : "Approved by the owner", p.side === "sell" ? "Order sent" : "Payment sent", s === "refunded" ? "Refunded" : s === "failed" ? "Failed" : s === "rejected" ? "Rejected" : "Filled"];
  return (
    <div className={`tr-card live ${working ? "working" : ""} ${s === "success" ? "ok" : ""}`}>
      <div className="tr-head">
        <h2 className="tr-title">{p.side === "sell" ? `Sell ${Math.round((p.fraction ?? 1) * 100)}% of ${p.symbol} (about ${usd(p.usd)})` : `Buy ${usd(p.usd)} of ${p.symbol}`} <span className="muted small">{p.ticker} · {p.topic}</span></h2>
        <div className="pills"><span className="pill tr-pill-live">real money</span><span className="pill">{s.replace("_", " ")}</span></div>
      </div>

      <div className="tr-track">
        <span className="fill" style={{ width: `${(Math.min(idx, 3) / 3) * 75}%` }} />
        {stops.map((label, i) => {
          const cls = endBad && i === 3 ? "bad" : s === "success" || i <= idx ? "done" : i === idx + 1 && !endBad ? "now" : "";
          return <span key={label} className={`tr-stop ${cls}`}><i />{label}</span>;
        })}
      </div>
      {s === "deposited" && sentAt && (
        <div className="tr-wait"><span className="tr-dots"><span /><span /><span /></span>NEAR Intents is swapping {p.side === "sell" ? `${p.symbol} into NEAR` : `the payment into ${p.symbol}`} · <Elapsed since={sentAt} /> so far. If it cannot complete, the {p.side === "sell" ? "tokens come" : "payment comes"} back.</div>
      )}

      <div className="tr-agent">
        <div className="tr-avatar">{ICON.agent}</div>
        <div>
          <div className="tr-model">{manual ? "OWNER · MANUAL SALE IN NEAR.COM" : `TRADING AGENT · ${(p.model ?? "model").replace(/_/g, " ").toUpperCase()}`}</div>
          <p className="tr-say">{animate ? typed : p.rationale}{animate && typed.length < p.rationale.length && <span className="caret" />}</p>
          {p.risks.length > 0 && <ul className="tr-risks">{p.risks.map((r) => <li key={r}>{r}</li>)}</ul>}
        </div>
      </div>

      <div className="tr-kv">
        <div><div className="k">Pays</div><div className="v">{usd(inUsd ?? p.usd)} in NEAR</div></div>
        <div><div className="k">{s === "success" ? "Received" : "Quoted"}</div><div className="v">{p.result?.amountOutFormatted ?? q?.amountOutFormatted ? `${Number(p.result?.amountOutFormatted ?? q?.amountOutFormatted).toFixed(5)} ${p.side === "sell" ? "NEAR" : p.symbol}` : "–"}</div></div>
        <div><div className="k">Quoted cost</div><div className="v">{cost != null ? `${cost.toFixed(2)}%` : "–"}</div></div>
        <div><div className="k">Stock&apos;s last close</div><div className="v">{usd(p.ref_close)}<span className="muted small"> {p.ref_close_date ?? ""}</span></div></div>
      </div>
      {p.error && <div className="notice notice-warn small">{p.error}</div>}
      <div className="small muted">
        {fmtDate(p.created_at)}
        {p.deposit_tx && <> · <a href={explorer.replace("{tx}", p.deposit_tx)} target="_blank" rel="noopener noreferrer">payment transaction ↗</a></>}
        {p.chain?.explorer_url && <> · <a href={p.chain.explorer_url} target="_blank" rel="noopener noreferrer">record sealed on NEAR {p.chain.network === "mainnet" ? "mainnet" : "testnet"} ↗</a></>}
      </div>
      <details>
        <summary className="small muted" style={{ cursor: "pointer" }}>Step log</summary>
        <ol className="tr-log">{p.history.map((e, i) => <li key={i}>{fmtDate(e.at)} · {e.status.replace("_", " ")}{e.note ? `: ${e.note}` : ""}</li>)}</ol>
      </details>
    </div>
  );
}

/* ------------------------------------------------------------------ shadow portfolio */
function ShadowPortfolio({ t, orders }: { t: Trading; orders: TradeProposal[] }) {
  const pf = t.shadow_portfolio;
  const [on, setOn] = useState(false);
  useEffect(() => { const id = setTimeout(() => setOn(true), 150); return () => clearTimeout(id); }, []);
  if (!pf || pf.positions.length === 0) return null;
  const parts = [...pf.positions.map((p, i) => ({ label: p.symbol, topic: p.topic, v: p.cost_usd, c: COLOURS[i % COLOURS.length] })),
    { label: "Cash", topic: "kept by the agent", v: pf.cash_usd, c: "#3a4240" }];
  let acc = 0;
  const plan = orders.find((o) => o.model_cost_usd > 0 && o.status !== "hold") ?? orders[0];
  return (
    <div className="tr-card">
      <div className="tr-head">
        <h2 className="tr-title">Shadow portfolio <span className="muted small">pretend money · real quotes · nothing sent</span></h2>
        <div className="pills"><span className="pill tr-pill-shadow">shadow</span></div>
      </div>
      <div className="sp-grid">
        <div className="sp-wrap">
          <svg className="sp-donut" viewBox="0 0 120 120" role="img" aria-label={parts.map((p) => `${p.label} $${Math.round(p.v)}`).join(", ")}>
            <circle className="bg" cx="60" cy="60" r="50" pathLength={100} />
            {parts.map((p) => {
              const share = (p.v / pf.budget_usd) * 100;
              const el = <circle key={p.label} cx="60" cy="60" r="50" pathLength={100} stroke={p.c} strokeDasharray={`${on ? Math.max(share - 0.8, 0) : 0} 100`} strokeDashoffset={-acc} />;
              acc += share;
              return el;
            })}
          </svg>
          <div className="sp-centre"><div><div className="big">{usd(pf.invested_usd, 0)}</div><div className="small muted">placed of {usd(pf.budget_usd, 0)}</div></div></div>
        </div>
        <div className="sp-rows">
          {parts.map((p) => (
            <div className="sp-row" key={p.label}>
              <span className="sw" style={{ background: p.c }} />
              <span>{p.label}<div className="topic">{p.topic}</div></span>
              <span className="bar"><span style={{ width: on ? `${(p.v / pf.budget_usd) * 100 * 2.5}%` : 0, maxWidth: "100%", background: p.c }} /></span>
              <span className="n">{usd(p.v, 0)}</span>
              <span className="n pct muted">{((p.v / pf.budget_usd) * 100).toFixed(0)}%</span>
            </div>
          ))}
        </div>
      </div>
      {plan?.rationale && (
        <div className="tr-agent">
          <div className="tr-avatar">{ICON.agent}</div>
          <div>
            <div className="tr-model">TRADING AGENT · {(plan.model ?? "model").replace(/_/g, " ").toUpperCase()} · sizes are its own choice</div>
            <p className="tr-say" style={{ minHeight: 0 }}>{plan.rationale}</p>
          </div>
        </div>
      )}
      <details>
        <summary className="small muted" style={{ cursor: "pointer" }}>Every shadow order and its real quote ({orders.length})</summary>
        <div className="tr-mini">
          {orders.map((o) => {
            const q = o.quote ?? o.dry_quote;
            return (
              <div key={o.id}>
                <b>{o.side === "hold" ? "hold" : usd(o.usd, 0)}</b>
                <span>{o.symbol || "cash"} <span className="why">· {o.status === "shadow_filled" ? `would receive ${Number(q?.amountOutFormatted ?? 0).toFixed(4)} ${o.symbol}` : o.error ?? o.status.replace("_", " ")} · {o.rationale.slice(0, 150)}</span></span>
                <span className="pill">{o.status.replace("_", " ")}</span>
              </div>
            );
          })}
        </div>
      </details>
    </div>
  );
}
