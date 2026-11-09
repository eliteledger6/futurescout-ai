"use client";

// Watch-mode status: what the platform did on its own (X scans, rising topics, research it started).
import Link from "next/link";
import { useEffect, useState } from "react";
import { api, fmtDate } from "@/lib/api";
import type { WatchStatus } from "@/lib/types";

const KIND_LABEL: Record<string, string> = { scan: "X scan", radar: "Radar", topics: "New topic", trigger: "Triggered", run: "Research run", skip: "Held back" };

function ago(iso: string): string {
  const mins = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 60000));
  if (mins < 60) return `${mins} min ago`;
  const h = Math.round(mins / 60);
  return h < 48 ? `${h} h ago` : `${Math.round(h / 24)} d ago`;
}

export function LivePanel() {
  const [w, setW] = useState<WatchStatus | null>(null);
  useEffect(() => {
    const load = () => api.watch().then(setW).catch(() => setW(null));
    load();
    const t = setInterval(load, 60_000);
    return () => clearInterval(t);
  }, []);
  if (!w) return null;
  const mentions = Object.entries(w.latest_mentions).sort((a, b) => b[1] - a[1]);
  return (
    <div className="live">
      <div className="live-head">
        <span className={`live-dot ${w.active ? "on" : ""}`} />
        <div>
          <div className="h3" style={{ margin: 0, fontSize: 18 }}>Autonomous watch</div>
          <div className="small muted">
            {w.active ? <>Last X scan {ago(w.last_scan_at!)} · scans every {w.scan_interval_minutes / 60} h · {w.runs_today}/{w.max_runs_per_day} research runs started today</>
                      : <>Not running. Start it with <span className="mono">python scripts\watch.py --loop</span></>}
          </div>
        </div>
      </div>
      {w.active && (
        <div className="live-grid">
          <div>
            <div className="eyebrow" style={{ fontSize: 11 }}>Rising in the last scan</div>
            {mentions.length === 0 ? <p className="small muted">No watched topic was mentioned in the newest posts.</p> : (
              <div className="pills" style={{ marginTop: 8 }}>
                {mentions.map(([t, n]) => <span key={t} className="pill pill-on">{t} · {n} post{n === 1 ? "" : "s"}</span>)}
              </div>
            )}
            <div className="eyebrow" style={{ fontSize: 11, marginTop: 18 }}>Research it started</div>
            {w.runs_started.length === 0 ? <p className="small muted">None yet.</p> : (
              <ul className="live-runs">
                {w.runs_started.slice(0, 5).map((r, i) => (
                  <li key={i}>
                    <span className="small muted">{fmtDate(r.at)}</span>
                    {r.run_id && !r.run_id.startsWith("saved") ? <Link href={`/runs/${r.run_id}`}>{r.topic} →</Link> : <span>{r.topic}</span>}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div>
            <div className="eyebrow" style={{ fontSize: 11 }}>Decision log</div>
            <ol className="live-log">
              {w.events.slice(0, 8).map((e, i) => (
                <li key={i} className={`k-${e.kind}`}>
                  <span className="live-kind">{KIND_LABEL[e.kind] ?? e.kind}</span>
                  <span className="live-detail">{e.detail}</span>
                  <span className="small muted">{ago(e.at)}</span>
                </li>
              ))}
            </ol>
          </div>
        </div>
      )}
    </div>
  );
}
