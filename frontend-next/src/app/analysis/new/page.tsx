"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Zap, ChevronDown, ChevronUp, Brain, Lightbulb, Building, DollarSign, Users, Calendar, Target, Wifi, Activity, Shield, Settings } from "lucide-react";
import { generateId, saveAnalysis } from "@/lib/api";
import { AnalysisOptions } from "@/lib/types";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.8)",
  backdropFilter: "blur(16px)",
  WebkitBackdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 24,
  overflow: "hidden",
};

const exampleProblems = [
  "Build an AI-powered automated code security review platform for enterprise DevOps teams.",
  "Create a blockchain-based supply chain transparency solution for pharmaceutical companies.",
  "Develop an AI telemedicine platform connecting rural patients with specialist doctors.",
  "Build a green energy management SaaS platform for commercial building operators.",
];

const industries = ["Technology", "Healthcare", "FinTech", "E-Commerce", "Education", "Manufacturing", "Agriculture", "Real Estate"];
const budgets = ["< $50K", "$50K–$250K", "$250K–$1M", "$1M+"];
const timelines = ["3 months", "6 months", "12 months", "18+ months"];
const securityLevels = ["Standard", "High", "Enterprise / Compliance"];
const userCounts = ["< 1,000", "1K–10K", "10K–100K", "100K+"];

const selectStyle: React.CSSProperties = {
  width: "100%",
  background: "rgba(30,41,59,0.6)",
  border: "1px solid rgba(99,102,241,0.2)",
  borderRadius: 10,
  padding: "9px 12px",
  fontSize: 13,
  color: "#cbd5e1",
  outline: "none",
  appearance: "auto",
};

