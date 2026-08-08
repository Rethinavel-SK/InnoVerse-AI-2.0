import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HeroInput from './components/HeroInput';
import ExecutiveSummary from './components/ExecutiveSummary';
import DirectorTab from './components/Tabs/DirectorTab';
import ArchitectureTab from './components/Tabs/ArchitectureTab';
import RoadmapTab from './components/Tabs/RoadmapTab';
import StrategyTab from './components/Tabs/StrategyTab';
import RiskTab from './components/Tabs/RiskTab';
import ResearchTab from './components/Tabs/ResearchTab';
import PatentTab from './components/Tabs/PatentTab';
import { runInnovationDiscovery, checkBackendHealth } from './services/api';
import { Target, Cpu, Rocket, Briefcase, ShieldAlert, BookOpen, FileText } from 'lucide-react';

const TABS = [
  { id: 'synthesis', label: 'Actions & Directives', icon: Target },
  { id: 'architect', label: 'Solution Architecture', icon: Cpu },
  { id: 'roadmap', label: 'MVP & Roadmap', icon: Rocket },
  { id: 'strategy', label: 'Business Strategy', icon: Briefcase },
  { id: 'risk', label: 'Risk Assessment', icon: ShieldAlert },
  { id: 'research', label: 'Research Papers', icon: BookOpen },
  { id: 'patent', label: 'Patent Intelligence', icon: FileText }
];

export default function App() {
  const [problem, setProblem] = useState('');
  const [loading, setLoading] = useState(false);
  const [fastMode, setFastMode] = useState(true); // Default to Fast Instant Mode for instant feedback
  const [progressStep, setProgressStep] = useState(null);
  const [activeTab, setActiveTab] = useState('synthesis');
  const [result, setResult] = useState(null);
  const [backendStatus, setBackendStatus] = useState(null);

  useEffect(() => {
    checkBackendHealth().then(setBackendStatus);
  }, []);

  const handleRun = async (overrideProblem) => {
    const textToRun = overrideProblem || problem;
    if (!textToRun.trim()) {
      alert("Please enter a problem statement or select a preset.");
      return;
    }

    setLoading(true);
    setResult(null);
    setProgressStep({ step: 1, label: "Initializing Multi-Agent Pipeline...", percent: 5 });

    try {
      const data = await runInnovationDiscovery(textToRun, fastMode, (stepInfo) => {
        setProgressStep(stepInfo);
      });
      setResult(data);
      setActiveTab('synthesis');
    } catch (err) {
      alert("Analysis failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col font-sans">
      
      {/* HEADER */}
      <Header backendStatus={backendStatus} />

      {/* MAIN BODY */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
        
        {/* HERO INPUT CARD */}
        <HeroInput 
          problem={problem}
          setProblem={setProblem}
          onRun={handleRun}
          loading={loading}
          fastMode={fastMode}
          setFastMode={setFastMode}
          progressStep={progressStep}
        />

        {/* RESULTS SECTION */}
        {result && (
          <div className="space-y-8 animate-fadeIn">
            
            {/* EXECUTIVE VERDICT & METRICS */}
            <ExecutiveSummary result={result} />

            {/* TAB NAVIGATION STRIP */}
            <div className="flex border-b border-slate-800 gap-2 overflow-x-auto pb-1 scrollbar-none">
              {TABS.map((tab) => {
                const IconComponent = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-2 px-5 py-3 font-heading font-semibold text-sm rounded-t-2xl transition-all whitespace-nowrap border-b-2 ${
                      isActive
                        ? "text-cyan-400 border-cyan-400 bg-slate-900/60 shadow-lg shadow-cyan-500/10"
                        : "text-slate-400 border-transparent hover:text-slate-200 hover:bg-slate-900/30"
                    }`}
                  >
                    <IconComponent className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>

            {/* ACTIVE TAB CONTENT PANEL */}
            <div className="space-y-6">
              {activeTab === 'synthesis' && <DirectorTab result={result} />}
              {activeTab === 'architect' && <ArchitectureTab data={result.solution_architecture} />}
              {activeTab === 'roadmap' && <RoadmapTab data={result.mvp_roadmap} />}
              {activeTab === 'strategy' && <StrategyTab data={result.business_strategy} />}
              {activeTab === 'risk' && <RiskTab data={result.risk_assessment} />}
              {activeTab === 'research' && <ResearchTab data={result.research_intelligence} />}
              {activeTab === 'patent' && <PatentTab data={result.patent_intelligence} />}
            </div>

          </div>
        )}

      </main>

      {/* FOOTER */}
      <footer className="mt-auto border-t border-slate-800/80 py-6 text-center text-xs text-slate-500 glass-card">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-heading font-bold text-slate-300">AI Innovation Discovery Platform</span>
            <span>&bull; Executive Multi-Agent Architecture</span>
          </div>
          <div className="text-slate-400">
            Powered by FastAPI & React 18
          </div>
        </div>
      </footer>

    </div>
  );
}
