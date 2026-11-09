import Link from "next/link";
import { AgentFlow } from "@/components/AgentFlow";
import { AgentIcon } from "@/components/AgentIcon";
import { LabelBadge, LABEL_HELP } from "@/components/ui";
import type { Label } from "@/lib/types";

const LABELS: Label[] = ["verified_fact", "ai_interpretation", "forecast", "unverified_claim", "assumption"];

const RULES = [
  ["seal", "Sources only from real APIs", "Every URL in a report comes from an API response, never from a model's memory. Invented source ids are removed by code."],
  ["shield", "Quotes are checked by code", "A 'verified fact' must quote its source word for word. Headlines and X posts can never verify a fact."],
  ["swords", "A second agent argues back", "The Risk agent searches independently for limits and failures, then challenges specific findings."],
  ["pulse", "Risk, not trading", "Price run-up is measured as a risk. No buy or sell signals, no price targets, no promised returns."],
] as const;

export default function About() {
  return (
    <>
      <section className="hero" style={{ padding: "96px 0 72px" }}>
        <div className="aurora" aria-hidden="true" />
        <div className="container">
          <div className="eyebrow">How it works</div>
          <h1 className="display" style={{ fontSize: "clamp(40px, 6vw, 76px)" }}>Eight agents, <span className="gradient-text">one rule: show the evidence</span></h1>
          <p className="lede">A hot technology shows up first in research papers and patent filings, then in company reports. FUTURESCOUT measures all three, argues the other side, and tells you which companies the evidence points to, and how much of the move may already be priced in.</p>
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
              fallbacks and per-run cost tracking. Each finished report's SHA-256 fingerprint is stored on NEAR testnet, so anyone
              can check it was not edited afterwards.
            </p>
          </div>
          <div className="card">
            <h3 className="h3">What it is not</h3>
            <p style={{ color: "var(--text-2)", margin: 0 }}>
              Not a trading bot. It never places trades, holds no wallet for trading, never promises returns and gives no price
              targets. It never posts, likes or follows on X.
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
