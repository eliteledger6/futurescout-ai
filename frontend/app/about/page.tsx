import Link from "next/link";
import { AgentFlow } from "@/components/AgentFlow";
import { AgentIcon } from "@/components/AgentIcon";
import { LabelBadge, LABEL_HELP } from "@/components/ui";
import type { Label } from "@/lib/types";

const LABELS: Label[] = ["verified_fact", "ai_interpretation", "forecast", "unverified_claim", "assumption"];

const RULES = [
  ["seal", "Sources only from real APIs", "Every URL in a report comes from an API response, never from a model's memory. Invented source ids are removed."],
  ["shield", "Quotes are checked", "A 'verified fact' must quote its source word for word. Headlines and X posts can never verify a fact."],
  ["building", "Companies come from the evidence", "No hand-made company list: a company is checked because the retrieved patents name it as assignee or its researchers wrote the papers. Patents and papers come first: a company named only in an SEC filing is used just when a topic has no company with patents or papers, and is then labelled as a fallback."],
  ["swords", "A second agent argues back", "The Risk agent searches independently for limits and failures, then challenges specific findings."],
  ["pulse", "Limits written in code", "The trading agent decides, but code sets the limits: a budget that is only what the owner puts into the agent's balance, an allowlist of tokenized stocks from reports rated strong or building, a cost cap, a kill switch, and an order checked field by field before it is signed. How confident a report is and whether the quoted price is acceptable against the last close are the agent's own judgement, written into every decision."],
  ["coin", "Agents pay their way", "A report costs what it took to make plus a small margin ($2–3), paid in NEAR, and is opened only by a payment (reports written since 11 November 2026 are open for the demo and marked so). The trading agent must buy a report before it may use it, and any other bot can buy through the API. The report agent stakes 70% of what it earns with NEAR AI, and the rewards pay for the agents' model calls."],
] as const;

export default function About() {
  return (
    <>
      <section className="hero" style={{ padding: "96px 0 72px" }}>
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">How it works</div>
          <h1 className="display" style={{ fontSize: "clamp(40px, 6vw, 76px)" }}>A team of agents, <span className="gradient-text">one rule: show the evidence</span></h1>
          <p className="lede">A hot technology shows up first in research papers and patent filings, then in company reports. FUTURESCOUT measures all three, argues the other side, and names the companies the evidence points to. Then the agents act on it: a report agent sells each report for NEAR, a trading agent buys it and trades tokenized stocks through NEAR Intents, and the report agent&apos;s earnings are staked so NEAR AI pays for the models.</p>
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          <h2 className="h2">The agent network</h2>
          <p className="sub">Hover or tap any agent.</p>
          <AgentFlow />
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          <h2 className="h2">The rules every agent follows</h2>
          <div className="grid grid-2">
            {RULES.map(([icon, title, text]) => (
              <div className="card" key={title}>
                <span style={{ color: "var(--accent)" }}><AgentIcon name={icon} size={26} /></span>
                <h3 className="h3" style={{ margin: 0 }}>{title}</h3>
                <p style={{ color: "var(--text-2)", margin: 0 }}>{text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container stack">
          <h2 className="h2">Reading the labels</h2>
          <div className="table-wrap">
            <table className="table">
              <tbody>{LABELS.map((l) => <tr key={l}><td style={{ width: 200 }}><LabelBadge label={l} /></td><td>{LABEL_HELP[l]}</td></tr>)}</tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container grid grid-2">
          <div className="card">
            <h3 className="h3">Where NEAR fits</h3>
            <p style={{ color: "var(--text-2)", margin: 0 }}>
              Every agent calls a model from the NEAR AI Cloud catalogue (Qwen, DeepSeek, GLM, Claude), each chosen per agent with
              fallbacks and per-run cost tracking. The trading agent trades through NEAR Intents on mainnet, signing orders from its
              near.com balance; it pays the report agent the same way. The report agent is listed on NEAR Agent Market, where anyone can hire it, and stakes with NEAR AI (Staking for Inference) for
              model credits. The fingerprint of every report since the first day's three test runs is stored on NEAR (new seals on mainnet, signed by the report agent; older ones on testnet). Earlier fund decisions and trade records were sealed as well; since 11 November 2026 only reports are, to save NEAR.
            </p>
          </div>
          <div className="card">
            <h3 className="h3">What it is not</h3>
            <p style={{ color: "var(--text-2)", margin: 0 }}>
              Not financial advice and not a money machine. The trading agent works only with the money the owner puts into its balance, buys only
              tokenized stocks from its allowlist, and never promises returns or gives price targets. It never posts, likes or follows on X.
            </p>
          </div>
        </div>
        <div className="container" style={{ marginTop: 32 }}>
          <Link className="btn btn-solid" href="/">See the reports →</Link>
        </div>
      </section>
    </>
  );
}
