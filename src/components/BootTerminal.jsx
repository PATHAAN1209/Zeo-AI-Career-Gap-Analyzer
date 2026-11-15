import React, { useState, useEffect } from 'react';
import { Terminal, Check, Loader2 } from 'lucide-react';

export default function BootTerminal({ roleTitle }) {
  const [progress, setProgress] = useState(15);
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    { label: "Initializing SG-Core neural telemetry subsystem...", detail: "Kernel online" },
    { label: "Scanning resume document artifact in-memory...", detail: "Stream tokenized" },
    { label: `Cross-referencing candidate skills against ${roleTitle || 'target role'} baseline...`, detail: "Taxonomy mapped" },
    { label: "Calculating programmatic readiness score (HAVE=1.0, PARTIAL=0.5, MISSING=0)...", detail: "Matrix computed" },
    { label: "Resolving verified learning resources (Videos, Books, Courses)...", detail: "Cartridges bound" },
    { label: "Compiling personalized week-by-week build sequence & portfolio recommendations...", detail: "Roadmap locked" },
    { label: "Telemetry sync complete. Launching Career Dossier...", detail: "Complete" }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(timer);
          return 100;
        }
        return prev + 15;
      });

      setActiveStep((prev) => {
        if (prev < steps.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 400);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="w-full max-w-3xl mx-auto my-8 p-6 sm:p-8 rounded-3xl glass-panel relative overflow-hidden animate-scale-in border border-cyan-500/30">
      {/* Top glowing ambient gradient */}
      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent" />
      <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-80 h-32 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Terminal Title Bar */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800/80 mb-6 relative z-10">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-cyan-500/10 border border-cyan-500/25 flex items-center justify-center">
            <Terminal className="w-3.5 h-3.5 text-cyan-400" />
          </div>
          <div>
            <span className="font-orbitron font-bold text-xs tracking-widest text-[#f0f9ff]">
              SG-CORE // ANALYSIS SEQUENCE
            </span>
            <span className="block text-[9px] font-mono text-slate-500">
              IN-MEMORY TELEMETRY PROCESSING
            </span>
          </div>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-slate-700" />
          <div className="w-2.5 h-2.5 rounded-full bg-amber-500/60" />
          <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_8px_#22d3ee]" />
        </div>
      </div>

      {/* Progress Bar & Readout */}
      <div className="space-y-2 mb-8 relative z-10">
        <div className="flex items-center justify-between text-xs font-mono">
          <span className="text-slate-400 flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping" />
            COMPUTING COMPETENCY DELTAS
          </span>
          <span className="gradient-text-cyan font-orbitron font-black text-sm">
            {Math.min(progress, 100)}%
          </span>
        </div>
        <div className="h-2 w-full bg-slate-900/90 rounded-full overflow-hidden border border-slate-800 p-0.5">
          <div 
            className="h-full bg-gradient-to-r from-cyan-500 via-blue-500 to-indigo-500 transition-all duration-300 rounded-full shadow-[0_0_12px_rgba(6,182,212,0.6)]"
            style={{ width: `${Math.min(progress, 100)}%` }}
          />
        </div>
      </div>

      {/* Terminal Steps Log */}
      <div className="space-y-3 font-mono text-xs sm:text-sm relative z-10">
        {steps.map((step, idx) => {
          const isDone = idx < activeStep || progress >= 100;
          const isCurrent = idx === activeStep && progress < 100;

          return (
            <div 
              key={idx}
              className={`flex items-start gap-3 transition-all duration-300 ${
                idx > activeStep ? 'opacity-20' : 'opacity-100'
              }`}
            >
              <div className="mt-0.5 flex-shrink-0">
                {isDone ? (
                  <div className="w-4 h-4 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center">
                    <Check className="w-2.5 h-2.5 text-emerald-400" />
                  </div>
                ) : isCurrent ? (
                  <Loader2 className="w-4 h-4 text-cyan-400 animate-spin" />
                ) : (
                  <span className="w-4 h-4 rounded-full border border-slate-800 flex items-center justify-center text-[9px] text-slate-600">
                    {idx + 1}
                  </span>
                )}
              </div>

              <div className="flex-1 min-w-0 flex items-baseline justify-between gap-2">
                <span className={isCurrent ? "text-cyan-300 font-medium" : isDone ? "text-slate-200" : "text-slate-500"}>
                  {step.label}
                </span>
                {isDone && (
                  <span className="text-[10px] text-cyan-400/80 bg-cyan-950/40 px-2 py-0.5 rounded-md border border-cyan-500/20 whitespace-nowrap">
                    {step.detail}
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Bottom status readout */}
      <div className="mt-8 pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs font-mono text-slate-500 relative z-10">
        <span className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
          ISOLATED ENCLAVE // ZERO DISK PERSISTENCE
        </span>
        <span className="gradient-text-cyan font-semibold">SYNCHRONIZING...</span>
      </div>
    </div>
  );
}
