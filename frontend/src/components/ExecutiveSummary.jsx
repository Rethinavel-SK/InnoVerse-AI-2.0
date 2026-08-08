import React from 'react';
import { Target, CheckCircle2, TrendingUp, DollarSign, Award, Layers } from 'lucide-react';

export default function ExecutiveSummary({ result }) {
  if (!result) return null;

  const score = Math.round(result.feasibility_score || 85);
  const recommendation = result.recommendation || 'GO';
  const synergies = result.cross_domain_synergies || [];

  // Gauge color based on recommendation
  const gaugeColor = 
    recommendation === 'GO' ? '#10b981' :
    recommendation === 'PIVOT' ? '#f59e0b' : '#f43f5e';

  const badgeStyle = 
    recommendation === 'GO' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' :
    recommendation === 'PIVOT' ? 'bg-amber-500/10 border-amber-500/30 text-amber-400' :
    'bg-rose-500/10 border-rose-500/30 text-rose-400';

  return (
    <div className="space-y-6 animate-fadeIn">
      
      {/* Top Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* Gauge Card (4 cols) */}
        <div className="md:col-span-4 glass-card rounded-3xl p-6 flex flex-col items-center justify-center text-center space-y-4 border border-slate-800/80 shadow-xl relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <Award className="w-24 h-24 text-white" />
          </div>

          <div 
            className="score-gauge-ring" 
            style={{ 
              '--score': score,
              '--gauge-color': gaugeColor 
            }}
          >
            <div className="relative z-10 flex flex-col items-center">
              <span className="font-heading font-extrabold text-4xl text-white tracking-tight">
                {score}
              </span>
              <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-widest">
                Out of 100
              </span>
            </div>
          </div>

          <div className="space-y-2">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest">
              Feasibility Score
            </p>
            <div className={`inline-flex items-center gap-2 px-5 py-1.5 rounded-full font-heading font-bold text-sm tracking-wider uppercase border shadow-md ${badgeStyle}`}>
              <span className="w-2 h-2 rounded-full bg-current animate-ping"></span>
              Verdict: {recommendation}
            </div>
          </div>
        </div>

        {/* Synthesis Text (8 cols) */}
        <div className="md:col-span-8 glass-card rounded-3xl p-6 md:p-8 space-y-4 border border-slate-800/80 shadow-xl relative">
          <div className="flex items-center justify-between">
            <h3 className="font-heading font-bold text-xl text-cyan-400 flex items-center gap-2.5">
              <Target className="w-5 h-5 text-cyan-400" />
              Executive Director Synthesis
            </h3>
            <span className="text-xs text-slate-400 bg-slate-900/60 px-3 py-1 rounded-full border border-slate-800 font-medium">
              Multi-Agent Consolidated
            </span>
          </div>

          <p className="text-slate-300 text-sm leading-relaxed font-sans">
            {result.executive_summary}
          </p>

          {synergies.length > 0 && (
            <div className="pt-3 border-t border-slate-800/80 space-y-2">
              <h4 className="font-heading font-semibold text-xs text-purple-400 uppercase tracking-wider flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5" /> Key Cross-Domain Synergies
              </h4>
              <div className="grid grid-cols-1 gap-2">
                {synergies.map((syn, idx) => (
                  <div key={idx} className="flex items-start gap-2.5 text-xs text-slate-300 bg-slate-900/40 p-2.5 rounded-xl border border-slate-800/60">
                    <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                    <span>{syn}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

      </div>

      {/* Metrics Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="glass-card rounded-2xl p-4 border border-slate-800/80 flex items-center gap-3">
          <div className="p-3 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <TrendingUp className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] text-slate-400 uppercase font-semibold block">Market Potential</span>
            <span className="font-heading font-bold text-slate-100 text-base">
              {result.business_strategy?.market_size?.tam || '$4.8 Billion'}
            </span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-slate-800/80 flex items-center gap-3">
          <div className="p-3 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] text-slate-400 uppercase font-semibold block">IP Novelty Score</span>
            <span className="font-heading font-bold text-slate-100 text-base">
              {result.patent_intelligence?.novelty_score || 92} / 100
            </span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-slate-800/80 flex items-center gap-3">
          <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <DollarSign className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] text-slate-400 uppercase font-semibold block">Prototype Cost</span>
            <span className="font-heading font-bold text-slate-100 text-base">
              {result.solution_architecture?.prototype_cost || '$180 / mo'}
            </span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-4 border border-slate-800/80 flex items-center gap-3">
          <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] text-slate-400 uppercase font-semibold block">MVP Timeline</span>
            <span className="font-heading font-bold text-slate-100 text-base">
              {result.mvp_roadmap?.timeline || '12 Weeks'}
            </span>
          </div>
        </div>
      </div>

    </div>
  );
}
