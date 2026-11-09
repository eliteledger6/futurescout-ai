"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { api, fmtDate, fmtUsd } from "@/lib/api";
import type { CompanySignal, Finding, Label, Report, RunDetail, Source, Theme } from "@/lib/types";
import { ConfidencePill, ErrorNotice, LABEL_HELP, LabelBadge, Loading } from "@/components/ui";
import { NearBadge } from "@/components/NearBadge";
import { AgentFlow } from "@/components/AgentFlow";
import { ReportToc } from "@/components/ReportToc";
import { Reveal, ScoreGauge } from "@/components/motion";
import { agentStats } from "@/lib/agents";

const HORIZON_NAME: Record<string, string> = { near_0_12m: "0-12 months", medium_1_3y: "1-3 years", long_3_5y: "3-5 years" };

export default function RunPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<RunDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.run(id).then(setData).catch((e: Error) => setError(e.message));
  }, [id]);

  if (error) return <section className="section"><div className="container"><ErrorNotice error={error} /></div></section>;
  if (!data) return <section className="section"><div className="container"><Loading lines={5} /></div></section>;
  return <ReportView data={data} />;
}

function ReportView({ data }: { data: RunDetail }) {
  const r = data.report;
  const sources = useMemo(() => {
    const m = new Map<string, Source>();
    [r.science, r.risk, r.market, r.x, r.patent, r.timing].forEach((p) => p?.sources.forEach((s) => m.set(s.id, s)));
    return m;
  }, [r]);
  const draft = r.investment?.draft;

  return (
    <>
      <section className="hero" style={{ padding: "72px 0 56px", textAlign: "left" }}>
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="row small muted"><Link href="/">← Reports</Link><span>·</span><span>{fmtDate(r.generated_at)}</span>{r.sector && <><span>·</span><span className="pill">{r.sector.replace(/_/g, " ")}</span></>}</div>
          <h1 className="display" style={{ fontSize: "clamp(40px, 6vw, 72px)", margin: "16px 0 14px", maxWidth: "none" }}>{r.topic}</h1>
          {r.question && <p className="lede" style={{ margin: 0 }}>Question: {r.question}</p>}
          <div className="pills" style={{ marginTop: 20 }}>
            {r.agents_run.map((a) => <span key={a} className="pill pill-on"><span className="dot" />{a}</span>)}
            {r.agents_not_run.map((a) => <span key={a} className="pill" title="No analysed evidence from this agent">{a}: not run</span>)}
          </div>
          <div className="pills" style={{ marginTop: 10 }}><NearBadge runId={data.summary.id} /></div>
        </div>
      </section>

      <ReportToc items={[
        { id: "summary", label: "Summary" }, { id: "trace", label: "Agent trace" },
        ...(r.investment?.score ? [{ id: "score", label: "Score" }] : []),
        ...(draft && draft.themes.length ? [{ id: "themes", label: "Themes" }] : []),
        { id: "evidence", label: "Evidence" },
        ...(r.science && Object.keys(r.science.publication_counts).length ? [{ id: "activity", label: "Research activity" }] : []),
        ...(r.patent && Object.keys(r.patent.publication_counts).length ? [{ id: "patents", label: "Patent activity" }] : []),
        ...(r.scout && (r.scout.candidates.length || r.scout.unlisted.length) ? [{ id: "scout", label: "Emerging companies" }] : []),
        ...(r.market && r.market.companies.length ? [{ id: "companies", label: "Companies" }] : []),
        ...(r.timing && r.timing.metrics.length ? [{ id: "timing", label: "Price & timing" }] : []),
        { id: "sources", label: "Sources" }, { id: "gaps", label: "Gaps" }, { id: "usage", label: "Cost" },
      ]} />

      <section className="section" id="summary">
        <div className="container stack">
          <h2 className="h3">Summary</h2>
          <p style={{ fontSize: 17, maxWidth: 900, color: "var(--text-2)" }}>
            {draft ? draft.summary : "No assessment was generated for this run (see errors below)."}
          </p>
          <div className="notice small">
            <strong style={{ color: "var(--text)" }}>Research information only, not investment advice.</strong> Every claim below carries a label.
            Hover a label to see what it means.
          </div>
        </div>
      </section>

      <section className="section" id="trace">
        <div className="container stack">
          <div>
            <div className="eyebrow">Agent trace</div>
            <h2 className="h2" style={{ marginTop: 10 }}>How the agents built this report</h2>
            <p className="sub">Green dot: the agent&apos;s analysis succeeded. Amber: data was gathered but not analysed. Dashed: not run for this report.
              Hover or tap an agent for its findings, sources, model and cost.</p>
          </div>
          <Reveal><AgentFlow stats={agentStats(r)} /></Reveal>
        </div>
      </section>

      {r.investment?.score && <ScoreSection report={r} />}
      {draft && draft.themes.length > 0 && <ThemesSection themes={draft.themes} />}
      <EvidenceSection report={r} sources={sources} />
      {r.science && Object.keys(r.science.publication_counts).length > 0 && <ActivitySection report={r} />}
      {r.patent && Object.keys(r.patent.publication_counts).length > 0 && <PatentActivitySection report={r} />}
      {r.scout && (r.scout.candidates.length > 0 || r.scout.unlisted.length > 0) && <ScoutSection report={r} sources={sources} />}
      {r.market && r.market.companies.length > 0 && <CompaniesSection report={r} />}
      {r.timing && r.timing.metrics.length > 0 && <TimingSection report={r} />}
      <SourcesSection sources={[...sources.values()]} />
      <GapsSection report={r} />
      <UsageSection report={r} />
    </>
  );
}

