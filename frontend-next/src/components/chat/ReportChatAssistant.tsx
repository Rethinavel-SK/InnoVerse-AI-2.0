"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, Send, X, Bot, User, Sparkles } from "lucide-react";
import { InnovationReport, ChatMessage } from "@/lib/types";

interface ReportChatAssistantProps {
  report: InnovationReport;
}

export function ReportChatAssistant({ report }: ReportChatAssistantProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      sender: "assistant",
      content: "Hello! I am your Innovation Report Assistant. Ask me anything about your technical architecture, business strategy, risks, or roadmap!",
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: "user",
      content: input.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    const userQuery = input.trim();
    setInput("");

    // Simulate context-aware AI response based on generated report content
    setTimeout(() => {
      let reply = "Based on your Innovation Report: ";
      const lower = userQuery.toLowerCase();

      if (lower.includes("microservice") || lower.includes("architecture")) {
        const arch = report.technical_summary?.architecture?.type ?? "Microservices Architecture";
        const rat = report.technical_summary?.architecture?.rationale ?? "Chosen for horizontal scalability and independent deployment.";
        reply += `The Solution Architect recommended **${arch}**. ${rat}`;
      } else if (lower.includes("cheap") || lower.includes("cost") || lower.includes("budget")) {
        const proto = report.technical_summary?.prototype_cost ?? "$250/mo";
        const bud = report.roadmap_summary?.estimated_budget ?? "$140K-$180K";
        reply += `The estimated prototype infrastructure cost is **${proto}**, and the 3-phase development budget is **${bud}**. You can lower early costs by starting with serverless functions and free cloud tiers.`;
      } else if (lower.includes("risk")) {
        const score = report.risk_summary?.overall_risk_score ?? 68;
        const sum = report.risk_summary?.summary ?? "Manageable technical and security risks with automated testing.";
        reply += `The overall risk score is **${score}/100**. ${sum}`;
      } else if (lower.includes("roadmap") || lower.includes("timeline")) {
        const time = report.roadmap_summary?.timeline ?? "26 Weeks";
        reply += `The current implementation roadmap is estimated at **${time}**. You can accelerate Phase 1 by focusing solely on core authentication and MVP APIs.`;
      } else {
        reply += `The Executive Summary highlights: "${report.executive_summary.slice(0, 180)}..."`;
      }

      const botMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "assistant",
        content: reply,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, botMsg]);
    }, 600);
  };

  const presetQuestions = [
    "Why Microservices?",
    "Can this be built cheaper?",
    "Explain the top risks",
    "Shorten the roadmap",
  ];

  return (
    <>
      {/* Floating Trigger Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(true)}
        style={{
          position: "fixed",
          bottom: 24,
          right: 24,
          zIndex: 2000,
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "12px 20px",
          borderRadius: 999,
          background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
          color: "#fff",
          fontSize: 14,
          fontWeight: 600,
          border: "none",
          cursor: "pointer",
          boxShadow: "0 8px 32px rgba(99,102,241,0.4)",
        }}
      >
        <Sparkles style={{ width: 18, height: 18 }} />
        AI Report Assistant
      </motion.button>

      {/* Chat Drawer */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.95 }}
            style={{
              position: "fixed",
              bottom: 88,
              right: 24,
              width: 380,
              maxHeight: 560,
              height: "75vh",
              zIndex: 2100,
              background: "#0f172a",
              border: "1px solid rgba(99,102,241,0.3)",
              borderRadius: 24,
              boxShadow: "0 20px 50px rgba(0,0,0,0.6)",
              display: "flex",
              flexDirection: "column",
              overflow: "hidden",
            }}
          >
            {/* Chat Header */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "16px 20px", background: "rgba(30,41,59,0.8)", borderBottom: "1px solid rgba(99,102,241,0.15)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ width: 32, height: 32, borderRadius: 10, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <Bot style={{ width: 18, height: 18, color: "#fff" }} />
                </div>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 700, color: "#fff" }}>AI Report Assistant</div>
                  <div style={{ fontSize: 11, color: "#34d399" }}>● Connected to Report Context</div>
                </div>
              </div>
              <button onClick={() => setIsOpen(false)} style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer" }}>
                <X style={{ width: 18, height: 18 }} />
              </button>
            </div>

            {/* Presets */}
            <div style={{ display: "flex", gap: 6, overflowX: "auto", padding: "10px 16px", background: "rgba(15,23,42,0.6)", borderBottom: "1px solid rgba(99,102,241,0.1)" }}>
              {presetQuestions.map((q) => (
                <button
                  key={q}
                  onClick={() => setInput(q)}
                  style={{ fontSize: 11, padding: "4px 10px", borderRadius: 999, background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", cursor: "pointer", whiteSpace: "nowrap" }}
                >
                  {q}
                </button>
              ))}
            </div>

            {/* Messages Stream */}
            <div style={{ flex: 1, padding: 16, overflowY: "auto", display: "flex", flexDirection: "column", gap: 12 }}>
              {messages.map((msg) => (
                <div key={msg.id} style={{ display: "flex", gap: 10, alignSelf: msg.sender === "user" ? "flex-end" : "flex-start", maxWidth: "85%" }}>
                  {msg.sender === "assistant" && (
                    <div style={{ width: 28, height: 28, borderRadius: "50%", background: "#6366f1", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
                      <Bot style={{ width: 14, height: 14, color: "#fff" }} />
                    </div>
                  )}
                  <div style={{
                    padding: "10px 14px",
                    borderRadius: 16,
                    fontSize: 13,
                    lineHeight: 1.5,
                    background: msg.sender === "user" ? "linear-gradient(135deg, #6366f1, #8b5cf6)" : "rgba(30,41,59,0.7)",
                    color: "#fff",
                    border: msg.sender === "user" ? "none" : "1px solid rgba(99,102,241,0.15)",
                  }}>
                    {msg.content}
                    <div style={{ fontSize: 10, color: "rgba(255,255,255,0.5)", marginTop: 4, textAlign: "right" }}>{msg.timestamp}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Input Box */}
            <div style={{ padding: 12, background: "rgba(30,41,59,0.8)", borderTop: "1px solid rgba(99,102,241,0.15)", display: "flex", gap: 8 }}>
              <input
                type="text"
                placeholder="Ask about this report..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                style={{ flex: 1, background: "rgba(15,23,42,0.8)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 12, padding: "8px 14px", fontSize: 13, color: "#fff", outline: "none" }}
              />
              <button onClick={handleSend} style={{ width: 36, height: 36, borderRadius: 12, background: "linear-gradient(135deg, #6366f1, #8b5cf6)", border: "none", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer" }}>
                <Send style={{ width: 16, height: 16 }} />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
