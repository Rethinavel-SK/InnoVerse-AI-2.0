"use client";

import React from "react";

interface RadarDataPoint {
  label: string;
  value: number; // 0 to 100
  color: string;
}

interface InnovationRadarChartProps {
  data: RadarDataPoint[];
  size?: number;
}

export function InnovationRadarChart({ data, size = 320 }: InnovationRadarChartProps) {
  const center = size / 2;
  const radius = center - 50;
  const totalAxes = data.length;
  const angleStep = (Math.PI * 2) / totalAxes;

  // Generate grid circles (20%, 40%, 60%, 80%, 100%)
  const levels = [0.2, 0.4, 0.6, 0.8, 1.0];

  // Helper to calculate coordinates
  const getCoordinates = (index: number, valueFactor: number) => {
    const angle = index * angleStep - Math.PI / 2;
    const r = radius * valueFactor;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle),
    };
  };

  // Generate data polygon points
  const points = data
    .map((d, i) => {
      const { x, y } = getCoordinates(i, d.value / 100);
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <svg width={size} height={size} style={{ overflow: "visible" }}>
        {/* Background Grid Circles */}
        {levels.map((level, lvlIdx) => {
          const r = radius * level;
          return (
            <circle
              key={lvlIdx}
              cx={center}
              cy={center}
              r={r}
              fill="none"
              stroke="rgba(99,102,241,0.15)"
              strokeDasharray={lvlIdx === levels.length - 1 ? "none" : "3,3"}
              strokeWidth="1"
            />
          );
        })}

        {/* Axis Lines */}
        {data.map((_, i) => {
          const { x, y } = getCoordinates(i, 1.0);
          return (
            <line
              key={i}
              x1={center}
              y1={center}
              x2={x}
              y2={y}
              stroke="rgba(99,102,241,0.2)"
              strokeWidth="1"
            />
          );
        })}

        {/* Polygon Area */}
        <polygon
          points={points}
          fill="rgba(99, 102, 241, 0.25)"
          stroke="#818cf8"
          strokeWidth="2.5"
        />

        {/* Data Points and Labels */}
        {data.map((d, i) => {
          const { x: ptX, y: ptY } = getCoordinates(i, d.value / 100);
          const { x: lblX, y: lblY } = getCoordinates(i, 1.18);

          return (
            <g key={i}>
              {/* Point indicator */}
              <circle cx={ptX} cy={ptY} r="5" fill={d.color} stroke="#fff" strokeWidth="1.5" />

              {/* Axis Label */}
              <text
                x={lblX}
                y={lblY}
                textAnchor="middle"
                dominantBaseline="central"
                fill="#cbd5e1"
                fontSize="11"
                fontWeight="600"
              >
                {d.label} ({Math.round(d.value)})
              </text>
            </g>
          );
        })}
      </svg>

      {/* Legend Grid */}
      <div style={{ marginTop: 24, display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: 10, width: "100%" }}>
        {data.map((d) => (
          <div
            key={d.label}
            style={{
              background: "rgba(30,41,59,0.5)",
              border: "1px solid rgba(99,102,241,0.12)",
              borderRadius: 10,
              padding: "8px 12px",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <div style={{ width: 8, height: 8, borderRadius: "50%", background: d.color }} />
              <span style={{ fontSize: 12, color: "#94a3b8" }}>{d.label}</span>
            </div>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#f1f5f9" }}>{Math.round(d.value)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
