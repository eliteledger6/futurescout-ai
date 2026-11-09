"use client";

// The report at a glance: numbers, small charts and one-line statements instead of paragraphs.
// Everything shown is taken from the stored report and the code-computed verdict; nothing is added here.
import { useState } from "react";
import { CountUp, Reveal, ScoreGauge } from "@/components/motion";
import type { Finding, Label, Report, Source, Verdict } from "@/lib/types";

const LABEL_ORDER: Label[] = ["verified_fact", "ai_interpretation", "forecast", "assumption", "unverified_claim"];
const LABEL_NAME: Record<Label, string> = {
  verified_fact: "Verified fact", ai_interpretation: "Interpretation", forecast: "Forecast",
  assumption: "Assumption", unverified_claim: "Unverified claim",
};
const LABEL_VAR: Record<Label, string> = {
  verified_fact: "var(--l-verified)", ai_interpretation: "var(--l-interp)", forecast: "var(--l-forecast)",
  assumption: "var(--l-assumption)", unverified_claim: "var(--l-unverified)",
};
const BAND_ICON: Record<string, string> = { strong: "▲", building: "◆", early: "●", weak: "▼", insufficient: "○" };

const pct = (v: number | null | undefined) => (v == null ? "–" : `${v > 0 ? "+" : ""}${Math.round(v)}%`);

function firstSentence(text: string | undefined | null, max = 150): string {
  const t = (text ?? "").replace(/\s*\[[^\]]*\]/g, "").replace(/\s*\((?:[A-Z]\d+[,\s]*)+\)/g, "").trim();   // drop citation markers
  const s = (t.split(/(?<=[.!?])\s/)[0] ?? t).trim();
  return s.length > max ? s.slice(0, max - 1).replace(/\s+\S*$/, "") + "…" : s;
}

function allFindings(r: Report): Finding[] {
  return [
    ...(r.science?.findings ?? []), ...(r.risk?.findings ?? []), ...(r.risk?.challenges ?? []).map((c) => c.finding),
    ...(r.market?.findings ?? []), ...(r.x?.findings ?? []), ...(r.patent?.findings ?? []), ...(r.timing?.findings ?? []),
    ...(r.scout?.findings ?? []),
  ];
}

export function ReportVisual({ report: r, verdict: v, sources }: { report: Report; verdict?: Verdict; sources: Map<string, Source> }) {
  const sc = r.investment?.score ?? null;
  const theme = r.investment?.draft?.themes?.[0];
  const findings = allFindings(r);
  return (
    <div className="rv">
      <Reveal><VerdictBanner v={v} score={sc?.score ?? null} reportable={!!sc?.reportable} confidence={sc?.confidence ?? null} /></Reveal>
      <Reveal delay={60}><Tiles r={r} findings={findings.length} sources={sources.size} /></Reveal>
      {sc && sc.dimensions.length > 0 && <Reveal delay={60}><ScoreBars r={r} /></Reveal>}
      {theme && <Reveal delay={60}><Scenarios bull={theme.bull.narrative} base={theme.base.narrative} bear={theme.bear.narrative} name={theme.name} /></Reveal>}
      {v?.available && <Reveal delay={60}><Signals v={v} /></Reveal>}
      {r.scout && r.scout.candidates.length > 0 && <Reveal delay={60}><Companies r={r} /></Reveal>}
      {r.timing && r.timing.metrics.length > 0 && <Reveal delay={60}><PriceCards r={r} /></Reveal>}
      {findings.length > 0 && <Reveal delay={60}><EvidenceMix findings={findings} sources={sources} /></Reveal>}
    </div>
  );
}

/* ------------------------------------------------------------------ verdict banner */
function VerdictBanner({ v, score, reportable, confidence }: { v?: Verdict; score: number | null; reportable: boolean; confidence: string | null }) {
  const [open, setOpen] = useState(false);
  const band = v?.band ?? "insufficient";
  const plain = v?.plain ?? "";
  const short = firstSentence(plain, 220);
  return (
    <section className={`rv-banner verdict-${band}`}>
      <div className="rv-banner-text">
        <div className="rv-kicker"><span className="rv-band-icon">{BAND_ICON[band]}</span> Verdict · forecast · computed from this report</div>
        <h2 className="rv-headline">{v?.headline ?? "No verdict"}</h2>
        {v?.qualifiers && v.qualifiers.length > 0 && (
          <div className="rv-chips">{v.qualifiers.slice(0, 3).map((q) => <span key={q} className="rv-chip">{firstSentence(q, 70)}</span>)}</div>
        )}
        {plain && (
          <p className="rv-plain">{open ? plain : short}{plain.length > short.length && (
            <button className="rv-more" onClick={() => setOpen(!open)}>{open ? " less" : " more"}</button>)}</p>
        )}
      </div>
      <div className="rv-gauge"><ScoreGauge score={score} reportable={reportable} confidence={confidence} size={168} /></div>
    </section>
  );
}

