"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ErrorNotice, Loading } from "@/components/ui";
import { api, fmtDate } from "@/lib/api";
import type { Radar, Sector, TopicSignal, Ytd } from "@/lib/types";

// Source errors come from the API verbatim; show a short reader-friendly version (full text in the tooltip).
const friendlyError = (e: string) => {
  const [source] = e.split(":");
  if (/paused|cache|quota/i.test(e)) return `${source}: not counted yet`;
  if (/rate|429|timeout|timed out|unavailable|connection/i.test(e)) return `${source}: source unavailable right now`;
  return `${source}: not counted`;
};
const pct = (v: number | null | undefined) => (v === null || v === undefined ? "–" : `${v > 0 ? "+" : ""}${v.toFixed(0)}%`);

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

// What the heat number covers, read from the data: the last two full years AND this year so far (same dates last year).
function heatNote(topics: Radar["topics"]): string {
  const acc = topics.find((t) => t.paper_acceleration)?.paper_acceleration;
  const ytd = topics.find((t) => t.paper_ytd)?.paper_ytd;
  const full = acc ? `${acc.previous_year} → ${acc.last_full_year}` : "the last two full years";
  if (!ytd) return `Heat = average of paper growth and patent growth, ${full}`;
  const [m, d] = String(ytd.cutoff).split("-").map(Number);
  const until = m && d ? `${d} ${MONTHS[m - 1]}` : ytd.cutoff;
  return `Heat = average of paper growth ${full}, papers so far in ${ytd.year} (1 Jan–${until}, against the same dates in ${ytd.previous_year}) and, where counted, patent growth ${full}. The newest 30 days are left out: new papers take weeks to be indexed.`;
}

