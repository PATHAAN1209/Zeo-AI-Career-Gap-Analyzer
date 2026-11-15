import React, { useState, useRef, useMemo } from 'react';
import {
  Upload, FileText, CheckCircle2, AlertTriangle, ArrowRight,
  ShieldCheck, FileCode, Sparkles, X, Search, Briefcase, Layers, Zap
} from 'lucide-react';

export default function Scanner({ roles = [], selectedRoleId, onSelectRole, onAnalyze, isAnalyzing, onQuickDemo }) {
  const [file, setFile] = useState(null);
  const [fileError, setFileError] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [showPasteText, setShowPasteText] = useState(false);
  const [pastedText, setPastedText] = useState('');
  const [activeCategory, setActiveCategory] = useState('All Categories');
  const [searchQuery, setSearchQuery] = useState('');
  const fileInputRef = useRef(null);

  const categoriesWithCounts = useMemo(() => {
    const map = {};
    roles.forEach((r) => { const c = r.category || 'General'; map[c] = (map[c] || 0) + 1; });
    return [{ name: 'All Categories', count: roles.length }, ...Object.keys(map).map((c) => ({ name: c, count: map[c] }))];
  }, [roles]);

  const filteredRoles = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    return roles.filter((r) => {
      const matchCat = activeCategory === 'All Categories' || r.category === activeCategory;
      const matchQ = !q || r.title.toLowerCase().includes(q) || r.category?.toLowerCase().includes(q);
      return matchCat && matchQ;
    });
  }, [roles, activeCategory, searchQuery]);

  const selectedRole = useMemo(() => roles.find((r) => r.id === selectedRoleId) || roles[0] || null, [roles, selectedRoleId]);

  const validateAndSetFile = (f) => {
    setFileError('');
    if (!f) return;
    if (!f.name.toLowerCase().endsWith('.pdf')) { setFileError('Invalid format. Please upload a PDF file.'); return; }
    if (f.size > 5 * 1024 * 1024) { setFileError(`File too large (${(f.size / 1048576).toFixed(1)} MB). Max 5 MB.`); return; }
    setFile(f);
  };

  const handleDrop = (e) => { e.preventDefault(); setIsDragging(false); if (e.dataTransfer.files?.[0]) validateAndSetFile(e.dataTransfer.files[0]); };
  const handleAnalyzeClick = () => {
    if (!file && !pastedText.trim()) { setFileError('Upload a PDF or paste resume text to begin.'); return; }
    onAnalyze({ file, roleId: selectedRoleId, resumeText: pastedText });
  };

  // Gradient color for each category pill
  const CAT_COLORS = [
    'from-cyan-500/20 to-blue-600/20 border-cyan-500/30 text-cyan-300',
    'from-violet-500/20 to-purple-600/20 border-violet-500/30 text-violet-300',
    'from-blue-500/20 to-indigo-600/20 border-blue-500/30 text-blue-300',
    'from-emerald-500/20 to-teal-600/20 border-emerald-500/30 text-emerald-300',
    'from-amber-500/20 to-orange-600/20 border-amber-500/30 text-amber-300',
    'from-pink-500/20 to-rose-600/20 border-pink-500/30 text-pink-300',
    'from-teal-500/20 to-cyan-600/20 border-teal-500/30 text-teal-300',
    'from-purple-500/20 to-pink-600/20 border-purple-500/30 text-purple-300',
    'from-sky-500/20 to-blue-600/20 border-sky-500/30 text-sky-300',
    'from-lime-500/20 to-green-600/20 border-lime-500/30 text-lime-300',
    'from-orange-500/20 to-red-600/20 border-orange-500/30 text-orange-300',
  ];

  return (
    <div className="w-full max-w-5xl mx-auto space-y-10">

      {/* ========== STEP 1: ROLE SELECTION ========== */}
      <div className="space-y-5">

        {/* Section header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-800/60">
          <div className="section-label">Step 1: Select Target Career Role</div>
          <div className="flex items-center gap-2 text-xs font-mono text-cyan-400 bg-cyan-500/8 border border-cyan-500/20 px-3 py-1 rounded-full">
            <Briefcase className="w-3.5 h-3.5" />
            {roles.length} Roles · 10 Domains
          </div>
        </div>

        {/* Selected role dossier banner */}
        {selectedRole && (
          <div className="relative rounded-2xl overflow-hidden border border-cyan-500/25 bg-gradient-to-br from-cyan-500/8 via-slate-900/80 to-blue-600/5 p-5 backdrop-blur-sm">
            <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent" />
            <div className="absolute top-0 right-0 w-40 h-40 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[9px] font-mono font-bold tracking-widest bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 uppercase">
                    ● Locked Target
                  </span>
                  <span className="text-xs font-mono text-slate-500">{selectedRole.category}</span>
                </div>
                <h3 className="font-orbitron font-black text-xl sm:text-2xl text-[#f0f9ff]">{selectedRole.title}</h3>
                <p className="font-inter text-xs sm:text-sm text-slate-500 max-w-2xl leading-relaxed">{selectedRole.description}</p>
              </div>

              <div className="flex items-center gap-4 flex-shrink-0">
                <div className="text-right">
                  <div className="text-[10px] font-mono text-slate-600 uppercase tracking-wider">Core Skills</div>
                  <div className="font-orbitron font-black text-2xl gradient-text-cyan">
                    {selectedRole.required_skills?.length || 8}
                  </div>
                </div>
                <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/25 flex items-center justify-center">
                  <CheckCircle2 className="w-6 h-6 text-cyan-400" />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Search + dropdown */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
          <div className="md:col-span-7 relative">
            <Search className="w-4 h-4 text-slate-600 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search 250+ roles (e.g. Full-Stack, MLOps, Penetration Tester, UX...)"
              className="w-full pl-10 pr-10 py-3 rounded-xl bg-slate-900/60 border border-slate-800 text-sm font-mono text-[#f0f9ff] placeholder-slate-600 focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/20 transition-all backdrop-blur-sm"
            />
            {searchQuery && (
              <button onClick={() => setSearchQuery('')} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-600 hover:text-slate-300">
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          <div className="md:col-span-5">
            <select
              value={selectedRoleId}
              onChange={(e) => onSelectRole(e.target.value)}
              className="w-full py-3 px-4 rounded-xl bg-slate-900/60 border border-slate-800 text-sm font-mono text-cyan-400 focus:border-cyan-500/60 focus:ring-1 focus:ring-cyan-500/20 cursor-pointer transition-all backdrop-blur-sm"
            >
              {categoriesWithCounts.filter((c) => c.name !== 'All Categories').map((cat) => {
                const catRoles = roles.filter((r) => r.category === cat.name);
                return (
                  <optgroup key={cat.name} label={`${cat.name} (${catRoles.length})`} className="bg-[#0a0f1e] text-slate-500">
                    {catRoles.map((r) => (
                      <option key={r.id} value={r.id} className="bg-[#0d1526] text-[#f0f9ff]">{r.title}</option>
                    ))}
                  </optgroup>
                );
              })}
            </select>
          </div>
        </div>

        {/* Category pills */}
        <div className="space-y-2">
          <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-600 uppercase tracking-wider">
            <Layers className="w-3 h-3 text-cyan-500" />
            Filter by Domain:
          </div>
          <div className="flex gap-2 overflow-x-auto pb-2">
            {categoriesWithCounts.map((cat, idx) => {
              const isActive = activeCategory === cat.name;
              const colorClass = cat.name === 'All Categories' ? 'from-slate-700/40 to-slate-800/40 border-slate-700 text-slate-300' : CAT_COLORS[(idx - 1) % CAT_COLORS.length];
              return (
                <button
                  key={cat.name}
                  onClick={() => setActiveCategory(cat.name)}
                  className={`flex-shrink-0 px-3.5 py-1.5 rounded-lg text-xs font-mono whitespace-nowrap transition-all duration-200 border flex items-center gap-1.5 bg-gradient-to-r ${
                    isActive ? colorClass + ' opacity-100 shadow-sm' : 'from-transparent to-transparent border-slate-800 text-slate-600 hover:border-slate-700 hover:text-slate-400'
                  }`}
                >
                  {cat.name === 'All Categories' ? '⊞ All' : cat.name.split(',')[0]}
                  <span className={`text-[9px] px-1 py-0.5 rounded ${isActive ? 'bg-black/20' : 'bg-slate-900'} leading-none`}>
                    {cat.count}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Roles grid */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-mono text-slate-600">
            <span>Showing {filteredRoles.length} roles</span>
            {searchQuery && <span className="text-cyan-500">"{searchQuery}"</span>}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 max-h-80 overflow-y-auto pr-1 rounded-2xl">
            {filteredRoles.map((r) => {
              const isSelected = r.id === selectedRoleId;
              return (
                <button
                  key={r.id}
                  onClick={() => onSelectRole(r.id)}
                  className={`text-left p-3.5 rounded-xl border transition-all duration-200 relative overflow-hidden group flex flex-col justify-between ${
                    isSelected
                      ? 'bg-cyan-500/8 border-cyan-500/40 shadow-[0_0_15px_rgba(6,182,212,0.12)] ring-1 ring-cyan-500/20'
                      : 'bg-slate-900/50 border-slate-800/60 hover:border-slate-700 hover:bg-slate-900/80'
                  }`}
                >
                  {isSelected && (
                    <>
                      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-cyan-500/60 to-transparent" />
                      <div className="absolute top-2 right-2 w-5 h-5 rounded-full bg-cyan-500/15 border border-cyan-500/40 flex items-center justify-center">
                        <CheckCircle2 className="w-3 h-3 text-cyan-400" />
                      </div>
                    </>
                  )}

                  <div>
                    <div className="text-[9px] font-mono text-slate-600 mb-1 truncate">{r.category}</div>
                    <div className={`font-orbitron font-bold text-xs leading-snug mb-1.5 transition-colors ${isSelected ? 'text-cyan-300' : 'text-[#f0f9ff] group-hover:text-cyan-300'}`}>
                      {r.title}
                    </div>
                    <div className="text-[11px] font-inter text-slate-600 line-clamp-2 leading-relaxed">{r.description}</div>
                  </div>

                  <div className="mt-2.5 pt-2 border-t border-slate-800/40 flex items-center justify-between text-[9px] font-mono">
                    <span className="text-slate-700">{r.required_skills?.length || 8} skills</span>
                    <span className={`transition-colors ${isSelected ? 'text-cyan-400 font-bold' : 'text-slate-700 group-hover:text-cyan-500'}`}>
                      {isSelected ? '● ACTIVE' : 'SELECT →'}
                    </span>
                  </div>
                </button>
              );
            })}

            {filteredRoles.length === 0 && (
              <div className="col-span-full py-10 text-center space-y-2">
                <p className="font-mono text-sm text-slate-600">No roles matched "{searchQuery}"</p>
                <button onClick={() => { setSearchQuery(''); setActiveCategory('All Categories'); }} className="text-xs font-mono text-cyan-500 hover:underline">
                  Clear filters
                </button>
              </div>
            )}
          </div>
        </div>

      </div>

      {/* ========== STEP 2: RESUME UPLOAD ========== */}
      <div className="space-y-4 pt-4 border-t border-slate-800/60">

        <div className="flex items-center justify-between">
          <div className="section-label">Step 2: Scan Resume Artifact</div>
          <button
            onClick={() => setShowPasteText(!showPasteText)}
            className="text-xs font-mono text-slate-500 hover:text-cyan-400 transition-colors flex items-center gap-1.5"
          >
            <FileCode className="w-3.5 h-3.5" />
            {showPasteText ? 'Switch to PDF Upload' : 'Paste Text Instead'}
          </button>
        </div>

        {!showPasteText ? (
          <div
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`relative rounded-2xl border-2 border-dashed p-10 sm:p-14 text-center cursor-pointer transition-all duration-300 overflow-hidden hud-bg-grid ${
              isDragging
                ? 'border-cyan-500/70 bg-cyan-500/8 shadow-[0_0_30px_rgba(6,182,212,0.15)]'
                : file
                ? 'border-emerald-500/50 bg-emerald-500/5'
                : 'border-slate-800 hover:border-slate-700 bg-slate-900/30'
            }`}
          >
            {/* Scanner line */}
            {isDragging && (
              <div className="absolute inset-x-0 h-0.5 bg-gradient-to-r from-transparent via-cyan-400 to-transparent animate-scanner-sweep shadow-[0_0_10px_#06b6d4]" />
            )}
            <input ref={fileInputRef} type="file" accept=".pdf" className="hidden" onChange={(e) => validateAndSetFile(e.target.files?.[0])} />

            {file ? (
              <div className="flex flex-col items-center gap-3">
                <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
                  <FileText className="w-8 h-8 text-emerald-400" />
                </div>
                <div>
                  <h4 className="font-orbitron font-bold text-base text-[#f0f9ff]">{file.name}</h4>
                  <p className="font-mono text-xs text-slate-500 mt-1">{(file.size / 1024).toFixed(1)} KB · PDF Verified</p>
                </div>
                <button onClick={(e) => { e.stopPropagation(); setFile(null); }} className="text-xs font-mono text-red-400 hover:text-red-300 flex items-center gap-1 mt-1">
                  <X className="w-3.5 h-3.5" /> Remove file
                </button>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-4">
                <div className={`w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-300 ${
                  isDragging ? 'bg-cyan-500/20 border-2 border-cyan-500/50' : 'bg-slate-800/60 border border-slate-700'
                }`}>
                  <Upload className={`w-8 h-8 transition-colors ${isDragging ? 'text-cyan-400' : 'text-slate-500'}`} />
                </div>
                <div>
                  <h4 className="font-orbitron font-semibold text-base text-[#f0f9ff]">Drop Resume PDF Here</h4>
                  <p className="font-inter text-sm text-slate-500 mt-1">
                    or <span className="text-cyan-400 font-medium cursor-pointer hover:underline">browse files</span> · Max 5 MB
                  </p>
                </div>
                <div className="flex items-center gap-2 px-3 py-1 rounded-lg bg-slate-900/60 border border-slate-800 text-[10px] font-mono text-slate-600">
                  <span>PDF ONLY</span>
                  <span>·</span>
                  <span>IN-MEMORY · NEVER STORED</span>
                </div>
              </div>
            )}
          </div>
        ) : (
          <textarea
            rows={8}
            value={pastedText}
            onChange={(e) => setPastedText(e.target.value)}
            placeholder="Paste your resume text here (experience, skills, projects, education, certifications)..."
            className="w-full rounded-2xl bg-slate-900/60 border border-slate-800 p-4 font-mono text-xs sm:text-sm text-[#f0f9ff] placeholder-slate-600 focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/15 transition-all backdrop-blur-sm resize-none"
          />
        )}

        {fileError && (
          <div className="flex items-center gap-2 p-3 rounded-xl bg-red-500/8 border border-red-500/25 text-red-400 text-xs font-mono">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            <span>{fileError}</span>
          </div>
        )}
      </div>

      {/* ========== STEP 3: LAUNCH ========== */}
      <div className="pt-4 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between gap-4">

        <div className="flex items-center gap-2 text-xs font-inter text-slate-600">
          <ShieldCheck className="w-4 h-4 text-emerald-500" />
          <span>Processed in-memory only. Zero data retention.</span>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          {/* Quick Demo */}
          <button
            onClick={() => onQuickDemo(selectedRoleId || 'frontend-web-developer')}
            disabled={isAnalyzing}
            className="btn-secondary text-[10px] py-2.5 px-4 flex-shrink-0"
          >
            <Sparkles className="w-3 h-3" />
            <span>Quick Demo</span>
          </button>

          {/* Primary button */}
          <button
            onClick={handleAnalyzeClick}
            disabled={isAnalyzing || (!file && !pastedText.trim())}
            className="btn-primary w-full sm:w-auto justify-center group"
          >
            <Zap className="w-4 h-4" />
            <span>{isAnalyzing ? 'Scanning...' : `Analyze · ${selectedRole?.title?.split(' ').slice(0, 3).join(' ') || 'Role'}`}</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>

    </div>
  );
}
