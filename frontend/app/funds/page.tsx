"use client";

import "./funds.css";
import Link from "next/link";
import { useEffect, useState } from "react";
import { TierBar, TierLegend, ValueLine, pct, tone, usd } from "@/components/FundBits";
import { Reveal } from "@/components/motion";
import { ErrorNotice, Loading } from "@/components/ui";
import { api, fmtDate } from "@/lib/api";
import { sectorLabel } from "@/lib/runs";
import type { FundListItem } from "@/lib/types";

export default function FundsPage() {
  const [funds, setFunds] = useState<FundListItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { api.funds().then((r) => setFunds(r.funds)).catch((e: Error) => setError(e.message)); }, []);

  return (
    <>
      <section className="hero" style={{ padding: "84px 0 56px" }}>
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">Topic funds · simulation · pretend money, real prices</div>
          <h1 className="display" style={{ fontSize: "clamp(38px, 6vw, 72px)" }}>One <span className="gradient-text">mini-ETF</span> per technology</h1>
          <p className="lede">Each topic gets a $10,000 paper fund split into low, medium and high-risk companies from its latest report.
            A decision agent with fixed, published rules decides how much to invest; every decision is fingerprinted on NEAR testnet.
            Holdings are checked against NEAR Intents for a real dry-run quote. <strong>No money moves. Not investment advice.</strong></p>
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          {error ? <ErrorNotice error={error} /> : !funds ? <Loading lines={4} /> : funds.length === 0 ? (
            <div className="notice">No topic funds yet. In the backend folder run <span className="mono">python scripts\funds.py</span>.</div>
          ) : (
            <>
              <TierLegend />
              <div className="fund-grid">
                {funds.map((f, i) => (
                  <Reveal key={f.slug} delay={Math.min(i, 8) * 40}>
                    <Link href={`/funds/${f.slug}`} className="fund-card">
                      <div className="fund-row">
                        <h3>{f.topic}</h3>
                        {f.last_band && <span className="pill band-pill">{f.last_band}</span>}
                      </div>
                      <div className="fund-row">
                        <span className="fund-big">{usd(f.value_usd)}</span>
                        <span className="small"><b style={{ color: tone(f.return_pct) }}>{pct(f.return_pct, 2)}</b>
                          <span className="muted"> vs S&amp;P 500 {pct(f.benchmark_return_pct, 2)}</span></span>
                      </div>
                      <ValueLine points={f.history} start={f.value_usd / (1 + f.return_pct / 100)} />
                      <TierBar tiers={f.tiers_usd} cash={f.cash_usd} total={f.value_usd} />
                      <div className="fund-row small muted">
                        <span>{f.invested_pct.toFixed(0)}% invested · {f.holdings} holdings</span>
                        <span>{sectorLabel(f.sector ?? undefined)}</span>
                      </div>
                      <div className="small muted">
                        NEAR Intents: {f.tradable_via_intents ? <b className="route-yes">{f.tradable_via_intents} tradable</b> : "no tokenized route yet"}
                        {f.last_decision_at && <> · decided {fmtDate(f.last_decision_at)}</>}
                      </div>
                    </Link>
                  </Reveal>
                ))}
              </div>
              <p className="small muted">Solid line = fund, dashed = S&amp;P 500 (SPY) over the same dates, both from $10,000. Returns are price only, after an assumed 0.3% cost per trade.</p>
            </>
          )}
        </div>
      </section>
    </>
  );
}
