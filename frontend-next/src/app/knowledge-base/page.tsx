"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Database, Upload, Search, Trash2, FileText, CheckCircle, Clock, HardDrive, Sparkles, Layers, BookOpen } from "lucide-react";
import { uploadKnowledgeDocument, getKnowledgeDocuments, searchKnowledgeBase, deleteKnowledgeDocument } from "@/lib/api";
import { KnowledgeDocument, DocumentChunk } from "@/lib/types";
import { toast } from "@/components/ui/toaster";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

export default function KnowledgeBasePage() {
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([]);
  const [uploading, setUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<DocumentChunk[]>([]);
  const [searching, setSearching] = useState(false);
  const [selectedChunk, setSelectedChunk] = useState<DocumentChunk | null>(null);

  useEffect(() => {
    loadDocs();
  }, []);

  const loadDocs = async () => {
    const list = await getKnowledgeDocuments();
    setDocuments(list);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    setUploading(true);

    try {
      for (let i = 0; i < files.length; i++) {
        await uploadKnowledgeDocument(files[i]);
      }
      toast({ title: "Documents uploaded and indexed!", variant: "success" });
      await loadDocs();
    } catch (err) {
      toast({ title: "Upload failed", variant: "destructive" });
    } finally {
      setUploading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    try {
      const results = await searchKnowledgeBase(searchQuery);
      setSearchResults(results);
      if (results.length === 0) {
        toast({ title: "No relevant chunks found." });
      }
    } catch {
      toast({ title: "Search failed", variant: "destructive" });
    } finally {
      setSearching(false);
    }
  };

  const handleDelete = async (docId: string) => {
    try {
      await deleteKnowledgeDocument(docId);
      toast({ title: "Document removed from RAG index." });
      await loadDocs();
    } catch {
      toast({ title: "Delete failed", variant: "destructive" });
    }
  };

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 16 }}>
            <Database style={{ width: 14, height: 14 }} /> RAG Vector Knowledge Base
          </span>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Enterprise Document Ingestion</h1>
          <p style={{ color: "#94a3b8", fontSize: 14, maxWidth: 620, margin: "0 auto" }}>Upload PDFs, Research Papers, DOCX, and Technical Specs. Context is automatically chunked, embedded, and supplied to all 9 AI agents.</p>
        </div>

        {/* Top Action Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 28 }}>
          {/* Upload Card */}
          <div style={CARD}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#fff", marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
              <Upload style={{ width: 16, height: 16, color: "#6366f1" }} /> Upload Enterprise Documents
            </h3>
            <label style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: 140, border: "2px dashed rgba(99,102,241,0.3)", borderRadius: 16, background: "rgba(30,41,59,0.3)", cursor: "pointer", transition: "all 0.2s" }}>
              <Upload style={{ width: 28, height: 28, color: "#818cf8", marginBottom: 8 }} />
              <span style={{ fontSize: 13, fontWeight: 600, color: "#f1f5f9" }}>
                {uploading ? "Uploading & Indexing..." : "Click or Drag PDF, DOCX, PPTX, TXT"}
              </span>
              <span style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>Chunked automatically with TF-IDF Vector Embeddings</span>
              <input type="file" multiple accept=".pdf,.docx,.pptx,.txt,.md" onChange={handleFileUpload} disabled={uploading} style={{ display: "none" }} />
            </label>
          </div>

          {/* Semantic Search Tester Card */}
          <div style={CARD}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#fff", marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
              <Search style={{ width: 16, height: 16, color: "#34d399" }} /> Semantic Vector Search
            </h3>
            <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
              <input
                type="text"
                placeholder="Query vector index (e.g. cloud architecture, TAM, security)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                style={{ flex: 1, background: "rgba(30,41,59,0.5)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 12, padding: "10px 14px", fontSize: 13, color: "#fff", outline: "none" }}
              />
              <button onClick={handleSearch} disabled={searching} style={{ padding: "10px 18px", borderRadius: 12, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", color: "#fff", fontSize: 13, fontWeight: 700, border: "none", cursor: "pointer" }}>
                {searching ? "Searching..." : "Search"}
              </button>
            </div>
            <div style={{ fontSize: 11, color: "#64748b" }}>Tests top-k semantic retrieval score (%) against active vector chunks</div>
          </div>
        </div>

        {/* Search Results Preview */}
        {searchResults.length > 0 && (
          <div style={{ ...CARD, marginBottom: 28 }}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#34d399", marginBottom: 16 }}>
              Top Semantic Search Results ({searchResults.length})
            </h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 12 }}>
              {searchResults.map((res) => (
                <div key={res.chunk_id} onClick={() => setSelectedChunk(res)} style={{ background: "rgba(30,41,59,0.5)", border: "1px solid rgba(52,211,153,0.3)", borderRadius: 14, padding: 14, cursor: "pointer" }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 6 }}>
                    <span style={{ fontSize: 12, fontWeight: 700, color: "#fff" }}>{res.doc_name}</span>
                    <span style={{ fontSize: 11, fontWeight: 700, color: "#34d399", padding: "2px 8px", borderRadius: 999, background: "rgba(16,185,129,0.1)" }}>{res.score}% Match</span>
                  </div>
                  <p style={{ fontSize: 12, color: "#94a3b8", margin: 0, lineHeight: 1.5, display: "-webkit-box", WebkitLineClamp: 3, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                    {res.content}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Indexed Documents Table */}
        <div style={CARD}>
          <h3 style={{ fontSize: 15, fontWeight: 700, color: "#fff", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
            <Layers style={{ width: 16, height: 16, color: "#818cf8" }} /> Indexed Enterprise Knowledge Documents ({documents.length})
          </h3>

          {documents.length > 0 ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {documents.map((doc) => (
                <div key={doc.doc_id} style={{ background: "rgba(30,41,59,0.4)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 14, padding: "14px 18px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <div style={{ width: 36, height: 36, borderRadius: 10, background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)", display: "flex", alignItems: "center", justifyContent: "center flexShrink: 0" }}>
                      <FileText style={{ width: 18, height: 18, color: "#818cf8" }} />
                    </div>
                    <div>
                      <div style={{ fontSize: 14, fontWeight: 700, color: "#fff" }}>{doc.filename}</div>
                      <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>
                        Format: <span style={{ color: "#a5b4fc" }}>{doc.file_type}</span> • {doc.total_chunks} Chunks • Uploaded {doc.upload_date}
                      </div>
                    </div>
                  </div>

                  <button onClick={() => handleDelete(doc.doc_id)} style={{ background: "transparent", border: "none", color: "#f87171", cursor: "pointer", padding: 6 }}>
                    <Trash2 style={{ width: 16, height: 16 }} />
                  </button>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: "center", padding: "40px 20px", color: "#64748b" }}>
              <BookOpen style={{ width: 40, height: 40, color: "#334155", margin: "0 auto 12px" }} />
              <div>No enterprise documents indexed yet. Upload PDFs or DOCX above.</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
