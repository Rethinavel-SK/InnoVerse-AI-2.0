"use client";

import React from "react";
import { MessageSquare, AlertTriangle, ShieldCheck, Scale } from "lucide-react";

interface DebatePanelProps {
  debateTrace?: any[];
  conflicts?: any[];
}

export function DebatePanel({ debateTrace = [], conflicts = [] }: DebatePanelProps) {
  const allDebates = [...debateTrace, ...conflicts];

  if (allDebates.length === 0) {
    return (
      <div className="glass-panel" style={{ borderRadius: 20, padding: 24, textAlign: "center" }}>
        <ShieldCheck style={{ width: 36, height: 36, color: "#34d399", margin: "0 auto 12px" }} />
        <h3 style={{ color: "#fff", fontSize: 16, fontWeight: 700, margin: 0 }}>Agent Consensus Reached</h3>
        <p style={{ color: "#94a3b8", fontSize: 13, margin: "6px 0 0" }}>
          All 11 specialist agents aligned on implementation strategy without major conflicts.
        </p>
      </div>
    );
  }

  return (
    <div className="glass-panel" style={{ borderRadius: 20, padding: 24 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
        <Scale style={{ width: 22, height: 22, color: "#f59e0b" }} />
        <div>
          <h3 style={{ fontSize: 18, fontWeight: 800, color: "#fff", margin: 0 }}>
            Multi-Agent Debate & Conflict Resolution
          </h3>
          <p style={{ color: "#94a3b8", fontSize: 13, margin: "2px 0 0" }}>
            Innovation Director reasoning traces across opposing agent recommendations
          </p>
        </div>
      </div>

      <div style={{ display: "grid", gap: 16 }}>
        {allDebates.map((item, idx) => {
          const topic = item.topic || item.conflict_description || "Agent Disagreement";
          const agents = item.agents_involved || [];
          const resolution = item.resolution || "Resolved by Director";
          const reasoning = item.reasoning || "";

          return (
            <div
              key={idx}
              style={{
                background: "rgba(15,23,42,0.6)",
                border: "1px solid rgba(245,158,11,0.3)",
                borderRadius: 14,
                padding: 16,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                <AlertTriangle style={{ width: 16, height: 16, color: "#f59e0b" }} />
                <span style={{ color: "#fbbf24", fontWeight: 700, fontSize: 14 }}>{topic}</span>
              </div>

              <div style={{ display: "flex", gap: 6, marginBottom: 12, flexWrap: "wrap" }}>
                {agents.map((ag: string) => (
                  <span
                    key={ag}
                    style={{
                      background: "rgba(99,102,241,0.2)",
                      border: "1px solid rgba(99,102,241,0.4)",
                      color: "#a5b4fc",
                      fontSize: 11,
                      fontWeight: 600,
                      padding: "2px 8px",
                      borderRadius: 999,
                    }}
                  >
                    {ag.replace("_", " ")}
                  </span>
                ))}
              </div>

              <div style={{ background: "rgba(255,255,255,0.03)", borderRadius: 8, padding: 12 }}>
                <div style={{ fontSize: 12, color: "#94a3b8", textTransform: "uppercase", fontWeight: 700, marginBottom: 4 }}>
                  Director Resolution
                </div>
                <div style={{ fontSize: 13, color: "#f1f5f9", lineHeight: 1.5 }}>
                  {resolution}
                </div>
                {reasoning && (
                  <div style={{ fontSize: 12, color: "#cbd5e1", marginTop: 6, fontStyle: "italic" }}>
                    Reasoning: {reasoning}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
