// Shapes returned by the FastAPI backend (backend/app/api). Only fields the dashboard uses.

export type Label = "verified_fact" | "ai_interpretation" | "forecast" | "assumption" | "unverified_claim";
export type Confidence = "low" | "medium" | "high";

export interface RunSummary {
  id: string;
  topic: string;
  question: string | null;
  generated_at: string;
  agents_run: string[];
  agents_not_run: string[];
  score: number | null;
  score_reportable: boolean;
  score_confidence: Confidence | null;
  coverage: number | null;
  findings: number;
  sources: number;
  errors: number;
  total_cost_usd: number;
}

export interface Source {
  id: string;
  url: string;
  source_name: string;
  content_type: string;
  title: string;
  published_at: string | null;
  text_depth: string;
  organization: string | null;
}

export interface Finding {
  fid: string | null;
  claim: string;
  label: Label;
  confidence: Confidence;
  horizon: string;
  source_ids: string[];
  companies: string[];
  rationale: string | null;
  supporting_excerpt: string | null;
  guard_note: string | null;
}

export interface Referenced { label: Label; finding_ids: string[]; note: string | null }
export interface Evidenced extends Referenced { text: string }
export interface Scenario extends Referenced { narrative: string }
export interface HorizonView extends Referenced { horizon: string; assessment: string; confidence: Confidence }
export interface Company extends Referenced { name: string; relevance: string }

export interface Theme {
  name: string;
  technologies: string[];
  horizons: HorizonView[];
  bull: Scenario;
  base: Scenario;
  bear: Scenario;
  catalysts: Evidenced[];
  risks: Evidenced[];
  companies: Company[];
  invalidation_conditions: Evidenced[];
  conflicting_evidence: Evidenced[];
}

export interface Dimension {
  key: string;
  label: string;
  weight: number;
  status: "scored" | "missing";
  rating: number | null;
  confidence: Confidence | null;
  rationale: string;
  finding_ids: string[];
  missing_reason: string | null;
}

export interface Score {
  reportable: boolean;
  score: number | null;
  base_score: number | null;
  coverage: number;
  confidence: Confidence;
  risk_rating: number | null;
  risk_penalty_pct: number | null;
  dimensions: Dimension[];
  notes: string[];
  formula: string;
}

export interface CompanyCheck {
  ticker: string; name: string; filings_checked: number; filings_with_mentions: number; error: string | null;
  discovered?: boolean; mentions_in_search?: number | null; press_releases_read?: number;
  fundamentals?: {
    currency: string; latest_year: number | null; revenue: Record<string, number>; revenue_growth_pct: number | null;
    rnd_intensity_pct: number | null; size_class: string | null; summary: string;
  } | null;
}

export interface CompanySignal {
  name: string; aliases: string[]; ticker: string | null; cik: number | null; sec_listed: boolean; incumbent: boolean;
  patents: number; patent_source_ids: string[]; papers: number; paper_source_ids: string[]; filings: number; filing_source_ids: string[];
  fundamentals: CompanyCheck["fundamentals"]; fundamentals_error: string | null;
  next_runner_score: number | null; score_reasons: string[]; signal_types: number;
}

export interface Report {
  topic: string;
  question: string | null;
  generated_at: string;
  agents_run: string[];
  agents_not_run: string[];
  plan: { topic_summary: string; key_questions: string[] } | null;
  science: {
    status: string; coverage_note: string; sources: Source[]; findings: Finding[];
    publication_counts: Record<string, number>;
    acceleration: { previous_year: number; previous_year_count: number; last_full_year: number; last_full_year_count: number; yoy_growth_pct: number | null; basis: string } | null;
    emerging_directions: string[]; open_problems: string[]; limitations: string[];
  } | null;
  risk: {
    status: string; sources: Source[]; findings: Finding[]; hype_flags: string[]; limitations: string[];
    challenges: { finding: Finding; target_finding_ids: string[]; severity: Confidence }[];
  } | null;
  market: {
    status: string; coverage_note: string; keywords: string[]; companies: CompanyCheck[];
    sources: Source[]; findings: Finding[]; limitations: string[];
  } | null;
  x: {
    status: string; coverage_note: string; keywords: string[]; accounts: string[];
    sources: Source[]; findings: Finding[]; limitations: string[];
    x_usage: { posts_read?: number; cost_usd?: number };
  } | null;
  patent: {
    status: string; coverage_note: string; terms: string[]; total_matches: number | null;
    publication_counts: Record<string, number>;
    acceleration: { previous_year: number; previous_year_count: number; last_full_year: number; last_full_year_count: number; yoy_growth_pct: number | null; basis: string } | null;
    top_applicants: [string, number][];
    sources: Source[]; findings: Finding[]; limitations: string[];
  } | null;
  timing: {
    status: string; coverage_note: string; sources: Source[]; findings: Finding[]; limitations: string[];
    metrics: {
      ticker: string; company: string; last_date: string; last_close: number; bars: number;
      return_1m_pct: number | null; return_3m_pct: number | null; vs_50d_avg_pct: number | null;
      volatility_20d_pct: number | null; from_window_high_pct: number; timing_risk: string; reasons: string[];
    }[];
  } | null;
  scout: {
    status: string; coverage_note: string; basis: string; limitations: string[]; lookups: number;
    candidates: CompanySignal[]; incumbents: CompanySignal[]; unlisted: CompanySignal[]; findings: Finding[];
  } | null;
  investment: {
    status: string;
    draft: { summary: string; themes: Theme[]; missing_data: string[]; limitations: string[] } | null;
    score: Score | null;
  } | null;
  usage: { agent: string; model: string; calls: number; prompt_tokens: number; completion_tokens: number; cost_usd: number }[];
  total_cost_usd: number;
  chain_record: { sha256: string; explorer_url: string | null; account: string } | null;
  errors: { agent: string; source: string; message: string }[];
}

