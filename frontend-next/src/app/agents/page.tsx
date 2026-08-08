"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, CheckCircle, X, ChevronRight } from "lucide-react";
import { AGENTS, AgentInfo } from "@/lib/types";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.8)",
  backdropFilter: "blur(16px)",
  WebkitBackdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
};

export default function AgentsDashboardPage() {
  const [selected, setSelected] = useState<AgentInfo | null>(null);

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "3rem" }}>
          <motion.span
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            style={{
              display: "inline-flex", alignItems: "center", gap: 8,
              padding: "6px 16px", borderRadius: 999,
              background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)",
              color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 20,
            }}
          >
            <Brain style={{ width: 14, height: 14 }} />
            Specialist AI Agent Registry
          </motion.span>
          <h1 style={{ fontSize: "clamp(1.8rem,4vw,2.6rem)", fontWeight: 800, color: "#f1f5f9", marginBottom: 12 }}>
            AI Agent Dashboard
          </h1>
          <p style={{ color: "#94a3b8", maxWidth: 560, margin: "0 auto", lineHeight: 1.7 }}>
            9 specialized AI agents working under the Innovation Director orchestrator.
            Each agent handles a distinct domain of innovation analysis.
          </p>
        </div>

        {/* Innovation Director Feature Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="animated-border"
          style={{ borderRadius: 24, padding: "28px 32px", marginBottom: 32, display: "flex", alignItems: "center", gap: 24, flexWrap: "wrap" }}
        >
          <motion.div
            animate={{ boxShadow: ["0 0 0 0 rgba(99,102,241,0.4)", "0 0 0 18px rgba(99,102,241,0)", "0 0 0 0 rgba(99,102,241,0)"] }}
            transition={{ duration: 2, repeat: Infinity }}
            style={{ width: 64, height: 64, borderRadius: 18, background: "linear-gradient(135deg,#6366f1,#8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}
          >
            <Brain style={{ width: 32, height: 32, color: "#fff" }} />
          </motion.div>
          <div style={{ flex: 1 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 6, flexWrap: "wrap" }}>
              <h2 style={{ fontSize: 22, fontWeight: 800, color: "#f1f5f9", margin: 0 }}>Innovation Director</h2>
              <span style={{ padding: "3px 12px", borderRadius: 999, background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.3)", color: "#a5b4fc", fontSize: 12, fontWeight: 600 }}>
                Master Orchestrator
              </span>
            </div>
            <p style={{ color: "#94a3b8", fontSize: 14, lineHeight: 1.6, margin: 0 }}>
              Coordinates all 9 specialist agents concurrently. Validates responses, resolves conflicts,
              calculates weighted scores, and synthesizes a comprehensive master innovation report.
            </p>
          </div>
          <div style={{ textAlign: "right", flexShrink: 0 }}>
            <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>Orchestrates</div>
            <div className="gradient-text" style={{ fontSize: 32, fontWeight: 800 }}>9 Agents</div>
          </div>
        </motion.div>

        {/* Agent Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
          {AGENTS.map((agent, i) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.07 }}
              onClick={() => setSelected(agent)}
              style={{ ...CARD, padding: "20px", cursor: "pointer", transition: "border-color 0.2s, box-shadow 0.2s" }}
              whileHover={{ boxShadow: "0 8px 32px rgba(99,102,241,0.15)" }}
            >
              {/* Agent Header */}
              <div style={{ display: "flex", alignItems: "flex-start", gap: 14, marginBottom: 16 }}>
                <div style={{
                  width: 48, height: 48, borderRadius: 14, fontSize: 22,
                  display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
                  background: `${agent.color}15`, border: `1px solid ${agent.color}30`,
                }}>
                  {agent.icon}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8 }}>
                    <h3 style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>{agent.name}</h3>
                    <span style={{ padding: "2px 10px", borderRadius: 999, fontSize: 11, fontWeight: 600, background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.25)", color: "#34d399", flexShrink: 0 }}>
                      Active
                    </span>
                  </div>
                  <p style={{ fontSize: 12, color: "#64748b", margin: "4px 0 0" }}>{agent.description}</p>
                </div>
              </div>

              {/* Stats Row */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 14 }}>
                {[
                  { label: "Confidence", value: "High" },
                  { label: "Avg Time", value: "~30s" },
                ].map(({ label, value }) => (
                  <div key={label} style={{ background: "rgba(30,41,59,0.5)", borderRadius: 10, padding: "8px 12px", textAlign: "center" }}>
                    <div style={{ fontSize: 11, color: "#475569", marginBottom: 3 }}>{label}</div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0" }}>{value}</div>
                  </div>
                ))}
              </div>

              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span style={{ fontSize: 11, color: "#475569" }}>Agent #{String(i + 1).padStart(2, "0")}</span>
                <ChevronRight style={{ width: 14, height: 14, color: "#6366f1" }} />
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Detail Modal */}
      <AnimatePresence>
        {selected && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelected(null)}
            style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.6)", backdropFilter: "blur(8px)", zIndex: 2000, display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              style={{ background: "#0f172a", border: "1px solid rgba(99,102,241,0.25)", borderRadius: 24, padding: 28, maxWidth: 480, width: "100%" }}
            >
              {/* Modal Header */}
              <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 24 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                  <div style={{ width: 56, height: 56, borderRadius: 16, fontSize: 28, display: "flex", alignItems: "center", justifyContent: "center", background: `${selected.color}15`, border: `1px solid ${selected.color}30` }}>
                    {selected.icon}
                  </div>
                  <div>
                    <h2 style={{ fontSize: 18, fontWeight: 800, color: "#f1f5f9", margin: "0 0 4px" }}>{selected.name}</h2>
                    <p style={{ fontSize: 13, color: "#64748b", margin: 0 }}>{selected.description}</p>
                  </div>
                </div>
                <button onClick={() => setSelected(null)} style={{ width: 34, height: 34, borderRadius: 10, background: "rgba(30,41,59,0.6)", border: "none", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", color: "#94a3b8" }}>
                  <X style={{ width: 16, height: 16 }} />
                </button>
              </div>

              {/* Stats */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 20 }}>
                {[
                  { label: "Status", value: "Active", color: "#34d399" },
                  { label: "Avg. Execution", value: "~25–45s", color: "#818cf8" },
                  { label: "Confidence", value: "High", color: "#a5b4fc" },
                  { label: "Agent ID", value: selected.id.replace(/_/g, " "), color: "#64748b" },
                ].map(({ label, value, color }) => (
                  <div key={label} style={{ background: "rgba(30,41,59,0.5)", borderRadius: 12, padding: "12px 14px" }}>
                    <div style={{ fontSize: 11, color: "#475569", marginBottom: 4 }}>{label}</div>
                    <div style={{ fontSize: 13, fontWeight: 600, color }}>{value}</div>
                  </div>
                ))}
              </div>

              {/* Capabilities */}
              <div style={{ background: "rgba(30,41,59,0.3)", borderRadius: 14, padding: "16px 18px" }}>
                <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 12 }}>Agent Capabilities</div>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {getCapabilities(selected.id).map((cap, i) => (
                    <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13, color: "#cbd5e1" }}>
                      <CheckCircle style={{ width: 14, height: 14, color: "#34d399", flexShrink: 0 }} />
                      {cap}
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function getCapabilities(agentId: string): string[] {
  const caps: Record<string, string[]> = {
    solution_architect: ["Technical architecture design", "Tech stack selection", "Scalability planning", "Cost estimation"],
    business_strategy: ["Business model generation", "SWOT analysis", "GTM strategy", "Revenue stream modeling"],
    research: ["arXiv & Semantic Scholar search", "Paper summarization", "Methodology extraction", "Research gap analysis"],
    patent_analysis: ["USPTO/EPO/WIPO search", "Novelty scoring", "Prior art detection", "Whitespace identification"],
    market_analysis: ["TAM/SAM/SOM sizing", "Competitor mapping", "Customer persona creation", "Market entry analysis"],
    trend_analysis: ["Technology trend mapping", "Hype cycle positioning", "Adoption lifecycle analysis", "Regulatory monitoring"],
    risk_assessment: ["Technical risk identification", "Financial risk scoring", "Legal & security risk", "Mitigation strategies"],
    sustainability: ["ESG compliance scoring", "Carbon footprint estimation", "SDG alignment mapping", "Green recommendations"],
    mvp_roadmap: ["MVP feature prioritization", "Timeline planning", "Sprint roadmap", "Budget estimation"],
  };
  return caps[agentId] ?? ["Advanced AI analysis", "Structured JSON output", "Confidence scoring"];
}
