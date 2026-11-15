import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import SGCore from './components/SGCore';
import Scanner from './components/Scanner';
import BootTerminal from './components/BootTerminal';
import ReactorRing from './components/ReactorRing';
import HoloRadar from './components/HoloRadar';
import StatusModules from './components/StatusModules';
import BuildSequence from './components/BuildSequence';
import ProjectCards from './components/ProjectCards';
import DataCartridges from './components/DataCartridges';
import Missions from './components/Missions';
import ExportModal from './components/ExportModal';

import { fetchRoles, fetchDemoAnalysis, analyzeResume } from './services/api';
import { ArrowLeft, Download, RefreshCw, Sparkles, AlertCircle, ChevronRight, Zap } from 'lucide-react';

export default function App() {
  const [roles, setRoles] = useState([]);
  const [selectedRoleId, setSelectedRoleId] = useState('frontend-web-developer');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');
  const [showExportModal, setShowExportModal] = useState(false);
  const [activeCartridgeSkill, setActiveCartridgeSkill] = useState('');
  const [coPilotStatus, setCoPilotStatus] = useState('Standby. Select target career role and scan resume.');

  useEffect(() => {
    async function initRoles() {
      try {
        const loadedRoles = await fetchRoles();
        setRoles(loadedRoles);
        if (loadedRoles.length > 0) setSelectedRoleId(loadedRoles[0].id);
      } catch (err) {
        console.error('Failed to initialize roles:', err);
      }
    }
    initRoles();
  }, []);

  const handleAnalyze = async ({ file, roleId, resumeText }) => {
    setIsAnalyzing(true);
    setErrorMsg('');
    setCoPilotStatus('Scanning resume document stream in-memory...');
    try {
      const [result] = await Promise.all([
        analyzeResume({ file, roleId, resumeText }),
        new Promise((resolve) => setTimeout(resolve, 2800))
      ]);
      setAnalysisResult(result);
      setCoPilotStatus(result.summary_insight || 'Analysis complete. Build sequence locked.');
    } catch (err) {
      setErrorMsg(err.message || 'An error occurred during resume analysis.');
      setCoPilotStatus('Error encountered during document parsing.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleQuickDemo = async (roleId) => {
    setSelectedRoleId(roleId);
    setIsAnalyzing(true);
    setErrorMsg('');
    setCoPilotStatus(`Synthesizing candidate telemetry for ${roleId}...`);
    try {
      const [result] = await Promise.all([
        fetchDemoAnalysis(roleId),
        new Promise((resolve) => setTimeout(resolve, 2400))
      ]);
      setAnalysisResult(result);
      setCoPilotStatus(result.summary_insight || 'Demo telemetry loaded. Ready for inspection.');
    } catch (err) {
      setErrorMsg('Failed to load demo scenario.');
      setCoPilotStatus('Demo telemetry unavailable.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setErrorMsg('');
    setCoPilotStatus('Standby. Select target career role and scan resume.');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectSkillToLearn = (skillName) => {
    setActiveCartridgeSkill(skillName);
    document.getElementById('data-cartridges-section')?.scrollIntoView({ behavior: 'smooth' });
  };

  const currentRole = roles.find((r) => r.id === selectedRoleId) || roles[0] || { title: 'Target Career Role' };

  return (
    <div className="min-h-screen mesh-bg text-[#f0f9ff] flex flex-col font-inter relative">
      {/* Grid overlay */}
      <div className="fixed inset-0 grid-overlay pointer-events-none z-0" />

      {/* Floating ambient orbs */}
      <div className="fixed top-[-10%] left-[-5%] w-[600px] h-[600px] rounded-full bg-indigo-600/8 blur-[120px] pointer-events-none z-0 animate-float-orb" />
      <div className="fixed top-[30%] right-[-8%] w-[500px] h-[500px] rounded-full bg-cyan-500/6 blur-[100px] pointer-events-none z-0 animate-float-orb-r" />
      <div className="fixed bottom-[10%] left-[20%] w-[400px] h-[400px] rounded-full bg-blue-600/5 blur-[90px] pointer-events-none z-0 animate-float-orb" style={{animationDelay: '3s'}} />

      {/* Navbar */}
      <Header onReset={handleReset} hasResults={!!analysisResult} />

      {/* Body */}
      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">

        {/* Error Banner */}
        {errorMsg && (
          <div className="flex items-center justify-between p-4 rounded-2xl bg-red-500/8 border border-red-500/30 backdrop-blur-sm animate-slide-up">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-red-500/15 flex items-center justify-center flex-shrink-0">
                <AlertCircle className="w-4 h-4 text-red-400" />
              </div>
              <span className="font-mono text-sm text-red-300">{errorMsg}</span>
            </div>
            <button
              onClick={() => setErrorMsg('')}
              className="text-xs font-mono text-red-400 hover:text-red-200 transition-colors px-3 py-1 rounded-lg hover:bg-red-500/10"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* BOOT TERMINAL */}
        {isAnalyzing ? (
          <div className="py-8 animate-fade-in">
            <BootTerminal roleTitle={currentRole.title} />
          </div>
        ) : !analysisResult ? (

          /* ---- LANDING PAGE ---- */
          <div className="space-y-10 animate-fade-in">

            {/* Hero */}
            <div className="text-center space-y-6 max-w-4xl mx-auto pt-6 pb-2">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-cyan-500/25 bg-cyan-500/8 backdrop-blur-sm text-xs font-mono tracking-widest uppercase text-cyan-400 mb-2">
                <Sparkles className="w-3 h-3" />
                Next-Gen Career Intelligence Platform
                <span className="w-1 h-1 rounded-full bg-cyan-400 animate-pulse" />
              </div>

              <h1 className="font-orbitron font-black text-4xl sm:text-6xl lg:text-7xl tracking-tight leading-[1.05]">
                <span className="text-[#f0f9ff]">Scan your skills.</span>
                <br />
                <span className="gradient-text-hero">Engineer your future.</span>
              </h1>

              <p className="font-inter text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
                Upload your resume, select your target career role, and let AI conduct a precision skill gap audit.
                Get a readiness score, roadmap, and curated resources — instantly.
              </p>

              <div className="flex flex-wrap items-center justify-center gap-6 pt-2">
                {[
                  { label: '250+', desc: 'Career Roles' },
                  { label: '10', desc: 'Industry Domains' },
                  { label: 'AI', desc: 'Powered Analysis' },
                ].map((stat) => (
                  <div key={stat.label} className="flex items-center gap-2.5">
                    <span className="font-orbitron font-black text-2xl gradient-text-cyan">{stat.label}</span>
                    <span className="text-xs font-mono text-slate-500">{stat.desc}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* SG-Core */}
            <div className="max-w-4xl mx-auto">
              <SGCore statusMessage={coPilotStatus} insight={null} isAnalyzing={isAnalyzing} />
            </div>

            {/* Scanner panel */}
            <div className="glass-panel rounded-3xl p-6 sm:p-10">
              <Scanner
                roles={roles}
                selectedRoleId={selectedRoleId}
                onSelectRole={setSelectedRoleId}
                onAnalyze={handleAnalyze}
                isAnalyzing={isAnalyzing}
                onQuickDemo={handleQuickDemo}
              />
            </div>

          </div>

        ) : (

          /* ---- RESULTS DASHBOARD ---- */
          <div className="space-y-10 animate-scale-in">

            {/* Results Header */}
            <div className="relative overflow-hidden rounded-3xl glass-panel p-6 sm:p-8">
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 via-transparent to-indigo-600/5 pointer-events-none" />
              <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

              <div className="relative flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-xs font-mono text-cyan-400">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
                    <span>ANALYSIS DOSSIER</span>
                    <ChevronRight className="w-3 h-3 text-slate-600" />
                    <span className="text-slate-400">{analysisResult.category}</span>
                  </div>
                  <h2 className="font-orbitron font-black text-2xl sm:text-4xl text-[#f0f9ff]">
                    {analysisResult.role_title}
                  </h2>
                  <p className="text-sm font-mono text-slate-500">Skill gap analysis completed · SG-Core telemetry synced</p>
                </div>

                <div className="flex items-center gap-3 flex-shrink-0">
                  <button
                    onClick={() => setShowExportModal(true)}
                    className="btn-secondary"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Export Dossier</span>
                  </button>
                  <button
                    onClick={handleReset}
                    className="btn-primary"
                  >
                    <RefreshCw className="w-3.5 h-3.5" />
                    <span>New Scan</span>
                  </button>
                </div>
              </div>
            </div>

            {/* SG-Core insight */}
            <SGCore
              statusMessage={analysisResult.co_pilot_status || 'Analysis locked and verified.'}
              insight={analysisResult.summary_insight}
              isAnalyzing={false}
            />

            {/* Reactor Ring + Radar */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              <div className="lg:col-span-5">
                <ReactorRing
                  score={analysisResult.readiness_score}
                  message={analysisResult.score_message}
                  bracket={analysisResult.score_bracket}
                  stats={analysisResult.stats}
                />
              </div>
              <div className="lg:col-span-7">
                <HoloRadar radarData={analysisResult.radar_data} skills={analysisResult.skills} />
              </div>
            </div>

            {/* Status Modules */}
            <StatusModules skills={analysisResult.skills} onSelectSkillToLearn={handleSelectSkillToLearn} />

            {/* Build Sequence */}
            <BuildSequence roadmap={analysisResult.roadmap} />

            {/* Portfolio Projects */}
            <ProjectCards projects={analysisResult.projects} />

            {/* Data Cartridges */}
            <div id="data-cartridges-section">
              <DataCartridges
                resources={analysisResult.resources}
                activeSkill={activeCartridgeSkill}
                onSelectSkill={setActiveCartridgeSkill}
              />
            </div>

            {/* Missions */}
            <Missions opportunities={analysisResult.opportunities} roleTitle={analysisResult.role_title} />

          </div>
        )}

      </main>

      {/* Export Modal */}
      {showExportModal && analysisResult && (
        <ExportModal result={analysisResult} onClose={() => setShowExportModal(false)} />
      )}

      {/* Footer */}
      <footer className="relative z-10 w-full border-t border-slate-800/60 bg-[#030712]/80 backdrop-blur-sm py-8">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="font-orbitron font-black text-sm gradient-text-cyan">SKILLGRAPH</span>
            <span className="text-slate-700 font-mono text-xs">//</span>
            <span className="text-xs font-mono text-slate-600">Engineer Your Future</span>
          </div>
          <div className="text-xs font-mono text-slate-700">
            Powered by React 18 · Vite · TailwindCSS · FastAPI · SG-Core
          </div>
        </div>
      </footer>
    </div>
  );
}
