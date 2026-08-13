"use client";

import { useState, useEffect } from "react";
import { Shield, Terminal, RefreshCw, MessageSquare } from "lucide-react";
import { AGENTS } from "@/lib/types";
import { getCommunicationLogs } from "@/lib/api";

const CARD: React.CSSProperties = {
  background: "rgba(15,23,42,0.75)",
  backdropFilter: "blur(16px)",
  border: "1px solid rgba(99,102,241,0.15)",
  borderRadius: 20,
  padding: 24,
};

interface CommLog {
  id: string;
  channel: string;
  direction: string;
  sender?: string;
  content: string;
  created_at: string;
}

export default function AdminDashboardPage() {
  const [commLogs, setCommLogs] = useState<CommLog[]>([]);

  useEffect(() => {
    let isMounted = true;
    const fetchLogs = async () => {
      const logs = await getCommunicationLogs();
      if (isMounted && logs && logs.length > 0) {
        setCommLogs(logs);
      }
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 3000); // Live poll every 3 seconds

    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <div style={{ minHeight: "100vh", padding: "2.5rem 1rem 5rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: 8, padding: "6px 16px", borderRadius: 999, background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", fontSize: 13, fontWeight: 500, marginBottom: 16 }}>
            <Shield style={{ width: 14, height: 14 }} /> System Admin & Live Caspian Mesh
          </span>
          <h1 style={{ fontSize: "clamp(1.8rem, 4vw, 2.5rem)", fontWeight: 800, color: "#fff", marginBottom: 10 }}>Admin Control Panel</h1>
          <p style={{ color: "#94a3b8", fontSize: 14, maxWidth: 560, margin: "0 auto" }}>Monitor real-time agent status, live Telegram/Discord/Email interactions, and backend execution logs.</p>
        </div>

        {/* Top Status Banner */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 16, marginBottom: 28 }}>
          {[
            { label: "Caspian SDK Mesh", value: "Connected", color: "#34d399" },
            { label: "Active Sub-Agents", value: "11 / 11 Healthy", color: "#818cf8" },
            { label: "Connected Channels", value: "Telegram, Discord, Email", color: "#a5b4fc" },
            { label: "Avg Request Latency", value: "320ms", color: "#fbbf24" },
          ].map((item) => (
            <div key={item.label} style={CARD}>
              <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{item.label}</div>
              <div style={{ fontSize: 18, fontWeight: 800, color: item.color }}>{item.value}</div>
            </div>
          ))}
        </div>

        {/* 11 Agent Health Table */}
        <div style={{ ...CARD, marginBottom: 28 }}>
          <h3 style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9", marginBottom: 16 }}>11 Specialist AI Agent Health Status</h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 12 }}>
            {AGENTS.map((agent) => (
              <div key={agent.id} style={{ background: "rgba(30,41,59,0.4)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: 14, padding: "14px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <span style={{ fontSize: 20 }}>{agent.icon}</span>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 700, color: "#fff" }}>{agent.name}</div>
                    <div style={{ fontSize: 11, color: "#64748b" }}>Model: llama-3.1-8b-instant</div>
                  </div>
                </div>
                <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 10px", borderRadius: 999, background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.3)", color: "#34d399" }}>
                  ● Healthy
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Live Caspian Multi-Channel Stream */}
        <div style={CARD}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
            <h3 style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9", margin: 0, display: "flex", alignItems: "center", gap: 8 }}>
              <MessageSquare style={{ width: 16, height: 16, color: "#818cf8" }} /> Live Caspian Multi-Channel Stream (Telegram / Discord / Email)
            </h3>
            <span style={{ fontSize: 11, color: "#34d399", display: "flex", alignItems: "center", gap: 4 }}>
              <RefreshCw className="animate-spin" style={{ width: 12, height: 12 }} /> Live 3s Polling
            </span>
          </div>

          <div style={{ background: "#020817", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 12, padding: "16px", fontFamily: "monospace", fontSize: 12, height: 260, overflowY: "auto", display: "flex", flexDirection: "column", gap: 8 }}>
            {commLogs.length === 0 ? (
              <div style={{ color: "#64748b", textAlign: "center", padding: "20px" }}>No communication events logged yet. Send a message to your Telegram bot to see it live here!</div>
            ) : (
              commLogs.map((log) => (
                <div key={log.id} style={{ display: "flex", gap: 12, alignItems: "flex-start", borderBottom: "1px dashed rgba(255,255,255,0.05)", paddingBottom: 6 }}>
                  <span style={{ color: "#475569", flexShrink: 0 }}>[{new Date(log.created_at).toLocaleTimeString()}]</span>
                  <span style={{ color: log.channel === "telegram" ? "#38bdf8" : "#818cf8", fontWeight: 700, textTransform: "uppercase", width: 75, flexShrink: 0 }}>
                    [{log.channel}]
                  </span>
                  <span style={{ color: log.direction === "inbound" ? "#f59e0b" : "#34d399", fontWeight: 700, width: 70, flexShrink: 0 }}>
                    {log.direction === "inbound" ? "INBOUND" : "OUTBOUND"}
                  </span>
                  <span style={{ color: "#cbd5e1" }}>{log.content}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
