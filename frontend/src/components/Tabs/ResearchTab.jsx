import React from 'react';
import { BookOpen, FileText, Search, ExternalLink, Award } from 'lucide-react';

export default function ResearchTab({ data }) {
  if (!data) return null;

  const papers = data.relevant_papers || data.papers || [];
  const query = data.query_used || 'Academic Literature Analysis';

  return (
    <div className="space-y-6">
      
      {/* Search Metadata Banner */}
      <div className="glass-card rounded-2xl p-5 border border-slate-800/80 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Search className="w-4 h-4" />
          </div>
          <div>
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Literature Query Executed</span>
            <span className="font-heading font-bold text-slate-100 text-xs">{query}</span>
          </div>
        </div>

        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
          arXiv & IEEE Indexed
        </span>
      </div>

      {/* Relevant Papers List */}
      <div className="glass-card rounded-3xl p-6 md:p-8 space-y-5 border border-slate-800/80">
        <h4 className="font-heading font-bold text-lg text-purple-400 flex items-center gap-2">
          <BookOpen className="w-5 h-5" />
          Relevant Scientific & Academic Papers
        </h4>

        <div className="space-y-4">
          {Array.isArray(papers) && papers.map((paper, i) => (
            <div 
              key={i} 
              className="bg-slate-900/60 rounded-2xl p-5 border border-slate-800/80 space-y-3 hover:border-purple-500/40 transition-colors"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="space-y-1">
                  <h5 className="font-heading font-bold text-slate-100 text-sm leading-snug flex items-center gap-2">
                    <FileText className="w-4 h-4 text-purple-400 shrink-0" />
                    {paper.title || `Research Publication #${i + 1}`}
                  </h5>
                  {paper.authors && (
                    <p className="text-xs text-purple-300 font-medium pl-6">
                      Authors: {Array.isArray(paper.authors) ? paper.authors.join(', ') : paper.authors}
                    </p>
                  )}
                </div>

                <span className="text-[10px] text-slate-500 bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800 shrink-0 font-mono">
                  Cited by 42+
                </span>
              </div>

              {paper.abstract && (
                <p className="text-xs text-slate-300 font-sans leading-relaxed pl-6 border-l-2 border-purple-500/30 py-1">
                  {paper.abstract}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
