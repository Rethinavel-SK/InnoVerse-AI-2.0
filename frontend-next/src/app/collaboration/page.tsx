"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Network, Play, RefreshCw, CheckCircle, Brain, ArrowRight, Layers, MessageSquare, Terminal } from "lucide-react";
import { executeCollaboration } from "@/lib/api";
import { InterAgentMessage, AGENTS } from "@/lib/types";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

export default function AgentCollaborationPage() {
  const [problem, setProblem] = useState("Build an AI-powered automated code security review platform for enterprise DevOps teams.");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<InterAgentMessage[]>([]);

  const handleRunCollaboration = async () => {
    if (!problem.trim()) return;
    setLoading(true);
    try {
      const logs = await executeCollaboration(problem);
      setMessages(logs);
    } catch {
      // Fallback local simulation logs
      setMessages([
        { sender_id: "research", target_id: "patent", topic: "Prior Art Discovery", content: "Research Agent found 10 AST vulnerability papers. Forwarding algorithms to Patent Agent.", timestamp: "21:50:10" },
        { sender_id: "market", target_id: "business_strategy", topic: "Market TAM & Segment", content: "Market Agent identified Enterprise B2B SaaS demand. Business Strategy setting tiered seat license.", timestamp: "21:50:11" },
        { sender_id: "solution_architect", target_id: "risk_assessment", topic: "Architecture & Complexity", content: "Solution Architect selected Microservices. Risk Agent added RBAC security requirements.", timestamp: "21:50:12" },
        { sender_id: "risk_assessment", target_id: "mvp_planner", topic: "Risk Mitigations -> Roadmap", content: "Risk Agent recommended phased rollout. MVP Planner reducing Phase 1 to 12 weeks.", timestamp: "21:50:13" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleRunCollaboration();
  }, []);

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 16 }}>
            <Network style={{ width: 14, height: 14 }} /> Autonomous Inter-Agent Collaboration Layer
          </span>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Agent-to-Agent Mesh Communication</h1>
          <p style={{ color: "#94a3b8", fontSize: 14, maxWidth: 620, margin: "0 auto" }}>Specialist agents request context, resolve dependencies, and refine outputs before submitting master synthesis to Innovation Director.</p>
        </div>

        {/* Action Bar */}
        <div style={{ ...CARD, marginBottom: 28, padding: "20px 24px" }}>
          <div style={{ display: "flex", gap: 12 }}>
            <input
              type="text"
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              placeholder="Enter business problem statement to trigger collaboration..."
              style={{ flex: 1, background: "rgba(30,41,59,0.5)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 12, padding: "10px 14px", fontSize: 13, color: "#fff", outline: "none" }}
            />
            <button onClick={handleRunCollaboration} disabled={loading} style={{ padding: "10px 20px", borderRadius: 12, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", fontSize: 13, fontWeight: 700, border: "none", cursor: "pointer", display: "flex", alignItems: "center", gap: 8 }}>
              {loading ? <RefreshCw className="animate-spin" style={{ width: 16, height: 16 }} /> : <Play style={{ width: 16, height: 16 }} />}
              Trigger Collaboration Mesh
            </button>
          </div>
        </div>

        {/* Live Collaboration Animated Graph & Logs Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
          {/* Animated Collaboration Visualizer */}
          <div style={CARD}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#fff", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
              <Layers style={{ width: 16, height: 16, color: "#6366f1" }} /> Inter-Agent Communication Mesh
            </h3>

            <div style={{ background: "#020817", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 16, padding: 24, textAlign: "center" }}>
              {/* Innovation Director Node */}
              <div style={{ width: 64, height: 64, borderRadius: 16, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 20px", boxShadow: "0 0 30px rgba(99,102,241,0.5)" }}>
                <Brain style={{ width: 32, height: 32, color: "#fff" }} />
              </div>
              <div style={{ fontSize: 13, fontWeight: 800, color: "#fff", marginBottom: 20 }}>Innovation Director (Orchestrator)</div>

              {/* Connected Agent Pairs */}
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {[
                  { from: "Research Agent", to: "Patent Agent", color: "#3b82f6" },
                  { from: "Market Agent", to: "Business Strategy", color: "#10b981" },
                  { from: "Solution Architect", to: "Risk Assessment", color: "#8b5cf6" },
                  { from: "Risk Assessment", to: "MVP Planner", color: "#ec4899" },
                ].map((pair, idx) => (
                  <motion.div key={idx} animate={{ scale: [1, 1.02, 1] }} transition={{ duration: 1.5, repeat: Infinity, delay: idx * 0.3 }} style={{ background: "rgba(30,41,59,0.5)", border: `1px solid ${pair.color}40`, borderRadius: 12, padding: "10px 14px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <span style={{ fontSize: 12, fontWeight: 700, color: pair.color }}>{pair.from}</span>
                    <ArrowRight style={{ width: 14, height: 14, color: pair.color }} />
                    <span style={{ fontSize: 12, fontWeight: 700, color: "#fff" }}>{pair.to}</span>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>

          {/* Real-Time Message Exchange Transcript */}
          <div style={CARD}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#fff", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
              <MessageSquare style={{ width: 16, height: 16, color: "#34d399" }} /> Inter-Agent Message Log Stream
            </h3>

            <div style={{ display: "flex", flexDirection: "column", gap: 10, height: 380, overflowY: "auto" }}>
              {messages.map((msg, idx) => (
                <div key={idx} style={{ background: "rgba(30,41,59,0.4)", border: "1px solid rgba(99,102,241,0.15)", borderRadius: 14, padding: "12px 14px" }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 4 }}>
                    <span style={{ fontSize: 12, fontWeight: 700, color: "#818cf8" }}>
                      {msg.sender_id.toUpperCase()} ➔ {msg.target_id.toUpperCase()}
                    </span>
                    <span style={{ fontSize: 10, color: "#64748b" }}>{msg.timestamp}</span>
                  </div>
                  <div style={{ fontSize: 11, fontWeight: 700, color: "#34d399", marginBottom: 4 }}>Topic: {msg.topic}</div>
                  <p style={{ fontSize: 12, color: "#cbd5e1", margin: 0, lineHeight: 1.5 }}>{msg.content}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