export interface RunDetail { summary: RunSummary; report: Report; markdown: string | null }

export interface ApiConfig {
  run_api_enabled: boolean;
  estimated_run_cost_usd: number;
  agents: Record<string, string>;
  agents_not_built: string[];
  store: string;
  disclaimer: string;
  model_provider: string;
}

export interface Acceleration {
  previous_year: number; previous_year_count: number; last_full_year: number; last_full_year_count: number;
  yoy_growth_pct: number | null; basis: string;
}

export interface Sector { key: string; name: string; hints: string; discovery_queries: string[]; topics: number; companies: number }

export interface TopicSignal {
  topic: string;
  sector: string;
  heat_basis?: "papers+patents" | "papers only" | "patents only" | null;
  terms: string[];
  paper_counts: Record<string, number>;
  paper_acceleration: Acceleration | null;
  patent_counts: Record<string, number>;
  patent_acceleration: Acceleration | null;
  filer_counts: Record<string, number>;
  heat: number | null;
  small_base: boolean;
  rank: number | null;
  errors: string[];
}

export interface Radar { generated_at: string; topics: TopicSignal[]; searches_used: number; basis: string }

export interface WatchStatus {
  active: boolean;
  last_scan_at: string | null;
  scan_interval_minutes: number;
  runs_started: { at: string; topic: string; run_id: string | null }[];
  runs_today: number;
  max_runs_per_day: number;
  latest_mentions: Record<string, number>;
  events: { at: string; kind: string; detail: string; topic?: string }[];
}

export interface Verification {
  status: "match" | "MISMATCH" | "not_recorded" | "unavailable";
  sha256: string;
  onchain_sha256?: string;
  explorer_url?: string;
  account?: string;
  detail?: string;
}

export interface Position {
  run_id: string; topic: string; report_date: string; ticker: string; company: string; next_runner_score: number | null;
  notional_usd: number; status: "pending" | "open" | "error"; entry_date: string | null; entry_close: number | null; shares: number | null;
  last_date: string | null; last_close: number | null; value_usd: number | null; return_pct: number | null; note: string | null;
  price_source_url: string | null;
}
export interface Portfolio {
  kind: "simulation"; label: string; disclaimer: string; prices_configured: boolean;
  created_at: string; updated_at: string | null; prices_updated_at: string | null;
  notional_usd: number; positions_per_report: number; positions: Position[]; notes: string[]; price_requests_last_update: number;
  benchmark: { ticker: string; entry_date: string | null; entry_close: number | null; last_date: string | null; last_close: number | null; return_pct: number | null; note: string | null } | null;
  summary: { positions: number; open: number; pending: number; invested_usd: number; value_usd: number; return_pct: number | null;
             benchmark_return_pct: number | null; best: string | null; worst: string | null; reports: number };
}
export interface Treasury {
  network: string; seller_account: string | null; price_near: number; earned_near: number; sales: number; spent_usd: number; runs: number;
  avg_cost_per_run_usd: number | null; balance: { available_near: number; locked_near: number; storage_bytes: number } | null; balance_error: string | null;
  near_usd_reference: number | null; sales_per_report_to_break_even: number | null;
  per_run: { run_id: string; topic: string; generated_at: string; cost_usd: number | null; sales: number; earned_near: number }[];
  recent_sales: { run_id: string; topic: string; buyer: string; amount_near: number; tx_hash: string; purchased_at: string | null; explorer_url: string }[];
  generated_at: string; note: string;
}

export interface Job { id: string; topic: string; status: "running" | "done" | "failed"; run_id: string | null; error: string | null; elapsed_s: number }
