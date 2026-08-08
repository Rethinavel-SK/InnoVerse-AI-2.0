import React from 'react';
import { Zap, Sparkles, Shield, Utensils, Bot, BatteryCharging, Lock, Gauge, CheckCircle2 } from 'lucide-react';

const PRESETS = [
  {
    id: 1,
    title: "DevOps Security AI",
    icon: Shield,
    text: "Build an AI-powered automated code security review platform for enterprise DevOps teams that detects zero-day vulnerabilities in real time."
  },
  {
    id: 2,
    title: "Restaurant Waste SaaS",
    icon: Utensils,
    text: "Build an AI-powered SaaS platform that helps small and medium restaurants manage inventory, predict demand, and eliminate food waste."
  },
  {
    id: 3,
    title: "Autonomous Robotics",
    icon: Bot,
    text: "Build an autonomous warehouse management robotics platform using computer vision and predictive AI to optimize inventory placement and task assignment."
  },
  {
    id: 4,
    title: "Green Energy Grid",
    icon: BatteryCharging,
    text: "Develop an AI-driven smart battery storage optimization platform for renewable solar/wind energy microgrids to maximize arbitrage revenue."
  },
  {
    id: 5,
    title: "FinTech Fraud Sentinel",
    icon: Lock,
    text: "Build a real-time cross-border payment fraud detection engine utilizing graph neural networks and privacy-preserving federated learning."
  }
];

export default function HeroInput({ problem, setProblem, onRun, loading, fastMode, setFastMode, progressStep }) {
  return (
    <section className="glass-card rounded-3xl p-8 border border-slate-800/80 shadow-2xl relative overflow-hidden group">
      
      {/* Ambient background glow */}
      <div className="absolute -top-24 -right-24 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none group-hover:bg-cyan-500/15 transition-all duration-700"></div>
      <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none group-hover:bg-purple-500/15 transition-all duration-700"></div>

      <div className="relative z-10 space-y-6">
        
        {/* Header Title & Speed Toggle */}
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
          <div className="max-w-3xl space-y-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Sparkles className="w-3.5 h-3.5" /> Next-Gen Enterprise AI Discovery
            </div>
            <h2 className="font-heading font-extrabold text-3xl md:text-4xl text-white tracking-tight leading-tight">
              Architect & Evaluate <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-purple-400">Breakthrough Innovations</span>
            </h2>
            <p className="text-slate-400 text-sm leading-relaxed">
              Enter your product vision or problem statement. The Innovation Director Agent orchestrates 6 specialist AI agents simultaneously to evaluate technology architecture, market size, IP patents, financial viability, and risk factors.
            </p>
          </div>

          {/* Instant Fast Mode Switch */}
          <div className="glass-card rounded-2xl p-3 border border-slate-800 flex items-center gap-3 shrink-0">
            <div className="flex flex-col">
              <span className="text-xs font-bold text-slate-200 flex items-center gap-1">
                <Zap className="w-3.5 h-3.5 text-amber-400 fill-current" /> Instant Mode
              </span>
              <span className="text-[10px] text-slate-400">Sub-second response</span>
            </div>
            <button
              onClick={() => setFastMode(!fastMode)}
              className={`w-12 h-6 rounded-full transition-colors relative p-0.5 ${
                fastMode ? 'bg-cyan-500' : 'bg-slate-800'
              }`}
            >
              <span 
                className={`block w-5 h-5 rounded-full bg-white transition-transform shadow-md ${
                  fastMode ? 'transform translate-x-6' : 'transform translate-x-0'
                }`}
              />
            </button>
          </div>
        </div>

        {/* Input Controls */}
        <div className="space-y-4">
          <div className="relative">
            <textarea
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              placeholder="e.g. Build an AI-powered automated code security review platform for enterprise DevOps teams that detects zero-day vulnerabilities in real time..."
              className="w-full h-36 glass-input rounded-2xl p-4 text-slate-100 placeholder-slate-500 focus:outline-none text-sm leading-relaxed transition-all resize-none font-sans"
            />
            {problem && (
              <button 
                onClick={() => setProblem('')}
                className="absolute top-3 right-3 text-xs text-slate-500 hover:text-slate-300 px-2 py-1 rounded bg-slate-900/60"
              >
                Clear
              </button>
            )}
          </div>

          {/* Presets and Action Bar */}
          <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
            
            {/* Presets */}
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs font-semibold text-slate-400 mr-1">Industry Presets:</span>
              {PRESETS.map((p) => {
                const IconComponent = p.icon;
                return (
                  <button
                    key={p.id}
                    onClick={() => {
                      setProblem(p.text);
                      onRun(p.text);
                    }}
                    className="inline-flex items-center gap-1.5 text-xs bg-slate-900/80 hover:bg-cyan-500/15 hover:border-cyan-500/40 border border-slate-800 text-slate-300 px-3 py-2 rounded-xl transition-all font-medium"
                  >
                    <IconComponent className="w-3.5 h-3.5 text-cyan-400" />
                    {p.title}
                  </button>
                );
              })}
            </div>

            {/* Run Button */}
            <button
              disabled={loading}
              onClick={() => onRun()}
              className="bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white font-heading font-bold px-8 py-3.5 rounded-2xl shadow-xl shadow-cyan-500/20 hover:shadow-purple-500/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:transform-none flex items-center justify-center gap-2.5 min-w-[240px]"
            >
              {loading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                  <span>Executing Agents...</span>
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 fill-current text-cyan-200" />
                  <span>Launch Discovery Analysis</span>
                </>
              )}
            </button>

          </div>

          {/* Real-time Progress Stepper Bar when Loading */}
          {loading && progressStep && (
            <div className="glass-card rounded-2xl p-4 border border-cyan-500/30 space-y-2.5 animate-fadeIn">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-cyan-400 flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
                  {progressStep.label}
                </span>
                <span className="text-slate-400">{progressStep.percent}%</span>
              </div>

              {/* Progress Bar */}
              <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                <div 
                  className="h-full bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-600 transition-all duration-500 ease-out"
                  style={{ width: `${progressStep.percent}%` }}
                />
              </div>
            </div>
          )}

        </div>

      </div>
    </section>
  );
}
