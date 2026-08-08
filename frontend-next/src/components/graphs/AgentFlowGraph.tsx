"use client";

import { motion } from "framer-motion";
import { Brain } from "lucide-react";
import { AGENTS } from "@/lib/types";

interface AgentFlowGraphProps {
  activeAgentId?: string;
  completedAgentIds?: string[];
}

export function AgentFlowGraph({ activeAgentId, completedAgentIds = [] }: AgentFlowGraphProps) {
  return (
    <div style={{ background: "rgba(15,23,42,0.8)", borderRadius: 20, border: "1px solid rgba(99,102,241,0.15)", padding: 24, textAlign: "center" }}>
      {/* Central Innovation Director Node */}
      <div style={{ display: "inline-block", position: "relative", marginBottom: 32 }}>
        <motion.div
          animate={{ boxShadow: ["0 0 20px rgba(99,102,241,0.3)", "0 0 40px rgba(99,102,241,0.6)", "0 0 20px rgba(99,102,241,0.3)"] }}
          transition={{ duration: 2, repeat: Infinity }}
          style={{
            width: 72, height: 72, borderRadius: 20,
            background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
            display: "flex", alignItems: "center", justifyContent: "center",
            margin: "0 auto 8px",
            boxShadow: "0 8px 32px rgba(99,102,241,0.4)",
          }}
        >
          <Brain style={{ width: 36, height: 36, color: "#fff" }} />
        </motion.div>
        <div style={{ fontSize: 15, fontWeight: 800, color: "#f1f5f9" }}>Innovation Director</div>
        <div style={{ fontSize: 11, color: "#818cf8" }}>Master Orchestrator</div>
      </div>

      {/* Grid of 9 Sub-agents */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: 12 }}>
        {AGENTS.map((agent) => {
          const isActive = activeAgentId === agent.id;
          const isDone = completedAgentIds.includes(agent.id);

          return (
            <motion.div
              key={agent.id}
              animate={isActive ? { scale: [1, 1.05, 1], borderColor: "#6366f1" } : {}}
              transition={{ duration: 1, repeat: isActive ? Infinity : 0 }}
              style={{
                background: isDone
                  ? "rgba(16,185,129,0.08)"
                  : isActive
                  ? "rgba(99,102,241,0.12)"
                  : "rgba(30,41,59,0.5)",
                border: isDone
                  ? "1px solid rgba(16,185,129,0.3)"
                  : isActive
                  ? "1px solid #6366f1"
                  : "1px solid rgba(99,102,241,0.15)",
                borderRadius: 14,
                padding: "12px 8px",
                transition: "all 0.3s",
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 6 }}>{agent.icon}</div>
              <div style={{ fontSize: 11, fontWeight: 600, color: isDone ? "#34d399" : isActive ? "#a5b4fc" : "#cbd5e1" }}>
                {agent.name}
              </div>
              <div style={{ fontSize: 10, color: isDone ? "#34d399" : isActive ? "#818cf8" : "#64748b", marginTop: 4 }}>
                {isDone ? "✓ Completed" : isActive ? "⟳ Processing" : "Queued"}
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
