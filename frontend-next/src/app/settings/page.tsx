"use client";

import { useState } from "react";
import { useTheme } from "next-themes";
import { motion } from "framer-motion";
import { Sun, Moon, Monitor, Bell, Shield, Trash2, Key } from "lucide-react";
import { cn } from "@/lib/utils";

export default function SettingsPage() {
  const { theme, setTheme } = useTheme();
  const [notifications, setNotifications] = useState(true);
  const [autoSave, setAutoSave] = useState(true);

  const handleClearData = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("idp_saved_analyses");
      alert("All saved analyses have been cleared.");
    }
  };

  return (
    <div className="pt-24 pb-16 min-h-screen">
      <div className="max-w-2xl mx-auto px-4 sm:px-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Settings</h1>
          <p className="text-slate-400 mt-1">Configure your platform preferences</p>
        </div>

        <div className="space-y-5">
          {/* Appearance */}
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-2xl border border-slate-800/50 p-6">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Appearance</h2>
            <div className="grid grid-cols-3 gap-3">
              {[
                { value: "light", label: "Light", icon: Sun },
                { value: "dark", label: "Dark", icon: Moon },
                { value: "system", label: "System", icon: Monitor },
              ].map(({ value, label, icon: Icon }) => (
                <button
                  key={value}
                  onClick={() => setTheme(value)}
                  className={cn(
                    "flex flex-col items-center gap-2 p-4 rounded-xl border transition-all",
                    theme === value
                      ? "bg-indigo-500/10 border-indigo-500/40 text-indigo-300"
                      : "bg-slate-800/20 border-slate-700 text-slate-400 hover:border-slate-600"
                  )}
                >
                  <Icon className="w-5 h-5" />
                  <span className="text-xs font-medium">{label}</span>
                </button>
              ))}
            </div>
          </motion.div>

          {/* Preferences */}
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass rounded-2xl border border-slate-800/50 p-6">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Preferences</h2>
            <div className="space-y-4">
              {[
                { label: "Toast Notifications", desc: "Show notifications for analysis completion", icon: Bell, value: notifications, onChange: setNotifications },
                { label: "Auto-Save Reports", desc: "Automatically save completed analyses", icon: Shield, value: autoSave, onChange: setAutoSave },
              ].map(({ label, desc, icon: Icon, value, onChange }) => (
                <div key={label} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-slate-800/50 flex items-center justify-center">
                      <Icon className="w-4 h-4 text-slate-500" />
                    </div>
                    <div>
                      <div className="text-sm text-slate-200">{label}</div>
                      <div className="text-xs text-slate-500">{desc}</div>
                    </div>
                  </div>
                  <button
                    onClick={() => onChange(!value)}
                    className={cn("w-11 h-6 rounded-full border-2 transition-all relative flex-shrink-0",
                      value ? "bg-indigo-600 border-indigo-500" : "bg-slate-700 border-slate-600"
                    )}
                  >
                    <span className={cn("absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all",
                      value ? "left-5" : "left-0.5"
                    )} />
                  </button>
                </div>
              ))}
            </div>
          </motion.div>

          {/* API Connection */}
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass rounded-2xl border border-slate-800/50 p-6">
            <h2 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
              <Key className="w-4 h-4" /> API Configuration
            </h2>
            <div className="space-y-3">
              <div>
                <label className="text-xs text-slate-500 mb-1.5 block">Backend API URL</label>
                <div className="flex gap-2">
                  <input readOnly value="http://localhost:8000" className="flex-1 bg-slate-900/50 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none" />
                  <div className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" /> Connected
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Danger Zone */}
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass rounded-2xl border border-rose-500/20 p-6">
            <h2 className="text-sm font-semibold text-rose-400 mb-4">Danger Zone</h2>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-slate-300">Clear All Saved Reports</div>
                <div className="text-xs text-slate-500">This will permanently delete all saved analyses from local storage.</div>
              </div>
              <button
                onClick={handleClearData}
                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm hover:bg-rose-500/20 transition-all flex-shrink-0"
              >
                <Trash2 className="w-3.5 h-3.5" /> Clear
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
