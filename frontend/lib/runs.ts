// Several runs can exist for one topic (re-runs, watch-mode triggers). Lists show the newest run per topic;
// older runs stay reachable from the report page. Nothing is deleted.

export interface TopicGroup<T> { topic: string; latest: T; older: T[] }

export function latestPerTopic<T extends { topic: string; generated_at: string }>(rows: T[]): TopicGroup<T>[] {
  const by = new Map<string, T[]>();
  for (const r of rows) {
    const k = r.topic.trim().toLowerCase();
    by.set(k, [...(by.get(k) ?? []), r]);
  }
  return [...by.values()]
    .map((list) => {
      const sorted = [...list].sort((a, b) => b.generated_at.localeCompare(a.generated_at));
      return { topic: sorted[0].topic, latest: sorted[0], older: sorted.slice(1) };
    })
    .sort((a, b) => b.latest.generated_at.localeCompare(a.latest.generated_at));
}

export const sectorLabel = (key?: string | null) => (key ? key.replace(/_/g, " ") : "technology");
