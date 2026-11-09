"use client";

// Small motion helpers. All of them respect prefers-reduced-motion (CSS turns the effects off).
import { useEffect, useRef, useState, type ReactNode } from "react";

/** Fades/slides children in when they scroll into view. */
export function Reveal({ children, delay = 0, className = "" }: { children: ReactNode; delay?: number; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [on, setOn] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (!("IntersectionObserver" in window)) { setOn(true); return; }
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { setOn(true); io.disconnect(); }
    }, { rootMargin: "0px 0px 12% 0px", threshold: 0.05 });
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return <div ref={ref} className={`reveal ${on ? "in" : ""} ${className}`} style={{ transitionDelay: `${delay}ms` }}>{children}</div>;
}

/** Counts from 0 to `value` once visible. Keeps the given number of decimals; `prefix`/`suffix` are plain text. */
export function CountUp({ value, decimals = 0, prefix = "", suffix = "", duration = 1100 }:
  { value: number; decimals?: number; prefix?: string; suffix?: string; duration?: number }) {
  const ref = useRef<HTMLSpanElement>(null);
  const [shown, setShown] = useState(0);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const reduced = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    if (reduced) { setShown(value); return; }
    let raf = 0;
    const start = () => {
      const t0 = performance.now();
      const tick = (t: number) => {
        const p = Math.min(1, (t - t0) / duration);
        const eased = 1 - Math.pow(1 - p, 3);
        setShown(value * eased);
        if (p < 1) raf = requestAnimationFrame(tick);
      };
      raf = requestAnimationFrame(tick);
    };
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) { start(); io.disconnect(); } }, { threshold: 0.3 });
    io.observe(el);
    return () => { io.disconnect(); cancelAnimationFrame(raf); };
  }, [value, duration]);
  return <span ref={ref}>{prefix}{shown.toFixed(decimals)}{suffix}</span>;
}

/** Animated arc gauge for a 0-100 score. */
export function ScoreGauge({ score, reportable, confidence, size = 180 }:
  { score: number | null; reportable: boolean; confidence?: string | null; size?: number }) {
  const r = 52, c = 2 * Math.PI * r;
  const v = Math.max(0, Math.min(100, score ?? 0));
  const [dash, setDash] = useState(c);
  useEffect(() => {
    const reduced = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
    const target = c - (c * 0.75 * v) / 100;   // 270° arc
    if (reduced) { setDash(target); return; }
    const t = setTimeout(() => setDash(target), 80);
    return () => clearTimeout(t);
  }, [v, c]);
  return (
    <div className="gauge" style={{ width: size, height: size }} role="img" aria-label={`Score ${score ?? "none"} of 100`}>
      <svg viewBox="0 0 120 120" width={size} height={size}>
        <defs>
          <linearGradient id="gaugeGrad" x1="0" y1="1" x2="1" y2="0">
            <stop offset="0%" stopColor="#1f9a6b" />
            <stop offset="100%" stopColor="var(--accent)" />
          </linearGradient>
        </defs>
        <g transform="rotate(135 60 60)">
          <circle cx="60" cy="60" r={r} className="gauge-track" strokeDasharray={`${c * 0.75} ${c}`} />
          <circle cx="60" cy="60" r={r} className={`gauge-arc ${reportable ? "" : "dim"}`} strokeDasharray={`${c} ${c}`} strokeDashoffset={dash} stroke="url(#gaugeGrad)" />
        </g>
      </svg>
      <div className="gauge-label">
        <div className="gauge-value">{score ?? "–"}</div>
        <div className="gauge-sub">{score === null ? "no score" : reportable ? `of 100 · ${confidence ?? ""}` : "not reportable"}</div>
      </div>
    </div>
  );
}
