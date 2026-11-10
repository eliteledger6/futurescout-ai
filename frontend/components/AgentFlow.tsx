"use client";

// Animated network of the FUTURESCOUT agents. Without `stats` it explains the system; with `stats`
// (one saved report) it becomes that run's agent trace: which agents ran, what each produced and cost.
import { useState } from "react";
import { AGENTS, type AgentKey, type AgentRunStat } from "@/lib/agents";
import { fmtUsd } from "@/lib/api";
import { AgentIcon } from "./AgentIcon";

const W = 178, H = 60;
// One left-to-right flow. Columns: plan, research, companies & review, timing & scout, write & seal, sell & fund, trade & stake.
// Science and Patent sit together (both feed Market); Risk and X signals below them (both feed the Chief review).
const COL = [14, 228, 442, 656, 870, 1084, 1388];
const POS: Record<AgentKey, [number, number]> = {
  chief: [COL[0], 260],
  science: [COL[1], 120], patent: [COL[1], 200], risk: [COL[1], 320], x: [COL[1], 400],
  market: [COL[2], 160],
  review: [COL[2], 360],
  timing: [COL[3], 220], scout: [COL[3], 300],
  investment: [COL[4], 220],
  near: [COL[4], 320],
  fund: [COL[5], 160], seller: [COL[5], 360],
  trader: [COL[6], 160], stake: [COL[6], 360],
  trader2: [COL[6], 460],
};
const AFTER_REPORT: AgentKey[] = ["fund", "trader", "seller", "stake", "trader2"];   // overview only, hidden in one report's trace
const PLANNED: AgentKey[] = ["trader2"];                                              // drawn dashed: the next step, not running yet
const EDGES: [AgentKey, AgentKey][] = [
  ["chief", "science"], ["chief", "patent"], ["chief", "risk"], ["chief", "x"],
  ["science", "market"], ["patent", "market"],
  ["market", "review"], ["risk", "review"], ["x", "review"],
  ["review", "timing"], ["review", "scout"],
  ["timing", "investment"], ["scout", "investment"],
  ["investment", "near"],
  ["near", "fund"], ["near", "seller"], ["fund", "trader"],
];
const ORDER: AgentKey[][] = [["chief"], ["science", "patent", "risk", "x"], ["market"], ["review"], ["timing", "scout"], ["investment"], ["near"],
  ["fund", "seller"], ["trader"], ["stake"], ["trader2"]];

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

// The deal between the report agent and the trading agent: report up, NEAR payment back down (two parallel curves).
const GAP_MID = (COL[5] + W + COL[6]) / 2;
const SALE = (() => {
  const [, sy] = POS.seller, [, ty] = POS.trader, x1 = COL[5] + W, x2 = COL[6];
  return {
    report: `M ${x1} ${sy - 22} C ${GAP_MID - 12} ${sy - 22}, ${GAP_MID - 12} ${ty + 4}, ${x2} ${ty + 4}`,    // report agent -> trading agent
    pay: `M ${x2} ${ty + 18} C ${GAP_MID + 12} ${ty + 18}, ${GAP_MID + 12} ${sy - 8}, ${x1} ${sy - 8}`,       // trading agent -> report agent
    stake: `M ${x1} ${sy + 14} L ${x2} ${sy + 14}`,                                                             // report agent -> staking
  };
})();

// NEAR AI credits: from staking along the bottom back to the Chief (they pay every agent's model calls).
const CREDIT_Y = 526;
const CREDITS = (() => {
  const [sx, sy] = POS.stake, [cx, cy] = POS.chief, r = 12;
  const xr = sx + W + 22, x2 = cx + W / 2;
  return `M ${sx + W} ${sy} L ${xr - r} ${sy} Q ${xr} ${sy} ${xr} ${sy + r} L ${xr} ${CREDIT_Y - r} Q ${xr} ${CREDIT_Y} ${xr - r} ${CREDIT_Y} `
       + `L ${x2 + r} ${CREDIT_Y} Q ${x2} ${CREDIT_Y} ${x2} ${CREDIT_Y - r} L ${x2} ${cy + H / 2}`;
})();

