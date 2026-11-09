"use client";

// Compact live radar: the hottest topics as glowing chips (home hero).
import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { TopicSignal } from "@/lib/types";

export function RadarStrip() {
  const [topics, setTopics] = useState<TopicSignal[] | null>(null);
  useEffect(() => { api.radar().then((r) => setTopics(r.topics.filter((t) => t.rank).slice(0, 6))).catch(() => setTopics([])); }, []);
  if (!topics || topics.length === 0) return null;
  const max = Math.max(...topics.map((t) => t.heat ?? 0), 1);
  return (
    <div className="radar-strip" aria-label="Hottest topics on the radar">
      <span className="radar-strip-label">Radar · hottest now</span>
      {topics.map((t) => (
        <Link key={t.topic} href="/radar" className="heat-chip" style={{ ["--h" as string]: `${Math.max(0.25, (t.heat ?? 0) / max)}` } as React.CSSProperties}>
          <span className="heat-chip-rank">#{t.rank}</span>{t.topic}<span className="heat-chip-val">{(t.heat ?? 0) > 0 ? "+" : ""}{Math.round(t.heat ?? 0)}%</span>
        </Link>
      ))}
    </div>
  );
}
