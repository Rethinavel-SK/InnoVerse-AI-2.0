"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { ArrowLeftRight, CheckCircle, XCircle, FileText, ChevronRight } from "lucide-react";
import { getSavedAnalyses } from "@/lib/api";
import { SavedAnalysis } from "@/lib/types";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

export default function ReportComparisonPage() {
  const [analyses, setAnalyses] = useState<SavedAnalysis[]>([]);
  const [idA, setIdA] = useState<string>("");
  const [idB, setIdB] = useState<string>("");

  useEffect(() => {
    const list = getSavedAnalyses();
    setAnalyses(list);
    if (list.length >= 2) {
      setIdA(list[0].id);
      setIdB(list[1].id);
    } else if (list.length === 1) {
      setIdA(list[0].id);
    }
  }, []);

  const reportA = analyses.find((a) => a.id === idA);
  const reportB = analyses.find((a) => a.id === idB);

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 16 }}>
            <ArrowLeftRight style={{ width: 14, height: 14 }} /> Report Comparison Matrix
          </span>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Side-by-Side Analysis</h1>
          <p style={{ color: "#94a3b8", fontSize: 14, maxWidth: 560, margin: "0 auto" }}>Select any two generated innovation reports to compare their architectures, business models, scores, and roadmaps.</p>
        </div>

        {/* Report Selectors */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 28 }}>
          <div style={CARD}>
            <label style={{ fontSize: 12, fontWeight: 700, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8, display: "block" }}>Report A (Left)</label>
            <select value={idA} onChange={(e) => setIdA(e.target.value)} style={{ width: "100%", background: "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 10, padding: "10px 12px", color: "#fff", fontSize: 13, outline: "none" }}>
              <option value="">Select a report...</option>
              {analyses.map((a) => (
                <option key={a.id} value={a.id}>{a.problem_statement.slice(0, 60)}...</option>
              ))}
            </select>
          </div>
          <div style={CARD}>
            <label style={{ fontSize: 12, fontWeight: 700, color: "#34d399", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8, display: "block" }}>Report B (Right)</label>
            <select value={idB} onChange={(e) => setIdB(e.target.value)} style={{ width: "100%", background: "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 10, padding: "10px 12px", color: "#fff", fontSize: 13, outline: "none" }}>
              <option value="">Select a report...</option>
              {analyses.map((a) => (
                <option key={a.id} value={a.id}>{a.problem_statement.slice(0, 60)}...</option>
              ))}
            </select>
          </div>
        </div>

        {/* Comparison Grid */}
        {reportA && reportB ? (
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {/* Score & Recommendation Row */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div style={CARD}>
                <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>Problem Statement A</div>
                <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9", marginBottom: 14 }}>{reportA.problem_statement}</div>
                <div style={{ display: "flex", gap: 10 }}>
                  <span style={{ fontSize: 18, fontWeight: 800, color: "#818cf8" }}>{reportA.score}/100</span>
                  <span style={{ padding: "4px 10px", borderRadius: 999, background: "rgba(16,185,129,0.1)", color: "#34d399", fontSize: 12, fontWeight: 600 }}>{reportA.recommendation}</span>
                </div>
              </div>

              <div style={CARD}>
                <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>Problem Statement B</div>
                <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9", marginBottom: 14 }}>{reportB.problem_statement}</div>
                <div style={{ display: "flex", gap: 10 }}>
                  <span style={{ fontSize: 18, fontWeight: 800, color: "#34d399" }}>{reportB.score}/100</span>
                  <span style={{ padding: "4px 10px", borderRadius: 999, background: "rgba(16,185,129,0.1)", color: "#34d399", fontSize: 12, fontWeight: 600 }}>{reportB.recommendation}</span>
                </div>
              </div>
            </div>

            {/* Architecture Comparison */}
            <div style={CARD}>
              <h3 style={{ fontSize: 14, fontWeight: 700, color: "#a5b4fc", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 16 }}>Architecture Comparison</h3>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
                <div>
                  <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>Report A Architecture</div>
                  <div style={{ fontSize: 14, fontWeight: 700, color: "#fff" }}>{reportA.report?.technical_summary?.architecture?.type ?? "Microservices"}</div>
                  <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 4 }}>Prototype Cost: {reportA.report?.technical_summary?.prototype_cost ?? "$250/mo"}</div>
                </div>
                <div>
                  <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>Report B Architecture</div>
                  <div style={{ fontSize: 14, fontWeight: 700, color: "#fff" }}>{reportB.report?.technical_summary?.architecture?.type ?? "Modular Monolith"}</div>
                  <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 4 }}>Prototype Cost: {reportB.report?.technical_summary?.prototype_cost ?? "$250/mo"}</div>
                </div>
              </div>
            </div>

            {/* Business Strategy Comparison */}
            <div style={CARD}>
              <h3 style={{ fontSize: 14, fontWeight: 700, color: "#34d399", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 16 }}>Business Strategy Comparison</h3>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
                <div>
                  <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>Report A Model</div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: "#fff" }}>{reportA.report?.business_summary?.business_model ?? "B2B SaaS"}</div>
                  <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 4 }}>TAM: {(reportA.report?.business_summary?.market_size as Record<string, string>)?.tam ?? "$4.8B"}</div>
                </div>
                <div>
                  <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>Report B Model</div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: "#fff" }}>{reportB.report?.business_summary?.business_model ?? "B2B SaaS"}</div>
                  <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 4 }}>TAM: {(reportB.report?.business_summary?.market_size as Record<string, string>)?.tam ?? "$4.8B"}</div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div style={{ ...CARD, textAlign: "center", padding: "60px 20px" }}>
            <FileText style={{ width: 48, height: 48, color: "#475569", margin: "0 auto 12px" }} />
            <p style={{ color: "#94a3b8", margin: 0 }}>Please generate at least 2 reports to compare them side-by-side.</p>
          </div>
        )}
      </div>
    </div>
  );
}
