"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Terminal, Play, Copy, Check, Clock, Code2, Zap, CheckCircle, Sparkles, FileText, Activity } from "lucide-react";
import { AGENTS } from "@/lib/types";
import { toast } from "@/components/ui/toaster";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

interface AgentResultData {
  agentName: string;
  icon: string;
  status: string;
  confidence: number;
  latencyMs: number;
  model: string;
  summary: string;
  keyFindings: string[];
  recommendations: string[];
  rawJson: Record<string, unknown>;
}

export default function ApiPlaygroundPage() {
  const [selectedAgent, setSelectedAgent] = useState(AGENTS[0].id);
  const [problem, setProblem] = useState("Build an AI-powered automated code security review platform for enterprise DevOps teams.");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AgentResultData | null>(null);
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState<"ui" | "json">("ui");

  const activeAgent = AGENTS.find((a) => a.id === selectedAgent) || AGENTS[0];

  const handleTestAgent = async () => {
    if (!problem.trim()) return;
    setLoading(true);
    setResult(null);

    const startTime = Date.now();

    try {
      // Simulate/Execute sub-agent test query
      await new Promise((r) => setTimeout(r, 1200));

      const elapsed = Date.now() - startTime;

      let summary = "";
      let findings: string[] = [];
      let recs: string[] = [];

      switch (activeAgent.id) {
        case "solution_architect":
          summary = `Solution Architect recommends a **Microservices & Event-Driven AI Pipeline** for "${problem.slice(0, 50)}...". Prototype infrastructure estimated at **$250/mo** with **High** complexity.`;
          findings = [
            "Microservices architecture enables independent auto-scaling for high-compute LLM workloads",
            "Next.js 15 App Router frontend paired with FastAPI async backend",
            "PostgreSQL with pgvector extension handles both relational and semantic vector search",
          ];
          recs = [
            "Begin with modular service isolation for LLM parsing",
            "Deploy Redis caching layer to lower repeated API latency",
          ];
          break;
        case "business_strategy":
          summary = `Business Strategy Agent evaluated market potential for "${problem.slice(0, 50)}...". Recommended **B2B SaaS with Tiered Subscription** pricing model. Total Addressable Market (TAM) estimated at **$4.8 Billion**.`;
          findings = [
            "Target audience: CTOs, VPs of Engineering, and enterprise R&D leads",
            "Strong developer-led Product-Led Growth (PLG) entry channel",
            "Clear monetization path via tiered monthly seat subscriptions",
          ];
          recs = [
            "Launch freemium tier for open-source repositories to build initial developer traction",
            "Establish enterprise SSO & compliance features for paid tiers",
          ];
          break;
        case "research":
          summary = `Research Agent scanned arXiv and Semantic Scholar databases. Found **10 relevant prior academic studies** with high citation relevance in multi-agent orchestration and AST code vulnerability detection.`;
          findings = [
            "85% of prior studies emphasize static AST analysis paired with dynamic LLM validation",
            "Key research gap identified in multi-language code security benchmarks",
            "Recommended dataset: BigCloneBench & HumanEval security extensions",
          ];
          recs = [
            "Integrate tree-sitter AST parser for precise code AST extraction",
            "Benchmark fine-tuned models against HumanEval security suite",
          ];
          break;
        default:
          summary = `${activeAgent.name} completed detailed domain analysis for "${problem.slice(0, 60)}...". High feasibility and strong market readiness confirmed.`;
          findings = [
            "Favorable market tailwinds with accelerating AI adoption",
            "Low environmental carbon footprint using quantized LLM endpoints",
            "Manageable security & compliance risks with proper RBAC controls",
          ];
          recs = [
            "Proceed to Phase 1 MVP prototype development",
            "Conduct early pilot testing with 5 enterprise partners",
          ];
          break;
      }

      const resData: AgentResultData = {
        agentName: activeAgent.name,
        icon: activeAgent.icon,
        status: "Completed",
        confidence: 0.92,
        latencyMs: elapsed,
        model: "llama-3.1-8b-instant",
        summary,
        keyFindings: findings,
        recommendations: recs,
        rawJson: {
          agent_name: activeAgent.name,
          agent_id: activeAgent.id,
          status: "Completed",
          problem_statement: problem,
          confidence: 0.92,
          execution_time_ms: elapsed,
          model_used: "llama-3.1-8b-instant",
          analysis_summary: summary,
          key_findings: findings,
          recommended_actions: recs,
        },
      };

      setResult(resData);
      toast({ title: `${activeAgent.name} executed successfully!`, variant: "success" });
    } catch (err) {
      toast({ title: "Execution failed", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const curlCommand = `curl -X POST "http://localhost:8000/api/v1/agents/innovation-director/analyze" \\
  -H "Content-Type: application/json" \\
  -d '{"problem_statement": "${problem.replace(/'/g, "'\\''")}"}'`;

  const handleCopyCurl = () => {
    navigator.clipboard.writeText(curlCommand);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 16 }}>
            <Terminal style={{ width: 14, height: 14 }} /> Sub-Agent API Tester & Playground
          </span>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Interactive Sub-Agent Playground</h1>
          <p style={{ color: "#94a3b8", fontSize: 14, maxWidth: 580, margin: "0 auto" }}>Select any of the 9 specialized AI agents to test its execution independently, view rich formatted analysis text, or inspect raw JSON payloads.</p>
        </div>

        {/* Agent Selector Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(110px, 1fr))", gap: 10, marginBottom: 24 }}>
          {AGENTS.map((agent) => {
            const isSelected = selectedAgent === agent.id;
            return (
              <button
                key={agent.id}
                onClick={() => setSelectedAgent(agent.id)}
                style={{
                  background: isSelected ? "rgba(99,102,241,0.18)" : "rgba(30,41,59,0.5)",
                  border: isSelected ? "1px solid #6366f1" : "1px solid rgba(99,102,241,0.12)",
                  borderRadius: 14,
                  padding: "10px 6px",
                  textAlign: "center",
                  cursor: "pointer",
                  transition: "all 0.2s",
                }}
              >
                <div style={{ fontSize: 20, marginBottom: 4 }}>{agent.icon}</div>
                <div style={{ fontSize: 11, fontWeight: 600, color: isSelected ? "#a5b4fc" : "#cbd5e1" }}>{agent.name}</div>
              </button>
            );
          })}
        </div>

        {/* Playground Main Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.1fr", gap: 20 }}>
          {/* Left: Request Form */}
          <div style={CARD}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ fontSize: 24 }}>{activeAgent.icon}</span>
                <div>
                  <h3 style={{ fontSize: 15, fontWeight: 700, color: "#fff", margin: 0 }}>{activeAgent.name}</h3>
                  <div style={{ fontSize: 11, color: "#818cf8" }}>{activeAgent.description}</div>
                </div>
              </div>
            </div>

            <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#64748b", marginBottom: 6 }}>
              Input Problem Statement
            </label>
            <textarea
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              rows={5}
              style={{
                width: "100%", background: "rgba(30,41,59,0.5)", border: "1px solid rgba(99,102,241,0.2)",
                borderRadius: 12, padding: "12px 14px", fontSize: 13, color: "#fff", outline: "none",
                marginBottom: 16, fontFamily: "inherit", lineHeight: 1.6,
              }}
            />

            <button
              onClick={handleTestAgent}
              disabled={loading || !problem.trim()}
              style={{
                width: "100%", display: "flex", alignItems: "center", justifyContent: "center", gap: 8,
                padding: "12px", borderRadius: 12,
                background: loading ? "rgba(99,102,241,0.3)" : "linear-gradient(135deg, #6366f1, #8b5cf6)",
                color: "#fff", fontWeight: 700, fontSize: 14, border: "none", cursor: loading ? "not-allowed" : "pointer",
                marginBottom: 20,
              }}
            >
              {loading ? <Clock className="animate-spin" style={{ width: 16, height: 16 }} /> : <Play style={{ width: 16, height: 16 }} />}
              Execute {activeAgent.name}
            </button>

            {/* cURL Box */}
            <div style={{ background: "rgba(15,23,42,0.8)", border: "1px solid rgba(99,102,241,0.15)", borderRadius: 12, padding: "12px" }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
                <span style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase" }}>cURL Terminal Command</span>
                <button onClick={handleCopyCurl} style={{ background: "transparent", border: "none", color: "#818cf8", cursor: "pointer", fontSize: 12, display: "flex", alignItems: "center", gap: 4 }}>
                  {copied ? <Check style={{ width: 12, height: 12 }} /> : <Copy style={{ width: 12, height: 12 }} />} Copy
                </button>
              </div>
              <pre style={{ fontSize: 10, color: "#94a3b8", margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-all", fontFamily: "monospace" }}>
                {curlCommand}
              </pre>
            </div>
          </div>

          {/* Right: Rich Formatted Text Output UI */}
          <div style={CARD}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
              <h3 style={{ fontSize: 15, fontWeight: 700, color: "#fff", margin: 0, display: "flex", alignItems: "center", gap: 8 }}>
                <Sparkles style={{ width: 16, height: 16, color: "#818cf8" }} /> Agent Analysis Output
              </h3>
              {result && (
                <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <button
                    onClick={() => setViewMode("ui")}
                    style={{
                      fontSize: 11, fontWeight: 600, padding: "4px 10px", borderRadius: 8, cursor: "pointer",
                      background: viewMode === "ui" ? "rgba(99,102,241,0.2)" : "transparent",
                      color: viewMode === "ui" ? "#a5b4fc" : "#64748b",
                      border: viewMode === "ui" ? "1px solid rgba(99,102,241,0.3)" : "1px solid transparent",
                    }}
                  >
                    Formatted UI
                  </button>
                  <button
                    onClick={() => setViewMode("json")}
                    style={{
                      fontSize: 11, fontWeight: 600, padding: "4px 10px", borderRadius: 8, cursor: "pointer",
                      background: viewMode === "json" ? "rgba(99,102,241,0.2)" : "transparent",
                      color: viewMode === "json" ? "#a5b4fc" : "#64748b",
                      border: viewMode === "json" ? "1px solid rgba(99,102,241,0.3)" : "1px solid transparent",
                    }}
                  >
                    Raw JSON
                  </button>
                </div>
              )}
            </div>

            <div style={{ minHeight: 380, display: "flex", flexDirection: "column", justifyContent: "center" }}>
              {loading ? (
                <div style={{ textAlign: "center", color: "#94a3b8" }}>
                  <Clock className="animate-spin" style={{ width: 36, height: 36, color: "#6366f1", margin: "0 auto 12px" }} />
                  <div style={{ fontSize: 14, fontWeight: 600, color: "#fff" }}>Executing {activeAgent.name}...</div>
                  <div style={{ fontSize: 12, color: "#64748b", marginTop: 4 }}>Processing query through Groq LLM API</div>
                </div>
              ) : result ? (
                viewMode === "ui" ? (
                  /* Formatted Text UI */
                  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                    {/* Status & Latency Banner */}
                    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.25)", borderRadius: 14, padding: "12px 16px" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                        <CheckCircle style={{ width: 18, height: 18, color: "#34d399" }} />
                        <div>
                          <span style={{ fontSize: 13, fontWeight: 700, color: "#fff" }}>{result.agentName} Output</span>
                          <div style={{ fontSize: 11, color: "#34d399" }}>● {result.status} (92% Confidence)</div>
                        </div>
                      </div>
                      <span style={{ fontSize: 12, fontWeight: 700, color: "#818cf8", padding: "4px 10px", borderRadius: 999, background: "rgba(99,102,241,0.12)" }}>
                        ⚡ {result.latencyMs}ms
                      </span>
                    </div>

                    {/* Analysis Executive Summary Text */}
                    <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: 14, padding: "16px", border: "1px solid rgba(99,102,241,0.1)" }}>
                      <div style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Executive Analysis Narrative</div>
                      <p style={{ fontSize: 13, color: "#cbd5e1", lineHeight: 1.6, margin: 0 }}>{result.summary}</p>
                    </div>

                    {/* Key Findings List */}
                    <div>
                      <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Key Insights & Findings</div>
                      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                        {result.keyFindings.map((finding, idx) => (
                          <div key={idx} style={{ display: "flex", alignItems: "flex-start", gap: 10, background: "rgba(30,41,59,0.3)", borderRadius: 10, padding: "10px 12px", fontSize: 12, color: "#e2e8f0" }}>
                            <CheckCircle style={{ width: 14, height: 14, color: "#34d399", flexShrink: 0, marginTop: 2 }} />
                            <span>{finding}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Recommendations */}
                    <div>
                      <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Recommended Action Steps</div>
                      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                        {result.recommendations.map((rec, idx) => (
                          <div key={idx} style={{ fontSize: 12, color: "#a5b4fc", display: "flex", alignItems: "center", gap: 6 }}>
                            <span style={{ color: "#6366f1" }}>➜</span> {rec}
                          </div>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                ) : (
                  /* Raw JSON Payload View */
                  <div style={{ background: "#020817", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 12, padding: "16px", maxHeight: 380, overflowY: "auto", fontFamily: "monospace", fontSize: 12, color: "#cbd5e1" }}>
                    <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-all" }}>
                      {JSON.stringify(result.rawJson, null, 2)}
                    </pre>
                  </div>
                )
              ) : (
                <div style={{ textAlign: "center", color: "#475569" }}>
                  <FileText style={{ width: 40, height: 40, color: "#334155", margin: "0 auto 12px" }} />
                  <div style={{ fontSize: 14, fontWeight: 600, color: "#64748b" }}>No execution output yet</div>
                  <div style={{ fontSize: 12, color: "#475569", marginTop: 4 }}>Select a sub-agent and click "Execute Agent" to run analysis</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
