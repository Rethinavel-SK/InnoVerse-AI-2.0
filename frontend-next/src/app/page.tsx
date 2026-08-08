"use client";

import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { FuturisticHeroNetwork } from "@/components/os/FuturisticHeroNetwork";
import { LiveOSMetricsBar } from "@/components/os/LiveOSMetricsBar";
import { FuturisticCommandPrompt } from "@/components/os/FuturisticCommandPrompt";
import { BentoAgentGrid } from "@/components/os/BentoAgentGrid";
import { ArchitectureDiagram } from "@/components/architecture/ArchitectureDiagram";
import { Sparkles, Brain, Cpu, ArrowRight, ShieldCheck, Network, Database, FileCheck } from "lucide-react";

export default function HomePage() {
  const router = useRouter();

  return (
    <div className="aurora-bg" style={{ minHeight: "100vh", paddingTop: "5.5rem", paddingBottom: "5rem" }}>
      <div style={{ maxWidth: 1240, margin: "0 auto", padding: "0 20px" }}>
        {/* Futuristic Hero Banner */}
        <div style={{ textAlign: "center", marginBottom: "2rem" }}>
          <motion.span
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              padding: "6px 18px",
              borderRadius: 999,
              background: "rgba(99,102,241,0.12)",
              border: "1px solid rgba(56,189,248,0.3)",
              color: "#38bdf8",
              fontSize: 12,
              fontWeight: 700,
              letterSpacing: "0.05em",
              textTransform: "uppercase",
              marginBottom: 20,
              boxShadow: "0 0 20px rgba(56,189,248,0.2)",
            }}
          >
            <Sparkles style={{ width: 14, height: 14 }} /> Autonomous Multi-Agent AI OS v2.5
          </motion.span>

          <h1 style={{ fontSize: "clamp(2.4rem, 5vw, 4rem)", fontWeight: 900, color: "#fff", lineHeight: 1.1, letterSpacing: "-0.03em", marginBottom: 16 }}>
            Enterprise <span className="gradient-text">AI Innovation</span> Platform
          </h1>

          <p style={{ color: "#94a3b8", fontSize: 16, maxWidth: 680, margin: "0 auto 28px", lineHeight: 1.6 }}>
            One central <strong style={{ color: "#fff" }}>Innovation Director Agent</strong> orchestrates 9 specialized AI agents in real-time to solve complex business problems, evaluate market TAM, verify patent prior-art, and design production microservices.
          </p>

          {/* Command Prompt Bar */}
          <FuturisticCommandPrompt />
        </div>

        {/* Live Telemetry Vision Pro Metrics Bar */}
        <div style={{ marginBottom: "3.5rem" }}>
          <LiveOSMetricsBar />
        </div>

        {/* Hero Central Neural Network Visualization */}
        <div style={{ marginBottom: "4rem" }}>
          <div style={{ textAlign: "center", marginBottom: 12 }}>
            <span style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Live Neural Communication Mesh
            </span>
          </div>
          <FuturisticHeroNetwork onAgentClick={(id) => router.push("/agents")} />
        </div>

        {/* Bento Grid AI Control Center */}
        <div style={{ marginBottom: "4rem" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
            <div>
              <h2 style={{ fontSize: 22, fontWeight: 800, color: "#fff", margin: 0, display: "flex", alignItems: "center", gap: 10 }}>
                <Cpu style={{ width: 20, height: 20, color: "#38bdf8" }} /> 9 Specialist AI Agent Registry
              </h2>
              <p style={{ color: "#64748b", fontSize: 13, margin: "4px 0 0" }}>Each agent executes independent domain analysis and collaborates before master synthesis</p>
            </div>
            <button onClick={() => router.push("/agents")} style={{ display: "inline-flex", alignItems: "center", gap: 6, color: "#38bdf8", background: "transparent", border: "none", fontSize: 13, fontWeight: 700, cursor: "pointer" }}>
              View Agent Analytics <ArrowRight style={{ width: 14, height: 14 }} />
            </button>
          </div>

          <BentoAgentGrid />
        </div>

        {/* Interactive Architecture Section */}
        <div style={{ marginBottom: "4rem" }}>
          <ArchitectureDiagram />
        </div>

        {/* Enterprise Modules Navigation Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 20 }}>
          <div onClick={() => router.push("/knowledge-base")} className="glass-panel" style={{ borderRadius: 20, padding: 24, cursor: "pointer" }}>
            <div style={{ width: 44, height: 44, borderRadius: 14, background: "rgba(56,189,248,0.15)", border: "1px solid rgba(56,189,248,0.3)", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 16 }}>
              <Database style={{ width: 22, height: 22, color: "#38bdf8" }} />
            </div>
            <h3 style={{ fontSize: 16, fontWeight: 800, color: "#fff", marginBottom: 6 }}>RAG Vector Knowledge Base</h3>
            <p style={{ fontSize: 13, color: "#94a3b8", margin: 0, lineHeight: 1.5 }}>Upload enterprise PDFs, DOCX, and PPTX. Context is chunked and supplied to agent prompts.</p>
          </div>

          <div onClick={() => router.push("/collaboration")} className="glass-panel" style={{ borderRadius: 20, padding: 24, cursor: "pointer" }}>
            <div style={{ width: 44, height: 44, borderRadius: 14, background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 16 }}>
              <Network style={{ width: 22, height: 22, color: "#818cf8" }} />
            </div>
            <h3 style={{ fontSize: 16, fontWeight: 800, color: "#fff", marginBottom: 6 }}>Inter-Agent Collaboration Mesh</h3>
            <p style={{ fontSize: 13, color: "#94a3b8", margin: 0, lineHeight: 1.5 }}>Inspect live agent-to-agent message exchanges and dependency chaining DAGs.</p>
          </div>

          <div onClick={() => router.push("/documents")} className="glass-panel" style={{ borderRadius: 20, padding: 24, cursor: "pointer" }}>
            <div style={{ width: 44, height: 44, borderRadius: 14, background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.3)", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 16 }}>
              <FileCheck style={{ width: 22, height: 22, color: "#34d399" }} />
            </div>
            <h3 style={{ fontSize: 16, fontWeight: 800, color: "#fff", marginBottom: 6 }}>Pitch Deck & SRS Generator</h3>
            <p style={{ fontSize: 13, color: "#94a3b8", margin: 0, lineHeight: 1.5 }}>Automatically generate 12-slide Pitch Decks (PPTX) and 15-section IEEE SRS specs (DOCX/PDF).</p>
          </div>
        </div>
      </div>
    </div>
  );
}
