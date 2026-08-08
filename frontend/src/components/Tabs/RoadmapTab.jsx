import React from 'react';
import { Calendar, Users, DollarSign, Rocket, Star, CheckCircle, Clock } from 'lucide-react';

export default function RoadmapTab({ data }) {
  if (!data) return null;

  const mvp = data.mvp_features || [];
  const future = data.future_features || [];

  return (
    <div className="space-y-6">
      
      {/* Top Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 flex items-center gap-4">
          <div className="p-3.5 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <Calendar className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Estimated Timeline</span>
            <span className="font-heading font-extrabold text-cyan-400 text-xl">{data.timeline || '12 Weeks'}</span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 flex items-center gap-4">
          <div className="p-3.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Users className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Team Composition</span>
            <span className="font-heading font-bold text-slate-100 text-sm block truncate">{data.team_size || '4 Engineers'}</span>
          </div>
        </div>

        <div className="glass-card rounded-2xl p-5 border border-slate-800/80 flex items-center gap-4">
          <div className="p-3.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <DollarSign className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs text-slate-400 font-semibold uppercase tracking-wider block">Estimated Budget</span>
            <span className="font-heading font-extrabold text-emerald-400 text-xl">{data.estimated_budget || '$85k - $110k'}</span>
          </div>
        </div>
      </div>

      {/* Feature Breakdown: Phase 1 MVP vs Post-MVP */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* MVP Features */}
        <div className="glass-card rounded-3xl p-6 md:p-8 space-y-5 border border-slate-800/80">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h4 className="font-heading font-bold text-md text-emerald-400 flex items-center gap-2">
              <Star className="w-4 h-4 fill-emerald-400 text-emerald-400" />
              Phase 1: Core MVP Features
            </h4>
            <span className="text-[10px] px-2.5 py-0.5 rounded-full font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Must-Have MVP
            </span>
          </div>

          <div className="space-y-3">
            {mvp.map((feat, i) => (
              <div key={i} className="bg-slate-900/60 rounded-2xl p-4 border border-slate-800/80 space-y-1.5 hover:border-emerald-500/40 transition-colors">
                <div className="flex items-center justify-between">
                  <span className="font-heading font-bold text-sm text-slate-100 flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
                    {typeof feat === 'object' ? feat.feature : feat}
                  </span>
                  {typeof feat === 'object' && feat.priority && (
                    <span className="text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                      {feat.priority}
                    </span>
                  )}
                </div>
                {typeof feat === 'object' && feat.description && (
                  <p className="text-xs text-slate-400 font-sans pl-6">{feat.description}</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Future Features */}
        <div className="glass-card rounded-3xl p-6 md:p-8 space-y-5 border border-slate-800/80">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h4 className="font-heading font-bold text-md text-cyan-400 flex items-center gap-2">
              <Rocket className="w-4 h-4 text-cyan-400" />
              Post-MVP & Scaling Roadmap
            </h4>
            <span className="text-[10px] px-2.5 py-0.5 rounded-full font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              Scale Phase
            </span>
          </div>

          <div className="space-y-3">
            {future.map((feat, i) => (
              <div key={i} className="bg-slate-900/60 rounded-2xl p-4 border border-slate-800/80 space-y-1.5 hover:border-cyan-500/40 transition-colors">
                <div className="flex items-center justify-between">
                  <span className="font-heading font-bold text-sm text-slate-100 flex items-center gap-2">
                    <Clock className="w-4 h-4 text-cyan-400 shrink-0" />
                    {typeof feat === 'object' ? feat.feature : feat}
                  </span>
                  {typeof feat === 'object' && feat.target_release && (
                    <span className="text-[10px] px-2 py-0.5 rounded font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                      {feat.target_release}
                    </span>
                  )}
                </div>
                {typeof feat === 'object' && feat.description && (
                  <p className="text-xs text-slate-400 font-sans pl-6">{feat.description}</p>
                )}
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
}