/* ---------------------------------------------------------------- score */
function ScoreSection({ report }: { report: Report }) {
  const sc = report.investment!.score!;
  return (
    <section className="section" id="score">
      <div className="container">
        <div className="section-head">
          <div>
            <h2 className="h2">Technology Opportunity Score</h2>
            <p className="sub">An explainable heuristic from cited ratings. Weights are initial assumptions, not a prediction of stock performance.</p>
          </div>
        </div>
        <div className="score-hero">
          <div className="score-left stack">
            <ScoreGauge score={sc.score} reportable={sc.reportable} confidence={sc.confidence} />
            <div className="pills">
              <ConfidencePill value={sc.confidence} />
              <span className="pill">coverage {Math.round(sc.coverage * 100)}%</span>
              {!sc.reportable && <span className="pill" style={{ color: "var(--l-unverified)" }}>not reportable</span>}
            </div>
            {sc.risk_rating !== null && (
              <p className="small muted">Risk rating {sc.risk_rating}/5 lowered the score by {sc.risk_penalty_pct}% (base {sc.base_score}).</p>
            )}
            <ul className="small muted" style={{ paddingLeft: 18, margin: 0 }}>
              {sc.notes.map((n, i) => <li key={i}>{n}</li>)}
            </ul>
          </div>
          <div className="score-right">
            {sc.dimensions.map((d) => (
              <div className="dim" key={d.key} title={d.status === "scored" ? d.rationale : d.missing_reason ?? ""}>
                <div className="dim-name">{d.label}<span>weight {Math.round(d.weight * 100)}%{d.status === "scored" && d.confidence ? ` · ${d.confidence}` : ""}</span></div>
                <div className="track" role="img" aria-label={`${d.label}: ${d.status === "scored" ? `${d.rating} of 5` : "missing"}`}>
                  {d.status === "scored"
                    ? <div className="bar" style={{ width: `${((d.rating ?? 0) / 5) * 100}%` }} />
                    : <div className="bar bar-missing" />}
                </div>
                <div className="dim-val">{d.status === "scored" ? `${d.rating}/5` : "–"}</div>
              </div>
            ))}
            <p className="small muted" style={{ marginTop: 12 }}>
              Hatched = missing: no agent supplied cited evidence (counted as missing, never as zero). Hover a row for the reasoning.
            </p>
          </div>
        </div>
        <details style={{ marginTop: 16 }}>
          <summary className="small muted" style={{ cursor: "pointer" }}>Show the reasoning and evidence for each dimension</summary>
          <div className="table-wrap" style={{ marginTop: 12 }}>
            <table className="table">
              <thead><tr><th>Dimension</th><th className="num">Rating</th><th>Evidence</th><th>Reasoning</th></tr></thead>
              <tbody>
                {sc.dimensions.map((d) => (
                  <tr key={d.key}>
                    <td>{d.label}</td>
                    <td className="num">{d.status === "scored" ? d.rating : "missing"}</td>
                    <td className="mono small">{d.finding_ids.map((f) => <a key={f} href={`#${f}`} style={{ marginRight: 6 }}>{f}</a>)}</td>
                    <td className="small">{d.status === "scored" ? d.rationale : d.missing_reason}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="small muted mono" style={{ marginTop: 10 }}>{sc.formula}</p>
        </details>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- themes */
function Refs({ ids }: { ids: string[] }) {
  if (!ids.length) return <span className="small muted"> [no supporting finding]</span>;
  return <span className="mono small"> {ids.map((f) => <a key={f} href={`#${f}`} style={{ marginRight: 5, color: "var(--muted)" }}>{f}</a>)}</span>;
}

function ThemesSection({ themes }: { themes: Theme[] }) {
  const [active, setActive] = useState(0);
  const t = themes[active];
  return (
    <section className="section" id="themes">
      <div className="container stack">
        <div className="section-head">
          <div>
            <h2 className="h2">Investment themes</h2>
            <p className="sub">Scenarios and horizon views are AI forecasts and interpretations tied to cited findings. They are not facts.</p>
          </div>
        </div>
        <div className="tabs" role="tablist">
          {themes.map((th, i) => (
            <button key={i} className={`tab ${i === active ? "on" : ""}`} onClick={() => setActive(i)} role="tab" aria-selected={i === active}>{th.name}</button>
          ))}
        </div>
        {t.technologies.length > 0 && <div className="pills">{t.technologies.map((x) => <span key={x} className="pill">{x}</span>)}</div>}

        <div className="table-wrap">
          <table className="table">
            <thead><tr><th style={{ width: 130 }}>Horizon</th><th>Assessment</th><th style={{ width: 110 }}>Confidence</th></tr></thead>
            <tbody>
              {t.horizons.map((h) => (
                <tr key={h.horizon}>
                  <td>{HORIZON_NAME[h.horizon] ?? h.horizon}</td>
                  <td><LabelBadge label={h.label} /> {h.assessment}<Refs ids={h.finding_ids} />{h.note && <div className="note guard">{h.note}</div>}</td>
                  <td>{h.confidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="scen">
          {(["bull", "base", "bear"] as const).map((k) => (
            <div key={k}>
              <h4 style={{ color: k === "bull" ? "var(--accent)" : k === "bear" ? "var(--l-unverified)" : "var(--text-2)" }}>{k} case</h4>
              <div><LabelBadge label={t[k].label} /></div>
              <p className="small" style={{ color: "var(--text-2)" }}>{t[k].narrative}<Refs ids={t[k].finding_ids} /></p>
            </div>
          ))}
        </div>

        <div className="grid grid-2">
          {([["Catalysts", t.catalysts], ["Risks", t.risks], ["What would invalidate this thesis", t.invalidation_conditions], ["Conflicting evidence", t.conflicting_evidence]] as const).map(([title, items]) => (
            <div className="card" key={title}>
              <h3 className="h3" style={{ fontSize: 18 }}>{title}</h3>
              {items.length === 0 ? <p className="small muted">None stated.</p> : items.map((it, i) => (
                <p key={i} className="small" style={{ margin: 0, color: "var(--text-2)" }}><LabelBadge label={it.label} /> {it.text}<Refs ids={it.finding_ids} /></p>
              ))}
            </div>
          ))}
        </div>

        <div className="panel">
          <h3 className="h3" style={{ fontSize: 18 }}>Companies named by cited evidence</h3>
          {t.companies.length === 0 ? <p className="small muted">None: no cited finding names a company for this theme.</p> : (
            <div className="stack">
              {t.companies.map((c) => <p key={c.name} className="small" style={{ margin: 0 }}><strong>{c.name}</strong> <span style={{ color: "var(--text-2)" }}>{c.relevance}</span><Refs ids={c.finding_ids} /></p>)}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- evidence */
type Group = "science" | "risk" | "challenges" | "market" | "x" | "patent" | "timing";

function EvidenceSection({ report, sources }: { report: Report; sources: Map<string, Source> }) {
  const groups: { key: Group; name: string; items: { f: Finding; extra?: string }[] }[] = [
    { key: "science", name: "Science", items: (report.science?.findings ?? []).map((f) => ({ f })) },
    { key: "risk", name: "Risk", items: (report.risk?.findings ?? []).map((f) => ({ f })) },
    { key: "challenges", name: "Risk challenges", items: (report.risk?.challenges ?? []).map((c) => ({ f: c.finding, extra: `challenges ${c.target_finding_ids.join(", ") || "general"} · severity ${c.severity}` })) },
    { key: "market", name: "Market", items: (report.market?.findings ?? []).map((f) => ({ f })) },
    { key: "x", name: "X signals", items: (report.x?.findings ?? []).map((f) => ({ f })) },
    { key: "patent", name: "Patents", items: (report.patent?.findings ?? []).map((f) => ({ f })) },
    { key: "timing", name: "Price & timing", items: (report.timing?.findings ?? []).map((f) => ({ f })) },
  ];
  const [group, setGroup] = useState<Group>("science");
  const [label, setLabel] = useState<Label | "all">("all");

  // Finding links (#S1, #R2, #C3, #M4) elsewhere on the page: open the right tab, then scroll to it.
  useEffect(() => {
    const prefix: Record<string, Group> = { S: "science", R: "risk", C: "challenges", M: "market", X: "x", P: "patent", T: "timing" };
    function open() {
      const fid = decodeURIComponent(window.location.hash.slice(1));
      const target = prefix[fid.charAt(0)];
      if (!target || !/^[SRCMXPT]\d+$/.test(fid)) return;
      setGroup(target);
      setLabel("all");
      setTimeout(() => {
        const el = document.getElementById(fid);
        if (el) {
          el.scrollIntoView({ behavior: "smooth", block: "center" });
          el.classList.add("flash");
          setTimeout(() => el.classList.remove("flash"), 1600);
        }
      }, 60);
    }
    open();
    window.addEventListener("hashchange", open);
    return () => window.removeEventListener("hashchange", open);
  }, []);
  const current = groups.find((g) => g.key === group)!;
  const shown = current.items.filter((i) => label === "all" || i.f.label === label);
  const labels: Label[] = ["verified_fact", "ai_interpretation", "forecast", "unverified_claim", "assumption"];

  return (
    <section className="section" id="evidence">
      <div className="container stack">
        <div className="section-head">
          <div>
            <h2 className="h2">Evidence</h2>
            <p className="sub">Every finding, its label, the exact quote that supports it (if any) and links to the real sources.</p>
          </div>
        </div>
        <div className="row" style={{ justifyContent: "space-between" }}>
          <div className="tabs" role="tablist">
            {groups.map((g) => (
              <button key={g.key} className={`tab ${g.key === group ? "on" : ""}`} onClick={() => setGroup(g.key)}>{g.name} · {g.items.length}</button>
            ))}
          </div>
          <div className="tabs">
            <button className={`tab ${label === "all" ? "on" : ""}`} onClick={() => setLabel("all")}>all labels</button>
            {labels.map((l) => (
              <button key={l} className={`tab ${label === l ? "on" : ""}`} onClick={() => setLabel(l)} title={LABEL_HELP[l]}>{l.replace("_", " ")}</button>
            ))}
          </div>
        </div>
        {group === "market" && report.market && <p className="small muted">{report.market.coverage_note}</p>}
        {group === "science" && report.science && <p className="small muted">{report.science.coverage_note}</p>}
        {group === "x" && report.x && (
          <p className="small muted">
            {report.x.coverage_note} Accounts: {report.x.accounts.map((a) => "@" + a).join(", ")}.
            {report.x.x_usage?.posts_read !== undefined && ` Posts read: ${report.x.x_usage.posts_read}.`}
          </p>
        )}
        {group === "patent" && report.patent && <p className="small muted">{report.patent.coverage_note}</p>}
        {group === "patent" && !report.patent && <p className="small muted">The Patent agent did not run for this report.</p>}
        {group === "x" && !report.x && <p className="small muted">The X agent did not run for this report (it was added after this run).</p>}
        <div className="panel" style={{ paddingTop: 4, paddingBottom: 4 }}>
          {shown.length === 0 ? <p className="small muted" style={{ padding: "16px 0" }}>No findings in this view.</p> : shown.map(({ f, extra }) => (
            <article className="finding" key={f.fid ?? f.claim} id={f.fid ?? undefined}>
              <div className="finding-head">
                <span className="fid">{f.fid}</span>
                <LabelBadge label={f.label} />
                <ConfidencePill value={f.confidence} />
                {extra && <span className="pill">{extra}</span>}
                {f.companies.map((c) => <span key={c} className="pill">{c}</span>)}
              </div>
              <div className="claim">{f.claim}</div>
              {f.supporting_excerpt && <blockquote className="excerpt">“{f.supporting_excerpt}”</blockquote>}
              {f.rationale && <div className="note">{f.rationale}</div>}
              {f.guard_note && <div className="note guard">Citation check: {f.guard_note}</div>}
              <div className="src-links">
                {f.source_ids.map((sid) => {
                  const s = sources.get(sid);
                  return s ? (
                    <a key={sid} href={s.url} target="_blank" rel="noopener noreferrer">
                      {s.title} · {s.source_name}, {s.published_at ?? "date unknown"} · {s.text_depth.replace("_", " ")}
                    </a>
                  ) : <span key={sid} className="small muted">{sid}</span>;
                })}
              </div>
            </article>
          ))}
        </div>
        {group === "risk" && report.risk && report.risk.hype_flags.length > 0 && (
          <div className="panel">
            <h3 className="h3" style={{ fontSize: 18 }}>Possible hype</h3>
            <ul className="small" style={{ color: "var(--text-2)", margin: 0, paddingLeft: 18 }}>{report.risk.hype_flags.map((h, i) => <li key={i}>{h}</li>)}</ul>
          </div>
        )}
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- research activity chart */
function ActivitySection({ report }: { report: Report }) {
  const s = report.science!;
  const entries = Object.entries(s.publication_counts).map(([y, c]) => [Number(y), c] as const).sort((a, b) => a[0] - b[0]);
  const max = Math.max(...entries.map(([, c]) => c), 1);
  const thisYear = new Date(report.generated_at).getFullYear();
  const a = s.acceleration;
  return (
    <section className="section" id="activity">
      <div className="container">
        <div className="grid grid-2" style={{ background: "transparent", border: 0, gap: 32 }}>
          <div style={{ background: "transparent" }}>
            <h2 className="h2">Research activity</h2>
            <p className="sub">OpenAlex works per publication year containing the exact topic phrase in title or abstract.</p>
            {a && (
              <div style={{ marginTop: 24 }}>
                <div className="stat-value" style={{ fontSize: 56 }}>{a.yoy_growth_pct !== null ? `${a.yoy_growth_pct > 0 ? "+" : ""}${a.yoy_growth_pct}%` : "–"}</div>
                <div className="stat-label">Research Acceleration {a.previous_year} → {a.last_full_year} ({a.previous_year_count} → {a.last_full_year_count} works)</div>
              </div>
            )}
            <p className="small muted" style={{ marginTop: 20 }}>{a?.basis} Research activity is not commercial success.</p>
          </div>
          <div style={{ background: "transparent" }}>
            <div className="cols" role="img" aria-label={`Works per year: ${entries.map(([y, c]) => `${y}: ${c}`).join(", ")}`}>
              {entries.map(([y, c]) => (
                <div className="col" key={y}>
                  <div className="col-tip">{y}: {c} works{y === thisYear ? " (partial year)" : ""}</div>
                  <div className={`col-bar ${y === thisYear ? "partial" : ""}`} style={{ height: `${(c / max) * 100}%` }} />
                </div>
              ))}
            </div>
            <div className="col-axis">{entries.map(([y]) => <span key={y}>{y}</span>)}</div>
            <p className="small muted" style={{ marginTop: 10 }}>Hatched = current year, still incomplete. Hover a bar for its count.</p>
            <details><summary className="small muted" style={{ cursor: "pointer" }}>Table view</summary>
              <table className="table" style={{ marginTop: 8 }}><thead><tr><th>Year</th><th className="num">Works</th></tr></thead>
                <tbody>{entries.map(([y, c]) => <tr key={y}><td>{y}</td><td className="num">{c}</td></tr>)}</tbody></table>
            </details>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- companies checked */
function CompaniesSection({ report }: { report: Report }) {
  const m = report.market!;
  return (
    <section className="section" id="companies">
      <div className="container stack">
        <h2 className="h2">Company filings checked</h2>
        <p className="sub">Latest SEC annual and quarterly reports (and recent 8-K press releases), searched for: {m.keywords.join(", ")}. A report that does not mention the keywords does not show that the company is absent from this market.
          Size classes (micro &lt; $100M, small &lt; $1B, mid &lt; $10B, large) are by reported revenue from SEC XBRL data, not market value.</p>
        <div className="table-wrap">
          <table className="table">
            <thead><tr><th>Company</th><th className="num">Reports read</th><th className="num">Mentioning keywords</th><th>Size (revenue)</th><th className="num">Revenue growth</th><th className="num">R&amp;D / revenue</th><th>Note</th></tr></thead>
            <tbody>{m.companies.map((c) => {
              const f = c.fundamentals;
              const rev = f?.latest_year ? f.revenue[String(f.latest_year)] : undefined;
              return (
                <tr key={c.ticker}>
                  <td>{c.name} <span className="muted mono small">{c.ticker}</span>{c.discovered && <span className="pill" style={{ marginLeft: 6 }}>discovered</span>}</td>
                  <td className="num">{c.filings_checked}{c.press_releases_read ? <div className="small muted">+{c.press_releases_read} press rel.</div> : null}</td>
                  <td className="num">{c.filings_with_mentions}</td>
                  <td title={f?.summary}>{rev !== undefined ? <><span className="pill">{f!.size_class}</span> <span className="small muted">{(rev / 1e9).toFixed(1)}B {f!.currency} · FY{f!.latest_year}</span></> : <span className="muted">–</span>}</td>
                  <td className="num">{f?.revenue_growth_pct != null ? `${f.revenue_growth_pct > 0 ? "+" : ""}${f.revenue_growth_pct.toFixed(1)}%` : "–"}</td>
                  <td className="num">{f?.rnd_intensity_pct != null ? `${f.rnd_intensity_pct.toFixed(1)}%` : "–"}</td>
                  <td className="small">{c.error ?? ""}</td>
                </tr>
              );
            })}</tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- sources */
function SourcesSection({ sources }: { sources: Source[] }) {
  const sorted = [...sources].sort((a, b) => (b.published_at ?? "").localeCompare(a.published_at ?? ""));
  return (
    <section className="section" id="sources">
      <div className="container stack">
        <h2 className="h2">Sources · {sources.length}</h2>
        <p className="sub">Every source was retrieved from a real API (OpenAlex, arXiv, SEC EDGAR, GDELT, X, EPO). News items are headlines only; X posts are social signals, never facts.</p>
        <div className="table-wrap">
          <table className="table">
            <thead><tr><th>Title</th><th>Source</th><th>Published</th><th>Text read</th></tr></thead>
            <tbody>{sorted.map((s) => (
              <tr key={s.id}>
                <td><a href={s.url} target="_blank" rel="noopener noreferrer" style={{ textDecoration: "underline", textDecorationColor: "var(--line-strong)", textUnderlineOffset: 3 }}>{s.title}</a></td>
                <td className="small">{s.source_name}</td>
                <td className="small mono">{s.published_at ?? "–"}</td>
                <td className="small">{s.text_depth.replace("_", " ")}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- gaps & errors */
function GapsSection({ report }: { report: Report }) {
  const d = report.investment?.draft;
  const items = [
    ...(d?.missing_data ?? []).map((t) => ["Missing data", t]),
    ...(d?.limitations ?? []).map((t) => ["Limitation", t]),
    ...(report.market?.limitations ?? []).map((t) => ["Market limitation", t]),
  ];
  return (
    <section className="section" id="gaps">
      <div className="container stack">
        <h2 className="h2">Gaps, limitations and errors</h2>
        {report.errors.length > 0 && (
          <div className="notice notice-err">
            {report.errors.map((e, i) => <div key={i} className="small">[{e.agent}/{e.source}] {e.message}</div>)}
          </div>
        )}
        {report.errors.length === 0 && <p className="small muted">No errors were recorded in this run.</p>}
        <ul style={{ color: "var(--text-2)", paddingLeft: 18, margin: 0 }} className="small">
          {items.map(([k, t], i) => <li key={i} style={{ marginBottom: 6 }}><span className="muted">{k}:</span> {t}</li>)}
        </ul>
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- usage */
function UsageSection({ report }: { report: Report }) {
  return (
    <section className="section" id="usage">
      <div className="container stack">
        <h2 className="h2">Model usage on NEAR AI Cloud</h2>
        <p className="sub">Estimated from token counts and the prices in model_config.yaml; the NEAR AI invoice is authoritative.</p>
        <div className="table-wrap">
          <table className="table">
            <thead><tr><th>Agent</th><th>Model</th><th className="num">Calls</th><th className="num">Tokens in / out</th><th className="num">Cost</th></tr></thead>
            <tbody>
              {report.usage.map((u, i) => (
                <tr key={i}><td>{u.agent}</td><td className="mono small">{u.model}</td><td className="num">{u.calls}</td><td className="num">{u.prompt_tokens.toLocaleString()} / {u.completion_tokens.toLocaleString()}</td><td className="num">{fmtUsd(u.cost_usd)}</td></tr>
              ))}
              <tr><td colSpan={4}><strong>Total</strong></td><td className="num"><strong>{fmtUsd(report.total_cost_usd)}</strong></td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}


/* ---------------------------------------------------------------- patent activity chart */
function PatentActivitySection({ report }: { report: Report }) {
  const p = report.patent!;
  const entries = Object.entries(p.publication_counts).map(([y, c]) => [Number(y), c] as const).sort((a, b) => a[0] - b[0]);
  const max = Math.max(...entries.map(([, c]) => c), 1);
  const thisYear = new Date(report.generated_at).getFullYear();
  const a = p.acceleration;
  return (
    <section className="section" id="patents">
      <div className="container">
        <div className="grid grid-2" style={{ background: "transparent", border: 0, gap: 32 }}>
          <div style={{ background: "transparent" }}>
            <h2 className="h2">Patent activity</h2>
            <p className="sub">Worldwide patent publications per year (EPO) mentioning: {p.terms.join(", ")}.</p>
            {a && (
              <div style={{ marginTop: 24 }}>
                <div className="stat-value" style={{ fontSize: 56 }}>{a.yoy_growth_pct !== null ? `${a.yoy_growth_pct > 0 ? "+" : ""}${a.yoy_growth_pct}%` : "–"}</div>
                <div className="stat-label">Patent Acceleration {a.previous_year} → {a.last_full_year} ({a.previous_year_count} → {a.last_full_year_count} publications)</div>
              </div>
            )}
            {p.top_applicants.length > 0 && (
              <div style={{ marginTop: 20 }}>
                <div className="small muted">Most frequent applicants among the {p.sources.length} newest publications</div>
                <div className="pills" style={{ marginTop: 8 }}>{p.top_applicants.map(([n, c]) => <span key={n} className="pill">{n} · {c}</span>)}</div>
              </div>
            )}
            <p className="small muted" style={{ marginTop: 20 }}>{a?.basis}</p>
          </div>
          <div style={{ background: "transparent" }}>
            <div className="cols" role="img" aria-label={`Patent publications per year: ${entries.map(([y, c]) => `${y}: ${c}`).join(", ")}`}>
              {entries.map(([y, c]) => (
                <div className="col" key={y}>
                  <div className="col-tip">{y}: {c} publications{y >= thisYear - 1 ? " (incomplete: publication delay)" : ""}</div>
                  <div className={`col-bar ${y >= thisYear - 1 ? "partial" : ""}`} style={{ height: `${(c / max) * 100}%` }} />
                </div>
              ))}
            </div>
            <div className="col-axis">{entries.map(([y]) => <span key={y}>{y}</span>)}</div>
            <p className="small muted" style={{ marginTop: 10 }}>Hatched = years still filling up (patents publish about 18 months after filing).</p>
            <details><summary className="small muted" style={{ cursor: "pointer" }}>Table view</summary>
              <table className="table" style={{ marginTop: 8 }}><thead><tr><th>Year</th><th className="num">Publications</th></tr></thead>
                <tbody>{entries.map(([y, c]) => <tr key={y}><td>{y}</td><td className="num">{c}</td></tr>)}</tbody></table>
            </details>
          </div>
        </div>
      </div>
    </section>
  );
}
/* ---------------------------------------------------------------- emerging companies (Company Scout) */
function ScoutSection({ report, sources }: { report: Report; sources: Map<string, Source> }) {
  const s = report.scout!;
  const [open, setOpen] = useState<string | null>(s.candidates[0]?.name ?? null);
  const fmtSize = (c: CompanySignal) => {
    const f = c.fundamentals;
    const rev = f?.latest_year ? f.revenue[String(f.latest_year)] : undefined;
    if (rev === undefined) return <span className="muted small" title={c.fundamentals_error ?? undefined}>{c.fundamentals_error ? "no XBRL data" : "–"}</span>;
    return <><span className="pill">{f!.size_class ?? f!.currency}</span> <span className="small muted">{(rev / 1e9).toFixed(2)}B {f!.currency} · FY{f!.latest_year}</span></>;
  };
  const pct = (v: number | null | undefined) => (v == null ? "–" : `${v > 0 ? "+" : ""}${v.toFixed(1)}%`);
  const Row = ({ c, rank }: { c: CompanySignal; rank?: number }) => (
    <>
      <tr className={open === c.name ? "on" : ""} onClick={() => setOpen(open === c.name ? null : c.name)} style={{ cursor: "pointer" }}>
        <td className="mono">{rank ?? "–"}</td>
        <td><strong>{c.name}</strong> <span className="muted mono small">{c.ticker ?? "not SEC-listed"}</span>
          {c.aliases.length > 1 && <div className="small muted">also seen as: {c.aliases.filter((a) => a !== c.name).slice(0, 3).join(", ")}</div>}</td>
        <td className="num">{c.patents || "–"}</td>
        <td className="num">{c.papers || "–"}</td>
        <td className="num">{c.filings || "–"}</td>
        <td>{fmtSize(c)}</td>
        <td className="num">{pct(c.fundamentals?.revenue_growth_pct)}</td>
        <td className="num">{c.fundamentals?.rnd_intensity_pct != null ? `${c.fundamentals.rnd_intensity_pct.toFixed(1)}%` : "–"}</td>
        <td className="num">{c.next_runner_score != null ? <span className="score-chip"><span className="label label-forecast" title="forecast: a heuristic, not a prediction of returns">{c.next_runner_score.toFixed(0)}</span></span> : "–"}</td>
      </tr>
      {open === c.name && (
        <tr className="detail-row"><td colSpan={9}>
          <div className="stack" style={{ gap: 8, padding: "6px 0 10px" }}>
            {c.score_reasons.length > 0 && <ul className="small" style={{ margin: 0, paddingLeft: 18, color: "var(--text-2)" }}>{c.score_reasons.map((r) => <li key={r}>{r}</li>)}</ul>}
            {c.fundamentals?.summary && <p className="small muted" style={{ margin: 0 }}>{c.fundamentals.summary}</p>}
            <div className="pills">
              {[...c.patent_source_ids, ...c.paper_source_ids, ...c.filing_source_ids].slice(0, 10).map((id) => {
                const src = sources.get(id);
                return src ? <a key={id} className="pill" href={src.url} target="_blank" rel="noopener noreferrer" title={src.title}>{src.content_type}: {src.title.slice(0, 48)}{src.title.length > 48 ? "…" : ""} ↗</a> : null;
              })}
            </div>
          </div>
        </td></tr>
      )}
    </>
  );
  const head = (
    <thead><tr><th>#</th><th>Company</th><th className="num">Patents</th><th className="num">Papers</th><th className="num">Filings</th><th>Size (revenue)</th><th className="num">Revenue growth</th><th className="num">R&amp;D / revenue</th><th className="num">Next-runner</th></tr></thead>
  );
  return (
    <section className="section" id="scout">
      <div className="container stack">
        <div className="section-head">
          <div>
            <div className="eyebrow">Company scout · code only, no model</div>
            <h2 className="h2" style={{ marginTop: 10 }}>Emerging companies behind the evidence</h2>
            <p className="sub">Every company named as a patent assignee, as a paper author&apos;s employer or in an SEC filing on this topic, matched to the SEC ticker file (never guessed)
              and sized from its own XBRL financials. The <strong>next-runner score</strong> is a transparent heuristic that favours smaller, growing, R&amp;D-heavy names with evidence from more than one place.
              It is labelled <em>forecast</em>: research information, not a recommendation. Click a row for the reasons and the sources.</p>
          </div>
        </div>
        <p className="small muted" style={{ margin: 0 }}>{s.coverage_note}</p>
        {s.candidates.length > 0 ? (
          <div className="table-wrap"><table className="table radar-table">{head}<tbody>{s.candidates.map((c, i) => <Row key={c.name} c={c} rank={i + 1} />)}</tbody></table></div>
        ) : <div className="notice small">No SEC-listed company outside the configured big-name list was found in this run&apos;s sources.</div>}
        {s.incumbents.length > 0 && (
          <details>
            <summary className="small" style={{ cursor: "pointer", color: "var(--text-2)" }}>Configured incumbents that also showed up ({s.incumbents.length})</summary>
            <div className="table-wrap" style={{ marginTop: 10 }}><table className="table radar-table">{head}<tbody>{s.incumbents.map((c) => <Row key={c.name} c={c} />)}</tbody></table></div>
          </details>
        )}
        {s.unlisted.length > 0 && (
          <div className="stack" style={{ gap: 6 }}>
            <div className="small" style={{ color: "var(--text-2)" }}>Also active, but not in the SEC ticker file (private, foreign, or the name did not match), so no financials:</div>
            <div className="pills">{s.unlisted.map((u) => <span key={u.name} className="pill" title={`${u.patents} patents · ${u.papers} papers · ${u.filings} filings`}>{u.name} · {u.patents + u.papers + u.filings}</span>)}</div>
          </div>
        )}
        <p className="small muted" style={{ margin: 0 }}>{s.basis}</p>
        {s.limitations.length > 0 && <ul className="small muted" style={{ margin: 0, paddingLeft: 18 }}>{s.limitations.map((l) => <li key={l}>{l}</li>)}</ul>}
      </div>
    </section>
  );
}

/* ---------------------------------------------------------------- price & timing risk */
function TimingSection({ report }: { report: Report }) {
  const t = report.timing!;
  const pct = (v: number | null) => (v === null ? "–" : `${v > 0 ? "+" : ""}${v.toFixed(1)}%`);
  const color = (level: string) => level === "elevated" ? "var(--l-unverified)" : level === "subdued" ? "var(--l-interp)" : "var(--text-2)";
  return (
    <section className="section" id="timing">
      <div className="container stack">
        <h2 className="h2">Price &amp; timing risk</h2>
        <p className="sub">Part of the Risk agent. How far the theme&apos;s stocks have already moved, computed by code from daily prices.
          A risk input, <strong>not</strong> a buy or sell signal; past prices do not predict future prices.</p>
        <div className="table-wrap">
          <table className="table">
            <thead><tr><th>Company</th><th className="num">Last close</th><th className="num">1 month</th><th className="num">3 months</th>
              <th className="num">vs 50-day avg</th><th className="num">Volatility (20d)</th><th className="num">From high</th><th>Timing risk</th></tr></thead>
            <tbody>{t.metrics.map((m) => (
              <tr key={m.ticker}>
                <td>{m.company} <span className="muted mono small">{m.ticker}</span></td>
                <td className="num">{m.last_close}<div className="small muted">{m.last_date}</div></td>
                <td className="num">{pct(m.return_1m_pct)}</td><td className="num">{pct(m.return_3m_pct)}</td>
                <td className="num">{pct(m.vs_50d_avg_pct)}</td>
                <td className="num">{m.volatility_20d_pct === null ? "–" : `${m.volatility_20d_pct}%`}</td>
                <td className="num">{pct(m.from_window_high_pct)}</td>
                <td><span className="pill" style={{ color: color(m.timing_risk), borderColor: color(m.timing_risk) }}>{m.timing_risk}</span>
                  <div className="small muted" style={{ marginTop: 4 }}>{m.reasons.join("; ")}</div></td>
              </tr>
            ))}</tbody>
          </table>
        </div>
        <p className="small muted">{t.coverage_note}</p>
      </div>
    </section>
  );
}
