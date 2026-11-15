import React from 'react';
import { FolderGit2, Code2, Rocket, Layers } from 'lucide-react';

const DIFFICULTY_STYLES = {
  beginner: { text: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/25', accent: '#10b981' },
  intermediate: { text: 'text-cyan-400', bg: 'bg-cyan-500/10', border: 'border-cyan-500/25', accent: '#06b6d4' },
  advanced: { text: 'text-violet-400', bg: 'bg-violet-500/10', border: 'border-violet-500/25', accent: '#8b5cf6' },
  expert: { text: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/25', accent: '#f59e0b' },
};

const CARD_GRADIENTS = [
  'from-cyan-500/5 to-blue-600/3',
  'from-violet-500/5 to-purple-600/3',
  'from-emerald-500/5 to-teal-600/3',
  'from-amber-500/5 to-orange-600/3',
];

export default function ProjectCards({ projects }) {
  if (!projects || projects.length === 0) return null;

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800/60">
        <div className="space-y-1">
          <h3 className="font-orbitron font-bold text-lg text-[#f0f9ff] flex items-center gap-2.5">
            <Layers className="w-4 h-4 text-cyan-400" />
            Portfolio Blueprints
          </h3>
          <p className="text-xs font-mono text-slate-600">
            Gap-targeted projects to build interview-ready portfolio evidence
          </p>
        </div>
        <span className="self-start sm:self-auto text-xs font-mono px-3 py-1.5 rounded-xl bg-slate-900/60 border border-slate-800 text-cyan-400">
          {projects.length} High-Impact Projects
        </span>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {projects.map((proj, idx) => {
          const diffKey = (proj.difficulty || 'intermediate').toLowerCase();
          const diff = DIFFICULTY_STYLES[diffKey] || DIFFICULTY_STYLES.intermediate;
          const gradient = CARD_GRADIENTS[idx % CARD_GRADIENTS.length];

          return (
            <div
              key={idx}
              className={`glass-panel rounded-2xl p-6 flex flex-col justify-between relative overflow-hidden group transition-all duration-300 hover:scale-[1.005]`}
            >
              {/* BG gradient */}
              <div className={`absolute inset-0 bg-gradient-to-br ${gradient} pointer-events-none`} />
              <div className="absolute inset-x-0 top-0 h-0.5" style={{ background: `linear-gradient(to right, transparent, ${diff.accent}60, transparent)` }} />

              <div className="relative z-10">
                {/* Header */}
                <div className="flex items-center justify-between gap-2 mb-4">
                  <div className="flex items-center gap-2">
                    <div className={`w-8 h-8 rounded-lg ${diff.bg} border ${diff.border} flex items-center justify-center`}>
                      <FolderGit2 className={`w-4 h-4 ${diff.text}`} />
                    </div>
                    <span className={`font-mono text-[10px] font-bold tracking-widest ${diff.text}`}>
                      PROJECT #{String(idx + 1).padStart(2, '0')}
                    </span>
                  </div>
                  <span className={`px-2.5 py-1 rounded-lg text-[9px] font-mono font-bold border ${diff.bg} ${diff.text} ${diff.border}`}>
                    {diffKey.toUpperCase()}
                  </span>
                </div>

                {/* Title */}
                <h4 className="font-orbitron font-bold text-base sm:text-lg text-[#f0f9ff] mb-2 group-hover:text-cyan-300 transition-colors leading-snug">
                  {proj.title}
                </h4>

                {/* Description */}
                <p className="font-inter text-xs sm:text-sm text-slate-500 leading-relaxed mb-4">
                  {proj.description}
                </p>

                {/* Skills tags */}
                <div className="mb-4">
                  <div className="text-[9px] font-mono text-slate-600 uppercase tracking-widest mb-2">Skills Covered</div>
                  <div className="flex flex-wrap gap-1.5">
                    {proj.skills_covered?.map((sk, sIdx) => (
                      <span
                        key={sIdx}
                        className={`text-[10px] font-mono px-2 py-0.5 rounded-md border ${diff.bg} ${diff.text} ${diff.border}`}
                      >
                        {sk}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Approach box */}
                {proj.suggested_approach && (
                  <div className="bg-slate-900/60 rounded-xl p-3.5 border border-slate-800/60 mb-4">
                    <div className="flex items-center gap-1.5 mb-1.5">
                      <Code2 className="w-3 h-3 text-cyan-500" />
                      <span className="text-[9px] font-mono text-slate-600 uppercase tracking-widest">Engineering Approach</span>
                    </div>
                    <p className="font-inter text-xs text-slate-400 leading-relaxed">{proj.suggested_approach}</p>
                  </div>
                )}
              </div>

              {/* Footer */}
              <div className="relative z-10 pt-3 border-t border-slate-800/40 flex items-center justify-between text-xs font-mono">
                <span className="text-slate-600 flex items-center gap-1.5">
                  <Rocket className="w-3 h-3 text-emerald-500" />
                  Deliverable:
                </span>
                <span className="text-emerald-400 font-semibold text-right max-w-[55%] leading-snug">
                  {proj.expected_outcome}
                </span>
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}
