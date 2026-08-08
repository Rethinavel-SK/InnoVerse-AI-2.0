"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Sparkles, ArrowRight, Terminal, Cpu } from "lucide-react";

export function FuturisticCommandPrompt() {
  const router = useRouter();
  const [problem, setProblem] = useState("");

  const presets = [
    "AI Code Security Reviewer for DevOps",
    "Telemedicine Patient Triage Platform",
    "Carbon Accounting & ESG Compliance Engine",
    "DeFi Cross-Chain Liquidity Protocol",
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!problem.trim()) return;
    const id = Date.now().toString();
    router.push(`/analysis/${id}/processing?problem=${encodeURIComponent(problem)}`);
  };

  return (
    <div style={{ maxWidth: 840, margin: "0 auto", position: "relative", zIndex: 20 }}>
      {/* Floating Glowing Input Container */}
      <motion.form
        onSubmit={handleSubmit}
        whileHover={{ boxShadow: "0 0 40px rgba(99,102,241,0.25)" }}
        className="glass-panel"
        style={{
          borderRadius: 24,
          padding: "16px 20px",
          display: "flex",
          alignItems: "center",
          gap: 14,
          border: "1px solid rgba(99,102,241,0.3)",
          boxShadow: "0 20px 50px rgba(0,0,0,0.5)",
        }}
      >
        <div style={{ width: 38, height: 38, borderRadius: 12, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
          <Sparkles style={{ width: 20, height: 20, color: "#fff" }} />
        </div>

        <input
          type="text"
          value={problem}
          onChange={(e) => setProblem(e.target.value)}
          placeholder="Describe your business problem statement to dispatch 9 AI agents..."
          style={{
            flex: 1,
            background: "transparent",
            border: "none",
            outline: "none",
            fontSize: 15,
            fontWeight: 500,
            color: "#fff",
            fontFamily: "inherit",
          }}
        />

        <button
          type="submit"
          disabled={!problem.trim()}
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            padding: "10px 20px",
            borderRadius: 14,
            background: problem.trim() ? "linear-gradient(135deg, #6366f1, #8b5cf6)" : "rgba(30,41,59,0.5)",
            color: problem.trim() ? "#fff" : "#64748b",
            fontSize: 13,
            fontWeight: 700,
            border: "none",
            cursor: problem.trim() ? "pointer" : "not-allowed",
            transition: "all 0.2s ease",
            flexShrink: 0,
          }}
        >
          Dispatch AI Agents <ArrowRight style={{ width: 15, height: 15 }} />
        </button>
      </motion.form>

      {/* Preset Problem Pills */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, marginTop: 14, flexWrap: "wrap" }}>
        <span style={{ fontSize: 11, color: "#64748b", fontWeight: 600, textTransform: "uppercase" }}>Preset Prompts:</span>
        {presets.map((preset) => (
          <button
            key={preset}
            onClick={() => setProblem(preset)}
            style={{
              fontSize: 11,
              fontWeight: 500,
              padding: "4px 12px",
              borderRadius: 999,
              background: "rgba(99,102,241,0.08)",
              border: "1px solid rgba(99,102,241,0.2)",
              color: "#a5b4fc",
              cursor: "pointer",
              transition: "all 0.2s",
            }}
          >
            + {preset}
          </button>
        ))}
      </div>
    </div>
  );
}
