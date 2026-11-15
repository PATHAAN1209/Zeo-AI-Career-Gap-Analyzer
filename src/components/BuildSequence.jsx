import React, { useState } from 'react';
import { Calendar, CheckSquare, Square, Award, BookOpen, Map } from 'lucide-react';

const WEEK_COLORS = [
  { accent: '#06b6d4', bg: 'rgba(6,182,212,0.08)', border: 'rgba(6,182,212,0.25)' },
  { accent: '#3b82f6', bg: 'rgba(59,130,246,0.08)', border: 'rgba(59,130,246,0.25)' },
  { accent: '#8b5cf6', bg: 'rgba(139,92,246,0.08)', border: 'rgba(139,92,246,0.25)' },
  { accent: '#10b981', bg: 'rgba(16,185,129,0.08)', border: 'rgba(16,185,129,0.25)' },
  { accent: '#f59e0b', bg: 'rgba(245,158,11,0.08)', border: 'rgba(245,158,11,0.25)' },
  { accent: '#ec4899', bg: 'rgba(236,72,153,0.08)', border: 'rgba(236,72,153,0.25)' },
];

export default function BuildSequence({ roadmap }) {
  const [completedTasks, setCompletedTasks] = useState({});

  const toggleTask = (weekIdx, taskIdx) => {
    const key = `${weekIdx}-${taskIdx}`;
    setCompletedTasks((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800/60">
        <div className="space-y-1">
          <h3 className="font-orbitron font-bold text-lg text-[#f0f9ff] flex items-center gap-2.5">
            <Map className="w-4 h-4 text-cyan-400" />
            Build Sequence
          </h3>
          <p className="text-xs font-mono text-slate-600">
            Week-by-week roadmap targeting your highest-impact skill gaps
          </p>
        </div>
        <span className="self-start sm:self-auto text-xs font-mono px-3 py-1.5 rounded-xl bg-slate-900/60 border border-slate-800 text-cyan-400">
          {roadmap.length} Weeks to Interview Readiness
        </span>
      </div>

      {/* Timeline */}
      <div className="relative pl-8 sm:pl-10 space-y-6">
        {/* Vertical line */}
        <div className="absolute left-3 sm:left-4 top-2 bottom-2 w-0.5 rounded-full bg-gradient-to-b from-cyan-500 via-blue-600 to-slate-800/20" />

        {roadmap.map((week, wIdx) => {
          const palette = WEEK_COLORS[wIdx % WEEK_COLORS.length];
          const completedCount = week.tasks.filter((_, tIdx) => completedTasks[`${wIdx}-${tIdx}`]).length;
          const progressPct = week.tasks.length > 0 ? (completedCount / week.tasks.length) * 100 : 0;

          return (
            <div key={wIdx} className="relative group animate-slide-up" style={{ animationDelay: `${wIdx * 0.08}s` }}>

              {/* Timeline node */}
              <div
                className="absolute -left-[20px] sm:-left-[26px] top-5 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-300 group-hover:scale-110"
                style={{ borderColor: palette.accent, background: `${palette.bg}`, boxShadow: `0 0 12px ${palette.accent}40` }}
              >
                <span className="font-orbitron font-black text-[8px]" style={{ color: palette.accent }}>
                  {week.week_number}
                </span>
              </div>

              {/* Week card */}
              <div
                className="rounded-2xl glass-panel p-5 sm:p-6 transition-all duration-300 overflow-hidden"
                style={{ borderColor: `rgba(26,45,79,0.9)` }}
              >
                {/* Accent top line */}
                <div className="absolute inset-x-0 top-0 h-0.5 rounded-t-2xl" style={{ background: `linear-gradient(to right, transparent, ${palette.accent}60, transparent)` }} />

                {/* Week header */}
                <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 mb-4">
                  <div className="flex items-center gap-3">
                    <span
                      className="font-orbitron font-bold text-[10px] tracking-widest px-2.5 py-1 rounded-lg border"
                      style={{ color: palette.accent, background: palette.bg, borderColor: palette.border }}
                    >
                      WEEK {week.week_number}
                    </span>
                    <h4 className="font-orbitron font-bold text-sm sm:text-base text-[#f0f9ff]">{week.focus}</h4>
                  </div>

                  {/* Progress */}
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <div className="w-16 h-1.5 rounded-full bg-slate-800 overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{ width: `${progressPct}%`, backgroundColor: palette.accent }}
                      />
                    </div>
                    <span className="text-[10px] font-mono text-slate-600">{completedCount}/{week.tasks.length}</span>
                  </div>
                </div>

                {/* Skill tags */}
                {week.skills_developed?.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mb-4">
                    {week.skills_developed.map((sk, sIdx) => (
                      <span
                        key={sIdx}
                        className="text-[10px] font-mono px-2 py-0.5 rounded-md border"
                        style={{ color: palette.accent, background: palette.bg, borderColor: palette.border }}
                      >
                        {sk}
                      </span>
                    ))}
                  </div>
                )}

                {/* Tasks */}
                <div className="space-y-2 mb-4">
                  <span className="text-[10px] font-mono text-slate-600 uppercase tracking-widest block">Execution Tasks</span>
                  {week.tasks.map((task, tIdx) => {
                    const isChecked = !!completedTasks[`${wIdx}-${tIdx}`];
                    return (
                      <div
                        key={tIdx}
                        onClick={() => toggleTask(wIdx, tIdx)}
                        className={`flex items-start gap-3 p-2.5 rounded-xl cursor-pointer transition-all duration-200 border ${
                          isChecked
                            ? 'bg-slate-900/30 border-slate-800/30 text-slate-600'
                            : 'bg-slate-900/50 border-slate-800/60 text-slate-300 hover:border-slate-700'
                        }`}
                      >
                        <div className="mt-0.5 flex-shrink-0">
                          {isChecked
                            ? <CheckSquare className="w-4 h-4" style={{ color: palette.accent }} />
                            : <Square className="w-4 h-4 text-slate-600" />
                          }
                        </div>
                        <span className={`font-inter text-xs sm:text-sm leading-relaxed ${isChecked ? 'line-through' : ''}`}>
                          {task}
                        </span>
                      </div>
                    );
                  })}
                </div>

                {/* Footer: resources + outcome */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-4 border-t border-slate-800/40">
                  <div className="flex items-start gap-2 bg-slate-900/40 rounded-xl p-3 border border-slate-800/40">
                    <BookOpen className="w-3.5 h-3.5 text-cyan-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <span className="text-[9px] font-mono text-slate-600 uppercase tracking-wider block">Blueprint</span>
                      <span className="text-xs font-inter text-slate-400 leading-snug">{week.recommended_resources?.join(' • ')}</span>
                    </div>
                  </div>
                  <div className="flex items-start gap-2 bg-slate-900/40 rounded-xl p-3 border border-slate-800/40">
                    <Award className="w-3.5 h-3.5 text-emerald-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <span className="text-[9px] font-mono text-slate-600 uppercase tracking-wider block">Milestone</span>
                      <span className="text-xs font-inter text-slate-400 leading-snug">{week.expected_outcome}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
