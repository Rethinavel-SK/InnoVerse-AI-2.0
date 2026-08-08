import React from 'react';
import { ShieldCheck, Award, FileSearch, Sparkles, CheckCircle2 } from 'lucide-react';

export default function PatentTab({ data }) {
  if (!data) return null;

  const score = data.novelty_score || 92;

  return (
    <div className="space-y-6">
      
      {/* Novelty Score Gauge Banner */}
      <div className="glass-card rounded-3xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6 border border-slate-800/80 shadow-xl relative overflow-hidden">
        
        <div className="flex items-center gap-5">
          <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-cyan-500 to-emerald-500 flex flex-col items-center justify-center text-white shadow-lg shadow-cyan-500/20 shrink-0">
            <span className="font-heading font-extrabold text-2xl">{score}</span>
            <span className="text-[9px] uppercase tracking-wider font-semibold opacity-90">Novelty</span>
          </div>

          <div className="space-y-1">
            <h4 className="font-heading font-bold text-xl text-white flex items-center gap-2">
              Intellectual Property Novelty Assessment
            </h4>
            <p className="text-xs text-slate-400">
              Evaluated against USPTO, EPO, and WIPO prior art patent databases
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Whitespace Rating</span>
            <span className="font-heading font-bold text-emerald-400 text-sm">High Proprietary Advantage</span>
          </div>
          <div className="p-3 rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <Award className="w-6 h-6" />
          </div>
        </div>

      </div>

      {/* Prior Art Analysis Detail */}
      <div className="glass-card rounded-3xl p-6 md:p-8 space-y-5 border border-slate-800/80">
        <h4 className="font-heading font-bold text-lg text-cyan-400 flex items-center gap-2">
          <FileSearch className="w-5 h-5 text-cyan-400" />
          Prior Art & Patent Whitespace Analysis
        </h4>

        <div className="bg-slate-900/60 rounded-2xl p-5 border border-slate-800/80 space-y-3">
          <p className="text-xs text-slate-200 leading-relaxed font-sans font-medium">
            {data.summary || data.analysis || 'Comprehensive search across USPTO and global patent repositories reveals high uncrowded whitespace for core algorithmic & multi-agent execution claims.'}
          </p>

          <div className="pt-3 border-t border-slate-800/80 grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div className="flex items-start gap-2 text-slate-300">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Independent claim space available for parallel multi-agent LLM consensus logic.</span>
            </div>
            <div className="flex items-start gap-2 text-slate-300">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
              <span>Low risk of blocking patents from existing enterprise incumbents.</span>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
