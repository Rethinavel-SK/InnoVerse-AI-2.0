"use client";

import { motion } from "framer-motion";
import { User, Mail, Building, MapPin, Calendar, Edit2, Activity, FileText, TrendingUp } from "lucide-react";

export default function ProfilePage() {
  return (
    <div className="pt-24 pb-16 min-h-screen">
      <div className="max-w-3xl mx-auto px-4 sm:px-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Profile</h1>
          <p className="text-slate-400 mt-1">Manage your account and preferences</p>
        </div>

        {/* Profile Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-2xl border border-slate-800/50 p-6 mb-6"
        >
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-3xl font-bold text-white flex-shrink-0">
              U
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-bold text-white">Innovation User</h2>
              <p className="text-slate-400 text-sm">user@innovationplatform.ai</p>
              <div className="flex items-center gap-3 mt-3">
                <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-indigo-500/10 border border-indigo-500/20 text-indigo-300">Pro Plan</span>
                <span className="text-xs text-slate-500 flex items-center gap-1"><Calendar className="w-3 h-3" /> Joined July 2026</span>
              </div>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 rounded-xl glass border border-slate-700 text-sm text-slate-400 hover:text-white hover:border-indigo-500/40 transition-all">
              <Edit2 className="w-3.5 h-3.5" /> Edit
            </button>
          </div>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          {[
            { label: "Total Analyses", value: "—", icon: FileText, color: "indigo" },
            { label: "Avg Score", value: "—", icon: TrendingUp, color: "emerald" },
            { label: "Agents Used", value: "9", icon: Activity, color: "purple" },
          ].map((s) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass rounded-2xl border border-slate-800/50 p-4 text-center"
            >
              <div className="text-2xl font-bold text-white mb-1">{s.value}</div>
              <div className="text-xs text-slate-500">{s.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Details */}
        <div className="glass rounded-2xl border border-slate-800/50 p-6">
          <h3 className="text-sm font-semibold text-slate-300 mb-4">Account Information</h3>
          <div className="space-y-4">
            {[
              { icon: User, label: "Full Name", value: "Innovation User" },
              { icon: Mail, label: "Email", value: "user@innovationplatform.ai" },
              { icon: Building, label: "Organization", value: "Innovation Team" },
              { icon: MapPin, label: "Location", value: "Global" },
            ].map(({ icon: Icon, label, value }) => (
              <div key={label} className="flex items-center gap-4">
                <div className="w-8 h-8 rounded-lg bg-slate-800/50 flex items-center justify-center flex-shrink-0">
                  <Icon className="w-4 h-4 text-slate-500" />
                </div>
                <div className="flex-1">
                  <div className="text-xs text-slate-500">{label}</div>
                  <div className="text-sm text-slate-200">{value}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
