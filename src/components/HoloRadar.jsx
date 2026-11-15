import React from 'react';
import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, Tooltip
} from 'recharts';
import { Target } from 'lucide-react';

const StatusColor = { HAVE: '#10b981', PARTIAL: '#f59e0b', MISSING: '#ef4444' };

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  const col = StatusColor[d.status] || '#06b6d4';
  return (
    <div className="p-3 rounded-xl bg-slate-900/95 border backdrop-blur-md text-xs font-mono" style={{ borderColor: `${col}50` }}>
      <div className="font-orbitron font-bold text-[#f0f9ff] mb-1.5">{d.subject}</div>
      <div className="flex items-center gap-2 mb-1">
        <span className="text-slate-500">Status:</span>
        <span className="font-bold" style={{ color: col }}>{d.status}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-slate-500">Mastery:</span>
        <span className="font-bold text-cyan-400">{d.user_level}%</span>
      </div>
    </div>
  );
};

export default function HoloRadar({ radarData, skills }) {
  return (
    <div className="hud-panel rounded-2xl p-6 sm:p-8 flex flex-col h-full relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/3 to-indigo-600/3 pointer-events-none" />
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent" />

      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800/60 mb-5">
        <div className="flex items-center gap-2">
          <Target className="w-4 h-4 text-cyan-400" />
          <span className="font-orbitron font-bold text-xs tracking-widest text-[#f0f9ff]">
            Competency Radar
          </span>
        </div>
        <div className="flex items-center gap-4 text-[10px] font-mono">
          <span className="flex items-center gap-1.5 text-cyan-400">
            <span className="w-2 h-2 rounded-full bg-cyan-400" /> Candidate
          </span>
          <span className="flex items-center gap-1.5 text-slate-600">
            <span className="w-2 h-2 rounded-full border border-slate-700" /> Baseline
          </span>
        </div>
      </div>

      {/* Chart (desktop) */}
      <div className="hidden md:block w-full flex-1" style={{ minHeight: '300px' }}>
        <ResponsiveContainer width="100%" height={300}>
          <RadarChart cx="50%" cy="50%" outerRadius="72%" data={radarData}>
            <defs>
              <radialGradient id="radarFill" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#06b6d4" stopOpacity={0.5} />
                <stop offset="100%" stopColor="#3b82f6" stopOpacity={0.1} />
              </radialGradient>
            </defs>
            <PolarGrid stroke="#1a2d4f" strokeDasharray="2 4" strokeOpacity={0.6} />
            <PolarAngleAxis
              dataKey="subject"
              stroke="#475569"
              tick={{ fill: '#64748b', fontSize: 10, fontFamily: 'JetBrains Mono' }}
            />
            <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#1a2d4f" tick={false} axisLine={false} />
            <Radar
              name="Baseline"
              dataKey="required_level"
              stroke="#1a2d4f"
              fill="#1a2d4f"
              fillOpacity={0.2}
            />
            <Radar
              name="Candidate"
              dataKey="user_level"
              stroke="#06b6d4"
              strokeWidth={2}
              fill="url(#radarFill)"
              fillOpacity={1}
            />
            <Tooltip content={<CustomTooltip />} />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Mobile: progress bars */}
      <div className="md:hidden space-y-3 mt-2">
        {skills.map((s, idx) => {
          const pct = s.status === 'HAVE' ? 100 : s.status === 'PARTIAL' ? 55 : 12;
          const col = StatusColor[s.status] || '#06b6d4';
          return (
            <div key={idx} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs font-mono">
                <span className="text-slate-300">{s.name}</span>
                <span className="font-bold" style={{ color: col }}>{s.status}</span>
              </div>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{ width: `${pct}%`, backgroundColor: col, boxShadow: `0 0 6px ${col}60` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer */}
      <div className="mt-5 pt-3 border-t border-slate-800/40 flex items-center justify-between text-[10px] font-mono text-slate-700">
        <span>{radarData?.length || 0} Core Skill Axes</span>
        <span className="text-cyan-500/60">Live Readout</span>
      </div>
    </div>
  );
}
