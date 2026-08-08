import React from 'react';
import { Target, CheckCircle2, ArrowRight, ShieldCheck, Cpu } from 'lucide-react';

export default function DirectorTab({ result }) {
  const actions = result?.recommended_actions || [];

  return (
    <div className="space-y-6">
      
      {/* Recommended Strategic Action Items */}
      <div className="glass-card rounded-3xl p-6 md:p-8 space-y-6 border border-slate-800/80">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h4 className="font-heading font-bold text-lg text-white flex items-center gap-2">
              <Target className="w-5 h-5 text-cyan-400" />
              Strategic Implementation Directives
            </h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Priority roadmap actions recommended by the Master Innovation Director Agent
            </p>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            {actions.length} High-Impact Directives
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {actions.map((action, i) => (
            <div 
              key={i} 
              className="glass-card glass-card-hover rounded-2xl p-5 border border-slate-800/80 space-y-3 relative overflow-hidden group"
            >
              <div className="flex items-center justify-between">
                <span className="w-8 h-8 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 text-white flex items-center justify-center font-heading font-extrabold text-xs shadow-md shadow-cyan-500/20">
                  0{i + 1}
                </span>
                <span className="text-[10px] uppercase font-semibold tracking-widest text-slate-400">
                  Priority Directive
                </span>
              </div>
              
              <p className="text-xs text-slate-200 leading-relaxed font-sans font-medium">
                {action}
              </p>

              <div className="pt-2 flex items-center text-[11px] text-cyan-400 font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                <span>View Details</span>
                <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Orchestration Matrix */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800/80 space-y-4">
        <h4 className="font-heading font-bold text-md text-white flex items-center gap-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          Agent Orchestration & Validation Matrix
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {[
            { name: "Solution Architect", status: "Validated", color: "emerald" },
            { name: "MVP & Roadmap", status: "Scheduled", color: "emerald" },
            { name: "Business Strategy", status: "Canvas Ready", color: "emerald" },
            { name: "Risk Assessment", status: "Mitigated", color: "emerald" },
            { name: "Research Intel", status: "Indexed", color: "emerald" },
            { name: "Patent Intel", status: "Novelty 92%", color: "cyan" }
          ].map((agent, i) => (
            <div key={i} className="bg-slate-900/60 rounded-xl p-3 border border-slate-800 space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-[10px] text-slate-400 uppercase font-semibold">{agent.name}</span>
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              </div>
              <p className="font-heading font-semibold text-xs text-slate-200">{agent.status}</p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
