import React from 'react';
import { Cpu, Sparkles } from 'lucide-react';

export default function SGCore({ statusMessage, insight, isAnalyzing }) {
  return (
    <div className="relative group">
      {/* Ambient glow */}
      <div className="absolute -inset-px rounded-2xl bg-gradient-to-r from-cyan-500/20 via-blue-600/10 to-indigo-600/20 blur-sm opacity-70 group-hover:opacity-100 transition-opacity duration-500" />

      <div className="relative rounded-2xl glass-panel p-4 sm:p-5">
        {/* Inner top highlight */}
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent rounded-t-2xl" />

        <div className="flex items-start gap-4">

          {/* Animated Orb */}
          <div className="relative flex-shrink-0 w-14 h-14 flex items-center justify-center">
            {/* Outer spinning ring */}
            <div className="absolute inset-0 rounded-full border border-dashed border-cyan-500/30 animate-radar-spin" />
            {/* Middle pulse ring */}
            <div className={`absolute inset-2 rounded-full border ${isAnalyzing ? 'border-cyan-400/80 animate-ping' : 'border-cyan-500/40 animate-pulse-glow'}`} />
            {/* Core */}
            <div className="relative w-9 h-9 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 shadow-[0_0_20px_rgba(6,182,212,0.5)] flex items-center justify-center">
              <Cpu className="w-4 h-4 text-[#030712]" />
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="font-orbitron font-bold text-sm tracking-widest gradient-text-cyan">SG-CORE</span>
                <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/25 tracking-widest">
                  AI CO-PILOT
                </span>
              </div>

              {/* Waveform */}
              <div className="flex items-end gap-0.5 h-5">
                {[10, 18, 7, 16, 11, 14, 8].map((h, i) => (
                  <div
                    key={i}
                    className="wave-bar"
                    style={{ height: `${h}px`, animationDelay: `${i * 0.12}s` }}
                  />
                ))}
              </div>
            </div>

            {/* Status text */}
            <p className="font-mono text-xs sm:text-sm text-slate-300 leading-relaxed">
              {statusMessage || 'Awaiting target career role and candidate resume upload.'}
            </p>

            {/* Insight callout */}
            {insight && (
              <div className="mt-3 p-3 rounded-xl bg-slate-900/60 border border-cyan-500/15 flex items-start gap-2.5">
                <Sparkles className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0 mt-0.5" />
                <span className="font-inter text-xs text-slate-400 leading-relaxed">{insight}</span>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
