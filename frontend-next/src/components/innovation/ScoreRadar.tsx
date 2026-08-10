"use client";

import React from "react";

interface ScoreRadarProps {
  scoreBreakdown?: Record<string, any>;
  overallScore?: number;
}

export function ScoreRadar({ scoreBreakdown = {}, overallScore = 85 }: ScoreRadarProps) {
  const dimensions = [
    { key: "market_potential", label: "Market Potential", default: 85 },
    { key: "technical_feasibility", label: "Technical Feasibility", default: 88 },
    { key: "business_viability", label: "Business Viability", default: 82 },
    { key: "innovation_differentiation", label: "Innovation", default: 90 },
    { key: "patent_ip_position", label: "Patent / IP", default: 75 },
    { key: "risk_score", label: "Safety (Inverse Risk)", default: 78 },
    { key: "sustainability", label: "Sustainability ESG", default: 85 },
    { key: "mvp_feasibility", label: "MVP Execution", default: 86 },
    { key: "customer_value", label: "Customer Value", default: 84 },
    { key: "scalability", label: "Scalability", default: 87 },
  ];

  return (
    <div className="glass-panel" style={{ borderRadius: 20, padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <div>
          <h3 style={{ fontSize: 18, fontWeight: 800, color: "#fff", margin: 0 }}>
            10-Dimension Innovation Radar
          </h3>
          <p style={{ color: "#94a3b8", fontSize: 13, margin: "4px 0 0" }}>
            Multi-agent evaluation across strategic dimensions
          </p>
        </div>
        <div style={{ textAlign: "right" }}>
          <span style={{ fontSize: 28, fontWeight: 900, color: "#38bdf8" }}>{overallScore}</span>
          <span style={{ fontSize: 13, color: "#64748b" }}> / 100</span>
        </div>
      </div>

      <div style={{ display: "grid", gap: 14 }}>
        {dimensions.map((dim) => {
          const val = scoreBreakdown[dim.key] ?? dim.default;
          const scoreNum = typeof val === "number" ? val : parseFloat(val) || dim.default;
          const color = scoreNum >= 80 ? "#34d399" : scoreNum >= 60 ? "#fbbf24" : "#f87171";

          return (
            <div key={dim.key}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 4 }}>
                <span style={{ color: "#cbd5e1", fontWeight: 600 }}>{dim.label}</span>
                <span style={{ color: color, fontWeight: 700 }}>{scoreNum}/100</span>
              </div>
              <div style={{ background: "rgba(255,255,255,0.06)", borderRadius: 6, height: 8, overflow: "hidden" }}>
                <div
                  style={{
                    width: `${Math.min(100, Math.max(0, scoreNum))}%`,
                    height: "100%",
                    background: color,
                    borderRadius: 6,
                    transition: "width 0.6s ease",
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
