import React from 'react';
import { Cpu, Server, Database, Layers, ShieldCheck, DollarSign, Activity } from 'lucide-react';

export default function ArchitectureTab({ data }) {
  if (!data) return null;

  const arch = data.architecture || {};
  const tech = data.technology_recommendations || {};

  return (
    <div className="space-y-6">
      
      {/* Top Architecture Overview Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 space-y-1">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Architecture Pattern</span>
          <span className="font-heading font-extrabold text-cyan-400 text-lg block truncate">
            {arch.type || 'Microservices'}
          </span>
          <span className="text-[10px] text-slate-500">Decoupled & Event-Driven</span>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 space-y-1">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Estimated Complexity</span>
          <span className="font-heading font-extrabold text-amber-400 text-lg block">
            {data.estimated_complexity || 'Moderate to High'}
          </span>
          <span className="text-[10px] text-slate-500">High Reliability Target</span>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 space-y-1">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Prototype Monthly Cost</span>
          <span className="font-heading font-extrabold text-emerald-400 text-lg block">
            {data.prototype_cost || '$180 / mo'}
          </span>
          <span className="text-[10px] text-slate-500">Cloud Infrastructure (AWS/GCP)</span>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 space-y-1">
          <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Production Cost</span>
          <span className="font-heading font-extrabold text-purple-400 text-lg block">
            {data.production_cost || '$1,450 / mo'}
          </span>
          <span className="text-[10px] text-slate-500">Scaled Multi-Region Cluster</span>
        </div>
      </div>

      {/* Rationale Card */}
      <div className="glass-card rounded-3xl p-6 space-y-3 border border-slate-800/80">
        <h4 className="font-heading font-bold text-md text-cyan-400 flex items-center gap-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          Architecture Design Rationale
        </h4>
        <p className="text-xs text-slate-300 leading-relaxed font-sans">
          {arch.rationale || 'Selected for maximum horizontal scalability, sub-second API responses, and resilient agent task execution.'}
        </p>
      </div>

      {/* Recommended Tech Stack Grid */}
      <div className="glass-card rounded-3xl p-6 md:p-8 space-y-6 border border-slate-800/80">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h4 className="font-heading font-bold text-lg text-white flex items-center gap-2">
              <Layers className="w-5 h-5 text-purple-400" />
              Recommended Technology Stack
            </h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Production-grade framework selection optimized for AI LLM workloads
            </p>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
            Cloud Native Stack
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(tech).map(([category, details], i) => (
            <div key={i} className="glass-card glass-card-hover rounded-2xl p-5 border border-slate-800/80 space-y-2">
              <span className="text-[10px] font-bold text-purple-400 uppercase tracking-widest block">
                {category.replace('_', ' ')}
              </span>
              <p className="font-heading font-bold text-sm text-slate-100">
                {typeof details === 'object' ? (details.technology || JSON.stringify(details)) : details}
              </p>
              {typeof details === 'object' && details.reason && (
                <p className="text-xs text-slate-400 leading-normal pt-1 border-t border-slate-800/60">
                  {details.reason}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