// The report agent's kept 30% pot: once it passes $200 it funds a second trading agent (planned).
const POT = (() => {
  const [sx, sy] = POS.seller, [nx, ny] = POS.trader2, r = 10;
  const x = sx + W / 2;
  return `M ${x} ${sy + H / 2} L ${x} ${ny - r} Q ${x} ${ny} ${x + r} ${ny} L ${nx} ${ny}`;
})();

function Badge({ x, y, text, tone }: { x: number; y: number; text: string; tone: "report" | "pay" | "pot" | "credit" }) {
  const w = text.length * 6.6 + 14;
  return (
    <g className={`flow-badge ${tone}`} transform={`translate(${x - w / 2} ${y - 9})`}>
      <rect width={w} height={18} rx={9} />
      <text x={w / 2} y={12.5} textAnchor="middle">{text}</text>
    </g>
  );
}

function Flow({ d, cls = "edge on" }: { d: string; cls?: string }) {
  return <g className={cls}><path d={d} className="edge-base" /><path d={d} className="edge-flow" /></g>;
}

export function AgentFlow({ stats, models }: { stats?: Record<AgentKey, AgentRunStat>; models?: Record<string, string> }) {
  const [active, setActive] = useState<AgentKey>("chief");
  const live = (k: AgentKey) => !stats || stats[k].state === "ran" || stats[k].state === "partial";
  const info = AGENTS[active];
  const stat = stats?.[active];

  return (
    <div className="flow">
      <div className="flow-swipe">Swipe sideways to see the whole network. Tap an agent for details.</div>
      <div className="flow-canvas">
        <svg className="flow-svg" viewBox={stats ? "0 0 1062 450" : "0 0 1610 545"} role="img"
             aria-label="Agent network, left to right: Chief plans; Science and Patent research, and the Market agent reads the SEC filings of the companies they point to; Risk and X signals research in parallel and the Chief reviews; price timing is checked while the Company scout finds the companies behind the patents and papers; Investment writes the report and its fingerprint is recorded on NEAR; the topic fund invests a paper fund and the report agent sells the report to the trading agent, which pays $2 to $3 in NEAR and trades tokenized stocks through NEAR Intents; the report agent stakes 70% of each payment with NEAR AI, whose credits pay every agent's model calls, and keeps 30%, which funds a planned second trading agent at $200.">
          <defs>
            <radialGradient id="nodeGlow" cx="50%" cy="50%" r="60%">
              <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.28" />
              <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
            </radialGradient>
          </defs>
          {/* stage labels */}
          {([["Plan", 0], ["Research in parallel", 1], ["Companies & review", 2], ["Timing & scout", 3], ["Write & seal", 4],
             ...(stats ? [] : [["Sell & fund", 5], ["Trade & stake", 6]])] as [string, number][]).map(([t, i]) => (
            <text key={t} x={COL[i] + W / 2} y={14} className="flow-stage" textAnchor="middle">{t}</text>
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
              <Flow d={SALE.report} cls="edge on sale-report" />
              <Flow d={SALE.pay} cls="edge on sale-pay" />
              <Flow d={SALE.stake} />
              <Badge x={GAP_MID} y={POS.trader[1] + 62} text="report ▸" tone="report" />
              <Badge x={GAP_MID} y={POS.seller[1] - 62} text="◂ pays 3–5 NEAR" tone="pay" />
              <Badge x={GAP_MID} y={POS.seller[1] + 32} text="stakes 70% ▸" tone="credit" />
              <Flow d={CREDITS} cls="edge on credits" />
              <Badge x={(POS.chief[0] + POS.stake[0] + W) / 2} y={CREDIT_Y} text="◂ NEAR AI credits from staking pay every agent's model calls" tone="credit" />
              <g className="edge planned-edge"><path d={POT} className="edge-base" /></g>
              <Badge x={GAP_MID - 26} y={POS.trader2[1] - 14} text="keeps 30% · at $200 ▸" tone="pot" />
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
              <g key={k} className={`node ${state} ${active === k ? "active" : ""} ${PLANNED.includes(k) ? "planned" : ""}`} transform={`translate(${x} ${y - H / 2})`}
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