export default function NewAnalysisPage() {
  const router = useRouter();
  const [problem, setProblem] = useState("");
  const [showOptions, setShowOptions] = useState(false);
  const [options, setOptions] = useState<AnalysisOptions>({
    industry: "", budget: "", expectedUsers: "", timeline: "",
    aiRequired: false, realTimeProcessing: false, iot: false,
    analytics: false, securityLevel: "Standard",
  });

  const handleGenerate = () => {
    if (!problem.trim() || problem.trim().length < 10) return;
    const id = generateId();
    saveAnalysis({
      id, problem_statement: problem.trim(),
      created_at: new Date().toISOString(), score: 0, recommendation: "Pending",
    });
    router.push(`/analysis/${id}/processing?problem=${encodeURIComponent(problem.trim())}`);
  };

  return (
    <div style={{ minHeight: "100vh", padding: "3rem 1rem 5rem" }}>
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
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
            9 AI Agents · Master Report
          </motion.span>
          <motion.h1
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            style={{ fontSize: "clamp(1.8rem,4vw,2.4rem)", fontWeight: 800, color: "#f1f5f9", marginBottom: 10 }}
          >
            Start Innovation Discovery
          </motion.h1>
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            style={{ color: "#94a3b8", fontSize: 15 }}
          >
            Describe your business problem in detail for the best analysis.
          </motion.p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          style={CARD}
        >
          {/* Textarea */}
          <div style={{ padding: "28px 28px 0" }}>
            <label style={{ display: "block", fontSize: 13, fontWeight: 600, color: "#94a3b8", marginBottom: 10 }}>
              Business Problem Statement <span style={{ color: "#f87171" }}>*</span>
            </label>
            <textarea
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              rows={7}
              placeholder="Describe your business problem, product idea, or innovation concept in detail. The more context you provide, the better the analysis..."
              style={{
                width: "100%",
                background: "rgba(30,41,59,0.5)",
                border: "1px solid rgba(99,102,241,0.2)",
                borderRadius: 14,
                padding: "14px 16px",
                fontSize: 14,
                color: "#e2e8f0",
                lineHeight: 1.7,
                resize: "vertical",
                outline: "none",
                fontFamily: "inherit",
                minHeight: 150,
              }}
            />
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 8 }}>
              <span style={{ fontSize: 12, color: "#475569" }}>{problem.length} characters</span>
              {problem.length > 0 && problem.length < 10 && (
                <span style={{ fontSize: 12, color: "#f87171" }}>Minimum 10 characters required</span>
              )}
            </div>
          </div>

          {/* Example Prompts */}
          <div style={{ padding: "16px 28px" }}>
            <p style={{ fontSize: 12, color: "#475569", marginBottom: 10 }}>Try an example:</p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {exampleProblems.slice(0, 2).map((ex) => (
                <button
                  key={ex}
                  onClick={() => setProblem(ex)}
                  style={{
                    fontSize: 12, padding: "6px 12px", borderRadius: 8,
                    background: "rgba(30,41,59,0.5)", border: "1px solid rgba(99,102,241,0.15)",
                    color: "#94a3b8", cursor: "pointer", textAlign: "left",
                    transition: "all 0.2s",
                  }}
                >
                  {ex.slice(0, 52)}...
                </button>
              ))}
            </div>
          </div>

          {/* Advanced Options */}
          <div style={{ borderTop: "1px solid rgba(99,102,241,0.1)" }}>
            <button
              onClick={() => setShowOptions(!showOptions)}
              style={{
                width: "100%", display: "flex", alignItems: "center", justifyContent: "space-between",
                padding: "16px 28px", background: "transparent", border: "none",
                fontSize: 14, color: "#94a3b8", cursor: "pointer",
              }}
            >
              <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <Settings style={{ width: 15, height: 15 }} /> Advanced Options
              </span>
              {showOptions ? <ChevronUp style={{ width: 15, height: 15 }} /> : <ChevronDown style={{ width: 15, height: 15 }} />}
            </button>

            {showOptions && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                style={{ padding: "0 28px 24px" }}
              >
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                  {[
                    { key: "industry", label: "Industry", icon: Building, options: industries },
                    { key: "budget", label: "Budget Range", icon: DollarSign, options: budgets },
                    { key: "expectedUsers", label: "Expected Users", icon: Users, options: userCounts },
                    { key: "timeline", label: "Timeline", icon: Calendar, options: timelines },
                    { key: "securityLevel", label: "Security Level", icon: Shield, options: securityLevels },
                  ].map(({ key, label, icon: Icon, options: opts }) => (
                    <div key={key}>
                      <label style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12, fontWeight: 600, color: "#64748b", marginBottom: 8 }}>
                        <Icon style={{ width: 13, height: 13 }} /> {label}
                      </label>
                      <select
                        value={(options as Record<string, unknown>)[key] as string}
                        onChange={(e) => setOptions({ ...options, [key]: e.target.value })}
                        style={selectStyle}
                      >
                        <option value="">Select...</option>
                        {opts.map((o) => <option key={o} value={o}>{o}</option>)}
                      </select>
                    </div>
                  ))}
                </div>

                {/* Toggles */}
                <div style={{ marginTop: 16, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                  {[
                    { key: "aiRequired", label: "AI / ML Required", icon: Brain },
                    { key: "realTimeProcessing", label: "Real-Time Processing", icon: Wifi },
                    { key: "iot", label: "IoT Integration", icon: Activity },
                    { key: "analytics", label: "Analytics Platform", icon: Target },
                  ].map(({ key, label, icon: Icon }) => (
                    <label key={key} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 12px", borderRadius: 10, background: "rgba(30,41,59,0.4)", border: "1px solid rgba(99,102,241,0.1)", cursor: "pointer" }}>
                      <input
                        type="checkbox"
                        checked={(options as Record<string, unknown>)[key] as boolean}
                        onChange={(e) => setOptions({ ...options, [key]: e.target.checked })}
                        style={{ width: 15, height: 15, accentColor: "#6366f1" }}
                      />
                      <Icon style={{ width: 13, height: 13, color: "#64748b" }} />
                      <span style={{ fontSize: 12, color: "#94a3b8" }}>{label}</span>
                    </label>
                  ))}
                </div>
              </motion.div>
            )}
          </div>

          {/* Submit */}
          <div style={{ padding: "0 28px 28px" }}>
            <button
              onClick={handleGenerate}
              disabled={!problem.trim() || problem.trim().length < 10}
              style={{
                width: "100%",
                display: "flex", alignItems: "center", justifyContent: "center", gap: 12,
                padding: "16px", borderRadius: 14,
                background: !problem.trim() || problem.trim().length < 10
                  ? "rgba(99,102,241,0.3)"
                  : "linear-gradient(135deg,#6366f1,#8b5cf6)",
                color: "#fff", fontWeight: 700, fontSize: 16,
                border: "none", cursor: !problem.trim() || problem.trim().length < 10 ? "not-allowed" : "pointer",
                boxShadow: !problem.trim() || problem.trim().length < 10 ? "none" : "0 8px 32px rgba(99,102,241,0.4)",
                transition: "all 0.3s",
              }}
            >
              <Zap style={{ width: 20, height: 20 }} />
              Generate Innovation Report
              <span style={{ fontSize: 12, opacity: 0.7, fontWeight: 400 }}>(9 AI Agents)</span>
            </button>
          </div>
        </motion.div>

        {/* More Examples */}
        <div style={{ marginTop: 24 }}>
          <p style={{ fontSize: 12, color: "#334155", textAlign: "center", marginBottom: 12 }}>More examples</p>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {exampleProblems.slice(2).map((ex) => (
              <button
                key={ex}
                onClick={() => setProblem(ex)}
                style={{
                  display: "flex", alignItems: "center", gap: 12,
                  padding: "14px 20px", borderRadius: 14, textAlign: "left",
                  background: "rgba(15,23,42,0.6)", border: "1px solid rgba(99,102,241,0.1)",
                  color: "#94a3b8", cursor: "pointer", fontSize: 14,
                  transition: "all 0.2s",
                }}
              >
                <Lightbulb style={{ width: 16, height: 16, color: "#fbbf24", flexShrink: 0 }} />
                {ex}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
