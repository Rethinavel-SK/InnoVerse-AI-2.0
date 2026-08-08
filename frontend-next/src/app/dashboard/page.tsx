"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Zap, TrendingUp, Clock, FileText,
  Plus, Trash2, ExternalLink, Search, Activity, ArrowLeftRight, Copy
} from "lucide-react";
import { getSavedAnalyses, deleteAnalysis, saveAnalysis } from "@/lib/api";
import { SavedAnalysis } from "@/lib/types";
import { formatDate, getScoreColor, truncate } from "@/lib/utils";
import { toast } from "@/components/ui/toaster";

const S = {
  page: { minHeight: "100vh", padding: "2rem 1rem 4rem" } as React.CSSProperties,
  container: { maxWidth: 1100, margin: "0 auto" } as React.CSSProperties,
  header: { display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 16, marginBottom: 40 } as React.CSSProperties,
  title: { fontSize: "clamp(1.6rem,4vw,2.2rem)", fontWeight: 800, color: "#f1f5f9", margin: 0 } as React.CSSProperties,
  subtitle: { color: "#64748b", fontSize: 14, marginTop: 4 } as React.CSSProperties,
  statsGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16, marginBottom: 40 } as React.CSSProperties,
  card: { background: "rgba(15,23,42,0.7)", backdropFilter: "blur(16px)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 20, padding: 20 } as React.CSSProperties,
};

