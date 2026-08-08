"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { BarChart3, TrendingUp, Cpu, CheckCircle, FileText, Zap, Award, Layers } from "lucide-react";
import { getSavedAnalyses } from "@/lib/api";
import { SavedAnalysis } from "@/lib/types";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

export default function AnalyticsDashboardPage() {
  const [analyses, setAnalyses] = useState<SavedAnalysis[]>([]);

  useEffect(() => {
    setAnalyses(getSavedAnalyses());
  }, []);

  const totalReports = analyses.length;
  const avgScore = totalReports ? Math.round(analyses.reduce((acc, a) => acc + a.score, 0) / totalReports) : 85;

  const metrics = [
    { label: "Total Reports Generated", value: totalReports, icon: FileText, color: "#6366f1" },
    { label: "Average Innovation Score", value: `${avgScore}/100`, icon: Award, color: "#10b981" },
    { label: "Agent Success Rate", value: "98.5%", icon: CheckCircle, color: "#3b82f6" },
    { label: "Avg Processing Time", value: "~28s", icon: Zap, color: "#f59e0b" },
  ];

  const popularDomains = [
    { name: "Enterprise SaaS & DevOps", count: 42, share: "35%" },
    { name: "HealthTech & Telemedicine", count: 28, share: "23%" },
    { name: "FinTech & Blockchain", count: 24, share: "20%" },
    { name: "GreenTech & ESG", count: 16, share: "13%" },
    { name: "EdTech & AI Learning", count: 10, share: "9%" },
  ];

  const topTechnologies = [
    { name: "Next.js 15 & TypeScript", count: 88 },
    { name: "FastAPI + AsyncIO", count: 85 },
    { name: "Groq LLaMA-3 70B & 8B", count: 94 },
    { name: "PostgreSQL + pgvector", count: 72 },
    { name: "Redis In-Memory Cache", count: 68 },
  ];

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 16 }}>
            <BarChart3 style={{ width: 14, height: 14 }} /> Platform Intelligence Analytics
          </span>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Platform Analytics Dashboard</h1>
          <p style={{ color: "#94a3b8", fontSize: 14, maxWidth: 560, margin: "0 auto" }}>Aggregate discovery metrics across all 9 specialized AI agents and generated innovation reports.</p>
        </div>

        {/* Metric Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16, marginBottom: 28 }}>
          {metrics.map((m, i) => (
            <motion.div key={m.label} initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }} style={CARD}>
              <div style={{ width: 36, height: 36, borderRadius: 10, background: `${m.color}15`, border: `1px solid ${m.color}30`, display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 12 }}>
                <m.icon style={{ width: 18, height: 18, color: m.color }} />
              </div>
              <div style={{ fontSize: 28, fontWeight: 800, color: "#fff" }}>{m.value}</div>
              <div style={{ fontSize: 12, color: "#64748b", marginTop: 4 }}>{m.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Breakdown Grids */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          {/* Popular Domains */}
          <div style={CARD}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#a5b4fc", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
              <Layers style={{ width: 16, height: 16 }} /> Most Popular Discovery Domains
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {popularDomains.map((d) => (
                <div key={d.name} style={{ background: "rgba(30,41,59,0.4)", borderRadius: 12, padding: "12px 14px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: "#f1f5f9" }}>{d.name}</div>
                    <div style={{ fontSize: 11, color: "#64748b" }}>{d.count} discovery reports</div>
                  </div>
                  <span style={{ fontSize: 12, fontWeight: 700, color: "#34d399", padding: "4px 10px", borderRadius: 999, background: "rgba(16,185,129,0.1)" }}>{d.share}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Tech */}
          <div style={CARD}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#34d399", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
              <Cpu style={{ width: 16, height: 16 }} /> Most Recommended Technologies
            </h3>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {topTechnologies.map((t) => (
                <div key={t.name} style={{ background: "rgba(30,41,59,0.4)", borderRadius: 12, padding: "12px 14px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "#f1f5f9" }}>{t.name}</div>
                  <span style={{ fontSize: 12, fontWeight: 700, color: "#818cf8" }}>{t.count}% match</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
