"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";
import { api, fmtDate, fmtUsd } from "@/lib/api";
import type { ApiConfig, Job, Proposal, ProposalList } from "@/lib/types";
import { ErrorNotice, Loading } from "@/components/ui";

const STATUS: Record<Proposal["status"], { label: string; tone: string }> = {
  queued: { label: "waiting for the AI reviewer", tone: "var(--text-2)" },
  approved: { label: "approved · research is next", tone: "var(--accent)" },
  rejected: { label: "not accepted", tone: "var(--l-danger)" },
  covered: { label: "already covered", tone: "var(--accent)" },
  done: { label: "report ready", tone: "var(--accent)" },
  failed: { label: "research failed", tone: "var(--l-danger)" },
};

export default function Research() {
  const router = useRouter();
  const [config, setConfig] = useState<ApiConfig | null>(null);
  const [list, setList] = useState<ProposalList | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [topic, setTopic] = useState("");
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState<Proposal | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  // the owner's own "start now" form (only where ENABLE_RUN_API=true, i.e. never on the hosted site)
  const [ownTopic, setOwnTopic] = useState("");
  const [question, setQuestion] = useState("");
  const [job, setJob] = useState<Job | null>(null);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  const load = useCallback(() => api.proposals().then(setList).catch((e: Error) => setError(e.message)), []);

  useEffect(() => {
    const preset = new URLSearchParams(window.location.search).get("topic");
    if (preset) setTopic(preset.slice(0, 80));
    api.config().then(setConfig).catch(() => setConfig(null));
    load();
    const t = setInterval(load, 30_000);
    return () => { clearInterval(t); if (timer.current) clearInterval(timer.current); };
  }, [load]);

  async function propose(e: React.FormEvent) {
    e.preventDefault();
    setSubmitError(null);
    setSent(null);
    setSending(true);
    try {
      setSent(await api.propose(topic.trim()));
      setTopic("");
      await load();
    } catch (err) {
      setSubmitError((err as Error).message);
    } finally {
      setSending(false);
    }
  }

  async function startOwn(e: React.FormEvent) {
    e.preventDefault();
    if (!config) return;
    if (!window.confirm(`Start a research run on "${ownTopic.trim()}"?\n\nThis makes real model calls on NEAR AI Cloud and costs about ${fmtUsd(config.estimated_run_cost_usd)} of credit. It takes 3-5 minutes.`)) return;
    setSubmitError(null);
    try {
      const started = await api.start(ownTopic.trim(), question.trim());
      setJob(started);
      timer.current = setInterval(async () => {
        try {
          const j = await api.job(started.id);
          setJob(j);
          if (j.status !== "running" && timer.current) {
            clearInterval(timer.current);
            if (j.status === "done" && j.run_id) router.push(`/runs/${j.run_id}`);
          }
        } catch (err) {
          setSubmitError((err as Error).message);
        }
      }, 3000);
    } catch (err) {
      setSubmitError((err as Error).message);
    }
  }

  const running = job?.status === "running";
  const market = list?.agent_market_url ?? "https://market.near.ai/a/futurescout";
  const canPropose = !!list && list.open && list.left_today > 0;

  return (
    <section className="section">
      <div className="container stack" style={{ maxWidth: 900 }}>
        <div>
          <div className="eyebrow">New research</div>
          <h1 className="h2" style={{ margin: "12px 0 8px" }}>What should the agents investigate?</h1>
          <p className="sub" style={{ margin: 0 }}>
            Any emerging technology, for example “solid-state batteries”, “co-packaged optics” or “humanoid robots”. There are two ways to get a report.
            Either way the agent team researches the topic, the report&apos;s fingerprint is sealed on NEAR, and the report is listed on this site.
          </p>
        </div>

        {error ? <ErrorNotice error={error} /> : list === null ? <Loading lines={3} /> : (
          <div className="grid grid-2" style={{ alignItems: "stretch" }}>
            <div className="panel stack">
              <div className="eyebrow">Option 1 · paid · your report, any topic</div>
              <h3 className="h3" style={{ margin: 0 }}>Hire the report agent on NEAR Agent Market</h3>
              <p className="small" style={{ color: "var(--text-2)", margin: 0 }}>
                $3 per hire, held by the marketplace until you accept the delivery. Give a topic in a few words; the full report is delivered
                to you, usually within minutes when the agent is online and within 12 hours at the latest. A missed deadline is refunded.
              </p>
              <div><a className="btn btn-solid" href={market} target="_blank" rel="noopener noreferrer">Hire on NEAR Agent Market ↗</a></div>
            </div>

            <div className="panel stack">
              <div className="eyebrow">Option 2 · free · {list.per_day} a day</div>
              <h3 className="h3" style={{ margin: 0 }}>Propose a topic</h3>
              <p className="small" style={{ color: "var(--text-2)", margin: 0 }}>
                An AI reviewer checks that the topic is a real technology worth a research run. If it is, the team researches it and the
                report appears on this site. During the demo new reports are free to read here; normally a report costs $2–3 in NEAR. At most {list.per_day} proposals are accepted a day.
              </p>
              <form onSubmit={propose} className="stack" style={{ gap: 10 }}>
                <input className="input" value={topic} onChange={(e) => setTopic(e.target.value)} placeholder="solid-state batteries"
                       minLength={3} maxLength={80} required disabled={!canPropose || sending} aria-label="Topic to propose" />
                <div className="row">
                  <button className="btn btn-solid" type="submit" disabled={!canPropose || sending || topic.trim().length < 3}>
                    {sending ? <><span className="spin" /> Sending…</> : "Propose topic"}
                  </button>
                  <span className="small muted">
                    {!list.open ? "Proposals are closed right now." : list.left_today > 0 ? `${list.left_today} of ${list.per_day} left today` : "Today's proposals are used up. Try tomorrow, or use option 1."}
                  </span>
                </div>
              </form>
              {sent && <div className="notice">Received: “{sent.topic}”. The reviewer looks at it when the report agent is next online; its status shows below.</div>}
              {submitError && <ErrorNotice error={submitError} />}
            </div>
          </div>
        )}

        {list && list.proposals.length > 0 && (
          <div className="panel stack">
            <div className="eyebrow">Recent proposals</div>
            <div className="stack" style={{ gap: 10 }}>
              {list.proposals.map((p) => (
                <div key={p.id} className="row" style={{ justifyContent: "space-between", alignItems: "flex-start", gap: 16, flexWrap: "wrap" }}>
                  <div style={{ minWidth: 0, flex: "1 1 280px" }}>
                    <div style={{ fontWeight: 600 }}>{p.topic}</div>
                    <div className="small muted">{fmtDate(p.created_at)}{p.reason ? ` · ${p.reason}` : ""}</div>
                  </div>
                  <div className="row" style={{ gap: 10 }}>
                    <span className="pill" style={{ color: STATUS[p.status].tone, borderColor: STATUS[p.status].tone, whiteSpace: "nowrap" }}>{STATUS[p.status].label}</span>
                    {p.run_id && (p.status === "done" || p.status === "covered") && <Link className="small" href={`/runs/${p.run_id}`} style={{ color: "var(--accent)" }}>Open report →</Link>}
                  </div>
                </div>
              ))}
            </div>
            <p className="small muted" style={{ margin: 0 }}>A proposal is used only as a topic name. A new report shows on the site after the owner&apos;s report agent publishes it.</p>
          </div>
        )}

        {config?.run_api_enabled && (
          <form onSubmit={startOwn} className="panel stack">
            <div className="eyebrow">Owner · start a run now (this computer only)</div>
            <div className="field">
              <label htmlFor="topic">Topic</label>
              <input id="topic" className="input" value={ownTopic} onChange={(e) => setOwnTopic(e.target.value)}
                     placeholder="high bandwidth memory" minLength={2} maxLength={120} required disabled={running} />
            </div>
            <div className="field">
              <label htmlFor="q">Specific question (optional)</label>
              <input id="q" className="input" value={question} onChange={(e) => setQuestion(e.target.value)}
                     placeholder="What could limit HBM supply over the next three years?" maxLength={500} disabled={running} />
            </div>
            <div className="row">
              <button className="btn btn-solid" type="submit" disabled={running || ownTopic.trim().length < 2}>
                {running ? <><span className="spin" /> Researching…</> : "Start research"}
              </button>
              <span className="small muted">≈ {fmtUsd(config.estimated_run_cost_usd)} per run · 3-5 minutes · one run at a time</span>
            </div>
            {job && (
              <div className={`notice ${job.status === "failed" ? "notice-err" : ""}`}>
                {job.status === "running" && <>Running “{job.topic}”… {Math.round(job.elapsed_s)} s elapsed.</>}
                {job.status === "done" && <>Done. <Link href={`/runs/${job.run_id}`} style={{ color: "var(--accent)" }}>Open the report →</Link></>}
                {job.status === "failed" && <>The run failed: {job.error}</>}
              </div>
            )}
          </form>
        )}
      </div>
    </section>
  );
}
