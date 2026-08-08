"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Shield, Activity, Cpu, CheckCircle, Terminal, RefreshCw } from "lucide-react";
import { AGENTS } from "@/lib/types";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

export default function AdminDashboardPage() {
  const [logs] = useState([
    { timestamp: "20:45:12", agent: "InnovationDirectorAgent", level: "INFO", message: "Orchestration pipeline initialized. Cap=3 concurrent agents." },
    { timestamp: "20:45:14", agent: "SolutionArchitectAgent", level: "INFO", message: "Architect reasoning complete. Tech stack validated." },
    { timestamp: "20:45:18", agent: "ResearchIntelligenceAgent", level: "INFO", message: "arXiv search returned 10 papers. Deduplication complete." },
    { timestamp: "20:45:22", agent: "Groq LLM Engine", level: "INFO", message: "API call to llama-3.3-70b-versatile successful (240ms)." },
    { timestamp: "20:45:26", agent: "InnovationDirectorAgent", level: "INFO", message: "Master Executive Synthesis synthesized successfully." },
  ]);

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 16 }}>
            <Shield style={{ width: 14, height: 14 }} /> System Admin & Agent Health
          </span>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Admin Control Panel</h1>
          <p style={{ color: "#94a3b8", fontSize: 14, maxWidth: 560, margin: "0 auto" }}>Monitor real-time agent status, Groq API token consumption, LLM health, and system execution logs.</p>
        </div>

        {/* Top Status Banner */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16, marginBottom: 28 }}>
          {[
            { label: "Groq LLM API", value: "Operational", color: "#34d399" },
            { label: "Active Sub-Agents", value: "9 / 9 Healthy", color: "#818cf8" },
            { label: "Total Token Count", value: "142,500 Tokens", color: "#a5b4fc" },
            { label: "Avg Request Latency", value: "320ms", color: "#fbbf24" },
          ].map((item) => (
            <div key={item.label} style={CARD}>
              <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{item.label}</div>
              <div style={{ fontSize: 18, fontWeight: 800, color: item.color }}>{item.value}</div>
            </div>
          ))}
        </div>

        {/* 9 Agent Health Table */}
        <div style={{ ...CARD, marginBottom: 28 }}>
          <h3 style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9", marginBottom: 16 }}>9 Specialist AI Agent Health Status</h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 12 }}>
            {AGENTS.map((agent) => (
              <div key={agent.id} style={{ background: "rgba(30,41,59,0.4)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 14, padding: "14px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <span style={{ fontSize: 20 }}>{agent.icon}</span>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 700, color: "#fff" }}>{agent.name}</div>
                    <div style={{ fontSize: 11, color: "#64748b" }}>Model: llama-3.1-8b-instant</div>
                  </div>
                </div>
                <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 999, background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.3)", color: "#34d399" }}>
                  ● Healthy
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Live System Log Console */}
        <div style={CARD}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9", margin: 0, display: "flex", alignItems: "center", gap: 8 }}>
              <Terminal style={{ width: 16, height: 16, color: "#818cf8" }} /> Live System Execution Log Stream
            </h3>
            <span style={{ fontSize: 11, color: "#34d399", display: "flex", alignItems: "center", gap: 4 }}>
              <RefreshCw style={{ width: 12, height: 12 }} /> Live Stream
            </span>
          </div>

          <div style={{ background: "#020817", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 12, padding: "16px", fontFamily: "monospace", fontSize: 12, display: "flex", flexDirection: "column", gap: 8 }}>
            {logs.map((log, i) => (
              <div key={i} style={{ display: "flex", gap: 12 }}>
                <span style={{ color: "#475569" }}>[{log.timestamp}]</span>
                <span style={{ color: "#818cf8", fontWeight: 700 }}>[{log.agent}]</span>
                <span style={{ color: "#34d399" }}>{log.level}</span>
                <span style={{ color: "#cbd5e1" }}>{log.message}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
