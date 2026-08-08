import React from 'react';
import { Cpu, Activity, ShieldCheck, Sparkles } from 'lucide-react';

export default function Header({ backendStatus }) {
  const isOnline = backendStatus?.status === 'ok';

  return (
    <header className="sticky top-0 z-50 glass-card border-b border-slate-800/80 px-6 py-4 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Identity */}
        <div className="flex items-center gap-3.5">
          <div className="relative flex items-center justify-center w-11 h-11 rounded-xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-purple-600 shadow-lg shadow-cyan-500/25 group">
            <Cpu className="w-6 h-6 text-white transform group-hover:rotate-12 transition-transform duration-300" />
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-cyan-400 rounded-full animate-ping opacity-75"></span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-heading font-extrabold text-xl text-white tracking-tight">
                Innovation Discovery <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">Platform</span>
              </h1>
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                v1.0
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium tracking-wider flex items-center gap-1.5 mt-0.5">
              <Sparkles className="w-3 h-3 text-cyan-400" /> Executive Multi-Agent Director Engine
            </p>
          </div>
        </div>

        {/* Live System Status Badges */}
        <div className="flex items-center gap-3">
          <div className={`hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold border transition-all ${
            isOnline 
              ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 shadow-sm shadow-emerald-500/10'
              : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
          }`}>
            <span className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
            {isOnline ? '7 Specialist Agents Active' : 'Offline Preview Mode (Mock Ready)'}
          </div>

          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300 text-xs font-medium">
            <Activity className="w-3.5 h-3.5 text-cyan-400" />
            <span>FastAPI Engine</span>
          </div>
        </div>

      </div>
    </header>
  );
}
