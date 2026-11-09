// FUTURESCOUT's own mark: a scope reticle over a rising line (not derived from any NEAR logo).
export function Logo({ size = 26 }: { size?: number }) {
  return (
    <svg className="brand-mark" width={size} height={size} viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <rect x="1" y="1" width="30" height="30" rx="4" stroke="currentColor" strokeWidth="1.5" />
      <circle cx="16" cy="16" r="7.5" stroke="currentColor" strokeWidth="1.5" />
      <path d="M16 4.5v5M16 22.5v5M4.5 16h5M22.5 16h5" stroke="currentColor" strokeWidth="1.5" />
      <path d="M11 19.5l3.5-3.5 2.5 2 4-5" stroke="#00ec97" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
