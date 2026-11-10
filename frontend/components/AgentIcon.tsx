// Small line icons for the agents (24x24, stroke = currentColor). Drawn for FUTURESCOUT; no third-party marks.
const PATHS: Record<string, string> = {
  compass: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18zM15.5 8.5l-2 5-5 2 2-5z",
  flask: "M9 3h6M10 3v6L4.5 18.5A1.6 1.6 0 0 0 6 21h12a1.6 1.6 0 0 0 1.5-2.5L14 9V3M7.5 15h9",
  shield: "M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6zM9.5 12l2 2 3.5-4",
  building: "M4 21V7l8-4 8 4v14M4 21h16M9 21v-5h6v5M8 10h.01M12 10h.01M16 10h.01M8 13h.01M12 13h.01M16 13h.01",
  signal: "M5 12.5a7 7 0 0 1 14 0M8 13a4 4 0 0 1 8 0M12 13v8M3 9a10.5 10.5 0 0 1 18 0",
  stamp: "M9 4h6l-1 6h3a2 2 0 0 1 2 2v3H5v-3a2 2 0 0 1 2-2h3zM5 19h14",
  search: "M11 4a7 7 0 1 0 0 14a7 7 0 1 0 0-14zM20 20l-4-4",
  swords: "M14.5 3.5L21 3l-.5 6.5L9 21l-6-6zM6 12l6 6M3 21l3-3",
  pulse: "M3 12h4l2-6 4 12 2-6h6",
  radar: "M12 3a9 9 0 1 0 9 9M12 7a5 5 0 1 0 5 5M12 12l7-7M12 12h.01",
  doc: "M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6",
  coin: "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18zM9 8v8M9 8l6 8M15 8v8",
  sprout: "M12 21v-9M12 12C12 8 9 6 5 6c0 4 3 6 7 6zM12 14c0-3.5 2.5-5.5 7-5.5 0 3.5-2.5 5.5-7 5.5zM7 21h10",
  seal: "M12 3l2.4 1.8 3-.2.9 2.9 2.5 1.7-1 2.8 1 2.8-2.5 1.7-.9 2.9-3-.2L12 21l-2.4-1.8-3 .2-.9-2.9L3.2 14.8l1-2.8-1-2.8 2.5-1.7.9-2.9 3 .2zM9 12l2 2 4-4",
};

export function AgentIcon({ name, size = 18 }: { name: string; size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6"
         strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d={PATHS[name] ?? PATHS.doc} />
    </svg>
  );
}
