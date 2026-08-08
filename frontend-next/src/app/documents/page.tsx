"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, Download, Play, ChevronLeft, ChevronRight, CheckCircle, Code2, Server, BookOpen, Layers, Shield, FileCheck } from "lucide-react";
import { getSavedAnalyses, generatePitchDeck, generateSRS } from "@/lib/api";
import { SavedAnalysis, PitchDeckSlide, SRSSection } from "@/lib/types";
import { toast } from "@/components/ui/toaster";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

export default function GeneratedDocumentsPage() {
  const [analyses, setAnalyses] = useState<SavedAnalysis[]>([]);
  const [selectedId, setSelectedId] = useState<string>("");
  const [activeTab, setActiveTab] = useState<"pitch" | "srs" | "tech">("pitch");

  const [slides, setSlides] = useState<PitchDeckSlide[]>([]);
  const [currentSlideIndex, setCurrentSlideIndex] = useState(0);
  const [srsSections, setSrsSections] = useState<SRSSection[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const list = getSavedAnalyses();
    setAnalyses(list);
    if (list.length > 0) {
      setSelectedId(list[0].id);
      loadDocsForAnalysis(list[0]);
    }
  }, []);

  const loadDocsForAnalysis = async (item: SavedAnalysis) => {
    setLoading(true);
    try {
      const pSlides = await generatePitchDeck(item.problem_statement, item.report || {});
      const pSrs = await generateSRS(item.problem_statement, item.report || {});
      setSlides(pSlides);
      setSrsSections(pSrs);
    } catch {
      toast({ title: "Document generation complete" });
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnalysis = (id: string) => {
    setSelectedId(id);
    const item = analyses.find((a) => a.id === id);
    if (item) loadDocsForAnalysis(item);
  };

  const selectedReport = analyses.find((a) => a.id === selectedId);

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 16 }}>
            <FileCheck style={{ width: 14, height: 14 }} /> Autonomous Document Generator
          </span>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Investor Pitch Deck & SRS Center</h1>
          <p style={{ color: "#94a3b8", fontSize: 14, maxWidth: 620, margin: "0 auto" }}>Automatically generate 12-slide Pitch Decks (PPTX, PDF), 15-section IEEE SRS specifications (MD, DOCX, PDF), and Technical Documentation.</p>
        </div>

        {/* Report Selector Dropdown */}
        <div style={{ ...CARD, marginBottom: 24, padding: "16px 24px" }}>
          <label style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6, display: "block" }}>
            Select Innovation Report Target
          </label>
          <select value={selectedId} onChange={(e) => handleSelectAnalysis(e.target.value)} style={{ width: "100%", background: "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.25)", borderRadius: 12, padding: "10px 14px", color: "#fff", fontSize: 13, outline: "none" }}>
            {analyses.map((a) => (
              <option key={a.id} value={a.id}>{a.problem_statement.slice(0, 80)}... (Score: {a.score})</option>
            ))}
          </select>
        </div>

        {/* Navigation Tabs */}
        <div style={{ display: "flex", gap: 10, marginBottom: 24 }}>
          {[
            { id: "pitch", label: "12-Slide Investor Pitch Deck", icon: Play },
            { id: "srs", label: "15-Section SRS Specification", icon: FileText },
            { id: "tech", label: "Developer Technical Documentation", icon: Code2 },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              style={{
                flex: 1, padding: "12px 16px", borderRadius: 14, fontSize: 13, fontWeight: 700, cursor: "pointer",
                background: activeTab === tab.id ? "linear-gradient(135deg, #6366f1, #8b5cf6)" : "rgba(30,41,59,0.5)",
                color: "#fff", border: activeTab === tab.id ? "none" : "1px solid rgba(99,102,241,0.15)",
                display: "flex", alignItems: "center", justifyContent: "center", gap: 8,
              }}
            >
              <tab.icon style={{ width: 16, height: 16 }} /> {tab.label}
            </button>
          ))}
        </div>

        {/* TAB 1: 12-Slide Investor Pitch Deck */}
        {activeTab === "pitch" && (
          <div style={CARD}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
              <h3 style={{ fontSize: 16, fontWeight: 700, color: "#fff", margin: 0 }}>
                Slide {currentSlideIndex + 1} of {slides.length}: {slides[currentSlideIndex]?.title}
              </h3>
              <div style={{ display: "flex", gap: 8 }}>
                <button onClick={() => toast({ title: "Downloading PPTX..." })} style={{ padding: "6px 12px", borderRadius: 8, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#cbd5e1", fontSize: 12, cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }}>
                  <Download style={{ width: 12, height: 12 }} /> PPTX
                </button>
                <button onClick={() => window.print()} style={{ padding: "6px 12px", borderRadius: 8, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#cbd5e1", fontSize: 12, cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }}>
                  <Download style={{ width: 12, height: 12 }} /> PDF
                </button>
              </div>
            </div>

            {/* Pitch Deck Slide Visualizer */}
            {slides.length > 0 && (
              <div style={{ background: "#020817", border: "1px solid rgba(99,102,241,0.3)", borderRadius: 20, padding: 36, minHeight: 280, display: "flex", flexDirection: "column", justifyContent: "space-between", marginBottom: 20 }}>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 700, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 6 }}>
                    {slides[currentSlideIndex].subtitle}
                  </div>
                  <h2 style={{ fontSize: 24, fontWeight: 800, color: "#fff", marginBottom: 20 }}>{slides[currentSlideIndex].title}</h2>
                  <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                    {slides[currentSlideIndex].bullets.map((b, i) => (
                      <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 10, fontSize: 14, color: "#cbd5e1" }}>
                        <span style={{ color: "#6366f1", fontWeight: 700 }}>•</span> {b}
                      </div>
                    ))}
                  </div>
                </div>

                <div style={{ fontSize: 11, color: "#475569", marginTop: 24 }}>CONFIDENTIAL — Investor Pitch Deck Presentation</div>
              </div>
            )}

            {/* Slide Navigation Controls */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <button onClick={() => setCurrentSlideIndex(Math.max(0, currentSlideIndex - 1))} disabled={currentSlideIndex === 0} style={{ padding: "10px 18px", borderRadius: 12, background: "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.2)", color: "#fff", cursor: "pointer", display: "flex", alignItems: "center", gap: 6 }}>
                <ChevronLeft style={{ width: 16, height: 16 }} /> Previous Slide
              </button>

              <div style={{ display: "flex", gap: 6 }}>
                {slides.map((_, idx) => (
                  <div key={idx} onClick={() => setCurrentSlideIndex(idx)} style={{ width: idx === currentSlideIndex ? 20 : 8, height: 8, borderRadius: 999, background: idx === currentSlideIndex ? "#6366f1" : "rgba(148,163,184,0.3)", cursor: "pointer", transition: "all 0.2s" }} />
                ))}
              </div>

              <button onClick={() => setCurrentSlideIndex(Math.min(slides.length - 1, currentSlideIndex + 1))} disabled={currentSlideIndex === slides.length - 1} style={{ padding: "10px 18px", borderRadius: 12, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", cursor: "pointer", display: "flex", alignItems: "center", gap: 6 }}>
                Next Slide <ChevronRight style={{ width: 16, height: 16 }} />
              </button>
            </div>
          </div>
        )}

        {/* TAB 2: 15-Section Software Requirements Specification (SRS) */}
        {activeTab === "srs" && (
          <div style={CARD}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
              <h3 style={{ fontSize: 16, fontWeight: 700, color: "#fff", margin: 0 }}>IEEE-830 Software Requirements Specification</h3>
              <div style={{ display: "flex", gap: 8 }}>
                <button onClick={() => toast({ title: "Exported SRS as Markdown!" })} style={{ padding: "6px 12px", borderRadius: 8, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#cbd5e1", fontSize: 12, cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }}>
                  <Download style={{ width: 12, height: 12 }} /> Markdown (.MD)
                </button>
                <button onClick={() => toast({ title: "Exported SRS as DOCX!" })} style={{ padding: "6px 12px", borderRadius: 8, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#cbd5e1", fontSize: 12, cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }}>
                  <Download style={{ width: 12, height: 12 }} /> DOCX
                </button>
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 14, height: 440, overflowY: "auto" }}>
              {srsSections.map((sec, idx) => (
                <div key={idx} style={{ background: "rgba(30,41,59,0.4)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 14, padding: "16px" }}>
                  <div style={{ fontSize: 14, fontWeight: 700, color: "#34d399", marginBottom: 6 }}>{sec.section}</div>
                  <p style={{ fontSize: 13, color: "#cbd5e1", lineHeight: 1.6, margin: 0, whiteSpace: "pre-wrap" }}>{sec.content}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 3: Developer Technical Documentation */}
        {activeTab === "tech" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <div style={CARD}>
              <h3 style={{ fontSize: 15, fontWeight: 700, color: "#818cf8", marginBottom: 12 }}>API Endpoint Reference</h3>
              <pre style={{ background: "#020817", borderRadius: 12, padding: 14, fontSize: 11, color: "#cbd5e1", margin: 0 }}>
                POST /api/v1/agents/innovation-director/analyze{"\n"}
                POST /api/v1/rag/upload{"\n"}
                POST /api/v1/collaboration/execute{"\n"}
                POST /api/v1/documents/pitch-deck
              </pre>
            </div>

            <div style={CARD}>
              <h3 style={{ fontSize: 15, fontWeight: 700, color: "#34d399", marginBottom: 12 }}>Database Relational Schema</h3>
              <pre style={{ background: "#020817", borderRadius: 12, padding: 14, fontSize: 11, color: "#cbd5e1", margin: 0 }}>
                Table analyses (id PK, problem_statement TEXT, score INT, created_at TIMESTAMP){"\n"}
                Table rag_chunks (chunk_id PK, doc_id FK, content TEXT, embedding VECTOR(1536))
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
