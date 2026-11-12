// What each agent does. Used by the agent-network diagram and the per-report agent trace.
import type { Report } from "./types";

export type AgentKey =
  | "chief" | "science" | "risk" | "market" | "x" | "patent" | "review" | "timing" | "scout" | "investment" | "near" | "fund" | "trader"
  | "seller" | "stake" | "trader2" | "intake" | "buyers" | "radar";

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

// What a box in the network really is. Only "ai" boxes call a model; the rest must not be counted as agents.
export type NodeKind = "ai" | "team" | "code" | "service" | "planned";
export const KIND_LABEL: Record<NodeKind, string> = { ai: "AI", team: "AI TEAM", code: "CODE", service: "NEAR", planned: "PLANNED" };
export const KIND_TEXT: Record<NodeKind, string> = {
  ai: "AI agent: calls a model on NEAR AI Cloud",
  team: "The Report agent: its 9 AI agents do the research; it collects their work and reports it out",
  code: "Code step: fixed rules and counts, no model",
  service: "NEAR ecosystem service the agents use",
  planned: "Planned, not built",
};
// The Report agent = one agent with its own NEAR account, made of these AI agents working as a team (plus code steps).
export const REPORT_TEAM: AgentKey[] = ["intake", "chief", "science", "patent", "risk", "x", "market", "timing", "investment"];
export function kindOf(k: AgentKey): NodeKind {
  if (k === "trader2") return "planned";
  if (k === "seller") return "team";
  if (k === "stake" || k === "buyers") return "service";
  return AGENTS[k].modelKey ? "ai" : "code";
}

