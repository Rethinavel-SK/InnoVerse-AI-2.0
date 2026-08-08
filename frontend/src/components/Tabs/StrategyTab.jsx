import React from 'react';
import { DollarSign, PieChart, TrendingUp, ShieldAlert, CheckCircle, Lightbulb } from 'lucide-react';

export default function StrategyTab({ data }) {
  if (!data) return null;

  const mkt = data.market_size || {};
  const swot = data.swot || {};

  return (
    <div className="space-y-6">
      
      {/* TAM SAM SOM Gauge Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 space-y-1">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block flex items-center gap-1.5">
            <PieChart className="w-3.5 h-3.5 text-cyan-400" /> Total Addressable Market (TAM)
          </span>
          <span className="font-heading font-extrabold text-cyan-400 text-2xl block">{mkt.tam || '$4.8 Billion'}</span>
          <span className="text-[10px] text-slate-500">Global market potential</span>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 space-y-1">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block flex items-center gap-1.5">
            <TrendingUp className="w-3.5 h-3.5 text-purple-400" /> Serviceable Market (SAM)
          </span>
          <span className="font-heading font-extrabold text-purple-400 text-2xl block">{mkt.sam || '$650 Million'}</span>
          <span className="text-[10px] text-slate-500">Serviceable obtainable region</span>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 space-y-1">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block flex items-center gap-1.5">
            <DollarSign className="w-3.5 h-3.5 text-emerald-400" /> Target Share (SOM)
          </span>
          <span className="font-heading font-extrabold text-emerald-400 text-2xl block">{mkt.som || '$45 Million'}</span>
          <span className="text-[10px] text-slate-500">3-Year SOM Target</span>
        </div>
      </div>

      {/* Osterwalder Business Model Canvas */}
      <div className="glass-card rounded-3xl p-6 md:p-8 space-y-5 border border-slate-800/80">
        <h4 className="font-heading font-bold text-lg text-white flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-amber-400" />
          Osterwalder Business Model Canvas
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="bg-slate-900/60 rounded-2xl p-4 border border-slate-800/80 space-y-2">
            <span className="font-heading font-bold text-cyan-400 text-sm block">Core Value Proposition</span>
            <p className="text-slate-300 leading-relaxed font-sans">{data.value_proposition || 'Automated multi-agent strategic & technical evaluation.'}</p>
          </div>

          <div className="bg-slate-900/60 rounded-2xl p-4 border border-slate-800/80 space-y-2">
            <span className="font-heading font-bold text-purple-400 text-sm block">Pricing & Monetization</span>
            <p className="text-slate-300 leading-relaxed font-sans">{data.pricing_model || 'Tiered B2B SaaS ($499/mo Starter, $2,499/mo Enterprise)'}</p>
          </div>

          <div className="bg-slate-900/60 rounded-2xl p-4 border border-slate-800/80 space-y-2">
            <span className="font-heading font-bold text-emerald-400 text-sm block">Go-To-Market Strategy</span>
            <p className="text-slate-300 leading-relaxed font-sans">{data.go_to_market || 'Product-led growth (PLG) supplemented by enterprise direct sales.'}</p>
          </div>
        </div>
      </div>

      {/* SWOT Analysis 2x2 Grid */}
      <div className="space-y-3">
        <h4 className="font-heading font-bold text-md text-slate-200">SWOT Strategic Matrix</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          
          {/* Strengths */}
          <div className="bg-emerald-950/20 border border-emerald-800/40 rounded-2xl p-5 space-y-2.5">
            <span className="font-heading font-bold text-emerald-400 text-sm flex items-center gap-2">
              <CheckCircle className="w-4 h-4" /> Core Strengths
            </span>
            <ul className="space-y-1.5 text-slate-300 font-sans">
              {(swot.strengths || ["First-mover advantage", "Parallel multi-agent execution"]).map((s, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-emerald-400 font-bold">•</span>
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Weaknesses */}
          <div className="bg-rose-950/20 border border-rose-800/40 rounded-2xl p-5 space-y-2.5">
            <span className="font-heading font-bold text-rose-400 text-sm flex items-center gap-2">
              <ShieldAlert className="w-4 h-4" /> Strategic Weaknesses
            </span>
            <ul className="space-y-1.5 text-slate-300 font-sans">
              {(swot.weaknesses || ["Requires fine-tuned prompts across specialist domains"]).map((w, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-rose-400 font-bold">•</span>
                  <span>{w}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Opportunities */}
          <div className="bg-cyan-950/20 border border-cyan-800/40 rounded-2xl p-5 space-y-2.5">
            <span className="font-heading font-bold text-cyan-400 text-sm flex items-center gap-2">
              <TrendingUp className="w-4 h-4" /> Market Opportunities
            </span>
            <ul className="space-y-1.5 text-slate-300 font-sans">
              {(swot.opportunities || ["Expansion into enterprise IP defense & technology audit markets"]).map((o, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-cyan-400 font-bold">•</span>
                  <span>{o}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Threats */}
          <div className="bg-amber-950/20 border border-amber-800/40 rounded-2xl p-5 space-y-2.5">
            <span className="font-heading font-bold text-amber-400 text-sm flex items-center gap-2">
              <ShieldAlert className="w-4 h-4" /> External Threats
            </span>
            <ul className="space-y-1.5 text-slate-300 font-sans">
              {(swot.threats || ["Hyperscalers building generic AI assistants"]).map((t, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-amber-400 font-bold">•</span>
                  <span>{t}</span>
                </li>
              ))}
            </ul>
          </div>

        </div>
      </div>

    </div>
  );
}
