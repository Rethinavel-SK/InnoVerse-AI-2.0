"use client";

import { use, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { Brain, CheckCircle, Clock, AlertTriangle, RefreshCw, Terminal, Layers } from "lucide-react";
import { runInnovationDirector, saveAnalysis } from "@/lib/api";
import { AGENTS, AgentStatus } from "@/lib/types";
import { AgentFlowGraph } from "@/components/graphs/AgentFlowGraph";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

export default function ProcessingPage({ params }: { params: Promise<{ id: string }> }) {
  const { id: analysisId } = use(params);
  const router = useRouter();
  const searchParams = useSearchParams();
  const problem = searchParams.get("problem") || "";

  const [directorStatus, setDirectorStatus] = useState<AgentStatus>("waiting");
  const [completedAgents, setCompletedAgents] = useState<string[]>([]);
  const [activeAgentId, setActiveAgentId] = useState<string | undefined>("solution_architect");
  const [logs, setLogs] = useState<Array<{ timestamp: string; text: string; level: string }>>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const timelineSteps = [
    { name: "Request Received", status: "completed" },
    { name: "Innovation Director Initialized", status: directorStatus === "waiting" ? "running" : "completed" },
    { name: "Concurrent 9-Agent Dispatch", status: completedAgents.length > 0 ? "completed" : "running" },
    { name: "Conflict Resolution & Scoring", status: completedAgents.length === 9 ? "running" : "waiting" },
    { name: "Executive Report Synthesis", status: directorStatus === "completed" ? "completed" : "waiting" },
  ];

  useEffect(() => {
    if (!problem) return;

    let isMounted = true;
    const startMs = Date.now();

    const addLog = (text: string, level = "INFO") => {
      if (!isMounted) return;
      const ts = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      setLogs((prev) => [...prev, { timestamp: ts, text, level }]);
    };

    addLog(`Received problem statement: "${problem.slice(0, 60)}..."`);
    addLog("Initializing Innovation Director Master Orchestrator...", "INFO");
    setDirectorStatus("running");

    // Simulate progressive agent completions for live feedback
    const timers: NodeJS.Timeout[] = [];
    AGENTS.forEach((agent, idx) => {
      const t = setTimeout(() => {
        if (!isMounted) return;
        setActiveAgentId(agent.id);
        addLog(`Dispatched ${agent.name} (${agent.id})...`, "INFO");
        setCompletedAgents((prev) => [...new Set([...prev, agent.id])]);
      }, (idx + 1) * 2200);
      timers.push(t);
    });

    // Execute actual backend request
    runInnovationDirector(problem)
      .then((report) => {
        if (!isMounted) return;
        const elapsedSec = ((Date.now() - startMs) / 1000).toFixed(1);
        addLog(`Master Synthesis complete in ${elapsedSec}s! Saving report...`, "SUCCESS");

        setDirectorStatus("completed");
        setCompletedAgents(AGENTS.map((a) => a.id));
        setActiveAgentId(undefined);

        saveAnalysis({
          id: analysisId,
          problem_statement: problem,
          created_at: new Date().toISOString(),
          score: report.overall_innovation_score ?? report.feasibility_score ?? 85,
          recommendation: typeof report.final_recommendation === "object"
            ? report.final_recommendation?.build_recommendation ?? report.recommendation ?? "GO"
            : report.recommendation ?? "GO",
          report,
        });

        setTimeout(() => {
          if (isMounted) router.push(`/analysis/${analysisId}`);
        }, 1200);
      })
      .catch((err) => {
        if (!isMounted) return;
        console.error("Discovery failed:", err);
        setErrorMsg(err?.response?.data?.detail || err?.message || "Internal server error");
        setDirectorStatus("failed");
        addLog(`Error executing discovery pipeline: ${err?.message}`, "ERROR");
      });

    return () => {
      isMounted = false;
      timers.forEach(clearTimeout);
    };
  }, [analysisId, problem, router]);

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1050, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: 10, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 600, marginBottom: 16 }}>
            <Brain className="animate-spin" style={{ width: 16, height: 16 }} /> Orchestrating 9 AI Agents
          </div>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Innovation Discovery Pipeline</h1>
          <p style={{ color: "#cbd5e1", fontSize: 14, maxWidth: 650, margin: "0 auto", lineHeight: 1.6 }}>"{problem}"</p>
        </div>

        {/* Real-Time Timeline Progress Bar */}
        <div style={{ ...CARD, marginBottom: 28, padding: "20px 24px" }}>
          <div style={{ fontSize: 12, fontWeight: 700, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 14 }}>Real-Time Execution Milestones</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 10 }}>
            {timelineSteps.map((s, i) => (
              <div key={i} style={{ background: s.status === "completed" ? "rgba(16,185,129,0.08)" : s.status === "running" ? "rgba(99,102,241,0.12)" : "rgba(30,41,59,0.4)", border: s.status === "completed" ? "1px solid rgba(16,185,129,0.3)" : s.status === "running" ? "1px solid #6366f1" : "1px solid rgba(71,85,105,0.3)", borderRadius: 12, padding: "10px 12px" }}>
                <div style={{ fontSize: 11, fontWeight: 600, color: s.status === "completed" ? "#34d399" : s.status === "running" ? "#a5b4fc" : "#64748b" }}>
                  {s.status === "completed" ? "✓ Done" : s.status === "running" ? "⟳ In Progress" : "Queued"}
                </div>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#f1f5f9", marginTop: 4 }}>{s.name}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Animated Flow Graph */}
        <div style={{ marginBottom: 28 }}>
          <AgentFlowGraph activeAgentId={activeAgentId} completedAgentIds={completedAgents} />
        </div>

        {/* Live Terminal Log Stream */}
        <div style={CARD}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
            <h3 style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9", margin: 0, display: "flex", alignItems: "center", gap: 8 }}>
              <Terminal style={{ width: 16, height: 16, color: "#818cf8" }} /> Live Agent Log Stream
            </h3>
            <span style={{ fontSize: 11, color: "#34d399", display: "flex", alignItems: "center", gap: 4 }}>
              <RefreshCw className="animate-spin" style={{ width: 12, height: 12 }} /> Live Output
            </span>
          </div>

          <div style={{ background: "#020817", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 14, padding: "16px", fontFamily: "monospace", fontSize: 12, height: 200, overflowY: "auto", display: "flex", flexDirection: "column", gap: 8 }}>
            {logs.map((log, idx) => (
              <div key={idx} style={{ display: "flex", gap: 10 }}>
                <span style={{ color: "#475569" }}>[{log.timestamp}]</span>
                <span style={{ color: log.level === "ERROR" ? "#f87171" : log.level === "SUCCESS" ? "#34d399" : "#a5b4fc" }}>
                  {log.text}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Error Notification */}
        {errorMsg && (
          <div style={{ marginTop: 24, background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: 16, padding: 20, textAlign: "center" }}>
            <AlertTriangle style={{ width: 32, height: 32, color: "#f87171", margin: "0 auto 8px" }} />
            <div style={{ fontSize: 16, fontWeight: 700, color: "#fff", marginBottom: 4 }}>Analysis Failed</div>
            <div style={{ fontSize: 13, color: "#fca5a5", marginBottom: 16 }}>{errorMsg}</div>
            <button onClick={() => window.location.reload()} style={{ padding: "10px 20px", borderRadius: 12, background: "#ef4444", color: "#fff", border: "none", cursor: "pointer", fontSize: 13, fontWeight: 600 }}>
              Try Again
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
