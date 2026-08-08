"use client";

import { motion } from "framer-motion";
import { Award, Zap, Activity, FileText, CheckCircle2, ShieldCheck } from "lucide-react";

interface LiveOSMetricsBarProps {
  score?: number;
  activeAgentsCount?: number;
  confidence?: number;
  reportsCount?: number;
  latencyMs?: number;
}

export function LiveOSMetricsBar({
  score = 88,
  activeAgentsCount = 9,
  confidence = 94,
  reportsCount = 42,
  latencyMs = 320,
}: LiveOSMetricsBarProps) {
  const metrics = [
    { label: "Master Innovation Score", value: `${score}/100`, icon: Award, color: "#10b981" },
    { label: "Active Sub-Agents", value: `${activeAgentsCount} / 9 Active`, icon: Activity, color: "#6366f1" },
    { label: "AI Confidence Rating", value: `${confidence}%`, icon: ShieldCheck, color: "#38bdf8" },
    { label: "Total Reports Generated", value: reportsCount, icon: FileText, color: "#f59e0b" },
    { label: "Avg Request Latency", value: `${latencyMs}ms`, icon: Zap, color: "#ec4899" },
  ];

  return (
    <div className="glass-pill" style={{ borderRadius: 999, padding: "14px 28px", maxWidth: 1050, margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, flexWrap: "wrap" }}>
      {metrics.map((m, idx) => {
        const Icon = m.icon;
        return (
          <div key={m.label} style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ width: 34, height: 34, borderRadius: 10, background: `${m.color}18`, border: `1px solid ${m.color}35`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
              <Icon style={{ width: 16, height: 16, color: m.color }} />
            </div>
            <div>
              <div style={{ fontSize: 15, fontWeight: 800, color: "#fff", lineHeight: 1.1 }}>{m.value}</div>
              <div style={{ fontSize: 11, color: "#64748b", marginTop: 2, fontWeight: 500 }}>{m.label}</div>
            </div>
            {idx < metrics.length - 1 && (
              <div style={{ width: 1, height: 24, background: "rgba(99,102,241,0.15)", marginLeft: 16 }} className="hide-mobile" />
            )}
          </div>
        );
      })}
    </div>
  );
}
