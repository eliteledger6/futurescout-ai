import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import Link from "next/link";
import "./globals.css";
import { NavLinks } from "@/components/NavLinks";
import { Logo } from "@/components/Logo";

const grotesk = Space_Grotesk({ subsets: ["latin"], weight: ["300", "400", "500"], variable: "--font-grotesk" });
const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "FUTURESCOUT AI",
  description: "Evidence-labelled technology research by AI agents running on NEAR AI Cloud, across semiconductors, AI, robotics, quantum, energy, space, biotech, cybersecurity and XR. Research information only, not investment advice.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${grotesk.variable} ${inter.variable}`}>
      <body>
        <header className="topbar">
          <div className="container topbar-inner">
            <Link href="/" className="brand" aria-label="FUTURESCOUT AI home">
              <Logo />
              <span>futurescout</span>
            </Link>
            <NavLinks />
            <div className="topbar-right">
              <span className="pill"><span className="dot" style={{ color: "var(--accent)" }} />Models on NEAR AI Cloud</span>
            </div>
          </div>
        </header>
        <main>{children}</main>
        <footer className="footer">
          <div className="container footer-grid">
            <p className="disclaimer">
              <strong style={{ color: "var(--text-2)" }}>Research information only, not investment advice.</strong>{" "}
              Reports are produced by AI agents from the sources they list. They do not recommend buying or selling
              anything, do not predict prices and do not promise any return. Forecasts are uncertain and may be wrong.
            </p>
            <p>FUTURESCOUT AI · MIT licence · built for NEAR HACKATHON</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
