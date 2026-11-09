import type { ApiConfig, Job, Portfolio, Radar, RunDetail, RunSummary, Sector, Treasury, Verification, WatchStatus } from "./types";

// The FastAPI backend started with `python scripts\serve.py` (backend folder).
export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, { cache: "no-store" });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  config: () => get<ApiConfig>("/api/config"),
  runs: () => get<RunSummary[]>("/api/runs"),
  run: (id: string) => get<RunDetail>(`/api/runs/${encodeURIComponent(id)}`),
  job: (id: string) => get<Job>(`/api/jobs/${encodeURIComponent(id)}`),
  radar: () => get<Radar>("/api/radar"),
  sectors: () => get<Sector[]>("/api/sectors"),
  watch: () => get<WatchStatus>("/api/watch"),
  verify: (id: string) => get<Verification>(`/api/runs/${encodeURIComponent(id)}/verify`),
  portfolio: () => get<Portfolio>("/api/portfolio"),
  treasury: () => get<Treasury>("/api/treasury"),
  async start(topic: string, question?: string): Promise<Job> {
    const res = await fetch(`${API_URL}/api/runs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, question: question || null }),
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(typeof body.detail === "string" ? body.detail : `HTTP ${res.status}`);
    return body as Job;
  },
};

export function fmtDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleString(undefined, { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

export function fmtUsd(v: number): string {
  return `$${v.toFixed(v < 1 ? 3 : 2)}`;
}