export const AGENTS: Record<AgentKey, AgentInfo> = {
  radar: { key: "radar", name: "Hot-Topic Radar", role: "Picks what to research", icon: "radar",
    detail: "Ranks every tracked topic by how fast its research papers and patent filings are growing; the counts are computed by code, with no model. The report agent recounts it once a day. From the ranking it writes reports by itself: each of the top 5 topics always has a report from the last 7 days, and every report sold pays for one more, on the next topic down the list (at most 2 a day). The list of topics grows too: when the Science agent has no job it reads 5 recent papers an hour and may add one new topic, but only if paper counts confirm it is growing.",
    sources: "OpenAlex · EPO and Google Patents · SEC EDGAR" },
  intake: { key: "intake", name: "Topic reviewer", role: "Screens proposed topics", icon: "shield", modelKey: "topic_review",
    detail: "Visitors can propose a topic for free on the Request a report page, at most 5 a day. This agent checks that the proposal is a real technology worth a research run, and rejects prices, coins, single companies, jokes and topics that are far too broad. A proposal is only ever used as a short topic name, never as instructions. Approved topics go to the Chief; a topic with a recent report is linked instead of researched again.",
    sources: "Visitor proposals (short topic only)" },
  buyers: { key: "buyers", name: "Agent Market", role: "Outside buyers hire: $3", icon: "signal",
    detail: "The report agent is listed on NEAR Agent Market. Anyone can hire it for $3: they give a topic, the marketplace holds the payment, and the agent delivers a sealed report (a recent one when it exists, otherwise a new research run, at most 3 a day). Once the buyer accepts, the fee joins the same split as report sales: 70% staked, 30% kept. Other trading bots can also buy any report through the API, paid in NEAR and checked on chain.",
    sources: "market.near.ai · the report market API" },
  chief: { key: "chief", name: "Chief", role: "Plans the research", icon: "compass", modelKey: "chief",
    detail: "Turns the topic into paper searches, contrarian searches and the keywords the other agents use.",
    sources: "No data: it only plans" },
  science: { key: "science", name: "Science", role: "Reads the research", icon: "flask", prefix: "S", modelKey: "science",
    detail: "Finds recent papers and preprints, counts papers per year (Research Acceleration) and writes cited findings. When there is no job, the same agent scouts: it reads 5 recent papers an hour and may name one technology the radar does not track yet; code adds it only when paper counts confirm real growth.",
    sources: "OpenAlex · arXiv" },
  risk: { key: "risk", name: "Risk", role: "Argues against", icon: "shield", prefix: "R", modelKey: "risk",
    detail: "Searches independently for limits, failures, cost and reliability problems and flags hype. After the Chief review it also challenges specific findings: thin samples, simulations, preprints, overstated labels.",
    sources: "OpenAlex · arXiv · the other agents' findings" },
  market: { key: "market", name: "Market", role: "From papers & patents", icon: "building", prefix: "M", modelKey: "market",
    detail: "There is no fixed company list. The companies are the SEC-listed patent assignees and employers of paper authors that the Patent and Science agents found, plus filers whose reports mention the topic. It reads their latest SEC annual and quarterly reports and keeps verbatim passages that mention the topic.",
    sources: "Patent assignees · paper affiliations · SEC EDGAR · news headlines" },
  x: { key: "x", name: "X signals", role: "Approved accounts only", icon: "signal", prefix: "X", modelKey: "x",
    detail: "Reads the last 7 days of posts from about 130 approved company, industry-body, press and analyst accounts (most approved by the owner, a few added by the agent under the owner's rules). Posts are signals, never facts. Read-only.",
    sources: "X API (read-only)" },
  patent: { key: "patent", name: "Patent", role: "Tracks patent filings", icon: "stamp", prefix: "P", modelKey: "patent",
    detail: "Counts patent publications per year (Patent Acceleration), lists top applicants and reads the newest filings.",
    sources: "Google Patents (SerpApi) · EPO" },
  review: { key: "review", name: "Chief review", role: "Checks for gaps", icon: "search", modelKey: "chief",
    detail: "The Chief agent's second pass, not a separate agent. Looks at everything gathered, names what is missing and may order one extra paper search (bounded).",
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
    detail: "Stores the report's SHA-256 fingerprint on NEAR (mainnet, signed by the report agent), so anyone can check it was not edited afterwards.",
    sources: "NEAR · SocialDB (social.near)" },
  fund: { key: "fund", name: "Topic fund", role: "Invests a paper fund", icon: "building",
    detail: "Builds a pretend-money fund for the topic from the companies the patents and papers name, split into low, medium and high risk, and keeps it fully invested. Every decision lists its reasons and carries its own fingerprint; the report it is based on is sealed on NEAR.",
    sources: "The sealed report · daily prices · NEAR Intents dry-run quotes" },
  seller: { key: "seller", name: "Report agent", role: "Collects & reports out", icon: "doc",
    detail: "The agent everything reports to. It takes a topic (from the radar, a visitor's proposal or a hire on NEAR Agent Market), hands it to its team of 9 AI agents, and collects their work into the finished report. Then it reports it out: it seals the report's fingerprint on NEAR, builds the topic's paper fund, publishes the report on this site, delivers it to whoever hired it, and sells it for $2 to $3 in NEAR to the trading agent or any other bot. It runs by itself on a cloud server under its own NEAR account, keeps the radar's top 5 topics covered, and every sale pays for the next report. A payment from the trading agent comes as a signed order from its near.com balance, checked before signing and confirmed when it arrives in the report agent's wallet.",
    sources: "Its own NEAR account · NEAR Intents" },
  stake: { key: "stake", name: "NEAR AI staking", role: "Earns credits for AI", icon: "sprout",
    detail: "The report agent stakes 70% of everything it earns (report sales and NEAR Agent Market fees) through NEAR AI Cloud's Staking for Inference (stake.dao, validator nearai.pool.near; at least 1 NEAR at a time) and keeps 30%; once the kept part passes $200 it funds a second trading agent (next step). The staking rewards become NEAR AI credits that go toward the agents' model calls (at today's amounts they cover a small part of the bill; the owner tops up the rest); the staked NEAR stays withdrawable.",
    sources: "NEAR mainnet · NEAR AI Cloud" },
  trader2: { key: "trader2", name: "Trading agent 2", role: "Planned: funded at $200", icon: "pulse",
    detail: "The next step, not built yet. The report agent keeps 30% of every payment in a pot; once that pot passes $200 it funds a second trading agent with its own account and budget, run like the first one. The first trading agent already shows the whole loop working with real money.",
    sources: "The report agent's kept 30%" },
  trader: { key: "trader", name: "Trading agent", role: "Buys reports, trades", icon: "pulse", modelKey: "trader",
    detail: "Wakes on a new report, a sharp price move or a daily review. Every hour it reads the live price of each share it holds, and a sharp move since it last looked wakes it too. Once a day it buys a short check-up on each holding from the report agent for $0.50 in NEAR (recent posts from approved X accounts and a risk note), reads it, and decides to hold, sell or buy. It may only use reports it has bought from the report agent (it buys one only when it could trade on it now), then buys, sells or holds a tokenized stock and explains why. It weighs each report's confidence and the quoted price against the stock's last close itself, and writes that judgement into the decision. Code checks the budget, the allowed stocks (reports rated strong or building) and the cost; then the agent approves its own order, which goes through NEAR Intents from its near.com balance. In shadow mode it places pretend orders at real quotes.",
    sources: "Bought reports · daily holding briefs · live prices · NEAR Intents quotes" },
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
    near: { state: r.chain_record ? "ran" : "off", note: r.chain_record ? r.chain_record.network === "mainnet" ? "fingerprint on mainnet" : "fingerprint on testnet" : "not recorded" },
    fund: { state: "off", note: "after the report: see Funds & trading" },       // not part of one report's trace (hidden there)
    trader: { state: "off", note: "after the report: see Funds & trading" },
    seller: { state: "off", note: "after the report: see Funds & trading" },
    stake: { state: "off", note: "after the report: see Funds & trading" },
    trader2: { state: "off", note: "planned" },
    intake: { state: "off", note: "before the report: see Request a report" },
    radar: { state: "off", note: "before the report: see Radar" },
    buyers: { state: "off", note: "after the report: see NEAR Agent Market" },
  };
}
