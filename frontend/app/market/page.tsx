"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ErrorNotice, Loading } from "@/components/ui";
import { TreasuryPanel } from "@/components/TreasuryPanel";
import { latestPerTopic } from "@/lib/runs";
import { API_URL, fmtDate } from "@/lib/api";

interface Teaser {
  id: string; topic: string; generated_at: string; score: number | null; score_reportable: boolean; findings: number; sources: number;
  price_near: number; seller_account: string | null; summary: string | null; themes: string[]; sha256: string;
  chain_record: { explorer_url: string | null } | null; how_to_buy: string;
}
interface Market { seller_account: string | null; price_near: number; enabled: boolean; reports: Teaser[] }

export default function MarketPage() {
  const [market, setMarket] = useState<Market | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [buyer, setBuyer] = useState("");
  const [counts, setCounts] = useState<Record<string, number>>({});

  useEffect(() => {
    fetch(`${API_URL}/api/market`, { cache: "no-store" }).then((r) => r.json()).then(async (m: Market) => {
      setMarket(m);
      const c: Record<string, number> = {};
      await Promise.all(m.reports.map(async (r) => {
        const p = await fetch(`${API_URL}/api/market/${r.id}/purchases`).then((x) => x.json()).catch(() => []);
        c[r.id] = Array.isArray(p) ? p.length : 0;
      }));
      setCounts(c);
    }).catch((e: Error) => setError(e.message));
  }, []);

  return (
    <>
      <section className="hero" style={{ padding: "84px 0 60px" }}>
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">Report market · NEAR testnet</div>
          <h1 className="display" style={{ fontSize: "clamp(40px, 6vw, 76px)" }}>Research that <span className="gradient-text">other agents pay for</span></h1>
          <p className="lede">Every report&apos;s summary and score are free. The full evidence unlocks after a NEAR payment to FUTURESCOUT&apos;s account,
            verified on-chain. A buyer can be a person or another bot. Testnet only: the tokens have no value.</p>
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          {error ? <ErrorNotice error={error} /> : market === null ? <Loading lines={4} /> : (
            <>
              <div className="stats">
                <div className="stat"><div className="stat-value">{latestPerTopic(market.reports).length}</div><div className="stat-label">reports for sale (newest per topic)</div></div>
                <div className="stat"><div className="stat-value">{market.price_near}</div><div className="stat-label">NEAR per report (testnet)</div></div>
                <div className="stat"><div className="stat-value">{Object.values(counts).reduce((a, b) => a + b, 0)}</div><div className="stat-label">purchases recorded</div></div>
                <div className="stat"><div className="stat-value" style={{ fontSize: 22, wordBreak: "break-all" }}>{market.seller_account ?? "not configured"}</div><div className="stat-label">seller account</div></div>
              </div>
              {!market.enabled && <div className="notice notice-warn">The seller account is not configured (NEAR_TESTNET_ACCOUNT_ID). Listings are shown, but nothing can be bought.</div>}

              <TreasuryPanel />

              <div className="panel stack">
                <h3 className="h3" style={{ margin: 0 }}>How a bot buys a report</h3>
                <ol className="small" style={{ color: "var(--text-2)", margin: 0, paddingLeft: 18 }}>
                  <li>Read the listings: <span className="mono">GET /api/market</span> (free teasers).</li>
                  <li>Send {market.price_near} NEAR on testnet from its own account to the seller account.</li>
                  <li>Call <span className="mono">POST /api/market/&#123;id&#125;/purchase</span> with its account id and the transaction hash. The API checks the payment on-chain.</li>
                  <li>Receive the full report and compare its SHA-256 with the fingerprint FUTURESCOUT recorded on NEAR.</li>
                </ol>
                <div className="field" style={{ maxWidth: 420 }}>
                  <label htmlFor="buyer">Check access for a NEAR account (optional)</label>
                  <input id="buyer" className="input" placeholder="buyerbot.testnet" value={buyer} onChange={(e) => setBuyer(e.target.value.trim())} />
                </div>
                <p className="small muted" style={{ margin: 0 }}>Demo buyer: <span className="mono">python scripts\buyer_bot.py</span> in the backend folder.</p>
              </div>

              <div className="grid grid-2">
                {latestPerTopic(market.reports).map((g) => <Listing key={g.latest.id} r={g.latest} buyer={buyer} purchases={counts[g.latest.id] ?? 0} />)}
              </div>
            </>
          )}
        </div>
      </section>
    </>
  );
}

function Listing({ r, buyer, purchases }: { r: Teaser; buyer: string; purchases: number }) {
  const [access, setAccess] = useState<boolean | null>(null);
  useEffect(() => {
    if (!buyer) { setAccess(null); return; }
    fetch(`${API_URL}/api/market/${r.id}?buyer=${encodeURIComponent(buyer)}`).then((x) => x.json()).then((d) => setAccess(d.locked === false)).catch(() => setAccess(null));
  }, [buyer, r.id]);
  return (
    <div className="card">
      <div className="card-kicker"><span>{fmtDate(r.generated_at)}</span><span>·</span><span>{r.price_near} NEAR</span></div>
      <div className="card-title">{r.topic}</div>
      <p className="small" style={{ color: "var(--text-2)", margin: 0 }}>{r.summary ? r.summary.slice(0, 260) + (r.summary.length > 260 ? "…" : "") : "No summary."}</p>
      {r.themes.length > 0 && <div className="pills">{r.themes.map((t) => <span key={t} className="pill">{t.length > 48 ? t.slice(0, 48) + "…" : t}</span>)}</div>}
      <div className="pills" style={{ marginTop: "auto" }}>
        <span className="pill">{r.score !== null ? `score ${r.score}` : "no score"}</span>
        <span className="pill">{r.findings} findings</span>
        <span className="pill">{r.sources} sources</span>
        <span className="pill">{purchases} purchase{purchases === 1 ? "" : "s"}</span>
        {r.chain_record?.explorer_url && <a className="pill pill-on" href={r.chain_record.explorer_url} target="_blank" rel="noopener noreferrer">sealed on NEAR ↗</a>}
      </div>
      <div className="small muted mono">sha256 {r.sha256.slice(0, 20)}…</div>
      {access === true && <Link className="btn btn-solid" href={`/runs/${r.id}`}>Unlocked for {buyer}: open report →</Link>}
      {access === false && <span className="notice small">Locked for {buyer}: not purchased yet.</span>}
    </div>
  );
}
