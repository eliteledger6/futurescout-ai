// What each agent does. Used by the agent-network diagram and the per-report agent trace.
import type { Report } from "./types";

export type AgentKey =
  | "chief" | "science" | "risk" | "market" | "x" | "patent" | "review" | "timing" | "scout" | "investment" | "near" | "fund" | "trader";

export interface AgentInfo {
  key: AgentKey;
  name: string;
  role: string;           // one line
  detail: string;         // what it does, in plain words
  sources: string;        // where its evidence comes from
  prefix?: string;        // finding id prefix
  modelKey?: string;      // key in /api/config agents
  icon: string;           // id of an icon in AgentIcon
}

export const AGENTS: Record<AgentKey, AgentInfo> = {
  chief: { key: "chief", name: "Chief", role: "Plans the research", icon: "compass", modelKey: "chief",
    detail: "Turns the topic into paper searches, contrarian searches and the keywords the other agents use.",
    sources: "No data: it only plans" },
  science: { key: "science", name: "Science", role: "Reads the research", icon: "flask", prefix: "S", modelKey: "science",
    detail: "Finds recent papers and preprints, counts papers per year (Research Acceleration) and writes cited findings.",
    sources: "OpenAlex · arXiv" },
  risk: { key: "risk", name: "Risk", role: "Argues against", icon: "shield", prefix: "R", modelKey: "risk",
    detail: "Searches independently for limits, failures, cost and reliability problems and flags hype. After the Chief review it also challenges specific findings: thin samples, simulations, preprints, overstated labels.",
    sources: "OpenAlex · arXiv · the other agents' findings" },
  market: { key: "market", name: "Market", role: "From papers & patents", icon: "building", prefix: "M", modelKey: "market",
    detail: "There is no fixed company list. The companies are the SEC-listed patent assignees and employers of paper authors that the Patent and Science agents found, plus filers whose reports mention the topic. It reads their latest SEC annual and quarterly reports and keeps verbatim passages that mention the topic.",
    sources: "Patent assignees · paper affiliations · SEC EDGAR · news headlines" },
  x: { key: "x", name: "X signals", role: "37 approved accounts", icon: "signal", prefix: "X", modelKey: "x",
    detail: "Reads the last 7 days of posts from 37 owner-approved company, industry-body, press and analyst accounts. Posts are signals, never facts. Read-only.",
    sources: "X API (read-only)" },
  patent: { key: "patent", name: "Patent", role: "Tracks patent filings", icon: "stamp", prefix: "P", modelKey: "patent",
    detail: "Counts patent publications per year (Patent Acceleration), lists top applicants and reads the newest filings.",
    sources: "Google Patents (SerpApi) · EPO" },
  review: { key: "review", name: "Chief review", role: "Checks for gaps", icon: "search", modelKey: "chief",
    detail: "Looks at everything gathered, names what is missing and may order one extra paper search (bounded).",
    sources: "The agents' findings" },
  timing: { key: "timing", name: "Price & timing", role: "Run-up risk", icon: "pulse", prefix: "T", modelKey: "timing",
    detail: "Computes how far the related stocks have already moved and labels timing risk by fixed rules. A risk input, never a buy signal.",
    sources: "Alpha Vantage daily prices" },
  scout: { key: "scout", name: "Company scout", role: "Finds the next runners", icon: "radar", prefix: "K",
    detail: "Collects every company named as a patent assignee, as a paper author's employer or in an SEC filing on the topic, matches them to the SEC's ticker file, pulls their XBRL financials and scores smaller, growing, R&D-heavy names with a transparent heuristic.",
    sources: "Patent assignees · OpenAlex affiliations · SEC EDGAR + XBRL" },
  investment: { key: "investment", name: "Investment", role: "Writes the report", icon: "doc", modelKey: "investment",
    detail: "Builds themes for 0-12 months, 1-3 years and 3-5 years, bull/base/bear cases and the explainable score. Every statement must cite findings.",
    sources: "All findings above" },
  near: { key: "near", name: "NEAR record", role: "Seals the report", icon: "seal",
    detail: "Stores the report's SHA-256 fingerprint on NEAR testnet, so anyone can check it was not edited afterwards.",
    sources: "NEAR testnet · SocialDB" },
  fund: { key: "fund", name: "Topic fund", role: "Sizes a paper fund", icon: "building",
    detail: "Builds a pretend-money fund for the topic from the report's companies (low, medium and high risk) and decides how much to invest by fixed rules: the verdict and the confidence. Every decision is fingerprinted on NEAR testnet.",
    sources: "The sealed report · daily prices · NEAR Intents dry-run quotes" },
  trader: { key: "trader", name: "Trading agent", role: "Buys via NEAR Intents", icon: "pulse", modelKey: "trader",
    detail: "Picks a tokenized stock from a price-checked list and explains why. Spending limits, a price check and the owner's approval come before any real order goes through NEAR Intents. In shadow mode it places pretend orders at real quotes.",
    sources: "Topic funds · NEAR Intents quotes" },
};

export type AgentState = "ran" | "partial" | "not_run" | "off";

export interface AgentRunStat {
  state: AgentState;
  findings?: number;
  sources?: number;
  cost?: number;
  models?: string[];
  note?: string;
}

/** Per-agent status for one saved report (drives the agent trace). */
export function agentStats(r: Report): Record<AgentKey, AgentRunStat> {
  const usage = (agent: string) => r.usage.filter((u) => u.agent === agent);
  const cost = (agent: string) => usage(agent).reduce((s, u) => s + u.cost_usd, 0);
  const models = (agent: string) => [...new Set(usage(agent).map((u) => u.model))];
  const ran = (k: string) => r.agents_run.includes(k);
  const st = (k: string, part: { findings?: { length: number } | null; sources?: { length: number } | null } | null | undefined): AgentRunStat => ({
    state: ran(k) ? "ran" : part ? "partial" : "off",
    findings: part?.findings?.length, sources: part?.sources?.length, cost: cost(k), models: models(k),
  });
  const xData = r.usage.find((u) => u.agent === "x (data)");
  return {
    chief: { state: ran("chief") ? "ran" : "partial", cost: cost("chief"), models: models("chief"),
             note: r.plan ? `${r.plan.key_questions?.length ?? 0} key questions` : undefined },
    science: st("science", r.science),
    risk: { ...st("risk", r.risk), findings: r.risk ? r.risk.findings.length + r.risk.challenges.length : undefined },
    market: st("market", r.market),
    x: { ...st("x", r.x), cost: cost("x") + (xData?.cost_usd ?? 0) },
    patent: st("patent", r.patent),
    review: { state: ran("chief") ? "ran" : "partial", note: "gap review" },
    timing: st("timing", r.timing),
    scout: { state: ran("scout") ? "ran" : r.scout ? "partial" : "off", findings: r.scout?.findings.length,
             note: r.scout ? `${r.scout.candidates.length} candidates · ${r.scout.unlisted.length} not SEC-listed` : undefined },
    investment: { state: r.investment?.draft ? "ran" : "partial", cost: cost("investment"), models: models("investment"),
                  note: r.investment?.draft ? `${r.investment.draft.themes.length} themes` : undefined },
    near: { state: r.chain_record ? "ran" : "off", note: r.chain_record ? "fingerprint on testnet" : "not recorded" },
    fund: { state: "off", note: "after the report: see Funds & trading" },       // not part of one report's trace (hidden there)
    trader: { state: "off", note: "after the report: see Funds & trading" },
  };
}
