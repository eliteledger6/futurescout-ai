"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

// Four tabs. Funds and Trading share one tab (sub-tabs on those pages). "New research" is a button on the Reports page. The older paper portfolio (/portfolio) is no longer linked.
const LINKS = [
  { href: "/", label: "Reports", also: ["/runs", "/research"] },
  { href: "/radar", label: "Radar", also: [] },
  { href: "/funds", label: "Funds & trading", also: ["/portfolio", "/trading"] },
  { href: "/about", label: "How it works", also: [] },
];

export function NavLinks() {
  const path = usePathname();
  return (
    <nav className="nav" aria-label="Main">
      {LINKS.map((l) => {
        const active = (l.href === "/" ? path === "/" : path.startsWith(l.href)) || l.also.some((a) => path.startsWith(a));
        return (
          <Link key={l.href} href={l.href} className={active ? "active" : undefined}>
            {l.label}
          </Link>
        );
      })}
    </nav>
  );
}
