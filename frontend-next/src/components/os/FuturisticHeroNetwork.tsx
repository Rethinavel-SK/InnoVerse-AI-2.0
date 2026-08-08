"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, Cpu, Shield, BookOpen, BarChart2, Flame, AlertTriangle, Leaf, Map, Sparkles } from "lucide-react";
import { AGENTS } from "@/lib/types";

interface FuturisticHeroNetworkProps {
  onAgentClick?: (agentId: string) => void;
}

export function FuturisticHeroNetwork({ onAgentClick }: FuturisticHeroNetworkProps) {
  const [hoveredAgent, setHoveredAgent] = useState<string | null>(null);

  // Circular placement math for 9 sub-agent nodes around the central director (radius 220px)
  const radius = 220;
  const totalAgents = AGENTS.length;

  // Inter-agent relationships mapping for hover highlight
  const collaborationMap: Record<string, string[]> = {
    solution_architect: ["risk_assessment", "mvp_planner"],
    business_strategy: ["market", "patent"],
    research: ["patent", "solution_architect"],
    patent: ["research", "business_strategy"],
    market: ["business_strategy", "trend"],
    trend: ["market", "solution_architect"],
    risk_assessment: ["solution_architect", "sustainability", "mvp_planner"],
    sustainability: ["risk_assessment", "mvp_planner"],
    mvp_planner: ["solution_architect", "risk_assessment", "sustainability"],
  };

  return (
    <div style={{ position: "relative", width: "100%", height: 560, display: "flex", alignItems: "center", justifyContent: "center", overflow: "visible" }}>
      <svg width="600" height="560" style={{ position: "absolute", inset: 0, margin: "auto", overflow: "visible", zIndex: 1 }}>
        <defs>
          <linearGradient id="laserGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#6366f1" stopOpacity="0.8" />
            <stop offset="50%" stopColor="#38bdf8" stopOpacity="0.9" />
            <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.8" />
          </linearGradient>
        </defs>

        {/* Ambient Outer Rings */}
        <circle cx="300" cy="280" r="220" fill="none" stroke="rgba(99,102,241,0.12)" strokeWidth="1" strokeDasharray="6,6" className="animate-rotate-slow" />
        <circle cx="300" cy="280" r="140" fill="none" stroke="rgba(56,189,248,0.1)" strokeWidth="1" />

        {/* SVG Laser Edges from Director (300, 280) to 9 Agents */}
        {AGENTS.map((agent, index) => {
          const angle = (index * 2 * Math.PI) / totalAgents - Math.PI / 2;
          const targetX = 300 + radius * Math.cos(angle);
          const targetY = 280 + radius * Math.sin(angle);

          const isHovered = hoveredAgent === agent.id;
          const isRelated = hoveredAgent ? collaborationMap[hoveredAgent]?.includes(agent.id) : false;

          return (
            <g key={agent.id}>
              {/* Core Laser Edge */}
              <line
                x1="300"
                y1="280"
                x2={targetX}
                y2={targetY}
                stroke={isHovered || isRelated ? "#38bdf8" : "url(#laserGrad)"}
                strokeWidth={isHovered || isRelated ? "2.5" : "1.2"}
                opacity={hoveredAgent ? (isHovered || isRelated ? 1.0 : 0.2) : 0.6}
                className="animate-laser-edge"
              />
            </g>
          );
        })}
      </svg>

      {/* Central Glowing Innovation Director Node */}
      <div style={{ position: "absolute", zIndex: 10, textAlign: "center" }}>
        <motion.div
          animate={{ scale: [1, 1.04, 1], boxShadow: ["0 0 30px rgba(99,102,241,0.4)", "0 0 60px rgba(99,102,241,0.8)", "0 0 30px rgba(99,102,241,0.4)"] }}
          transition={{ duration: 3, repeat: Infinity }}
          style={{
            width: 100,
            height: 100,
            borderRadius: 30,
            background: "linear-gradient(135deg, #6366f1, #8b5cf6, #3b82f6)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            margin: "0 auto 12px",
            border: "2px solid rgba(255,255,255,0.4)",
            cursor: "pointer",
          }}
        >
          <Brain style={{ width: 50, height: 50, color: "#fff" }} />
        </motion.div>
        <div style={{ fontSize: 16, fontWeight: 900, color: "#fff", textShadow: "0 0 16px rgba(99,102,241,0.8)", letterSpacing: "-0.01em" }}>
          Innovation Director
        </div>
        <div style={{ fontSize: 11, fontWeight: 600, color: "#a5b4fc", textTransform: "uppercase", letterSpacing: "0.08em" }}>
          Master AI Core
        </div>
      </div>

      {/* 9 Radial Orbiting Sub-Agent Nodes */}
      {AGENTS.map((agent, index) => {
        const angle = (index * 2 * Math.PI) / totalAgents - Math.PI / 2;
        const x = radius * Math.cos(angle);
        const y = radius * Math.sin(angle);

        const isHovered = hoveredAgent === agent.id;
        const isRelated = hoveredAgent ? collaborationMap[hoveredAgent]?.includes(agent.id) : false;

        return (
          <motion.div
            key={agent.id}
            onMouseEnter={() => setHoveredAgent(agent.id)}
            onMouseLeave={() => setHoveredAgent(null)}
            onClick={() => onAgentClick && onAgentClick(agent.id)}
            initial={{ opacity: 0, scale: 0 }}
            animate={{
              opacity: hoveredAgent ? (isHovered || isRelated ? 1 : 0.35) : 1,
              scale: isHovered ? 1.15 : 1,
              x,
              y,
            }}
            transition={{ duration: 0.3 }}
            style={{
              position: "absolute",
              zIndex: 5,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              cursor: "pointer",
            }}
          >
            <div
              style={{
                width: 54,
                height: 54,
                borderRadius: 16,
                background: isHovered ? "rgba(99,102,241,0.3)" : "rgba(15,23,42,0.85)",
                backdropFilter: "blur(12px)",
                border: isHovered || isRelated ? "2px solid #38bdf8" : "1px solid rgba(99,102,241,0.25)",
                boxShadow: isHovered ? "0 0 24px rgba(56,189,248,0.6)" : "0 4px 20px rgba(0,0,0,0.4)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 24,
                transition: "all 0.2s ease",
              }}
            >
              {agent.icon}
            </div>
            <div
              style={{
                fontSize: 11,
                fontWeight: 700,
                color: isHovered ? "#38bdf8" : isRelated ? "#a5b4fc" : "#cbd5e1",
                marginTop: 6,
                textAlign: "center",
                maxWidth: 100,
                lineHeight: 1.2,
                whiteSpace: "nowrap",
              }}
            >
              {agent.name.replace(" Agent", "")}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
