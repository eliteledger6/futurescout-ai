"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Verification } from "@/lib/types";

// Recomputes the report fingerprint on the server and compares it with the value stored on NEAR (mainnet or testnet).
export function NearBadge({ runId }: { runId: string }) {
  const [v, setV] = useState<Verification | null>(null);
  useEffect(() => { api.verify(runId).then(setV).catch(() => setV(null)); }, [runId]);
  if (!v) return null;
  const short = v.sha256.slice(0, 12);
  const net = v.network === "mainnet" ? "NEAR mainnet" : v.network === "testnet" ? "NEAR testnet" : "NEAR";
  if (v.status === "match") {
    return (
      <a className="pill pill-on" href={v.explorer_url} target="_blank" rel="noopener noreferrer"
         title={`SHA-256 ${v.sha256} matches the value stored by ${v.account} on ${net}`}>
        <span className="dot" />Unchanged since recorded on {net} · {short}… ↗
      </a>
    );
  }
  if (v.status === "MISMATCH") {
    return <span className="pill" style={{ color: "var(--l-danger)", borderColor: "var(--l-danger)" }}
                 title={`report ${v.sha256} vs on-chain ${v.onchain_sha256}`}>Changed after recording: fingerprint does not match {net}</span>;
  }
  if (v.status === "unavailable") {
    return <span className="pill" title={v.detail}>{net} check unavailable right now</span>;
  }
  return <span className="pill" title={`SHA-256 ${v.sha256}`}>Not recorded on NEAR · fingerprint {short}…</span>;
}
