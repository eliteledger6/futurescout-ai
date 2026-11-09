"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AgentFlow } from "@/components/AgentFlow";
import { AgentIcon } from "@/components/AgentIcon";
import { LivePanel } from "@/components/LivePanel";
import { RadarStrip } from "@/components/RadarStrip";
import { CountUp, Reveal } from "@/components/motion";
import { ErrorNotice, Loading } from "@/components/ui";
import { AGENTS, type AgentKey } from "@/lib/agents";
import { api, fmtDate, fmtUsd } from "@/lib/api";
import type { ApiConfig, RunSummary } from "@/lib/types";

const STRIP: AgentKey[] = ["science", "patent", "market", "x", "risk", "investment"];

export default function Home() {
  const [runs, setRuns] = useState<RunSummary[] | null>(null);
  const [config, setConfig] = useState<ApiConfig | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([api.runs(), api.config()])
      .then(([r, c]) => { setRuns(r); setConfig(c); })
      .catch((e: Error) => setError(e.message));
  }, []);

  const latest = runs?.[0];
  const avgCost = runs && runs.length ? runs.reduce((s, r) => s + r.total_cost_usd, 0) / runs.length : null;

  return (
    <>
      <section className="hero">
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">Multi-agent technology research · every sector · 1-5 year horizon</div>
          <h1 className="display">Find the next hot technology. <span className="gradient-text">Show the evidence.</span></h1>
          <p className="lede">
            Eight AI agents read papers, patents, SEC filings and X posts, argue the other side, measure price run-up risk, find the companies behind the evidence,
            and write a report where every claim carries a label and its sources. Models run on NEAR AI Cloud; every report
            is sealed on NEAR.
          </p>
          <div className="actions">
            {latest ? (
              <Link className="btn btn-solid" href={`/runs/${latest.id}`}>Open latest report →</Link>
            ) : (
              <Link className="btn btn-solid" href="/research">Start research →</Link>
            )}
            <a className="btn btn-ghost" href="#agents">See the agents work</a>
          </div>
          <RadarStrip />
          <div className="marquee" aria-label="Data sources">
            {["OpenAlex", "arXiv", "Google Patents", "SEC EDGAR", "X API", "Alpha Vantage", "NEAR AI Cloud", "NEAR testnet"].map((s) => <span key={s}>{s}</span>)}
          </div>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 40, paddingBottom: 40 }}>
        <div className="container"><LivePanel /></div>
      </section>

      <section className="section" id="agents">
        <div className="container stack">
          <div className="section-head">
            <div>
              <div className="eyebrow">How the agents work together</div>
              <h2 className="h2" style={{ marginTop: 10 }}>One question, twelve steps, one sealed report</h2>
              <p className="sub">Hover or tap an agent to see what it does, where its data comes from and which model runs it.</p>
            </div>
          </div>
          <Reveal><AgentFlow models={config?.agents} /></Reveal>
          <div className="agent-strip">
            {STRIP.map((k) => (
              <div key={k}>
                <span className="ico"><AgentIcon name={AGENTS[k].icon} size={22} /></span>
                <strong style={{ fontFamily: "var(--font-display)", fontWeight: 500 }}>{AGENTS[k].name}</strong>
                <span className="small muted">{AGENTS[k].role}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          {error ? <ErrorNotice error={error} /> : (
            <Reveal>
              <div className="stats">
                <div className="stat"><div className="stat-value">{runs ? <CountUp value={runs.length} /> : "–"}</div><div className="stat-label">saved research runs</div></div>
                <div className="stat"><div className="stat-value">{config ? <CountUp value={Object.keys(config.agents).length} /> : "–"}</div><div className="stat-label">agents with live models</div></div>
                <div className="stat"><div className="stat-value">{latest ? <CountUp value={latest.sources} /> : "–"}</div><div className="stat-label">real sources in latest run</div></div>
                <div className="stat"><div className="stat-value">{avgCost !== null ? <CountUp value={avgCost} decimals={2} prefix="$" /> : "–"}</div><div className="stat-label">average cost per run</div></div>
              </div>
            </Reveal>
          )}
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="section-head">
            <div>
              <h2 className="h2">Research reports</h2>
              <p className="sub">Newest first{config ? ` · read from ${config.store === "database" ? "PostgreSQL" : "report files"}` : ""}.</p>
            </div>
            <Link className="btn btn-ghost" href="/research">New research</Link>
          </div>
          {error ? null : runs === null ? <Loading /> : runs.length === 0 ? (
            <div className="notice">No saved runs yet. Start one from <Link href="/research" style={{ color: "var(--accent)" }}>New research</Link>, or run <span className="mono">python scripts\run_research.py --topic "…"</span> in the backend folder.</div>
          ) : (
            <div className="grid grid-3">
              {runs.map((r, i) => <Reveal key={r.id} delay={Math.min(i, 5) * 70}><RunCard run={r} /></Reveal>)}
            </div>
          )}
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

function RunCard({ run }: { run: RunSummary }) {
  const score = run.score ?? 0;
  return (
    <Link className="card" href={`/runs/${run.id}`} onMouseMove={glow} style={{ height: "100%" }}>
      <div className="card-kicker"><span>{fmtDate(run.generated_at)}</span>{run.sector && <><span>·</span><span>{run.sector.replace(/_/g, " ")}</span></>}</div>
      <div className="row" style={{ alignItems: "flex-start", flexWrap: "nowrap" }}>
        <div className="card-title" style={{ flex: 1 }}>{run.topic}</div>
        {run.score !== null && (
          <div className="score-ring" style={{ ["--v" as string]: score } as React.CSSProperties} title={`Score ${score}/100`}>
            <span>{Math.round(score)}</span>
          </div>
        )}
      </div>
      {run.question && <div className="small muted">{run.question}</div>}
      <div className="small muted">
        {run.score === null ? "no score" : run.score_reportable ? `score confidence: ${run.score_confidence}` : "score not reportable"}
      </div>
      <div className="pills" style={{ marginTop: "auto" }}>
        <span className="pill">{run.agents_run.length} agents</span>
        <span className="pill">{run.findings} findings</span>
        <span className="pill">{run.sources} sources</span>
        <span className="pill">{fmtUsd(run.total_cost_usd)}</span>
        {run.errors > 0 && <span className="pill" style={{ color: "var(--l-unverified)" }}>{run.errors} errors</span>}
      </div>
    </Link>
  );
}