export default function RadarPage() {
  const [radar, setRadar] = useState<Radar | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [active, setActive] = useState<TopicSignal | null>(null);
  const [sector, setSector] = useState<string | null>(null);
  const [sectors, setSectors] = useState<Sector[]>([]);

  useEffect(() => {
    api.radar().then((r) => { setRadar(r); setActive(r.topics[0] ?? null); }).catch((e: Error) => setError(e.message));
    api.sectors().then(setSectors).catch(() => setSectors([]));
  }, []);

  const maxHeat = radar ? Math.max(...radar.topics.map((t) => Math.abs(t.heat ?? 0)), 1) : 1;
  const sectorKeys = radar ? [...new Set(radar.topics.map((t) => t.sector ?? "semiconductors"))] : [];
  const sectorName = (k: string) => sectors.find((s) => s.key === k)?.name ?? k;

  return (
    <>
      <section className="hero" style={{ padding: "84px 0 60px" }}>
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">Hot-topic radar</div>
          <h1 className="display" style={{ fontSize: "clamp(40px, 6vw, 76px)" }}>Where research and patents are <span className="gradient-text">heating up</span></h1>
          <p className="lede">A topic gets hot in papers and patent filings before it shows up in company reports. The radar ranks topics by the growth of both.
            It measures activity, not investment merit.</p>
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          {error ? <ErrorNotice error={error.includes("No radar") ? "No radar has been computed yet. In the backend folder run: python scripts\\run_radar.py" : error} />
           : radar === null ? <Loading lines={5} /> : (
            <>
              <div className="row small muted" style={{ justifyContent: "space-between" }}>
                <span>Computed {fmtDate(radar.generated_at)} · {radar.topics.length} topics across {sectorKeys.length} sectors</span>
                <span>{heatNote(radar.topics)}</span>
              </div>
              <div className="tabs" role="tablist" aria-label="Sector">
                <button role="tab" aria-selected={sector === null} className={sector === null ? "tab on" : "tab"} onClick={() => setSector(null)}>All sectors</button>
                {sectorKeys.map((k) => (
                  <button key={k} role="tab" aria-selected={sector === k} className={sector === k ? "tab on" : "tab"} onClick={() => setSector(k)}>
                    {sectorName(k)} <span className="muted">· {radar.topics.filter((t) => (t.sector ?? "semiconductors") === k).length}</span>
                  </button>
                ))}
              </div>
              <div className="radar-grid">
                <div className="table-wrap">
                  <table className="table radar-table">
                    <thead><tr><th>#</th><th>Topic</th><th>Heat</th><th className="num">Papers</th><th className="num">This year so far</th><th className="num">Patents</th>{radar.topics.some((t) => Object.keys(t.filer_counts).length) && <th className="num">SEC filers</th>}</tr></thead>
                    <tbody>
                      {radar.topics.filter((t) => sector === null || (t.sector ?? "semiconductors") === sector).map((t) => {
                        const pa = t.paper_acceleration, pt = t.patent_acceleration;
                        const lastYear = pa?.last_full_year ?? pt?.last_full_year;
                        return (
                          <tr key={t.topic} className={active?.topic === t.topic ? "on" : ""} onClick={() => setActive(t)} style={{ cursor: "pointer" }}>
                            <td className="mono">{t.rank ?? "–"}</td>
                            <td><strong>{t.topic}</strong>
                              {t.small_base && <div className="small muted">small base: fewer than 20 documents in the earlier year, so not ranked</div>}
                              {t.errors.length > 0 && <div className="small guard" title={t.errors.join("; ")}>{t.errors.map(friendlyError).join(" · ")}</div>}</td>
                            <td style={{ minWidth: 160 }}>
                              <div className="heat-row">
                                <div className="track" style={{ flex: 1 }}>
                                  <div className={`bar ${(t.heat ?? 0) < 0 ? "bar-neg" : ""}`} style={{ width: `${Math.min(100, Math.abs(t.heat ?? 0) / maxHeat * 100)}%` }} />
                                </div>
                                <span className="mono small" style={{ width: 52, textAlign: "right" }} title={t.heat_basis ?? undefined}>{pct(t.heat)}{t.heat_basis && !t.heat_basis.includes("patents") ? <span className="muted" title="patents not counted for this topic: heat uses papers only">*</span> : null}</span>
                              </div>
                            </td>
                            <td className="num">{pa ? <>{pa.previous_year_count} → {pa.last_full_year_count}<div className="small muted">{pct(pa.yoy_growth_pct)}</div></> : "–"}</td>
                            <td className="num">{t.paper_ytd ? <>{t.paper_ytd.previous_count} → {t.paper_ytd.count}<div className="small"><TrendChip t={t.paper_ytd} /></div></> : "–"}</td>
                            <td className="num">{pt ? <>{pt.previous_year_count} → {pt.last_full_year_count}<div className="small muted">{pct(pt.yoy_growth_pct)}</div></> : "–"}</td>
                            {Object.keys(t.filer_counts).length > 0 && <td className="num">{lastYear ? t.filer_counts[String(lastYear)] ?? "–" : "–"}</td>}
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
                {active && <TopicDetail t={active} />}
              </div>
              <p className="small muted">{radar.basis} * = papers only (patents not counted for that topic).</p>
            </>
          )}
        </div>
      </section>
    </>
  );
}

function TrendChip({ t }: { t: Ytd }) {
  const label = t.trend ?? "small base";
  const colour = t.trend === "rising" ? "var(--accent)" : t.trend === "cooling" ? "var(--l-danger)" : "var(--muted)";
  return (
    <span className="mono" style={{ color: colour, fontSize: 11 }} title={t.basis}>
      {pct(t.growth_pct)} · {label}
    </span>
  );
}

function Spark({ counts, label, partialFrom }: { counts: Record<string, number>; label: string; partialFrom: number }) {
  const entries = Object.entries(counts).map(([y, c]) => [Number(y), c] as const).sort((a, b) => a[0] - b[0]);
  const max = Math.max(...entries.map(([, c]) => c), 1);
  return (
    <div>
      <div className="small muted" style={{ marginBottom: 6 }}>{label}</div>
      <div className="cols" style={{ height: 90 }} role="img" aria-label={`${label}: ${entries.map(([y, c]) => `${y}: ${c}`).join(", ")}`}>
        {entries.map(([y, c]) => (
          <div className="col" key={y}>
            <div className="col-tip">{y}: {c}{y >= partialFrom ? " (incomplete)" : ""}</div>
            <div className={`col-bar ${y >= partialFrom ? "partial" : ""}`} style={{ height: `${(c / max) * 100}%` }} />
          </div>
        ))}
      </div>
      <div className="col-axis">{entries.map(([y]) => <span key={y}>{String(y).slice(2)}</span>)}</div>
    </div>
  );
}

function TopicDetail({ t }: { t: TopicSignal }) {
  const year = new Date().getFullYear();
  return (
    <div className="panel stack">
      <div>
        <div className="eyebrow">#{t.rank ?? "–"}</div>
        <h2 className="h3" style={{ margin: "6px 0 2px", fontSize: 24 }}>{t.topic}</h2>
        <div className="small muted">Terms: {t.terms.join(", ")}</div>
      </div>
      <div className="stat-value" style={{ fontSize: 48 }}>{pct(t.heat)}<span className="small muted" style={{ fontFamily: "var(--font-body)", letterSpacing: 0, marginLeft: 10 }}>heat</span></div>
      {Object.keys(t.paper_counts).length > 0 && <Spark counts={t.paper_counts} label="Papers per year (OpenAlex)" partialFrom={year} />}
      {Object.keys(t.patent_counts).length > 0 && <Spark counts={t.patent_counts} label="Patent publications per year (Google Patents)" partialFrom={year - 1} />}
      {Object.keys(t.filer_counts).length > 0 && <Spark counts={t.filer_counts} label="SEC filers mentioning it, per year" partialFrom={year} />}
      <Link className="btn btn-ghost" href={`/research?topic=${encodeURIComponent(t.topic)}`}>Research this topic →</Link>
    </div>
  );
}
