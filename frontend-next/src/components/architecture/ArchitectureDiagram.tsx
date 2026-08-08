"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Monitor, Server, Database, Cpu, Layers, HardDrive, Wifi, Shield, X, ZoomIn, ZoomOut } from "lucide-react";

interface NodeDetail {
  id: string;
  name: string;
  category: "Frontend" | "Backend" | "Database" | "Cache" | "Queue" | "AI Models" | "APIs";
  tech: string;
  icon: React.ElementType;
  color: string;
  description: string;
}

const architectureNodes: NodeDetail[] = [
  { id: "frontend", name: "Client Layer", category: "Frontend", tech: "Next.js 15 + React 19", icon: Monitor, color: "#6366f1", description: "Glassmorphism UI rendering, real-time agent visualization, client state management." },
  { id: "backend", name: "API Gateway", category: "Backend", tech: "FastAPI + AsyncIO", icon: Server, color: "#10b981", description: "High-throughput asynchronous REST API gateway routing requests to agent microservices." },
  { id: "director", name: "Director Orchestrator", category: "AI Models", tech: "Innovation Director Agent", icon: Cpu, color: "#8b5cf6", description: "Master AI orchestrator driving concurrent 9-agent dispatches, response validation, and synthesis." },
  { id: "database", name: "Primary Database", category: "Database", tech: "PostgreSQL + pgvector", icon: Database, color: "#3b82f6", description: "Relational data store for structured reports and vector embeddings for patent & prior-art search." },
  { id: "cache", name: "Caching Layer", category: "Cache", tech: "Redis", icon: HardDrive, color: "#ef4444", description: "Low-latency in-memory cache for paper metadata, patent candidates, and rate limit tokens." },
  { id: "llm", name: "AI Inference Stack", category: "AI Models", tech: "Groq LLaMA-3.3 70B & 8B", icon: Layers, color: "#f59e0b", description: "Sub-second LLM inference pipeline running specialized system prompts." },
  { id: "apis", name: "External APIs", category: "APIs", tech: "arXiv + Semantic Scholar + USPTO", icon: Wifi, color: "#06b6d4", description: "Multi-source research paper query engine and patent office prior art search APIs." },
];

export function ArchitectureDiagram() {
  const [selectedNode, setSelectedNode] = useState<NodeDetail | null>(null);
  const [zoom, setZoom] = useState(1);

  return (
    <div style={{ background: "rgba(15,23,42,0.8)", borderRadius: 20, border: "1px solid rgba(99,102,241,0.15)", padding: 24 }}>
      {/* Controls Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <div>
          <h3 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>System Architecture Diagram</h3>
          <p style={{ fontSize: 12, color: "#64748b", margin: "2px 0 0" }}>Click any component node to inspect technology details</p>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <button onClick={() => setZoom(Math.min(zoom + 0.15, 1.4))} style={{ width: 32, height: 32, borderRadius: 8, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", display: "flex", alignItems: "center", justifyContent: "center", color: "#cbd5e1", cursor: "pointer" }}>
            <ZoomIn style={{ width: 14, height: 14 }} />
          </button>
          <button onClick={() => setZoom(Math.max(zoom - 0.15, 0.75))} style={{ width: 32, height: 32, borderRadius: 8, background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", display: "flex", alignItems: "center", justifyContent: "center", color: "#cbd5e1", cursor: "pointer" }}>
            <ZoomOut style={{ width: 14, height: 14 }} />
          </button>
        </div>
      </div>

      {/* Interactive Node Map */}
      <div style={{ transform: `scale(${zoom})`, transformOrigin: "top center", transition: "transform 0.2s", display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 16 }}>
        {architectureNodes.map((node) => {
          const Icon = node.icon;
          return (
            <motion.div
              key={node.id}
              whileHover={{ scale: 1.03 }}
              onClick={() => setSelectedNode(node)}
              style={{
                background: "rgba(30,41,59,0.5)",
                border: `1px solid ${node.color}40`,
                borderRadius: 16,
                padding: "16px",
                cursor: "pointer",
                boxShadow: `0 4px 20px ${node.color}15`,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 10 }}>
                <div style={{ width: 36, height: 36, borderRadius: 10, background: `${node.color}15`, border: `1px solid ${node.color}30`, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                  <Icon style={{ width: 18, height: 18, color: node.color }} />
                </div>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: "#f1f5f9" }}>{node.name}</div>
                  <div style={{ fontSize: 11, color: node.color, fontWeight: 600 }}>{node.category}</div>
                </div>
              </div>
              <div style={{ fontSize: 12, color: "#cbd5e1", background: "rgba(15,23,42,0.6)", borderRadius: 8, padding: "6px 10px" }}>
                {node.tech}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Tech Details Modal */}
      <AnimatePresence>
        {selectedNode && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedNode(null)}
            style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.6)", backdropFilter: "blur(8px)", zIndex: 3000, display: "flex", alignItems: "center", justifyContent: "center", padding: 20 }}
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              onClick={(e) => e.stopPropagation()}
              style={{ background: "#0f172a", border: `1px solid ${selectedNode.color}50`, borderRadius: 24, padding: 28, maxWidth: 440, width: "100%" }}
            >
              <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 16 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <div style={{ width: 44, height: 44, borderRadius: 12, background: `${selectedNode.color}20`, border: `1px solid ${selectedNode.color}40`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <selectedNode.icon style={{ width: 22, height: 22, color: selectedNode.color }} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: 18, fontWeight: 800, color: "#fff", margin: 0 }}>{selectedNode.name}</h3>
                    <span style={{ fontSize: 12, color: selectedNode.color, fontWeight: 600 }}>{selectedNode.category}</span>
                  </div>
                </div>
                <button onClick={() => setSelectedNode(null)} style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer" }}>
                  <X style={{ width: 18, height: 18 }} />
                </button>
              </div>

              <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: 12, padding: "12px 14px", marginBottom: 16 }}>
                <div style={{ fontSize: 11, color: "#64748b", marginBottom: 2 }}>Technology Stack</div>
                <div style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9" }}>{selectedNode.tech}</div>
              </div>

              <p style={{ fontSize: 13, color: "#cbd5e1", lineHeight: 1.6, margin: 0 }}>{selectedNode.description}</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
