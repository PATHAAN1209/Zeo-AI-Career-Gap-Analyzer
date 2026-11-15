import React from 'react';
import { ExternalLink, Globe, Rocket, Award } from 'lucide-react';

const BADGE_STYLES = [
  { bg: 'bg-cyan-500/10', text: 'text-cyan-400', border: 'border-cyan-500/25', accent: '#06b6d4' },
  { bg: 'bg-violet-500/10', text: 'text-violet-400', border: 'border-violet-500/25', accent: '#8b5cf6' },
  { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/25', accent: '#10b981' },
  { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/25', accent: '#f59e0b' },
  { bg: 'bg-blue-500/10', text: 'text-blue-400', border: 'border-blue-500/25', accent: '#3b82f6' },
  { bg: 'bg-pink-500/10', text: 'text-pink-400', border: 'border-pink-500/25', accent: '#ec4899' },
];

export default function Missions({ opportunities, roleTitle }) {
  if (!opportunities || opportunities.length === 0) return null;

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800/60">
        <div className="space-y-1">
          <h3 className="font-orbitron font-bold text-lg text-[#f0f9ff] flex items-center gap-2.5">
            <Rocket className="w-4 h-4 text-cyan-400" />
            Career Launchpad
          </h3>
          <p className="text-xs font-mono text-slate-600">
            Fellowships, hackathons, open-source & hiring challenges for {roleTitle}
          </p>
        </div>
        <span className="self-start sm:self-auto text-xs font-mono px-3 py-1.5 rounded-xl bg-slate-900/60 border border-slate-800 text-cyan-400">
          {opportunities.length} Active Streams
        </span>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {opportunities.map((opp, idx) => {
          const style = BADGE_STYLES[idx % BADGE_STYLES.length];
          return (
            <a
              key={opp.id || idx}
              href={opp.url}
              target="_blank"
              rel="noopener noreferrer"
              className="glass-panel rounded-2xl p-5 flex flex-col justify-between group relative overflow-hidden transition-all duration-300 hover:scale-[1.01]"
            >
              {/* Gradient top line */}
              <div
                className="absolute inset-x-0 top-0 h-0.5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                style={{ background: `linear-gradient(to right, transparent, ${style.accent}80, transparent)` }}
              />

              <div>
                {/* Org + Badge */}
                <div className="flex items-start justify-between gap-2 mb-3">
                  <span className={`text-xs font-mono font-semibold ${style.text}`}>
                    {opp.organization}
                  </span>
                  <span className={`flex-shrink-0 px-2 py-0.5 rounded-full text-[9px] font-mono font-bold border ${style.bg} ${style.text} ${style.border}`}>
                    {opp.badge}
                  </span>
                </div>

                <h4 className="font-orbitron font-bold text-sm text-[#f0f9ff] mb-2 group-hover:text-cyan-300 transition-colors leading-snug line-clamp-2">
                  {opp.title}
                </h4>

                <p className="font-inter text-xs text-slate-500 leading-relaxed mb-4 line-clamp-3">
                  {opp.description}
                </p>
              </div>

              {/* Footer */}
              <div className="pt-3 border-t border-slate-800/40 flex items-center justify-between text-xs font-mono">
                <span className="text-slate-600 flex items-center gap-1.5">
                  <Globe className="w-3 h-3 text-slate-700" />
                  {opp.location || 'Remote / Global'}
                </span>
                <span className={`flex items-center gap-1.5 font-semibold ${style.text} group-hover:translate-x-0.5 transition-transform`}>
                  Enter Mission
                  <ExternalLink className="w-3 h-3" />
                </span>
              </div>
            </a>
          );
        })}
      </div>

    </div>
  );
}
