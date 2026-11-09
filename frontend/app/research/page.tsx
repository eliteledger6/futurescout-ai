"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { api, fmtUsd } from "@/lib/api";
import type { ApiConfig, Job } from "@/lib/types";
import { ErrorNotice, Loading } from "@/components/ui";

export default function Research() {
  const router = useRouter();
  const [config, setConfig] = useState<ApiConfig | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [topic, setTopic] = useState("");
  const [question, setQuestion] = useState("");
  const [job, setJob] = useState<Job | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    const preset = new URLSearchParams(window.location.search).get("topic");
    if (preset) setTopic(preset.slice(0, 120));
    api.config().then(setConfig).catch((e: Error) => setError(e.message));
    return () => { if (timer.current) clearInterval(timer.current); };
  }, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!config) return;
    const ok = window.confirm(
      `Start a research run on "${topic.trim()}"?\n\nThis makes real model calls on NEAR AI Cloud and costs about ${fmtUsd(config.estimated_run_cost_usd)} of credit. It takes 3-5 minutes.`,
    );
    if (!ok) return;
    setSubmitError(null);
    try {
      const started = await api.start(topic.trim(), question.trim());
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

  return (
    <section className="section">
      <div className="container" style={{ maxWidth: 760 }}>
        <div className="eyebrow">New research</div>
        <h1 className="h2" style={{ margin: "12px 0 8px" }}>What should the agents investigate?</h1>
        <p className="sub">
          Any technology, e.g. “high bandwidth memory”, “solid-state battery”, “humanoid robot”, “post-quantum cryptography”. Topics on the radar carry their sector; others run as general technology.
          The Chief plans the searches; Science, Risk and Market agents gather evidence in parallel; the Investment agent writes the report.
        </p>
        <div className="spacer" />

        {error ? <ErrorNotice error={error} /> : config === null ? <Loading lines={2} /> : (
          <>
            {!config.run_api_enabled && (
              <div className="notice notice-warn" style={{ marginBottom: 20 }}>
                Starting runs from the dashboard is <strong>switched off</strong>, because each run spends NEAR AI credit
                (about {fmtUsd(config.estimated_run_cost_usd)}). To switch it on, add <span className="mono">ENABLE_RUN_API=true</span> to
                your <span className="mono">.env</span> and restart <span className="mono">python scripts\serve.py</span>.
                You can still run research from the command line and browse all saved reports.
              </div>
            )}
            <form onSubmit={submit} className="panel stack">
              <div className="field">
                <label htmlFor="topic">Topic</label>
                <input id="topic" className="input" value={topic} onChange={(e) => setTopic(e.target.value)}
                       placeholder="high bandwidth memory" minLength={2} maxLength={120} required disabled={running} />
              </div>
              <div className="field">
                <label htmlFor="q">Specific question (optional)</label>
                <input id="q" className="input" value={question} onChange={(e) => setQuestion(e.target.value)}
                       placeholder="What could limit HBM supply over the next three years?" maxLength={500} disabled={running} />
              </div>
              <div className="row">
                <button className="btn btn-solid" type="submit"
                        disabled={!config.run_api_enabled || running || topic.trim().length < 2}>
                  {running ? <><span className="spin" /> Researching…</> : "Start research"}
                </button>
                <span className="small muted">≈ {fmtUsd(config.estimated_run_cost_usd)} per run · 3-5 minutes · one run at a time</span>
              </div>
            </form>

            {job && (
              <div className={`notice ${job.status === "failed" ? "notice-err" : ""}`} style={{ marginTop: 20 }}>
                {job.status === "running" && <>Running “{job.topic}”… {Math.round(job.elapsed_s)} s elapsed. You can leave this page; the report will appear on the Reports page when it is done.</>}
                {job.status === "done" && <>Done. <Link href={`/runs/${job.run_id}`} style={{ color: "var(--accent)" }}>Open the report →</Link></>}
                {job.status === "failed" && <>The run failed: {job.error}</>}
              </div>
            )}
            {submitError && <div style={{ marginTop: 20 }}><ErrorNotice error={submitError} /></div>}

            <div className="spacer" />
            <div className="small muted">
              Models in use: {Object.entries(config.agents).map(([a, m]) => `${a}: ${m}`).join(" · ")}. Not built yet: {config.agents_not_built.join(", ")}.
            </div>
          </>
        )}
      </div>
    </section>
  );
}
