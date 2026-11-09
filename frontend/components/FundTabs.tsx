import Link from "next/link";

// Funds and Trading are one area: the paper funds are the simulation, the trading agent is the small real-money test.
export function FundTabs({ active }: { active: "funds" | "trading" }) {
  const tabs = [
    { key: "funds", href: "/funds", label: "Paper funds" },
    { key: "trading", href: "/trading", label: "Trading agent" },
  ] as const;
  return (
    <nav className="tabs" aria-label="Funds and trading">
      {tabs.map((t) => (
        <Link key={t.key} href={t.href} className={`tab ${active === t.key ? "on" : ""}`} aria-current={active === t.key ? "page" : undefined}
              style={{ textDecoration: "none" }}>{t.label}</Link>
      ))}
    </nav>
  );
}