/* ------------------------------------------------------------------ number tiles */
function MiniBars({ counts, partialFrom }: { counts: Record<string, number>; partialFrom: number }) {
  const entries = Object.entries(counts).map(([y, c]) => [Number(y), c] as const).sort((a, b) => a[0] - b[0]).slice(-5);
  const max = Math.max(...entries.map(([, c]) => c), 1);
  return (
    <div className="rv-minibars" role="img" aria-label={entries.map(([y, c]) => `${y}: ${c}`).join(", ")}>
      {entries.map(([y, c]) => (
        <div key={y} className="rv-mb" title={`${y}: ${c}${y >= partialFrom ? " (year not finished)" : ""}`}>
          <div className={`rv-mb-bar ${y >= partialFrom ? "partial" : ""}`} style={{ ["--h" as string]: `${Math.max(4, (c / max) * 100)}%` } as React.CSSProperties} />
          <span>{String(y).slice(2)}</span>
        </div>
      ))}
    </div>
  );
}

function Tiles({ r, findings, sources }: { r: Report; findings: number; sources: number }) {
  const year = new Date(r.generated_at).getFullYear();
  const a = r.science?.acceleration, y = r.science?.ytd, pa = r.patent?.acceleration;
  const risk = r.investment?.score?.risk_rating ?? null;
  const cov = r.investment?.score?.coverage ?? null;
  const cands = (r.scout?.candidates ?? []).filter((c) => !c.off_sector);
  const trendColour = y?.trend === "rising" ? "var(--accent)" : y?.trend === "cooling" ? "var(--l-danger)" : "var(--text-2)";
  return (
    <section className="rv-tiles">
      <div className="rv-tile">
        <div className="rv-tile-label">Research growth</div>
        <div className="rv-tile-value">{a?.yoy_growth_pct != null ? <CountUp value={Math.abs(a.yoy_growth_pct)} prefix={a.yoy_growth_pct >= 0 ? "+" : "−"} suffix="%" /> : "–"}</div>
        <div className="rv-tile-sub">papers {a ? `${a.previous_year}→${a.last_full_year}` : ""}{y && <> · <span style={{ color: trendColour }}>{y.year} so far {pct(y.growth_pct)} {y.trend ?? ""}</span></>}</div>
        {r.science && Object.keys(r.science.publication_counts).length > 0 && <MiniBars counts={r.science.publication_counts} partialFrom={year} />}
      </div>
      <div className="rv-tile">
        <div className="rv-tile-label">Patent growth</div>
        <div className="rv-tile-value">{pa?.yoy_growth_pct != null ? <CountUp value={Math.abs(pa.yoy_growth_pct)} prefix={pa.yoy_growth_pct >= 0 ? "+" : "−"} suffix="%" /> : "–"}</div>
        <div className="rv-tile-sub">{pa ? `publications ${pa.previous_year}→${pa.last_full_year}` : "patents not counted for this run"}</div>
        {r.patent && Object.keys(r.patent.publication_counts).length > 0 && <MiniBars counts={r.patent.publication_counts} partialFrom={year - 1} />}
      </div>
      <div className="rv-tile">
        <div className="rv-tile-label">Risk</div>
        <div className="rv-dots" aria-label={risk == null ? "risk not rated" : `risk ${risk} of 5`}>
          {[1, 2, 3, 4, 5].map((i) => <span key={i} className={`rv-dot ${risk != null && i <= risk ? "on" : ""} ${risk != null && risk >= 4 ? "hot" : ""}`} />)}
        </div>
        <div className="rv-tile-sub">{risk == null ? "not rated" : risk >= 4 ? "high" : risk >= 3 ? "moderate" : "low"} · from the Risk agent</div>
      </div>
      <div className="rv-tile">
        <div className="rv-tile-label">Evidence coverage</div>
        <div className="rv-tile-value">{cov != null ? <CountUp value={cov * 100} suffix="%" /> : "–"}</div>
        <div className="rv-tile-sub">of the score backed by cited findings</div>
        {cov != null && <div className="rv-meter"><div className="rv-meter-fill" style={{ ["--w" as string]: `${cov * 100}%` } as React.CSSProperties} /></div>}
      </div>
      <div className="rv-tile">
        <div className="rv-tile-label">Companies found</div>
        <div className="rv-tile-value"><CountUp value={cands.length} /></div>
        <div className="rv-tile-sub">{cands.slice(0, 3).map((c) => c.ticker ?? c.name).join(" · ") || "none outside the big names"}</div>
      </div>
      <div className="rv-tile">
        <div className="rv-tile-label">Evidence read</div>
        <div className="rv-tile-value"><CountUp value={sources} /></div>
        <div className="rv-tile-sub">sources · {findings} labelled findings</div>
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ score breakdown */
function ScoreBars({ r }: { r: Report }) {
  const sc = r.investment!.score!;
  const dims = [...sc.dimensions].sort((a, b) => (b.rating ?? -1) - (a.rating ?? -1));
  return (
    <section className="rv-card">
      <div className="rv-card-head"><h3>What the score is made of</h3><span className="small muted">0–5 per dimension · hover a bar for the reason</span></div>
      <div className="rv-bars">
        {dims.map((d) => (
          <div key={d.key} className="rv-bar-row" title={d.status === "scored" ? firstSentence(d.rationale, 240) : (d.missing_reason ?? "no cited evidence")}>
            <span className="rv-bar-label">{d.label}</span>
            <div className="rv-bar-track">
              {d.status === "scored" && d.rating != null
                ? <div className="rv-bar-fill" style={{ ["--w" as string]: `${(d.rating / 5) * 100}%` } as React.CSSProperties} />
                : <div className="rv-bar-missing">no evidence</div>}
            </div>
            <span className="rv-bar-val">{d.status === "scored" && d.rating != null ? `${d.rating}/5` : "–"}</span>
          </div>
        ))}
        {sc.risk_rating != null && (
          <div className="rv-bar-row" title={`Risk lowers the score by ${sc.risk_penalty_pct ?? 0}%`}>
            <span className="rv-bar-label">Risk (lowers score)</span>
            <div className="rv-bar-track"><div className="rv-bar-fill risk" style={{ ["--w" as string]: `${(sc.risk_rating / 5) * 100}%` } as React.CSSProperties} /></div>
            <span className="rv-bar-val">{sc.risk_rating}/5</span>
          </div>
        )}
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ scenarios */
function Scenarios({ bull, base, bear, name }: { bull: string; base: string; bear: string; name: string }) {
  const items = [
    { k: "bull", t: "If it goes well", icon: "▲", text: bull },
    { k: "base", t: "Most likely", icon: "●", text: base },
    { k: "bear", t: "If it goes badly", icon: "▼", text: bear },
  ];
  return (
    <section className="rv-card">
      <div className="rv-card-head"><h3>Three ways it could play out</h3><span className="small muted">{name} · forecasts, not facts · click to read more</span></div>
      <div className="rv-scen">
        {items.map((s) => <ScenarioCard key={s.k} {...s} />)}
      </div>
    </section>
  );
}

function ScenarioCard({ k, t, icon, text }: { k: string; t: string; icon: string; text: string }) {
  const [open, setOpen] = useState(false);
  return (
    <button className={`rv-scen-card ${k}`} onClick={() => setOpen(!open)} aria-expanded={open}>
      <span className="rv-scen-icon">{icon}</span>
      <span className="rv-scen-title">{t}</span>
      <span className="rv-scen-text">{open ? text.replace(/\s*\[[^\]]*\]/g, "") : firstSentence(text, 140)}</span>
    </button>
  );
}

/* ------------------------------------------------------------------ why / watch / change */
function Signals({ v }: { v: Verdict }) {
  const cols = [
    { k: "why", t: "Why", icon: "✓", items: v.why ?? [] },
    { k: "watch", t: "Watch out", icon: "!", items: v.watch ?? [] },
    { k: "change", t: "What would change it", icon: "↻", items: v.change ?? [] },
  ];
  return (
    <section className="rv-signals">
      {cols.map((c) => (
        <div key={c.k} className={`rv-sig ${c.k}`}>
          <div className="rv-sig-head"><span className="rv-sig-icon">{c.icon}</span>{c.t}</div>
          <ul>{c.items.slice(0, 3).map((x) => <li key={x} title={x}>{tidy(x)}</li>)}</ul>
        </div>
      ))}
    </section>
  );
}

// "Research Momentum rated 5/5: Code-computed OpenAlex counts ..." -> "Research Momentum 5/5 · OpenAlex counts ..."
function tidy(line: string): string {
  const m = line.match(/^(.+?) rated (\d)\/5:\s*(.*)$/);
  const text = m ? `${m[1]} ${m[2]}/5 · ${m[3]}` : line;
  return firstSentence(text.replace(/\bCode-computed\s+/gi, "").replace(/^(Stronger|Weaker) if:\s*/i, (_, w) => `${w} if `), 95);
}

/* ------------------------------------------------------------------ companies */
function Companies({ r }: { r: Report }) {
  const list = r.scout!.candidates.filter((c) => !c.off_sector).slice(0, 6);
  if (!list.length) return null;
  return (
    <section className="rv-card">
      <div className="rv-card-head"><h3>Companies behind the evidence</h3><span className="small muted">beyond the big names · next-runner score is a heuristic, not a recommendation</span></div>
      <div className="rv-cos">
        {list.map((c) => {
          const f = c.fundamentals;
          return (
            <div key={c.name} className="rv-co" title={c.score_reasons.join("\n")}>
              <span className="rv-co-avatar">{(c.ticker ?? c.name).slice(0, 2)}</span>
              <div className="rv-co-body">
                <div className="rv-co-name">{c.name} <span className="mono small muted">{c.ticker}</span></div>
                <div className="rv-co-meta">
                  {f?.size_class && <span className="pill">{f.size_class}</span>}
                  {f?.revenue_growth_pct != null && <span className="small muted">revenue {pct(f.revenue_growth_pct)}</span>}
                  {c.patents > 0 && <span className="small muted">{c.patents} patents</span>}
                  {c.papers > 0 && <span className="small muted">{c.papers} papers</span>}
                </div>
                <div className="rv-meter"><div className="rv-meter-fill" style={{ ["--w" as string]: `${c.next_runner_score ?? 0}%` } as React.CSSProperties} /></div>
              </div>
              <span className="rv-co-score">{c.next_runner_score != null ? Math.round(c.next_runner_score) : "–"}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ price cards */
function Spark({ closes }: { closes: number[] }) {
  if (closes.length < 2) return null;
  const w = 220, h = 54, min = Math.min(...closes), max = Math.max(...closes), span = max - min || 1;
  const pts = closes.map((c, i) => `${(i / (closes.length - 1)) * w},${h - ((c - min) / span) * (h - 6) - 3}`).join(" ");
  const up = closes[closes.length - 1] >= closes[0];
  return (
    <svg className="rv-spark" viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" role="img" aria-label={`last ${closes.length} closes, ${up ? "up" : "down"}`}>
      <polyline points={pts} fill="none" stroke={up ? "var(--accent)" : "var(--l-danger)"} strokeWidth="2" strokeLinejoin="round" vectorEffect="non-scaling-stroke" />
    </svg>
  );
}

function PriceCards({ r }: { r: Report }) {
  const t = r.timing!;
  return (
    <section className="rv-card">
      <div className="rv-card-head"><h3>Has the market already moved?</h3><span className="small muted">last ~100 trading days · a risk check, never a buy or sell signal</span></div>
      <div className="rv-prices">
        {t.metrics.map((m) => (
          <div key={m.ticker} className="rv-price" title={m.reasons.join("; ")}>
            <div className="rv-price-head"><strong>{m.ticker}</strong><span className={`rv-level ${m.timing_risk}`}>{m.timing_risk === "elevated" ? "already ran hard" : m.timing_risk === "subdued" ? "weak lately" : "normal"}</span></div>
            {m.closes && <Spark closes={m.closes} />}
            <div className="rv-price-foot"><span>3 months <b>{pct(m.return_3m_pct)}</b></span><span>vs 50-day avg <b>{pct(m.vs_50d_avg_pct)}</b></span></div>
          </div>
        ))}
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ evidence mix */
function EvidenceMix({ findings, sources }: { findings: Finding[]; sources: Map<string, Source> }) {
  const counts = LABEL_ORDER.map((l) => ({ l, n: findings.filter((f) => f.label === l).length })).filter((x) => x.n > 0);
  const total = counts.reduce((s, x) => s + x.n, 0) || 1;
  const types = new Map<string, number>();
  for (const s of sources.values()) types.set(s.content_type, (types.get(s.content_type) ?? 0) + 1);
  return (
    <section className="rv-card">
      <div className="rv-card-head"><h3>How solid is the evidence?</h3><span className="small muted">every claim carries one of these labels</span></div>
      <div className="rv-stack" role="img" aria-label={counts.map((c) => `${LABEL_NAME[c.l]}: ${c.n}`).join(", ")}>
        {counts.map((c) => (
          <div key={c.l} className="rv-stack-seg" title={`${LABEL_NAME[c.l]}: ${c.n}`}
               style={{ ["--w" as string]: `${(c.n / total) * 100}%`, background: LABEL_VAR[c.l] } as React.CSSProperties} />
        ))}
      </div>
      <div className="rv-legend">
        {counts.map((c) => <span key={c.l}><i style={{ background: LABEL_VAR[c.l] }} />{LABEL_NAME[c.l]} <b>{c.n}</b></span>)}
      </div>
      <div className="rv-legend muted">
        {[...types.entries()].sort((a, b) => b[1] - a[1]).map(([t, n]) => <span key={t}>{t.replace(/_/g, " ")} <b>{n}</b></span>)}
      </div>
    </section>
  );
}
