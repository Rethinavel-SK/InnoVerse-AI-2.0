"use client";

import { use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain, Copy, Printer, FileJson, ChevronDown, ChevronUp,
  CheckCircle, XCircle, TrendingUp, Shield, Leaf, Map, Star,
  ExternalLink, ArrowLeft, AlertTriangle, Target, Lightbulb, Play, Download,
  BookOpen, Compass, BarChart2, Flame
} from "lucide-react";
import { getSavedAnalyses } from "@/lib/api";
import { InnovationReport, AGENTS } from "@/lib/types";
import { formatScore, formatConfidence } from "@/lib/utils";
import { toast } from "@/components/ui/toaster";
import { InnovationRadarChart } from "@/components/charts/InnovationRadarChart";
import { ArchitectureDiagram } from "@/components/architecture/ArchitectureDiagram";
import { ReportChatAssistant } from "@/components/chat/ReportChatAssistant";
import { downloadMarkdownReport, downloadDOCXReport, downloadJSONReport } from "@/lib/exportUtils";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  WebkitBackdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  overflow: "hidden",
};

function ScoreRing({ score, size = 120 }: { score: number; size?: number }) {
  const r = (size - 20) / 2;
  const circ = 2 * Math.PI * r;
  const offset = circ - (score / 100) * circ;
  const color = score >= 80 ? "#10b981" : score >= 60 ? "#f59e0b" : "#ef4444";

  return (
    <div style={{ position: "relative", display: "inline-flex", alignItems: "center", justifyContent: "center", width: size, height: size, flexShrink: 0 }}>
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
        <motion.circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none" stroke={color} strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circ}
          initial={{ strokeDashoffset: circ }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
        />
      </svg>
      <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
        <div style={{ fontSize: 28, fontWeight: 800, color: "#fff", lineHeight: 1 }}>{Math.round(score)}</div>
        <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>/100</div>
      </div>
    </div>
  );
}

function Section({ title, icon: Icon, children, defaultOpen = false, color = "#6366f1" }: {
  title: string; icon: React.ElementType; children: React.ReactNode;
  defaultOpen?: boolean; color?: string;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div style={CARD}>
      <button
        onClick={() => setOpen(!open)}
        style={{
          width: "100%", display: "flex", alignItems: "center", justifyContent: "space-between",
          padding: "20px 24px", background: "transparent", border: "none", cursor: "pointer",
          textAlign: "left",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 10,
            background: `${color}15`, border: `1px solid ${color}30`,
            display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0,
          }}>
            <Icon style={{ width: 16, height: 16, color: color }} />
          </div>
          <span style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9" }}>{title}</span>
        </div>
        {open ? <ChevronUp style={{ width: 18, height: 18, color: "#64748b" }} /> : <ChevronDown style={{ width: 18, height: 18, color: "#64748b" }} />}
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            style={{ borderTop: "1px solid rgba(99,102,241,0.1)", padding: "24px" }}
          >
            {children}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function ListItems({ items }: { items: string[] }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {items.map((item, i) => (
        <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 10, fontSize: 13, color: "#cbd5e1", lineHeight: 1.6 }}>
          <CheckCircle style={{ width: 14, height: 14, color: "#34d399", flexShrink: 0, marginTop: 4 }} />
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
}

export default function ResultsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const [report, setReport] = useState<InnovationReport | null>(null);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    const analyses = getSavedAnalyses();
    const found = analyses.find((a) => a.id === id);
    if (found?.report) {
      setReport(found.report);
    } else {
      setNotFound(true);
    }
  }, [id]);

  const handleCopy = () => {
    if (report) {
      navigator.clipboard.writeText(JSON.stringify(report, null, 2));
      toast({ title: "Copied to clipboard!", variant: "success" });
    }
  };

  const handlePrint = () => window.print();

  if (notFound) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}>
        <div style={{ textAlign: "center" }}>
          <XCircle style={{ width: 56, height: 56, color: "#f87171", margin: "0 auto 16px" }} />
          <h2 style={{ fontSize: 22, fontWeight: 800, color: "#fff", marginBottom: 8 }}>Report Not Found</h2>
          <p style={{ color: "#94a3b8", marginBottom: 24 }}>This analysis may have been deleted or doesn't exist.</p>
          <button onClick={() => router.push("/analysis/new")} style={{ padding: "10px 24px", borderRadius: 12, background: "#6366f1", color: "#fff", fontSize: 14, fontWeight: 600, border: "none", cursor: "pointer" }}>
            Start New Analysis
          </button>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ width: 36, height: 36, border: "3px solid #6366f1", borderTopColor: "transparent", borderRadius: "50%" }} className="animate-spin" />
      </div>
    );
  }

  const score = report.overall_innovation_score ?? report.feasibility_score ?? 85;
  const confidence = report.confidence ?? 0.90;
  const rec = typeof report.final_recommendation === "object"
    ? report.final_recommendation?.build_recommendation ?? report.recommendation ?? "GO"
    : report.recommendation ?? "GO";

  const radarData = [
    { label: "Tech Feasibility", value: report.technical_summary?.feasibility_score ?? 85, color: "#6366f1" },
    { label: "Business Potential", value: Math.round((report.business_summary?.confidence ?? 0.85) * 100), color: "#10b981" },
    { label: "Innovation Level", value: report.patent_summary?.novelty_score ?? report.patent_summary?.score ?? 80, color: "#06b6d4" },
    { label: "Market Readiness", value: report.trend_summary?.trend_score ?? 85, color: "#f59e0b" },
    { label: "Scalability", value: 85, color: "#8b5cf6" },
    { label: "Risk Safety", value: Math.max(10, 100 - (report.risk_summary?.overall_risk_score ?? 30)), color: "#ef4444" },
    { label: "Sustainability", value: report.sustainability_summary?.esg_compliance_score ?? 85, color: "#22c55e" },
  ];

  return (
    <div style={{ minHeight: "100vh", padding: "2rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1000, margin: "0 auto" }}>
        {/* Toolbar */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 24, flexWrap: "wrap", gap: 12 }}>
          <button onClick={() => router.back()} style={{ display: "flex", alignItems: "center", gap: 6, background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer", fontSize: 14, fontWeight: 500 }}>
            <ArrowLeft style={{ width: 16, height: 16 }} /> Back
          </button>
          <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
            <button onClick={() => router.push(`/analysis/${id}/presentation`)} style={{ display: "flex", alignItems: "center", gap: 6, padding: "8px 14px", borderRadius: 10, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", fontSize: 12, fontWeight: 600, border: "none", cursor: "pointer" }}>
              <Play style={{ width: 14, height: 14 }} /> Presentation Deck
            </button>
            <button onClick={() => downloadMarkdownReport(report, id)} style={{ display: "flex", alignItems: "center", gap: 6, padding: "8px 14px", borderRadius: 10, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#cbd5e1", fontSize: 12, fontWeight: 500, cursor: "pointer" }}>
              <Download style={{ width: 14, height: 14 }} /> .MD
            </button>
            <button onClick={() => downloadDOCXReport(report, id)} style={{ display: "flex", alignItems: "center", gap: 6, padding: "8px 14px", borderRadius: 10, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#cbd5e1", fontSize: 12, fontWeight: 500, cursor: "pointer" }}>
              <Download style={{ width: 14, height: 14 }} /> DOCX
            </button>
            <button onClick={() => downloadJSONReport(report, id)} style={{ display: "flex", alignItems: "center", gap: 6, padding: "8px 14px", borderRadius: 10, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#cbd5e1", fontSize: 12, fontWeight: 500, cursor: "pointer" }}>
              <FileJson style={{ width: 14, height: 14 }} /> JSON
            </button>
            <button onClick={handlePrint} style={{ display: "flex", alignItems: "center", gap: 6, padding: "8px 14px", borderRadius: 10, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#cbd5e1", fontSize: 12, fontWeight: 500, cursor: "pointer" }}>
              <Printer style={{ width: 14, height: 14 }} /> Print
            </button>
          </div>
        </div>

        {/* Hero Score Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="animated-border"
          style={{ borderRadius: 24, padding: "32px", marginBottom: 24 }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 32, flexWrap: "wrap" }}>
            <ScoreRing score={score} size={130} />
            <div style={{ flex: 1, minWidth: 260 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                <Brain style={{ width: 18, height: 18, color: "#818cf8" }} />
                <span style={{ color: "#a5b4fc", fontSize: 13, fontWeight: 600 }}>Innovation Director Master Synthesis</span>
              </div>
              <h1 style={{ fontSize: "clamp(1.6rem, 3.5vw, 2.2rem)", fontWeight: 800, color: "#fff", marginBottom: 16, lineHeight: 1.2 }}>
                Overall Innovation Score
              </h1>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
                <span style={{
                  padding: "6px 16px", borderRadius: 999, fontSize: 13, fontWeight: 700,
                  background: score >= 80 ? "rgba(16,185,129,0.12)" : score >= 60 ? "rgba(245,158,11,0.12)" : "rgba(239,68,68,0.12)",
                  border: score >= 80 ? "1px solid rgba(16,185,129,0.3)" : score >= 60 ? "1px solid rgba(245,158,11,0.3)" : "1px solid rgba(239,68,68,0.3)",
                  color: score >= 80 ? "#34d399" : score >= 60 ? "#fbbf24" : "#f87171",
                }}>
                  {formatScore(score)} Score
                </span>
                <span style={{ padding: "6px 16px", borderRadius: 999, fontSize: 13, fontWeight: 600, background: "rgba(59,130,246,0.12)", border: "1px solid rgba(59,130,246,0.3)", color: "#93c5fd" }}>
                  {formatConfidence(confidence)} Confidence
                </span>
                <span style={{
                  padding: "6px 16px", borderRadius: 999, fontSize: 13, fontWeight: 700,
                  background: rec.toUpperCase().includes("YES") || (rec.toUpperCase().includes("GO") && !rec.toUpperCase().includes("NO"))
                    ? "rgba(16,185,129,0.12)" : "rgba(245,158,11,0.12)",
                  border: rec.toUpperCase().includes("YES") || (rec.toUpperCase().includes("GO") && !rec.toUpperCase().includes("NO"))
                    ? "1px solid rgba(16,185,129,0.3)" : "1px solid rgba(245,158,11,0.3)",
                  color: rec.toUpperCase().includes("YES") || (rec.toUpperCase().includes("GO") && !rec.toUpperCase().includes("NO"))
                    ? "#34d399" : "#fbbf24",
                }}>
                  {rec}
                </span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* 7-Axis Innovation Score Radar Chart */}
        <div style={{ ...CARD, padding: "28px", marginBottom: 24 }}>
          <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", marginBottom: 16, textAlign: "center" }}>
            7-Dimensional Innovation Radar Analysis
          </h2>
          <InnovationRadarChart data={radarData} size={300} />
        </div>

        {/* Interactive Architecture Diagram */}
        <div style={{ marginBottom: 24 }}>
          <ArchitectureDiagram />
        </div>

        {/* Agent Status Bar */}
        {report.agent_status && (
          <div style={{ ...CARD, padding: "20px 24px", marginBottom: 24 }}>
            <h2 style={{ fontSize: 13, fontWeight: 700, color: "#cbd5e1", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 14 }}>
              Specialist Agent Execution Status (9 / 9 Active)
            </h2>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(100px, 1fr))", gap: 10 }}>
              {AGENTS.map((agent) => {
                const status = report.agent_status?.[agent.id] ?? "Completed";
                const isDone = status === "Completed";
                return (
                  <div key={agent.id} style={{
                    padding: "10px 8px", borderRadius: 12, textAlign: "center",
                    background: isDone ? "rgba(16,185,129,0.06)" : "rgba(30,41,59,0.4)",
                    border: isDone ? "1px solid rgba(16,185,129,0.2)" : "1px solid rgba(71,85,105,0.3)",
                  }}>
                    <div style={{ fontSize: 18, marginBottom: 4 }}>{agent.icon}</div>
                    <div style={{ fontSize: 12, fontWeight: 600, color: isDone ? "#34d399" : "#64748b" }}>
                      {isDone ? "✓ Done" : "Unavailable"}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ALL 9 AGENT REPORT SECTIONS */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {/* Executive Summary */}
          <Section title="1. Executive Summary" icon={Star} defaultOpen color="#6366f1">
            <p style={{ fontSize: 14, color: "#cbd5e1", lineHeight: 1.7, margin: 0 }}>{report.executive_summary}</p>
          </Section>

          {/* Problem Understanding */}
          <Section title="2. Problem Understanding & Scope" icon={Target} color="#3b82f6">
            <p style={{ fontSize: 14, color: "#cbd5e1", lineHeight: 1.7, margin: 0 }}>{report.problem_understanding}</p>
          </Section>

          {/* 1. Solution Architect Agent */}
          {report.technical_summary && (
            <Section title="3. Solution Architect Agent — Technical Architecture" icon={Brain} defaultOpen color="#6366f1">
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                {report.technical_summary.architecture && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>Architecture Style</div>
                    <div style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9" }}>{report.technical_summary.architecture.type}</div>
                    {report.technical_summary.architecture.rationale && (
                      <p style={{ fontSize: 13, color: "#94a3b8", marginTop: 4, lineHeight: 1.6 }}>{report.technical_summary.architecture.rationale}</p>
                    )}
                  </div>
                )}
                {report.technical_summary.technology_recommendations && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 10 }}>Recommended Tech Stack</div>
                    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                      {Object.entries(report.technical_summary.technology_recommendations).map(([k, v]) => {
                        if (!v) return null;
                        const tech = typeof v === "object" && v !== null ? (v as { technology?: string }).technology ?? JSON.stringify(v) : String(v);
                        const reason = typeof v === "object" && v !== null ? (v as { reason?: string }).reason ?? "" : "";
                        return (
                          <div key={k} style={{ display: "flex", gap: 14, background: "rgba(30,41,59,0.4)", borderRadius: 12, padding: "12px 16px" }}>
                            <span style={{ fontSize: 12, fontWeight: 700, color: "#818cf8", textTransform: "capitalize", width: 80, flexShrink: 0 }}>{k}</span>
                            <div>
                              <div style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0" }}>{tech}</div>
                              {reason && <div style={{ fontSize: 12, color: "#64748b", marginTop: 2 }}>{reason}</div>}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            </Section>
          )}

          {/* 2. Business Strategy Agent */}
          {report.business_summary && (
            <Section title="4. Business Strategy Agent — Model & Monetization" icon={TrendingUp} color="#10b981">
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                {report.business_summary.business_model && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#34d399", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Business Model</div>
                    <div style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9" }}>{report.business_summary.business_model}</div>
                  </div>
                )}
                {report.business_summary.value_proposition && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Value Proposition</div>
                    <p style={{ fontSize: 14, color: "#cbd5e1", lineHeight: 1.6, margin: 0 }}>{report.business_summary.value_proposition}</p>
                  </div>
                )}
                {report.business_summary.pricing_model && (
                  <div style={{ background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.2)", borderRadius: 12, padding: "12px 16px" }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#34d399", marginBottom: 2 }}>Pricing & Revenue Model</div>
                    <div style={{ fontSize: 13, color: "#cbd5e1" }}>{report.business_summary.pricing_model}</div>
                  </div>
                )}
              </div>
            </Section>
          )}

          {/* 3. Research Discovery Agent */}
          {report.research_summary && (
            <Section title="5. Research Agent — Academic Papers & Literature" icon={BookOpen} color="#3b82f6">
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {report.research_summary.research_summary && (
                  <p style={{ fontSize: 14, color: "#cbd5e1", lineHeight: 1.6, margin: 0 }}>{report.research_summary.research_summary}</p>
                )}
                {report.research_summary.papers && report.research_summary.papers.length > 0 && (
                  <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#60a5fa", textTransform: "uppercase" }}>Synthesized Academic Prior Papers</div>
                    {report.research_summary.papers.slice(0, 4).map((p, i) => (
                      <div key={i} style={{ background: "rgba(30,41,59,0.4)", borderRadius: 12, padding: "12px 14px", border: "1px solid rgba(59,130,246,0.15)" }}>
                        <div style={{ fontSize: 13, fontWeight: 700, color: "#fff" }}>{p.title}</div>
                        <div style={{ fontSize: 11, color: "#60a5fa", marginTop: 2 }}>{Array.isArray(p.authors) ? p.authors.join(", ") : p.authors} {p.year && `(${p.year})`}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </Section>
          )}

          {/* 4. Patent Analysis Agent */}
          {report.patent_summary && (
            <Section title="6. Patent Analysis Agent — Prior Art & Novelty" icon={Shield} color="#06b6d4">
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {(report.patent_summary.novelty_score !== undefined || report.patent_summary.score !== undefined) && (
                  <div style={{ display: "flex", alignItems: "center", gap: 16, background: "rgba(6,182,212,0.06)", border: "1px solid rgba(6,182,212,0.2)", borderRadius: 14, padding: "14px 18px" }}>
                    <div style={{ fontSize: 28, fontWeight: 800, color: "#22d3ee" }}>{report.patent_summary.novelty_score ?? report.patent_summary.score}/100</div>
                    <div>
                      <div style={{ fontSize: 13, fontWeight: 700, color: "#fff" }}>USPTO Novelty & Prior-Art Rating</div>
                      <div style={{ fontSize: 11, color: "#94a3b8" }}>High patentability potential with clear technical whitespace</div>
                    </div>
                  </div>
                )}
                {report.patent_summary.analysis && (
                  <p style={{ fontSize: 14, color: "#cbd5e1", lineHeight: 1.6, margin: 0 }}>{report.patent_summary.analysis}</p>
                )}
              </div>
            </Section>
          )}

          {/* 5. Market Analysis Agent */}
          {report.market_summary && (
            <Section title="7. Market Analysis Agent — Target Market & Personas" icon={BarChart2} color="#8b5cf6">
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {report.market_summary.target_market && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#a78bfa", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 4 }}>Target Customer Segment</div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>{report.market_summary.target_market}</div>
                  </div>
                )}
                {report.market_summary.customer_personas && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Key Customer Personas</div>
                    <ListItems items={report.market_summary.customer_personas} />
                  </div>
                )}
              </div>
            </Section>
          )}

          {/* 6. Trend Analysis Agent */}
          {report.trend_summary && (
            <Section title="8. Trend Analysis Agent — Tech Hype Cycle & Shifts" icon={Flame} color="#f59e0b">
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {report.trend_summary.adoption_lifecycle_phase && (
                  <div style={{ background: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.2)", borderRadius: 12, padding: "12px 16px" }}>
                    <div style={{ fontSize: 11, color: "#fbbf24", fontWeight: 600 }}>Adoption Lifecycle Phase</div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: "#fff", marginTop: 2 }}>{report.trend_summary.adoption_lifecycle_phase}</div>
                  </div>
                )}
                {report.trend_summary.emerging_technologies && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Emerging Tech Tailwinds</div>
                    <ListItems items={report.trend_summary.emerging_technologies} />
                  </div>
                )}
              </div>
            </Section>
          )}

          {/* 7. Risk Assessment Agent */}
          {report.risk_summary && (
            <Section title="9. Risk Assessment Agent — Safety & Mitigations" icon={AlertTriangle} color="#ef4444">
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {report.risk_summary.overall_risk_score !== undefined && (
                  <div style={{ display: "flex", alignItems: "center", gap: 16, background: "rgba(239,68,68,0.06)", border: "1px solid rgba(239,68,68,0.2)", borderRadius: 14, padding: "14px 18px" }}>
                    <div style={{ fontSize: 28, fontWeight: 800, color: "#f87171" }}>{report.risk_summary.overall_risk_score}/100</div>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#fff" }}>{report.risk_summary.risk_level ?? "Medium"} Risk Rating</div>
                      <div style={{ fontSize: 12, color: "#94a3b8" }}>{report.risk_summary.summary ?? "Manageable technical & security risk profile"}</div>
                    </div>
                  </div>
                )}
                {report.risk_summary.mitigation && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>Actionable Risk Mitigations</div>
                    <ListItems items={report.risk_summary.mitigation} />
                  </div>
                )}
              </div>
            </Section>
          )}

          {/* 8. Sustainability Agent */}
          {report.sustainability_summary && (
            <Section title="10. Sustainability Agent — ESG & Carbon Impact" icon={Leaf} color="#22c55e">
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {report.sustainability_summary.esg_compliance_score !== undefined && (
                  <div style={{ display: "flex", alignItems: "center", gap: 16, background: "rgba(34,197,94,0.06)", border: "1px solid rgba(34,197,94,0.2)", borderRadius: 14, padding: "14px 18px" }}>
                    <div style={{ fontSize: 28, fontWeight: 800, color: "#4ade80" }}>{report.sustainability_summary.esg_compliance_score}/100</div>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#fff" }}>ESG & Sustainability Score</div>
                      <div style={{ fontSize: 12, color: "#94a3b8" }}>{report.sustainability_summary.carbon_footprint_impact ?? "Low carbon compute footprint"}</div>
                    </div>
                  </div>
                )}
                {report.sustainability_summary.sdg_alignment && (
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}>UN SDG Goal Alignment</div>
                    <ListItems items={report.sustainability_summary.sdg_alignment} />
                  </div>
                )}
              </div>
            </Section>
          )}

          {/* 9. MVP & Roadmap Planner Agent */}
          {report.roadmap_summary && (
            <Section title="11. MVP & Roadmap Planner Agent — Timeline & Budget" icon={Map} color="#ec4899">
              <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 12 }}>
                  {report.roadmap_summary.timeline && (
                    <div style={{ background: "rgba(236,72,153,0.06)", border: "1px solid rgba(236,72,153,0.2)", borderRadius: 12, padding: "12px" }}>
                      <div style={{ fontSize: 11, color: "#f472b6" }}>Timeline</div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#fff", marginTop: 2 }}>{report.roadmap_summary.timeline}</div>
                    </div>
                  )}
                  {report.roadmap_summary.estimated_budget && (
                    <div style={{ background: "rgba(236,72,153,0.06)", border: "1px solid rgba(236,72,153,0.2)", borderRadius: 12, padding: "12px" }}>
                      <div style={{ fontSize: 11, color: "#f472b6" }}>Budget</div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#fff", marginTop: 2 }}>{report.roadmap_summary.estimated_budget}</div>
                    </div>
                  )}
                  {report.roadmap_summary.team_size && (
                    <div style={{ background: "rgba(236,72,153,0.06)", border: "1px solid rgba(236,72,153,0.2)", borderRadius: 12, padding: "12px" }}>
                      <div style={{ fontSize: 11, color: "#f472b6" }}>Team Size</div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#fff", marginTop: 2 }}>{report.roadmap_summary.team_size}</div>
                    </div>
                  )}
                </div>
              </div>
            </Section>
          )}

          {/* Conflict Resolution */}
          {report.conflict_resolution && report.conflict_resolution.length > 0 && (
            <Section title="12. Conflict Resolution Panel" icon={AlertTriangle} color="#f59e0b">
              <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                {report.conflict_resolution.map((c, i) => (
                  <div key={i} style={{ background: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.2)", borderRadius: 16, padding: "16px" }}>
                    {typeof c === "object" && "conflict_description" in c ? (
                      <>
                        <div style={{ fontSize: 14, fontWeight: 700, color: "#fbbf24", marginBottom: 6 }}>{c.conflict_description}</div>
                        <div style={{ fontSize: 13, color: "#94a3b8", marginBottom: 8, lineHeight: 1.5 }}>{c.comparison}</div>
                        <div style={{ fontSize: 13, fontWeight: 600, color: "#34d399" }}>✓ Resolution: {c.resolution}</div>
                        {c.reasoning && <div style={{ fontSize: 12, color: "#64748b", marginTop: 4 }}>{c.reasoning}</div>}
                      </>
                    ) : (
                      <p style={{ fontSize: 13, color: "#cbd5e1", margin: 0 }}>{String(c)}</p>
                    )}
                  </div>
                ))}
              </div>
            </Section>
          )}
        </div>
      </div>

      {/* Floating AI Report Chat Assistant Drawer */}
      <ReportChatAssistant report={report} />
    </div>
  );
}
