import React, { useState } from 'react';
import { Video, Book, GraduationCap, ExternalLink, Sparkles, BookOpen } from 'lucide-react';

export default function DataCartridges({ resources, activeSkill, onSelectSkill }) {
  const skillNames = Object.keys(resources || {});
  const [selectedSkill, setSelectedSkill] = useState(activeSkill || skillNames[0] || '');
  const [activeTab, setActiveTab] = useState('videos');

  React.useEffect(() => {
    if (activeSkill && skillNames.includes(activeSkill)) setSelectedSkill(activeSkill);
  }, [activeSkill]);

  if (skillNames.length === 0) return null;

  const cur = resources[selectedSkill] || { videos: [], books: [], courses: [] };

  const tabs = [
    { key: 'videos', label: 'Videos', icon: Video, count: cur.videos?.length || 0 },
    { key: 'books', label: 'Books', icon: Book, count: cur.books?.length || 0 },
    { key: 'courses', label: 'Courses', icon: GraduationCap, count: cur.courses?.length || 0 },
  ];

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800/60">
        <div className="space-y-1">
          <h3 className="font-orbitron font-bold text-lg text-[#f0f9ff] flex items-center gap-2.5">
            <BookOpen className="w-4 h-4 text-cyan-400" />
            Learning Blueprints
          </h3>
          <p className="text-xs font-mono text-slate-600">
            Curated resources for your skill gaps — videos, books &amp; courses
          </p>
        </div>
        <span className="self-start sm:self-auto text-xs font-mono px-3 py-1.5 rounded-xl bg-slate-900/60 border border-slate-800 text-emerald-400">
          Verified External Links
        </span>
      </div>

      {/* Skill selector */}
      <div className="flex gap-2 overflow-x-auto pb-1">
        {skillNames.map((sk) => {
          const isActive = sk === selectedSkill;
          return (
            <button
              key={sk}
              onClick={() => setSelectedSkill(sk)}
              className={`flex-shrink-0 px-4 py-2 rounded-xl text-xs font-mono whitespace-nowrap transition-all duration-200 border ${
                isActive
                  ? 'bg-cyan-500/12 border-cyan-500/40 text-cyan-300 font-semibold shadow-[0_0_12px_rgba(6,182,212,0.12)]'
                  : 'bg-slate-900/50 border-slate-800 text-slate-500 hover:border-slate-700 hover:text-slate-300'
              }`}
            >
              {sk}
            </button>
          );
        })}
      </div>

      {/* Main card */}
      <div className="glass-panel rounded-2xl p-5 sm:p-7">
        {/* Sub-tabs */}
        <div className="flex items-center justify-between border-b border-slate-800/60 pb-4 mb-6">
          <div className="flex items-center gap-1 p-1 bg-slate-900/60 rounded-xl border border-slate-800/60">
            {tabs.map((t) => {
              const Icon = t.icon;
              const isActive = activeTab === t.key;
              return (
                <button
                  key={t.key}
                  onClick={() => setActiveTab(t.key)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono transition-all ${
                    isActive
                      ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 font-semibold'
                      : 'text-slate-500 hover:text-slate-300'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  {t.label} <span className="text-[9px] opacity-60">({t.count})</span>
                </button>
              );
            })}
          </div>
          <span className="hidden md:block font-mono text-xs text-slate-600">
            Skill: <span className="text-cyan-500">{selectedSkill}</span>
          </span>
        </div>

        {/* Videos */}
        {activeTab === 'videos' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {cur.videos?.map((vid, idx) => (
              <a
                key={idx}
                href={vid.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex flex-col justify-between rounded-xl bg-slate-900/60 border border-slate-800/60 hover:border-cyan-500/30 p-4 transition-all duration-300 relative overflow-hidden hover:shadow-[0_0_20px_rgba(6,182,212,0.08)]"
              >
                {vid.start_here && (
                  <div className="absolute top-2 right-2 z-10 flex items-center gap-1 px-2 py-0.5 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 text-[#030712] font-orbitron font-black text-[8px] tracking-widest">
                    <Sparkles className="w-2.5 h-2.5" />
                    START HERE
                  </div>
                )}

                <div>
                  {/* Thumbnail */}
                  <div className="w-full h-32 rounded-lg overflow-hidden bg-slate-800 mb-3 relative">
                    <img
                      src={vid.thumbnail}
                      alt={vid.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      onError={(e) => { e.target.style.display = 'none'; }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 via-transparent to-transparent" />
                    <div className="absolute bottom-2 left-2 px-1.5 py-0.5 rounded bg-black/60 text-[9px] font-mono text-cyan-400">
                      {vid.duration || 'Video'}
                    </div>
                  </div>

                  <h5 className="font-orbitron font-bold text-xs text-[#f0f9ff] group-hover:text-cyan-300 transition-colors line-clamp-2 mb-1 leading-snug">
                    {vid.title}
                  </h5>
                  <p className="font-mono text-[10px] text-slate-600 mb-3">{vid.channel}</p>
                </div>

                <div className="pt-2 border-t border-slate-800/40 flex items-center justify-between text-[10px] font-mono">
                  <span className={`px-2 py-0.5 rounded-md border ${vid.cost === 'Free' || !vid.cost ? 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' : 'text-amber-400 bg-amber-500/10 border-amber-500/20'}`}>
                    {vid.cost || 'Free'}
                  </span>
                  <span className="flex items-center gap-1 text-cyan-400 group-hover:translate-x-0.5 transition-transform">
                    Watch <ExternalLink className="w-3 h-3" />
                  </span>
                </div>
              </a>
            ))}
            {(!cur.videos || cur.videos.length === 0) && (
              <div className="col-span-full py-8 text-center text-sm font-mono text-slate-600">No videos available for this skill.</div>
            )}
          </div>
        )}

        {/* Books */}
        {activeTab === 'books' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {cur.books?.map((bk, idx) => (
              <a
                key={idx}
                href={bk.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex gap-4 rounded-xl bg-slate-900/60 border border-slate-800/60 hover:border-cyan-500/30 p-4 transition-all duration-300"
              >
                <div className="w-20 h-28 rounded-lg overflow-hidden bg-slate-800 flex-shrink-0 border border-slate-700/40">
                  <img
                    src={bk.cover}
                    alt={bk.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    onError={(e) => { e.target.style.display = 'none'; }}
                  />
                </div>

                <div className="flex-1 flex flex-col justify-between min-w-0">
                  <div>
                    <h5 className="font-orbitron font-bold text-sm text-[#f0f9ff] group-hover:text-cyan-300 transition-colors line-clamp-2 mb-1 leading-snug">
                      {bk.title}
                    </h5>
                    <p className="font-mono text-[10px] text-slate-600">by {bk.author}</p>
                  </div>

                  <div className="pt-2 flex items-center justify-between text-[10px] font-mono">
                    <span className="text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-md">
                      {bk.cost || 'Paid'}
                    </span>
                    <span className="flex items-center gap-1 text-cyan-400 group-hover:translate-x-0.5 transition-transform">
                      View Book <ExternalLink className="w-3 h-3" />
                    </span>
                  </div>
                </div>
              </a>
            ))}
            {(!cur.books || cur.books.length === 0) && (
              <div className="col-span-full py-8 text-center text-sm font-mono text-slate-600">No books available for this skill.</div>
            )}
          </div>
        )}

        {/* Courses */}
        {activeTab === 'courses' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {cur.courses?.map((crs, idx) => (
              <a
                key={idx}
                href={crs.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex flex-col justify-between rounded-xl bg-slate-900/60 border border-slate-800/60 hover:border-cyan-500/30 p-4 transition-all duration-300"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[10px] font-mono text-cyan-400 bg-cyan-500/10 border border-cyan-500/20 px-2 py-0.5 rounded-md">
                      {crs.provider}
                    </span>
                    <span className="text-[10px] font-mono text-emerald-400">
                      {crs.cost || 'Free Audit'}
                    </span>
                  </div>

                  <h5 className="font-orbitron font-bold text-sm text-[#f0f9ff] group-hover:text-cyan-300 transition-colors mb-2 leading-snug">
                    {crs.title}
                  </h5>

                  <p className="font-mono text-[10px] text-slate-600">Level: {crs.level || 'Beginner to Intermediate'}</p>
                </div>

                <div className="pt-3 mt-3 border-t border-slate-800/40 flex items-center justify-between text-[10px] font-mono">
                  <span className="text-slate-600">Official Syllabus</span>
                  <span className="flex items-center gap-1 text-cyan-400 group-hover:translate-x-0.5 transition-transform">
                    Enroll <ExternalLink className="w-3 h-3" />
                  </span>
                </div>
              </a>
            ))}
            {(!cur.courses || cur.courses.length === 0) && (
              <div className="col-span-full py-8 text-center text-sm font-mono text-slate-600">No courses available for this skill.</div>
            )}
          </div>
        )}
      </div>

    </div>
  );
}
