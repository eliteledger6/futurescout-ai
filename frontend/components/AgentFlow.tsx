"use client";

// Animated network of the FUTURESCOUT agents. Without `stats` it explains the system; with `stats`
// (one saved report) it becomes that run's agent trace: which agents ran, what each produced and cost.
import { useState } from "react";
import { AGENTS, type AgentKey, type AgentRunStat } from "@/lib/agents";
import { fmtUsd } from "@/lib/api";
import { AgentIcon } from "./AgentIcon";

const W = 178, H = 60;
const POS: Record<AgentKey, [number, number]> = {
  chief: [14, 275],
  science: [242, 140], risk: [242, 230], x: [242, 320], patent: [242, 410],
  market: [470, 185],
  review: [470, 365],
  timing: [698, 230], scout: [698, 320],
  investment: [918, 160],
  near: [918, 290],
  seller: [918, 420],
  fund: [1196, 160],
  trader: [1196, 290],
  stake: [1196, 420],
};
const AFTER_REPORT: AgentKey[] = ["fund", "trader", "seller", "stake"];     // shown in the overview, hidden in one report's trace
const EDGES: [AgentKey, AgentKey][] = [
  ["chief", "science"], ["chief", "risk"], ["chief", "x"], ["chief", "patent"],
  ["science", "market"], ["patent", "market"],
  ["market", "review"], ["risk", "review"], ["x", "review"],
  ["review", "timing"], ["review", "scout"],
  ["timing", "investment"], ["scout", "investment"],
  ["investment", "near"], ["near", "seller"], ["near", "fund"], ["fund", "trader"], ["seller", "stake"],
];
const ORDER: AgentKey[][] = [["chief"], ["science", "risk", "x", "patent"], ["market"], ["review"], ["timing", "scout"], ["investment"], ["near"],
  ["seller", "fund"], ["trader"], ["stake"]];

function edgePath(a: AgentKey, b: AgentKey): string {
  const [ax, ay] = POS[a], [bx, by] = POS[b];
  if (ax === bx) {
    const x = ax + W / 2;
    return `M ${x} ${ay + H / 2} L ${x} ${by - H / 2}`;
  }
  const x1 = ax + W, x2 = bx, mid = (x1 + x2) / 2;
  return `M ${x1} ${ay} C ${mid} ${ay}, ${mid} ${by}, ${x2} ${by}`;
}

const LOOP = (() => {
  const [rx, ry] = POS.review, [sx, sy] = POS.science, [mx, my] = POS.market;
  const top = Math.min(sy, my) - 70;
  return `M ${rx + W} ${ry - 6} C ${rx + W + 70} ${top}, ${sx + W / 2} ${top - 10}, ${sx + W / 2} ${sy - H / 2}`;
})();

// The deal between the two agents: the report goes to the trading agent, its NEAR payment goes back to the report agent.
const SALE = (() => {
  const [sx, sy] = POS.seller, [tx, ty] = POS.trader;
  const x1 = sx + W, x2 = tx, mid = (x1 + x2) / 2;
  return {
    report: `M ${x1} ${sy - 10} C ${mid} ${sy - 10}, ${mid} ${ty + 4}, ${x2} ${ty + 4}`,            // report agent -> trading agent
    pay: `M ${x2} ${ty + 18} C ${mid + 12} ${ty + 18}, ${mid + 12} ${sy + 4}, ${x1} ${sy + 4}`,     // trading agent -> report agent
    mid,
  };
})();

// The loop that closes the agent economy: staking rewards come back as NEAR AI credits that pay every agent's model calls.
const CREDIT_Y = 528;
const CREDITS = (() => {
  const [sx, sy] = POS.stake, [cx, cy] = POS.chief;
  const x1 = sx + W / 2, x2 = cx + W / 2;
  return `M ${x1} ${sy + H / 2} L ${x1} ${CREDIT_Y - 14} Q ${x1} ${CREDIT_Y} ${x1 - 14} ${CREDIT_Y} L ${x2 + 14} ${CREDIT_Y} Q ${x2} ${CREDIT_Y} ${x2} ${CREDIT_Y - 14} L ${x2} ${cy + H / 2}`;
})();

