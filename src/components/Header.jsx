import React from 'react';
import { RotateCcw } from 'lucide-react';

export default function Header({ onReset, hasResults }) {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800/60 bg-[#030712]/80 backdrop-blur-xl">
      {/* Subtle top gradient line */}
      <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

        {/* Brand */}
        <div
          onClick={onReset}
          className="flex items-center gap-3 cursor-pointer group"
        >
          {/* Logo Icon */}
          <div className="relative w-9 h-9 flex items-center justify-center">
            <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 group-hover:border-cyan-500/60 transition-all duration-300" />
            <div className="absolute inset-0 rounded-xl bg-cyan-500/10 opacity-0 group-hover:opacity-100 blur-sm transition-opacity duration-300" />
            <svg className="relative w-5 h-5" viewBox="0 0 100 100" fill="none">
              <polygon points="50,8 86,29 86,71 50,92 14,71 14,29"
                stroke="url(#hGrad)" strokeWidth="7" fill="none" />
              <circle cx="50" cy="50" r="8" fill="url(#hGrad)" />
              <circle cx="50" cy="20" r="4" fill="#3b82f6" />
              <circle cx="76" cy="35" r="4" fill="#3b82f6" />
              <circle cx="76" cy="65" r="4" fill="#3b82f6" />
              <circle cx="24" cy="35" r="4" fill="#3b82f6" />
              <circle cx="24" cy="65" r="4" fill="#3b82f6" />
              <line x1="50" y1="50" x2="50" y2="20" stroke="#06b6d4" strokeWidth="2.5" strokeOpacity="0.8"/>
              <line x1="50" y1="50" x2="76" y2="35" stroke="#06b6d4" strokeWidth="2.5" strokeOpacity="0.8"/>
              <line x1="50" y1="50" x2="76" y2="65" stroke="#06b6d4" strokeWidth="2.5" strokeOpacity="0.8"/>
              <line x1="50" y1="50" x2="24" y2="35" stroke="#06b6d4" strokeWidth="2.5" strokeOpacity="0.8"/>
              <line x1="50" y1="50" x2="24" y2="65" stroke="#06b6d4" strokeWidth="2.5" strokeOpacity="0.8"/>
              <defs>
                <linearGradient id="hGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4" />
                  <stop offset="100%" stopColor="#3b82f6" />
                </linearGradient>
              </defs>
            </svg>
          </div>

          {/* Brand Text */}
          <div>
            <div className="flex items-center gap-2">
              <span className="font-orbitron font-black text-lg tracking-wider gradient-text-cyan group-hover:opacity-90 transition-opacity">
                SKILLGRAPH
              </span>
              <span className="hidden sm:inline-block px-1.5 py-0.5 text-[9px] font-mono tracking-widest text-cyan-400/60 border border-cyan-500/20 rounded-md">
                v1.0
              </span>
            </div>
            <p className="text-[10px] font-mono text-slate-600 tracking-wider hidden sm:block leading-none mt-0.5">
              Scan your skills. Engineer your future.
            </p>
          </div>
        </div>

        {/* Right Controls */}
        <div className="flex items-center gap-3">

          {/* SG-Core Status Pill */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/80 border border-slate-800 backdrop-blur-sm">
            <div className="relative">
              <span className="absolute w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping opacity-60" />
              <span className="relative w-2 h-2 rounded-full bg-cyan-400 block" />
            </div>
            <span className="text-xs font-mono font-medium text-slate-300 tracking-wider hidden md:inline">SG-CORE</span>
            <span className="text-[10px] font-mono text-cyan-400 font-semibold">ONLINE</span>
          </div>

          {/* New Scan Button */}
          {hasResults && (
            <button
              onClick={onReset}
              className="btn-secondary text-[11px] py-1.5 px-4"
            >
              <RotateCcw className="w-3 h-3" />
              <span>NEW SCAN</span>
            </button>
          )}
        </div>

      </div>
    </header>
  );
}
