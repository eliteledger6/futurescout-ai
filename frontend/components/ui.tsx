import type { Confidence, Label } from "@/lib/types";

const LABEL_TEXT: Record<Label, string> = {
  verified_fact: "verified fact",
  ai_interpretation: "AI interpretation",
  forecast: "forecast",
  assumption: "assumption",
  unverified_claim: "unverified claim",
};

export const LABEL_HELP: Record<Label, string> = {
  verified_fact: "A quoted passage in a cited source supports it (checked by code).",
  ai_interpretation: "The AI's reading or comparison of the evidence.",
  forecast: "A prediction about the future.",
  assumption: "Taken as given; no supporting evidence cited.",
  unverified_claim: "Asserted (e.g. by a company or a headline) but not confirmed.",
};

export function LabelBadge({ label }: { label: Label }) {
  return (
    <span className={`label label-${label}`} title={LABEL_HELP[label]}>
      {LABEL_TEXT[label] ?? label}
    </span>
  );
}

export function ConfidencePill({ value, prefix = "confidence" }: { value: Confidence | null | undefined; prefix?: string }) {
  if (!value) return null;
  return <span className="pill">{prefix} {value}</span>;
}

export function ErrorNotice({ error }: { error: string }) {
  const offline = /fetch|network|Failed/i.test(error);
  return (
    <div className="notice notice-err">
      {offline ? (
        <>
          Cannot reach the FUTURESCOUT API. Start it from the <span className="mono">backend</span> folder with{" "}
          <span className="mono">python scripts\serve.py</span>, then reload this page.
        </>
      ) : (
        <>Error: {error}</>
      )}
    </div>
  );
}

export function Loading({ lines = 3 }: { lines?: number }) {
  return (
    <div className="stack" aria-busy="true" aria-label="Loading">
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="skeleton" style={{ height: 22, width: `${90 - i * 15}%` }} />
      ))}
    </div>
  );
}
