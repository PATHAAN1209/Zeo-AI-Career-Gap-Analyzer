import React, { useEffect, useState } from 'react';
import { Zap } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function ReactorRing({ score, message, bracket, stats }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const duration = 1400;
    const totalFrames = Math.round(duration / (1000 / 60));
    let frame = 0;
    const timer = setInterval(() => {
      frame++;
      // Ease-out cubic
      const progress = frame / totalFrames;
      const eased = 1 - Math.pow(1 - progress, 3);
      setAnimatedScore(Math.min(score, Math.round(score * eased)));
      if (frame >= totalFrames) {
        clearInterval(timer);
        setAnimatedScore(score);
        if (score >= 70) {
          try {
            confetti({ particleCount: 60, spread: 70, origin: { y: 0.6 }, colors: ['#06b6d4', '#3b82f6', '#10b981'] });
          } catch (e) {}
        }
      }
    }, 1000 / 60);
    return () => clearInterval(timer);
  }, [score]);

  const getTheme = () => {
    if (score >= 90) return { stroke: '#10b981', glow: 'rgba(16,185,129,0.6)', text: 'text-emerald-400', label: 'ELITE', labelColor: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30' };
    if (score >= 70) return { stroke: '#06b6d4', glow: 'rgba(6,182,212,0.6)', text: 'text-cyan-400', label: 'STRONG', labelColor: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/30' };
    if (score >= 40) return { stroke: '#f59e0b', glow: 'rgba(245,158,11,0.6)', text: 'text-amber-400', label: 'GROWING', labelColor: 'bg-amber-500/15 text-amber-400 border-amber-500/30' };
    return { stroke: '#ef4444', glow: 'rgba(239,68,68,0.6)', text: 'text-red-400', label: 'EARLY', labelColor: 'bg-red-500/15 text-red-400 border-red-500/30' };
  };

  const theme = getTheme();
  const radius = 78;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="hud-panel rounded-2xl p-6 sm:p-8 flex flex-col items-center text-center relative overflow-hidden">
      {/* Radial ambient */}
      <div
        className="absolute inset-0 opacity-15 pointer-events-none"
        style={{ background: `radial-gradient(ellipse at center, ${theme.stroke}30 0%, transparent 70%)` }}
      />

      {/* Top line */}
      <div className="absolute inset-x-0 top-0 h-px" style={{ background: `linear-gradient(to right, transparent, ${theme.stroke}60, transparent)` }} />

      {/* Header */}
      <div className="flex items-center gap-2 mb-5 z-10">
        <Zap className="w-4 h-4 text-cyan-400" />
        <span className="font-orbitron text-[10px] font-bold tracking-[0.2em] text-slate-500 uppercase">
          Career Readiness Reactor
        </span>
      </div>

      {/* SVG Ring */}
      <div className="relative w-56 h-56 flex items-center justify-center z-10">
        {/* Decorative outer rings */}
        <div className="absolute inset-0 rounded-full border border-slate-800/80 animate-radar-spin" />
        <div className="absolute inset-4 rounded-full border border-dashed border-slate-800/50" />
        <div className="absolute inset-8 rounded-full border border-slate-800/30" />

        <svg className="absolute w-full h-full -rotate-90" viewBox="0 0 200 200">
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="4" result="coloredBlur" />
              <feMerge><feMergeNode in="coloredBlur" /><feMergeNode in="SourceGraphic" /></feMerge>
            </filter>
            <linearGradient id="arcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor={theme.stroke} />
              <stop offset="100%" stopColor="#3b82f6" />
            </linearGradient>
          </defs>
          {/* Track */}
          <circle cx="100" cy="100" r={radius} fill="none" stroke="#0d1526" strokeWidth="12" />
          <circle cx="100" cy="100" r={radius} fill="none" stroke="#1a2d4f" strokeWidth="12" opacity="0.5" />
          {/* Progress arc */}
          <circle
            cx="100" cy="100" r={radius} fill="none"
            stroke="url(#arcGrad)"
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            filter="url(#glow)"
            className="transition-all duration-1000 ease-out"
          />
          {/* Secondary thin ring */}
          <circle
            cx="100" cy="100" r={radius - 16} fill="none"
            stroke={theme.stroke}
            strokeWidth="1.5"
            strokeDasharray={circumference - 100}
            strokeDashoffset={offset * 0.8}
            opacity="0.3"
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center readout */}
        <div className="absolute flex flex-col items-center justify-center gap-1">
          <span className="font-orbitron font-black text-5xl leading-none" style={{ color: theme.stroke }}>
            {animatedScore}
            <span className="text-2xl font-mono text-slate-500">%</span>
          </span>
          <span className={`text-[9px] font-mono font-bold tracking-widest px-2.5 py-1 rounded-full border ${theme.labelColor}`}>
            {theme.label}
          </span>
        </div>
      </div>

      {/* Message */}
      <div className="mt-5 max-w-xs z-10 space-y-1">
        <h4 className={`font-orbitron font-bold text-sm sm:text-base ${theme.text}`}>{message}</h4>
        <p className="font-inter text-xs text-slate-600 leading-relaxed">
          Programmatically derived from {bracket} role competency requirements
        </p>
      </div>

      {/* Stats breakdown */}
      {stats && (
        <div className="grid grid-cols-3 gap-2 w-full max-w-xs mt-6 pt-5 border-t border-slate-800/60 z-10">
          {[
            { label: 'Have', val: stats.have_count, color: '#10b981', bg: 'bg-emerald-500/8', border: 'border-emerald-500/20' },
            { label: 'Partial', val: stats.partial_count, color: '#f59e0b', bg: 'bg-amber-500/8', border: 'border-amber-500/20' },
            { label: 'Missing', val: stats.missing_count, color: '#ef4444', bg: 'bg-red-500/8', border: 'border-red-500/20' },
          ].map((s) => (
            <div key={s.label} className={`p-2.5 rounded-xl ${s.bg} border ${s.border} flex flex-col items-center`}>
              <div className="text-[9px] font-mono text-slate-600 uppercase tracking-widest">{s.label}</div>
              <div className="font-orbitron font-black text-xl mt-0.5" style={{ color: s.color }}>{s.val}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
