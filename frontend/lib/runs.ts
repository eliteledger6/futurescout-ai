// Several runs can exist for one topic (re-runs, watch-mode triggers). Lists show the newest run per topic;
// older runs stay reachable from the report page. Nothing is deleted.

export interface TopicGroup<T> { topic: string; latest: T; older: T[] }

export function latestPerTopic<T extends { topic: string; generated_at: string; score?: number | null }>(rows: T[]): TopicGroup<T>[] {
  const by = new Map<string, T[]>();
  for (const r of rows) {
    const k = r.topic.trim().toLowerCase();
    by.set(k, [...(by.get(k) ?? []), r]);
  }
  return [...by.values()]
    .map((list) => {
      const sorted = [...list].sort((a, b) => b.generated_at.localeCompare(a.generated_at));
      // the newest SCORED run leads; an unscored run (an outage left no analysis) stays reachable among the older ones
      const lead = sorted.find((r) => r.score != null) ?? sorted[0];
      return { topic: lead.topic, latest: lead, older: sorted.filter((r) => r !== lead) };
    })
    .sort((a, b) => b.latest.generated_at.localeCompare(a.latest.generated_at));
}

export const sectorLabel = (key?: string | null) => (key ? key.replace(/_/g, " ") : "technology");
