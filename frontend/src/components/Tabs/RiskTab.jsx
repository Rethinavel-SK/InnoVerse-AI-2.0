import React from 'react';
import { ShieldAlert, AlertTriangle, ShieldCheck, CheckCircle2 } from 'lucide-react';

export default function RiskTab({ data }) {
  if (!data) return null;

  const risks = data.risks || data.identified_risks || [];

  return (
    <div className="space-y-6">
      
      {/* Risk Header Banner */}
      <div className="glass-card rounded-3xl p-6 md:p-8 space-y-6 border border-slate-800/80">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div>
            <h4 className="font-heading font-bold text-lg text-amber-400 flex items-center gap-2">
              <ShieldAlert className="w-5 h-5" />
              Risk Matrix & Preventive Mitigation Protocols
            </h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Comprehensive security, operational, and financial risk evaluation
            </p>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            {Array.isArray(risks) ? risks.length : 0} Identified Risks
          </span>
        </div>

        {/* Risk Items */}
        <div className="space-y-4">
          {Array.isArray(risks) && risks.map((r, i) => {
            const riskName = typeof r === 'object' ? r.risk : r;
            const impact = typeof r === 'object' ? r.impact : 'Medium';
            const mitigation = typeof r === 'object' ? r.mitigation : 'Standard contingency protocol.';

            const impactStyle = 
              impact.toLowerCase().includes('high') ? 'bg-rose-500/20 text-rose-400 border-rose-500/30' :
              impact.toLowerCase().includes('medium') ? 'bg-amber-500/20 text-amber-400 border-amber-500/30' :
              'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';

            return (
              <div 
                key={i} 
                className="bg-slate-900/60 rounded-2xl p-5 border border-slate-800/80 space-y-3 hover:border-amber-500/40 transition-colors"
              >
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />
                    <span className="font-heading font-bold text-sm text-slate-100">
                      {riskName}
                    </span>
                  </div>

                  <span className={`text-[10px] px-3 py-1 rounded-full font-bold uppercase tracking-wider border shrink-0 ${impactStyle}`}>
                    Impact: {impact}
                  </span>
                </div>

                {mitigation && (
                  <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-850 space-y-1">
                    <div className="flex items-center gap-1.5 text-xs font-semibold text-cyan-400">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>Mitigation Protocol</span>
                    </div>
                    <p className="text-xs text-slate-300 font-sans leading-relaxed">
                      {mitigation}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