export default function DashboardPage() {
  const [analyses, setAnalyses] = useState<SavedAnalysis[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => { setAnalyses(getSavedAnalyses()); }, []);

  const filtered = analyses.filter((a) =>
    a.problem_statement.toLowerCase().includes(search.toLowerCase())
  );

  const handleDelete = (id: string) => {
    deleteAnalysis(id);
    setAnalyses(getSavedAnalyses());
    toast({ title: "Report deleted" });
  };

  const handleDuplicate = (item: SavedAnalysis) => {
    const newId = Date.now().toString();
    saveAnalysis({
      ...item,
      id: newId,
      created_at: new Date().toISOString(),
      problem_statement: `${item.problem_statement} (Copy)`,
    });
    setAnalyses(getSavedAnalyses());
    toast({ title: "Report duplicated!", variant: "success" });
  };

  const avgScore = analyses.length
    ? Math.round(analyses.reduce((acc, a) => acc + a.score, 0) / analyses.length)
    : 0;

  const goCount = analyses.filter((a) =>
    a.recommendation?.toUpperCase().includes("GO") && !a.recommendation?.toUpperCase().includes("NO")
  ).length;

  const stats = [
    { label: "Total Analyses", value: analyses.length, icon: FileText, gradient: "linear-gradient(135deg,#6366f1,#818cf8)" },
    { label: "Average Score", value: analyses.length ? `${avgScore}/100` : "—", icon: TrendingUp, gradient: "linear-gradient(135deg,#10b981,#34d399)" },
    { label: "Latest", value: analyses[0] ? new Date(analyses[0].created_at).toLocaleDateString() : "—", icon: Clock, gradient: "linear-gradient(135deg,#8b5cf6,#a78bfa)" },
    { label: "GO Reports", value: goCount, icon: Activity, gradient: "linear-gradient(135deg,#f59e0b,#fbbf24)" },
  ];

  return (
    <div style={S.page}>
      <div style={S.container}>
        {/* Header */}
        <div style={S.header}>
          <div>
            <h1 style={S.title}>Dashboard</h1>
            <p style={S.subtitle}>Your innovation discovery & report management hub</p>
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <Link href="/compare" style={{
              display: "inline-flex", alignItems: "center", gap: 8,
              padding: "10px 16px", borderRadius: 12,
              background: "rgba(30,41,59,0.7)", border: "1px solid rgba(99,102,241,0.25)",
              color: "#a5b4fc", fontWeight: 600, fontSize: 13, textDecoration: "none",
            }}>
              <ArrowLeftRight style={{ width: 14, height: 14 }} /> Compare Reports
            </Link>
            <Link href="/analysis/new" style={{
              display: "inline-flex", alignItems: "center", gap: 8,
              padding: "10px 20px", borderRadius: 12,
              background: "linear-gradient(135deg,#6366f1,#8b5cf6)",
              color: "#fff", fontWeight: 600, fontSize: 14, textDecoration: "none",
              boxShadow: "0 4px 16px rgba(99,102,241,0.35)",
            }}>
              <Plus style={{ width: 16, height: 16 }} /> New Analysis
            </Link>
          </div>
        </div>

        {/* Stats */}
        <div style={S.statsGrid}>
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.08 }}
              style={S.card}
            >
              <div style={{
                width: 36, height: 36, borderRadius: 10,
                background: s.gradient,
                display: "flex", alignItems: "center", justifyContent: "center",
                marginBottom: 14,
              }}>
                <s.icon style={{ width: 16, height: 16, color: "#fff" }} />
              </div>
              <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "#f1f5f9" }}>{s.value}</div>
              <div style={{ fontSize: 12, color: "#64748b", marginTop: 4 }}>{s.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Search */}
        <div style={{ position: "relative", marginBottom: 24 }}>
          <Search style={{ position: "absolute", left: 16, top: "50%", transform: "translateY(-50%)", width: 16, height: 16, color: "#64748b" }} />
          <input
            type="text"
            placeholder="Search reports by keyword, domain, or technology..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{
              width: "100%", padding: "12px 16px 12px 44px", borderRadius: 12,
              background: "rgba(15,23,42,0.6)", border: "1px solid rgba(99,102,241,0.15)",
              color: "#fff", fontSize: 14, outline: "none",
            }}
          />
        </div>

        {/* Reports Grid */}
        {filtered.length > 0 ? (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: 16 }}>
            {filtered.map((item) => (
              <div key={item.id} style={{ ...S.card, display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
                <div>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
                    <span style={{ fontSize: 12, color: "#64748b" }}>{formatDate(item.created_at)}</span>
                    <span style={{ fontSize: 12, fontWeight: 700, padding: "2px 8px", borderRadius: 999, background: "rgba(99,102,241,0.12)", color: "#a5b4fc" }}>
                      Score: {item.score}
                    </span>
                  </div>
                  <h3 style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9", marginBottom: 10, lineHeight: 1.4 }}>
                    {truncate(item.problem_statement, 90)}
                  </h3>
                </div>

                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: 20, paddingTop: 12, borderTop: "1px solid rgba(99,102,241,0.1)" }}>
                  <div style={{ display: "flex", gap: 6 }}>
                    <button onClick={() => handleDuplicate(item)} style={{ background: "transparent", border: "none", color: "#64748b", cursor: "pointer", padding: 4 }} title="Duplicate">
                      <Copy style={{ width: 14, height: 14 }} />
                    </button>
                    <button onClick={() => handleDelete(item.id)} style={{ background: "transparent", border: "none", color: "#f87171", cursor: "pointer", padding: 4 }} title="Delete">
                      <Trash2 style={{ width: 14, height: 14 }} />
                    </button>
                  </div>
                  <Link href={`/analysis/${item.id}`} style={{ display: "inline-flex", alignItems: "center", gap: 4, color: "#818cf8", fontSize: 13, fontWeight: 600, textDecoration: "none" }}>
                    View Report <ExternalLink style={{ width: 13, height: 13 }} />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ ...S.card, textAlign: "center", padding: "60px 20px" }}>
            <FileText style={{ width: 48, height: 48, color: "#475569", margin: "0 auto 12px" }} />
            <h3 style={{ fontSize: 16, fontWeight: 700, color: "#fff", marginBottom: 6 }}>No Reports Found</h3>
            <p style={{ color: "#64748b", fontSize: 13, marginBottom: 20 }}>Start a new analysis to trigger the Innovation Director orchestrator.</p>
            <Link href="/analysis/new" style={{ padding: "10px 20px", borderRadius: 12, background: "#6366f1", color: "#fff", fontSize: 13, fontWeight: 600, textDecoration: "none" }}>
              Start New Analysis
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
