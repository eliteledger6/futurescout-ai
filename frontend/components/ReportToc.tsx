"use client";

// Sticky section navigator for a report page; highlights the section in view.
import { useEffect, useState } from "react";

export function ReportToc({ items }: { items: { id: string; label: string }[] }) {
  const [active, setActive] = useState(items[0]?.id);
  useEffect(() => {
    const els = items.map((i) => document.getElementById(i.id)).filter(Boolean) as HTMLElement[];
    if (!els.length) return;
    const io = new IntersectionObserver((entries) => {
      const visible = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible[0]) setActive(visible[0].target.id);
    }, { rootMargin: "-20% 0px -65% 0px" });
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, [items]);
  return (
    <nav className="toc" aria-label="Report sections">
      <div className="container toc-inner">
        {items.map((i) => (
          <a key={i.id} href={`#${i.id}`} className={active === i.id ? "on" : ""}
             onClick={(e) => { e.preventDefault(); document.getElementById(i.id)?.scrollIntoView({ behavior: "smooth", block: "start" }); }}>
            {i.label}
          </a>
        ))}
      </div>
    </nav>
  );
}
