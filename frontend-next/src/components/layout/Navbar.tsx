"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTheme } from "next-themes";
import { useState, useEffect } from "react";
import { Brain, Sun, Moon, Zap, Menu, X, ShieldCheck } from "lucide-react";

const navLinks = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/analysis/new", label: "New Analysis" },
  { href: "/agents", label: "AI Agents" },
  { href: "/knowledge-base", label: "Knowledge Base" },
  { href: "/collaboration", label: "Collaboration" },
  { href: "/documents", label: "Documents" },
  { href: "/compare", label: "Compare" },
  { href: "/analytics", label: "Analytics" },
  { href: "/playground", label: "Playground" },
  { href: "/admin", label: "Admin" },
];

export function Navbar() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const isActive = (href: string) =>
    pathname === href || (href !== "/" && pathname.startsWith(href));

  return (
    <header
      style={{
        position: "fixed",
        top: 16,
        left: 0,
        right: 0,
        zIndex: 1000,
        maxWidth: 1280,
        margin: "0 auto",
        padding: "0 16px",
      }}
    >
      <div
        className="glass-pill"
        style={{
          borderRadius: 999,
          height: 60,
          padding: "0 24px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 16,
        }}
      >
        {/* Logo */}
        <Link href="/" style={{ display: "flex", alignItems: "center", gap: 10, textDecoration: "none", flexShrink: 0 }}>
          <div style={{ width: 34, height: 34, borderRadius: 10, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, boxShadow: "0 0 16px rgba(99,102,241,0.5)" }}>
            <Brain style={{ width: 18, height: 18, color: "#fff" }} />
          </div>
          <span style={{ fontWeight: 800, fontSize: 16, letterSpacing: "-0.02em" }}>
            <span className="gradient-text">IDP</span>
            <span style={{ color: "#38bdf8", fontSize: 11, fontWeight: 700, marginLeft: 6, textTransform: "uppercase" }}>AI OS</span>
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav style={{ display: "flex", alignItems: "center", gap: 2 }} className="hide-mobile">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              style={{
                padding: "6px 12px",
                borderRadius: 999,
                fontSize: 12,
                fontWeight: 600,
                textDecoration: "none",
                transition: "all 0.2s",
                background: isActive(link.href) ? "rgba(99,102,241,0.2)" : "transparent",
                color: isActive(link.href) ? "#38bdf8" : "#94a3b8",
                border: isActive(link.href) ? "1px solid rgba(56,189,248,0.3)" : "1px solid transparent",
              }}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Actions */}
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
          <Link
            href="/analysis/new"
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
              padding: "7px 16px",
              borderRadius: 999,
              background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              color: "#fff",
              fontSize: 12,
              fontWeight: 700,
              textDecoration: "none",
              boxShadow: "0 0 16px rgba(99,102,241,0.4)",
            }}
            className="hide-mobile"
          >
            <Zap style={{ width: 14, height: 14 }} /> Dispatch AI
          </Link>

          {mounted && (
            <button
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              style={{ width: 34, height: 34, borderRadius: "50%", background: "rgba(30,41,59,0.5)", border: "1px solid rgba(99,102,241,0.2)", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", color: "#94a3b8" }}
            >
              {theme === "dark" ? <Sun style={{ width: 15, height: 15 }} /> : <Moon style={{ width: 15, height: 15 }} />}
            </button>
          )}

          <button onClick={() => setMobileOpen(!mobileOpen)} style={{ width: 34, height: 34, borderRadius: 8, background: "rgba(30,41,59,0.5)", border: "1px solid rgba(99,102,241,0.2)", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", color: "#94a3b8" }} className="show-mobile">
            {mobileOpen ? <X style={{ width: 18, height: 18 }} /> : <Menu style={{ width: 18, height: 18 }} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileOpen && (
        <div style={{ background: "rgba(2,8,23,0.95)", backdropFilter: "blur(20px)", borderRadius: 20, border: "1px solid rgba(99,102,241,0.2)", marginTop: 8, padding: "16px" }}>
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href} onClick={() => setMobileOpen(false)} style={{ display: "block", padding: "8px 12px", borderRadius: 8, fontSize: 13, fontWeight: 500, textDecoration: "none", color: isActive(link.href) ? "#a5b4fc" : "#94a3b8" }}>
              {link.label}
            </Link>
          ))}
        </div>
      )}

      <style>{`
        @media (max-width: 1024px) { .hide-mobile { display: none !important; } }
        @media (min-width: 1025px) { .show-mobile { display: none !important; } }
      `}</style>
    </header>
  );
}
