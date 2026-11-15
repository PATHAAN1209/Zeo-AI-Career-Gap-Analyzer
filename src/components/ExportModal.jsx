import React from 'react';
import { Printer, X, Award, CheckCircle2, ChevronRight, FileText } from 'lucide-react';

export default function ExportModal({ result, onClose }) {
  if (!result) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#030712]/80 backdrop-blur-xl animate-fade-in">
      <div className="w-full max-w-2xl rounded-3xl glass-panel border border-cyan-500/30 p-6 sm:p-8 space-y-6 max-h-[90vh] overflow-y-auto relative shadow-[0_0_50px_rgba(0,0,0,0.8)]">
        
        {/* Top gradient highlight */}
        <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent" />

        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800/80">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-cyan-500/10 border border-cyan-500/25 flex items-center justify-center">
              <Award className="w-4 h-4 text-cyan-400" />
            </div>
            <div>
              <h3 className="font-orbitron font-bold text-base sm:text-lg text-[#f0f9ff]">
                Career Dossier Export
              </h3>
              <p className="text-xs font-mono text-slate-500">{result.role_title} · Readiness Audit</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-500 hover:text-slate-200 hover:bg-slate-800/60 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Dossier Preview Summary */}
        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800/80 space-y-2.5 text-xs font-mono">
          <div className="flex items-center justify-between">
            <span className="text-slate-500">TARGET ROLE:</span>
            <span className="text-cyan-400 font-bold font-orbitron">{result.role_title}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-slate-500">READINESS METRIC:</span>
            <span className="text-emerald-400 font-bold font-orbitron text-sm">
              {result.readiness_score}% ({result.score_bracket})
            </span>
          </div>
          <div className="flex items-center justify-between border-t border-slate-800/60 pt-2">
            <span className="text-slate-500">DIAGNOSTIC VERDICT:</span>
            <span className="text-slate-200">{result.score_message}</span>
          </div>
        </div>

        {/* Roadmap Preview */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs font-mono">
            <h4 className="font-orbitron font-bold text-cyan-400 tracking-wider">
              ROADMAP SCHEDULE ({result.roadmap.length} WEEKS)
            </h4>
            <span className="text-slate-500">Curated Plan</span>
          </div>
          
          <div className="space-y-2.5 max-h-60 overflow-y-auto pr-1">
            {result.roadmap.map((week, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-slate-900/50 border border-slate-800/70 text-xs font-inter space-y-1.5 hover:border-slate-700 transition-colors">
                <div className="flex items-center justify-between">
                  <span className="font-orbitron text-xs text-cyan-300 font-bold">
                    Week {week.week_number} · {week.focus}
                  </span>
                  <span className="text-[10px] font-mono text-emerald-400/90 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20">
                    {week.expected_outcome}
                  </span>
                </div>
                <div className="text-slate-400 text-[11px] font-mono">
                  Skills: {week.skills_developed.join(', ')}
                </div>
                <div className="text-slate-300 text-xs leading-relaxed">
                  Tasks: {week.tasks.join(' • ')}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Print / Action Buttons */}
        <div className="pt-4 border-t border-slate-800/80 flex items-center justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-xl text-xs font-mono text-slate-400 hover:text-slate-200 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handlePrint}
            className="btn-primary"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print / Save PDF</span>
          </button>
        </div>

      </div>
    </div>
  );
}
