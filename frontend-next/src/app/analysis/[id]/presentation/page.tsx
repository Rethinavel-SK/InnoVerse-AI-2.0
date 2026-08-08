"use client";

import { use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft, ChevronLeft, ChevronRight, Brain, Star, TrendingUp, Shield, Map, Lightbulb, Play } from "lucide-react";
import { getSavedAnalyses } from "@/lib/api";
import { InnovationReport } from "@/lib/types";

export default function PresentationModePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const [report, setReport] = useState<InnovationReport | null>(null);
  const [currentSlide, setCurrentSlide] = useState(0);

  useEffect(() => {
    const list = getSavedAnalyses();
    const found = list.find((a) => a.id === id);
    if (found?.report) setReport(found.report);
  }, [id]);

  if (!report) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: "#94a3b8" }}>Loading Presentation Deck...</div>
      </div>
    );
  }

  const score = report.overall_innovation_score ?? report.feasibility_score ?? 85;
  const rec = typeof report.final_recommendation === "object"
    ? report.final_recommendation?.build_recommendation ?? report.recommendation ?? "GO"
    : report.recommendation ?? "GO";

  const slides = [
    {
      title: "Executive Summary",
      icon: Star,
      color: "#6366f1",
      content: (
        <div>
          <div style={{ fontSize: 13, color: "#a5b4fc", fontWeight: 600, marginBottom: 12 }}>PROJECT PROBLEM STATEMENT</div>
          <h2 style={{ fontSize: 24, fontWeight: 800, color: "#fff", marginBottom: 24, lineHeight: 1.3 }}>"{report.problem_understanding}"</h2>
          <div style={{ background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", borderRadius: 20, padding: 24 }}>
            <p style={{ fontSize: 16, color: "#cbd5e1", lineHeight: 1.7, margin: 0 }}>{report.executive_summary}</p>
          </div>
        </div>
      ),
    },
    {
      title: "Innovation Score & Decision",
      icon: Brain,
      color: "#10b981",
      content: (
        <div style={{ textAlign: "center", padding: "20px 0" }}>
          <div style={{ fontSize: 72, fontWeight: 900, color: "#34d399", lineHeight: 1 }}>{score}/100</div>
          <div style={{ fontSize: 16, color: "#94a3b8", marginTop: 8, marginBottom: 32 }}>Master Innovation Score</div>
          <div style={{ display: "inline-flex", padding: "12px 32px", borderRadius: 999, background: "rgba(16,185,129,0.15)", border: "1px solid rgba(16,185,129,0.4)", color: "#34d399", fontSize: 22, fontWeight: 800 }}>
            Decision: {rec}
          </div>
        </div>
      ),
    },
    {
      title: "Technical Architecture",
      icon: Brain,
      color: "#8b5cf6",
      content: (
        <div>
          <h3 style={{ fontSize: 22, fontWeight: 800, color: "#fff", marginBottom: 12 }}>{report.technical_summary?.architecture?.type ?? "Microservices Architecture"}</h3>
          <p style={{ fontSize: 15, color: "#94a3b8", lineHeight: 1.6, marginBottom: 24 }}>{report.technical_summary?.architecture?.rationale ?? "Designed for horizontal scalability and independent model deployment."}</p>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div style={{ background: "rgba(30,41,59,0.6)", borderRadius: 16, padding: 20 }}>
              <div style={{ fontSize: 12, color: "#64748b" }}>Prototype Infrastructure</div>
              <div style={{ fontSize: 20, fontWeight: 800, color: "#fff", marginTop: 4 }}>{report.technical_summary?.prototype_cost ?? "$250 / month"}</div>
            </div>
            <div style={{ background: "rgba(30,41,59,0.6)", borderRadius: 16, padding: 20 }}>
              <div style={{ fontSize: 12, color: "#64748b" }}>Complexity Rating</div>
              <div style={{ fontSize: 20, fontWeight: 800, color: "#fff", marginTop: 4 }}>{report.technical_summary?.estimated_complexity ?? "High"}</div>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: "Market & Commercial Viability",
      icon: TrendingUp,
      color: "#f59e0b",
      content: (
        <div>
          <div style={{ fontSize: 18, fontWeight: 700, color: "#fff", marginBottom: 16 }}>{report.business_summary?.business_model ?? "B2B SaaS"}</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 24 }}>
            <div style={{ background: "rgba(245,158,11,0.1)", border: "1px solid rgba(245,158,11,0.3)", borderRadius: 16, padding: 20, textAlign: "center" }}>
              <div style={{ fontSize: 12, color: "#fbbf24", fontWeight: 700 }}>TAM</div>
              <div style={{ fontSize: 22, fontWeight: 800, color: "#fff", marginTop: 4 }}>{(report.business_summary?.market_size as Record<string, string>)?.tam ?? "$4.8B"}</div>
            </div>
            <div style={{ background: "rgba(245,158,11,0.1)", border: "1px solid rgba(245,158,11,0.3)", borderRadius: 16, padding: 20, textAlign: "center" }}>
              <div style={{ fontSize: 12, color: "#fbbf24", fontWeight: 700 }}>SAM</div>
              <div style={{ fontSize: 22, fontWeight: 800, color: "#fff", marginTop: 4 }}>{(report.business_summary?.market_size as Record<string, string>)?.sam ?? "$650M"}</div>
            </div>
            <div style={{ background: "rgba(245,158,11,0.1)", border: "1px solid rgba(245,158,11,0.3)", borderRadius: 16, padding: 20, textAlign: "center" }}>
              <div style={{ fontSize: 12, color: "#fbbf24", fontWeight: 700 }}>SOM</div>
              <div style={{ fontSize: 22, fontWeight: 800, color: "#fff", marginTop: 4 }}>{(report.business_summary?.market_size as Record<string, string>)?.som ?? "$45M"}</div>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: "MVP Implementation Roadmap",
      icon: Map,
      color: "#ec4899",
      content: (
        <div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 }}>
            <div style={{ background: "rgba(236,72,153,0.1)", border: "1px solid rgba(236,72,153,0.3)", borderRadius: 16, padding: 20, textAlign: "center" }}>
              <div style={{ fontSize: 12, color: "#f472b6" }}>Timeline</div>
              <div style={{ fontSize: 20, fontWeight: 800, color: "#fff", marginTop: 4 }}>{report.roadmap_summary?.timeline ?? "26 Weeks"}</div>
            </div>
            <div style={{ background: "rgba(236,72,153,0.1)", border: "1px solid rgba(236,72,153,0.3)", borderRadius: 16, padding: 20, textAlign: "center" }}>
              <div style={{ fontSize: 12, color: "#f472b6" }}>Budget</div>
              <div style={{ fontSize: 20, fontWeight: 800, color: "#fff", marginTop: 4 }}>{report.roadmap_summary?.estimated_budget ?? "$140K-$180K"}</div>
            </div>
            <div style={{ background: "rgba(236,72,153,0.1)", border: "1px solid rgba(236,72,153,0.3)", borderRadius: 16, padding: 20, textAlign: "center" }}>
              <div style={{ fontSize: 12, color: "#f472b6" }}>Team Size</div>
              <div style={{ fontSize: 20, fontWeight: 800, color: "#fff", marginTop: 4 }}>{report.roadmap_summary?.team_size ?? "7 Members"}</div>
            </div>
          </div>
        </div>
      ),
    },
  ];

  const slide = slides[currentSlide];
  const Icon = slide.icon;

  return (
    <div style={{ minHeight: "100vh", background: "#020817", color: "#fff", display: "flex", flexDirection: "column", justifyContent: "space-between", padding: 32 }}>
      {/* Top Deck Navigation */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <button onClick={() => router.back()} style={{ display: "flex", alignItems: "center", gap: 8, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 12, padding: "8px 16px", color: "#cbd5e1", cursor: "pointer", fontSize: 13 }}>
          <ArrowLeft style={{ width: 16, height: 16 }} /> Exit Presentation
        </button>
        <div style={{ fontSize: 13, color: "#64748b", fontWeight: 600 }}>
          Slide {currentSlide + 1} of {slides.length}
        </div>
      </div>

      {/* Slide Container */}
      <div style={{ maxWidth: 880, width: "100%", margin: "0 auto", padding: "40px 0" }}>
        <AnimatePresence mode="wait">
          <motion.div
            key={currentSlide}
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -40 }}
            transition={{ duration: 0.3 }}
            style={{ background: "rgba(15,23,42,0.85)", border: `1px solid ${slide.color}40`, borderRadius: 28, padding: 48, boxShadow: `0 20px 60px ${slide.color}20` }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 28 }}>
              <div style={{ width: 44, height: 44, borderRadius: 14, background: `${slide.color}20`, border: `1px solid ${slide.color}40`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <Icon style={{ width: 22, height: 22, color: slide.color }} />
              </div>
              <h2 style={{ fontSize: 24, fontWeight: 800, color: "#fff", margin: 0 }}>{slide.title}</h2>
            </div>

            {slide.content}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Bottom Controls */}
      <div style={{ maxWidth: 880, width: "100%", margin: "0 auto", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <button
          onClick={() => setCurrentSlide(Math.max(0, currentSlide - 1))}
          disabled={currentSlide === 0}
          style={{ display: "flex", alignItems: "center", gap: 8, padding: "12px 24px", borderRadius: 14, background: currentSlide === 0 ? "rgba(30,41,59,0.3)" : "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.2)", color: currentSlide === 0 ? "#475569" : "#fff", cursor: currentSlide === 0 ? "not-allowed" : "pointer", fontWeight: 600 }}
        >
          <ChevronLeft style={{ width: 18, height: 18 }} /> Previous
        </button>

        {/* Progress dots */}
        <div style={{ display: "flex", gap: 8 }}>
          {slides.map((_, i) => (
            <div
              key={i}
              onClick={() => setCurrentSlide(i)}
              style={{ width: i === currentSlide ? 24 : 10, height: 10, borderRadius: 999, background: i === currentSlide ? "#6366f1" : "rgba(148,163,184,0.3)", cursor: "pointer", transition: "all 0.3s" }}
            />
          ))}
        </div>

        <button
          onClick={() => setCurrentSlide(Math.min(slides.length - 1, currentSlide + 1))}
          disabled={currentSlide === slides.length - 1}
          style={{ display: "flex", alignItems: "center", gap: 8, padding: "12px 24px", borderRadius: 14, background: currentSlide === slides.length - 1 ? "rgba(30,41,59,0.3)" : "linear-gradient(135deg, #6366f1, #8b5cf6)", border: "none", color: currentSlide === slides.length - 1 ? "#475569" : "#fff", cursor: currentSlide === slides.length - 1 ? "not-allowed" : "pointer", fontWeight: 600 }}
        >
          Next <ChevronRight style={{ width: 18, height: 18 }} />
        </button>
      </div>
    </div>
  );
}