export function AgentFlow({ stats, models }: { stats?: Record<AgentKey, AgentRunStat>; models?: Record<string, string> }) {
  const [active, setActive] = useState<AgentKey>("chief");
  const live = (k: AgentKey) => !stats || stats[k].state === "ran" || stats[k].state === "partial";
  const info = AGENTS[active];
  const stat = stats?.[active];

  return (
    <div className="flow">
      <div className="flow-swipe">Swipe sideways to see the whole network. Tap an agent for details.</div>
      <div className="flow-canvas">
        <svg className="flow-svg" viewBox={`0 0 ${stats ? 1110 : 1388} ${stats ? 505 : 548}`} role="img"
             aria-label="Agent network: Chief plans; Science, Risk, X and Patent research in parallel; Market reads the SEC filings of the companies the papers and patents point to; Chief reviews; price timing is checked while the Company scout finds the companies behind the patents and papers; Investment writes the report; the fingerprint is recorded on NEAR; the report agent sells the report to the trading agent for NEAR and stakes its earnings with NEAR AI; the staking rewards come back as NEAR AI credits that pay every agent's model calls; a fully invested paper fund is built for the topic; the trading agent buys and sells through NEAR Intents and approves its own orders after the code checks.">
          <defs>
            <radialGradient id="nodeGlow" cx="50%" cy="50%" r="60%">
              <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.28" />
              <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
            </radialGradient>
          </defs>
          {/* stage labels */}
          {([["Plan", 103], ["Research in parallel", 331], ["Companies & review", 559], ["Timing & scout", 787], ["Write, seal & sell", 1007],
             ...(stats ? [] : [["Fund, trade & stake", 1285]])] as [string, number][]).map(([t, x]) => (
            <text key={t} x={x} y={14} className="flow-stage" textAnchor="middle">{t}</text>
          ))}
          {/* edges */}
          {EDGES.filter(([a, b]) => !stats || !(AFTER_REPORT.includes(a) || AFTER_REPORT.includes(b))).map(([a, b]) => {
            const on = live(a) && live(b);
            const d = edgePath(a, b);
            return (
              <g key={`${a}-${b}`} className={on ? "edge on" : "edge off"}>
                <path d={d} className="edge-base" />
                {on && <path d={d} className="edge-flow" />}
              </g>
            );
          })}
          {!stats && (
            <>
              <g className="edge on credits">
                <path d={CREDITS} className="edge-base" />
                <path d={CREDITS} className="edge-flow" />
              </g>
              <text x={(POS.chief[0] + POS.stake[0] + W) / 2} y={CREDIT_Y - 8} className="flow-note" textAnchor="middle">
                staking rewards return as NEAR AI credits: they pay the model calls of every agent, from the Chief to the trading agent
              </text>
              <g className="edge on sale-report"><path d={SALE.report} className="edge-base" /><path d={SALE.report} className="edge-flow" /></g>
              <g className="edge on sale-pay"><path d={SALE.pay} className="edge-base" /><path d={SALE.pay} className="edge-flow" /></g>
              <text x={SALE.mid - 6} y={POS.trader[1] + 50} className="flow-note" textAnchor="end">report →</text>
              <text x={SALE.mid + 4} y={POS.seller[1] - 44} className="flow-note" textAnchor="middle">← pays</text>
              <text x={SALE.mid + 4} y={POS.seller[1] - 32} className="flow-note" textAnchor="middle">3–5 NEAR</text>
              <text x={(POS.seller[0] + W + POS.stake[0]) / 2} y={POS.stake[1] + 18} className="flow-note" textAnchor="middle">stakes 80%</text>
            </>
          )}
          <g className="edge loop">
            <path d={LOOP} className="edge-base" />
            <text x={(POS.review[0] + POS.science[0]) / 2 + W / 2} y={POS.science[1] - 52} className="flow-note" textAnchor="middle">
              at most one extra search round
            </text>
          </g>
          {/* nodes */}
          {(Object.keys(POS) as AgentKey[]).filter((k) => !stats || !AFTER_REPORT.includes(k)).map((k) => {
            const [x, y] = POS[k];
            const a = AGENTS[k];
            const s = stats?.[k];
            const state = s?.state ?? "ran";
            return (
              <g key={k} className={`node ${state} ${active === k ? "active" : ""}`} transform={`translate(${x} ${y - H / 2})`}
                 tabIndex={0} role="button" aria-label={`${a.name}: ${a.role}`}
                 onMouseEnter={() => setActive(k)} onFocus={() => setActive(k)} onClick={() => setActive(k)}>
                {active === k && <ellipse cx={W / 2} cy={H / 2} rx={W * 0.75} ry={H * 1.1} fill="url(#nodeGlow)" />}
                <rect width={W} height={H} rx={8} className="node-box" />
                <foreignObject x={12} y={12} width={22} height={22}>
                  <div className="node-icon"><AgentIcon name={a.icon} /></div>
                </foreignObject>
                <text x={42} y={26} className="node-name">{a.name}</text>
                <text x={42} y={44} className="node-role">
                  {s ? statLine(k, s) : a.role}
                </text>
                <circle cx={W - 12} cy={12} r={4} className={`node-dot ${state}`} />
              </g>
            );
          })}
        </svg>
      </div>

      {/* phone layout: the same pipeline as a vertical list */}
      <ol className="flow-list">
        {ORDER.filter((stage) => !stats || !stage.some((k) => AFTER_REPORT.includes(k))).map((stage, i) => (
          <li key={i}>
            {stage.map((k) => (
              <button key={k} className={`flow-chip ${stats?.[k]?.state ?? "ran"} ${active === k ? "active" : ""}`} onClick={() => setActive(k)}>
                <AgentIcon name={AGENTS[k].icon} size={15} /> {AGENTS[k].name}
              </button>
            ))}
          </li>
        ))}
      </ol>

      <div className="flow-detail" aria-live="polite">
        <div className="flow-detail-head">
          <span className="flow-detail-icon"><AgentIcon name={info.icon} size={22} /></span>
          <div>
            <div className="h3" style={{ margin: 0, fontSize: 20 }}>{info.name}{info.prefix ? <span className="muted mono small"> · findings {info.prefix}1, {info.prefix}2…</span> : null}</div>
            <div className="small muted">{info.role}</div>
          </div>
          {stat && <span className={`pill state-${stat.state}`} style={{ marginLeft: "auto" }}>{STATE_TEXT[stat.state]}</span>}
        </div>
        <p style={{ color: "var(--text-2)", margin: "12px 0" }}>{info.detail}</p>
        <div className="pills">
          <span className="pill">Data: {info.sources}</span>
          {info.modelKey && models?.[info.modelKey] && <span className="pill">Model: {models[info.modelKey]}</span>}
          {stat?.models?.map((m) => <span key={m} className="pill">Ran on: {m}</span>)}
          {stat?.findings !== undefined && <span className="pill">{stat.findings} findings</span>}
          {stat?.sources !== undefined && <span className="pill">{stat.sources} sources</span>}
          {stat?.cost ? <span className="pill">{fmtUsd(stat.cost)}</span> : null}
          {stat?.note && <span className="pill">{stat.note}</span>}
        </div>
      </div>
    </div>
  );
}

const STATE_TEXT = { ran: "ran", partial: "retrieved, no analysis", not_run: "not run", off: "not run" } as const;

function statLine(k: AgentKey, s: AgentRunStat): string {
  if (s.state === "off") return "not run in this report";
  if (s.state === "partial") return k === "chief" || k === "review" ? "default plan" : "data only, no analysis";
  const bits = [];
  if (s.findings !== undefined) bits.push(`${s.findings} findings`);
  if (s.sources !== undefined) bits.push(`${s.sources} src`);
  if (!bits.length && s.note) bits.push(s.note);
  return bits.join(" · ") || AGENTS[k].role;
}
