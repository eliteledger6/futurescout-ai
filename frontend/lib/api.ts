import type { ApiConfig, FundListItem, Job, Portfolio, TopicFund, Trading, Radar, RunDetail, RunSummary, Sector, Verification, WatchStatus, Economy, Proposal, ProposalList } from "./types";

// Empty (default) = same origin: Next proxies /api/* to the FastAPI server (API_INTERNAL_URL, see next.config.mjs).
// Set NEXT_PUBLIC_API_URL to talk to an API directly, e.g. http://127.0.0.1:8001 for a second dev server.
export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, { cache: "no-store" });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    if (res.status === 402 && body.detail && typeof body.detail === "object") {     // early access: the report is for sale
      const e = new Error(body.detail.message ?? "locked") as Error & { locked?: unknown };
      e.locked = body.detail;
      throw e;
    }
    throw new Error(typeof body.detail === "string" ? body.detail : `HTTP ${res.status}`);
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
  funds: () => get<{ funds: FundListItem[]; disclaimer: string }>("/api/funds"),
  trading: () => get<Trading>("/api/trading"),
  economy: () => get<Economy>("/api/economy"),
  fund: (slug: string) => get<TopicFund>(`/api/funds/${encodeURIComponent(slug)}`),
  proposals: () => get<ProposalList>("/api/proposals"),
  async propose(topic: string): Promise<Proposal> {
    const res = await fetch(`${API_URL}/api/proposals`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic }),
    });
    const body = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(typeof body.detail === "string" ? body.detail : `HTTP ${res.status}`);
    return body as Proposal;
  },
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
