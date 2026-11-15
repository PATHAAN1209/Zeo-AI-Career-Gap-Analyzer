import React, { useState } from 'react';
import { CheckCircle2, AlertCircle, XCircle, ArrowUpRight, Zap } from 'lucide-react';

const STATUS_CONFIG = {
  HAVE: {
    icon: CheckCircle2,
    label: 'HAVE',
    color: '#10b981',
    textClass: 'text-emerald-400',
    bgClass: 'bg-emerald-500/8',
    borderClass: 'border-emerald-500/20',
    badgeClass: 'bg-emerald-500/12 text-emerald-400 border-emerald-500/25',
    barColor: '#10b981',
    leftBorder: 'border-l-emerald-500/60',
    glowClass: 'glow-green',
  },
  PARTIAL: {
    icon: AlertCircle,
    label: 'PARTIAL',
    color: '#f59e0b',
    textClass: 'text-amber-400',
    bgClass: 'bg-amber-500/8',
    borderClass: 'border-amber-500/20',
    badgeClass: 'bg-amber-500/12 text-amber-400 border-amber-500/25',
    barColor: '#f59e0b',
    leftBorder: 'border-l-amber-500/60',
    glowClass: 'glow-amber',
  },
  MISSING: {
    icon: XCircle,
    label: 'MISSING',
    color: '#ef4444',
    textClass: 'text-red-400',
    bgClass: 'bg-red-500/8',
    borderClass: 'border-red-500/20',
    badgeClass: 'bg-red-500/12 text-red-400 border-red-500/25',
    barColor: '#ef4444',
    leftBorder: 'border-l-red-500/60',
    glowClass: 'glow-red',
  },
};

export default function StatusModules({ skills, onSelectSkillToLearn }) {
  const [filter, setFilter] = useState('ALL');

  const counts = {
    HAVE: skills.filter((s) => s.status === 'HAVE').length,
    PARTIAL: skills.filter((s) => s.status === 'PARTIAL').length,
    MISSING: skills.filter((s) => s.status === 'MISSING').length,
  };

  const filtered = filter === 'ALL' ? skills : skills.filter((s) => s.status === filter);

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800/60">
        <div className="space-y-1">
          <h3 className="font-orbitron font-bold text-lg text-[#f0f9ff] flex items-center gap-2.5">
            <Zap className="w-4 h-4 text-cyan-400" />
            Skill Verification Matrix
          </h3>
          <p className="text-xs font-mono text-slate-600">
            Full diagnostic breakdown against role prerequisites
          </p>
        </div>

        {/* Filter tabs */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-900/60 border border-slate-800/60 backdrop-blur-sm flex-shrink-0">
          <button
            onClick={() => setFilter('ALL')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all ${
              filter === 'ALL'
                ? 'bg-slate-700/60 text-[#f0f9ff] font-semibold'
                : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            All ({skills.length})
          </button>
          {['HAVE', 'PARTIAL', 'MISSING'].map((s) => {
            const cfg = STATUS_CONFIG[s];
            const isActive = filter === s;
            return (
              <button
                key={s}
                onClick={() => setFilter(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all flex items-center gap-1.5 ${
                  isActive ? `${cfg.bgClass} ${cfg.textClass} border ${cfg.borderClass} font-semibold` : 'text-slate-500 hover:text-slate-300'
                }`}
              >
                <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: cfg.color }} />
                {s.charAt(0) + s.slice(1).toLowerCase()} ({counts[s]})
              </button>
            );
          })}
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((s, idx) => {
          const cfg = STATUS_CONFIG[s.status] || STATUS_CONFIG.HAVE;
          const Icon = cfg.icon;
          const isGap = s.status === 'PARTIAL' || s.status === 'MISSING';

          return (
            <div
              key={idx}
              className={`relative rounded-2xl border-l-4 ${cfg.leftBorder} glass-panel p-5 flex flex-col justify-between group transition-all duration-200`}
            >
              {/* Top: skill name + badge */}
              <div>
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="font-orbitron font-bold text-sm text-[#f0f9ff] group-hover:text-cyan-300 transition-colors leading-snug">
                    {s.name}
                  </div>
                  <div className={`flex-shrink-0 flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold border ${cfg.badgeClass}`}>
                    <Icon className="w-3 h-3" />
                    {cfg.label}
                  </div>
                </div>

                {/* Priority + score */}
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-slate-900/60 border border-slate-800 text-slate-500">
                    {s.importance?.toUpperCase()} PRIORITY
                  </span>
                  <span className="text-[10px] font-mono text-slate-600">
                    +{s.score_contribution} pts
                  </span>
                </div>

                {/* Evidence bar */}
                <div className="mb-3">
                  <div className="h-0.5 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-1000"
                      style={{
                        width: s.status === 'HAVE' ? '100%' : s.status === 'PARTIAL' ? '50%' : '5%',
                        backgroundColor: cfg.color,
                        boxShadow: `0 0 6px ${cfg.color}60`,
                      }}
                    />
                  </div>
                </div>

                {/* Evidence text */}
                <p className="font-inter text-xs text-slate-500 leading-relaxed line-clamp-2 bg-slate-900/40 rounded-lg p-2.5 border border-slate-800/40">
                  {s.evidence_or_reason}
                </p>
              </div>

              {/* Footer CTA */}
              {isGap && onSelectSkillToLearn && (
                <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between">
                  <span className="text-[10px] font-mono text-slate-600">Skill gap detected</span>
                  <button
                    onClick={() => onSelectSkillToLearn(s.name)}
                    className={`flex items-center gap-1.5 text-xs font-mono ${cfg.textClass} hover:opacity-80 transition-opacity`}
                  >
                    View Resources
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
