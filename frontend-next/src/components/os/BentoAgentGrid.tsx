"use client";

import { motion } from "framer-motion";
import { AGENTS } from "@/lib/types";
import { CheckCircle2, RefreshCw, Cpu, Activity, Clock } from "lucide-react";

const agentColorMap: Record<string, string> = {
  solution_architect: "#6366f1",
  business_strategy: "#10b981",
  research: "#3b82f6",
  patent: "#06b6d4",
  market: "#8b5cf6",
  trend: "#f59e0b",
  risk_assessment: "#ef4444",
  sustainability: "#22c55e",
  mvp_planner: "#ec4899",
};

export function BentoAgentGrid() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 16 }}>
      {AGENTS.map((agent, i) => {
        const color = agentColorMap[agent.id] || "#6366f1";
        return (
          <motion.div
            key={agent.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            whileHover={{ scale: 1.02, borderColor: color }}
            className="glass-panel"
            style={{
              borderRadius: 20,
              padding: "20px",
              border: `1px solid ${color}30`,
              boxShadow: `0 8px 32px ${color}10`,
              position: "relative",
              overflow: "hidden",
            }}
          >
            {/* Top Accent Glow line */}
            <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: `linear-gradient(90deg, ${color}, transparent)` }} />

            <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 12 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                <div style={{ width: 44, height: 44, borderRadius: 14, background: `${color}15`, border: `1px solid ${color}35`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 22 }}>
                  {agent.icon}
                </div>
                <div>
                  <h4 style={{ fontSize: 14, fontWeight: 700, color: "#fff", margin: 0 }}>{agent.name}</h4>
                  <div style={{ fontSize: 11, color: color, fontWeight: 600 }}>llama-3.1-8b-instant</div>
                </div>
              </div>

              <span style={{ fontSize: 10, fontWeight: 700, padding: "3px 8px", borderRadius: 999, background: "rgba(16,185,129,0.12)", border: "1px solid rgba(16,185,129,0.3)", color: "#34d399", display: "flex", alignItems: "center", gap: 4 }}>
                <CheckCircle2 style={{ width: 10, height: 10 }} /> Ready
              </span>
            </div>

            <p style={{ fontSize: 12, color: "#94a3b8", lineHeight: 1.5, margin: "0 0 16px" }}>{agent.description}</p>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingTop: 10, borderTop: "1px solid rgba(99,102,241,0.1)", fontSize: 11, color: "#64748b" }}>
              <span style={{ display: "flex", alignItems: "center", gap: 4 }}>
                <Clock style={{ width: 12, height: 12, color }} /> Avg 240ms
              </span>
              <span style={{ fontWeight: 600, color: "#cbd5e1" }}>94% Confidence</span>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
