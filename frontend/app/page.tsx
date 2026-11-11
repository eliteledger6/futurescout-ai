"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { AgentFlow } from "@/components/AgentFlow";
import { LivePanel } from "@/components/LivePanel";
import { RadarStrip } from "@/components/RadarStrip";
import { Reveal } from "@/components/motion";
import { ErrorNotice, Loading } from "@/components/ui";
import { api, fmtDate } from "@/lib/api";
import { latestPerTopic, SECTOR_NAMES, sectorLabel, type TopicGroup } from "@/lib/runs";
import type { RunSummary } from "@/lib/types";

export default function Home() {
  const [runs, setRuns] = useState<RunSummary[] | null>(null);
  const [, setNamesReady] = useState(0);            // re-render once the sector names have loaded
  const [error, setError] = useState<string | null>(null);
  const [sector, setSector] = useState<string | null>(null);

  useEffect(() => {
    api.runs().then(setRuns).catch((e: Error) => setError(e.message));
    api.sectors().then((list) => { for (const x of list) SECTOR_NAMES[x.key] = x.name; setNamesReady((n) => n + 1); }).catch(() => undefined);
  }, []);

  const groups = useMemo(() => latestPerTopic(runs ?? []), [runs]);
  const sectors = useMemo(() => [...new Set(groups.map((g) => g.latest.sector ?? "semiconductors"))], [groups]);
  const shown = groups.filter((g) => sector === null || (g.latest.sector ?? "semiconductors") === sector);
  const latest = groups[0]?.latest;

  return (
    <>
      <section className="hero hero-compact">
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">Autonomous research and trading agents on NEAR · 1–5 year horizon</div>
          <h1 className="display">Find the next hot technology. <span className="gradient-text">Show the evidence.</span></h1>
          <p className="lede">AI agents read papers, patents, company filings and X, argue the other side, and write a report where every claim has a label and a source.
            Reports are sold for $2–3 each, paid in NEAR: our trading agent buys them and trades tokenized stocks through NEAR Intents, inside hard
            limits, and any other trading bot can buy them too. The report agent stakes what it earns, so NEAR AI pays for its models. Every report
            is sealed on NEAR (new seals on mainnet).</p>
          <div className="actions">
            {latest ? <Link className="btn btn-solid" href={`/runs/${latest.id}`}>Open latest report →</Link>
              : <Link className="btn btn-solid" href="/research">Start research →</Link>}
            <Link className="btn btn-ghost" href="/radar">See what&apos;s heating up</Link>
            <Link className="btn btn-ghost" href="/trading">Watch the trading agent</Link>
          </div>
          <RadarStrip />
        </div>
      </section>

      <section className="section" style={{ paddingTop: 48 }} id="how-it-works">
        <div className="container stack">
          <div>
            <div className="eyebrow">How it works</div>
            <h2 className="h2" style={{ margin: "10px 0 6px" }}>The agent network</h2>
            <p className="sub" style={{ margin: 0 }}>
              From finding a topic to a sealed report, a sale and a trade. Hover or tap any agent to see what it does.
              The rules every agent follows are on <Link href="/about" style={{ color: "var(--accent)" }}>How it works →</Link>
            </p>
          </div>
          <Reveal><AgentFlow /></Reveal>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 16 }}>
        <div className="container stack">
          <div className="section-head">
            <div>
              <h2 className="h2">Reports</h2>
              <p className="sub">The newest report for each technology. {runs && runs.length > groups.length ? `${runs.length - groups.length} earlier runs are kept and linked from each report.` : ""}</p>
            </div>
            <Link className="btn btn-ghost" href="/research">Request a report</Link>
          </div>
          {sectors.length > 1 && (
            <div className="chips" role="tablist" aria-label="Sector">
              <button className={`chip ${sector === null ? "on" : ""}`} onClick={() => setSector(null)}>All · {groups.length}</button>
              {sectors.map((s) => (
                <button key={s} className={`chip ${sector === s ? "on" : ""}`} onClick={() => setSector(s)}>
                  {sectorLabel(s)} · {groups.filter((g) => (g.latest.sector ?? "semiconductors") === s).length}
                </button>
              ))}
            </div>
          )}
          {error ? <ErrorNotice error={error} /> : runs === null ? <Loading /> : groups.length === 0 ? (
            <div className="notice">No reports yet. Start one from <Link href="/research" style={{ color: "var(--accent)" }}>New research</Link>, or run <span className="mono">python scripts\run_research.py --topic &quot;…&quot;</span> in the backend folder.</div>
          ) : (
            <div className="grid grid-3">
              {shown.map((g, i) => <Reveal key={g.latest.id} delay={Math.min(i, 5) * 60}><TopicCard g={g} /></Reveal>)}
            </div>
          )}
        </div>
      </section>

      <section className="section" style={{ paddingTop: 16 }}>
        <div className="container stack">
          <LivePanel />
        </div>
      </section>
    </>
  );
}

function glow(e: React.MouseEvent<HTMLElement>) {
  const r = e.currentTarget.getBoundingClientRect();
  e.currentTarget.style.setProperty("--mx", `${((e.clientX - r.left) / r.width) * 100}%`);
  e.currentTarget.style.setProperty("--my", `${((e.clientY - r.top) / r.height) * 100}%`);
}

function TopicCard({ g }: { g: TopicGroup<RunSummary> }) {
  const run = g.latest;
  const score = run.score ?? 0;
  return (
    <Link className="card topic-card" href={`/runs/${run.id}`} onMouseMove={glow} style={{ height: "100%" }}>
      <div className="card-kicker"><span>{sectorLabel(run.sector)}</span><span>·</span><span>{fmtDate(run.generated_at)}</span></div>
      {run.locked && (
        <div><span className="pill" style={{ color: "#e0b04a", borderColor: "#e0b04a", whiteSpace: "nowrap" }}>
          {run.unlock_at ? "Early access" : "Paid"}{run.price_near != null ? ` · ${run.price_near} NEAR` : ""}
        </span></div>
      )}
      {run.demo_free && (
        <div><span className="pill pill-on" style={{ whiteSpace: "nowrap" }}>Unlocked for demo</span></div>
      )}
      <div className="row" style={{ alignItems: "flex-start", flexWrap: "nowrap", gap: 14 }}>
        <div className="card-title" style={{ flex: 1 }}>{run.topic}</div>
        {run.score !== null && (
          <div className="score-ring" style={{ ["--v" as string]: score } as React.CSSProperties} title={`Score ${score}/100`}>
            <span>{Math.round(score)}</span>
          </div>
        )}
      </div>
      <div className="small muted" style={{ marginTop: "auto" }}>
        {run.score === null ? "no score" : `${run.score_confidence ?? "low"} confidence`} · {run.findings} findings · {run.sources} sources
        {g.older.length > 0 && <> · {g.older.length + 1} runs</>}
      </div>
    </Link>
  );
}
