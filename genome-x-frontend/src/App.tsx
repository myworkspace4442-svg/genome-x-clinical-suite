import React, { useState, useEffect, useRef } from 'react';

declare const $3Dmol: any;

export default function App() {
  // Navigation & Theme States
  const [isDarkMode, setIsDarkMode] = useState<boolean>(true);
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(true);
  const [activeView, setActiveView] = useState<'alignment' | '3d' | 'jobs'>('alignment');

  // Input States
  const sampleFasta = `>sp|P0A6Y8|DNAK_ECOLI Chaperone protein DnaK\nATGGCAGCAAAAGACGTAAAATTCGGTAACGACGCTCGTGACAAAATG\nTCGCGTCACGGTGTATTCGTACTTGATGTTCAGCAAGCTTGCCG`;
  const [sequenceInput, setSequenceInput] = useState<string>(sampleFasta);
  const [eValue, setEValue] = useState<string>('0.001');
  const [gapPenalty, setGapPenalty] = useState<number>(11);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // 3D Visualizer State
  const [displayMode, setDisplayMode] = useState<'cartoon' | 'sphere' | 'stick'>('cartoon');
  const viewerRef = useRef<HTMLDivElement>(null);
  const molViewerInstance = useRef<any>(null);

  // Sample Alignment Sequence Data
  const refSequence = ['A', 'T', 'G', 'C', 'G', 'T', 'A', 'C', 'T', 'G', 'A', 'C', 'C', 'G', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A'];
  const querySequence = ['A', 'T', 'G', 'C', 'G', 'A', 'A', 'C', 'T', 'G', 'A', 'C', 'C', 'G', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'T', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A'];

  // 3Dmol Engine Script Loading
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://3Dmol.org/build/3Dmol-min.js';
    script.async = true;
    script.onload = () => {
      init3DViewer();
    };
    document.head.appendChild(script);
  }, []);

  // Re-render 3D view when tab or display mode changes
  useEffect(() => {
    if (activeView === '3d') {
      setTimeout(() => init3DViewer(), 100);
    }
  }, [activeView, displayMode]);

  const init3DViewer = () => {
    if (viewerRef.current && typeof $3Dmol !== 'undefined') {
      viewerRef.current.innerHTML = '';
      const config = { backgroundColor: '#090D16' };
      const viewer = $3Dmol.createViewer(viewerRef.current, config);
      molViewerInstance.current = viewer;

      // Fetch PDB 1KZN Structure
      $3Dmol.download('pdb:1KZN', viewer, {}, () => {
        if (displayMode === 'cartoon') {
          viewer.setStyle({}, { cartoon: { color: 'spectrum' } });
        } else if (displayMode === 'sphere') {
          viewer.setStyle({}, { sphere: { colorscheme: 'amino' } });
        } else {
          viewer.setStyle({}, { stick: { colorscheme: 'default' } });
        }
        viewer.zoomTo();
        viewer.render();
      });
    }
  };

  // Button Action Handlers
  const handleLoadSample = () => setSequenceInput(sampleFasta);
  const handleClear = () => setSequenceInput('');
  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setSequenceInput(text);
    } catch (err) {
      alert('Clipboard empty or permission denied');
    }
  };

  const handleExecute = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      setActiveView('alignment');
    }, 500);
  };

  // Color Mapping for Bases
  const getBaseBadge = (base: string) => {
    switch (base) {
      case 'A': return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      case 'T': return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
      case 'C': return 'bg-sky-500/20 text-sky-300 border-sky-500/40';
      case 'G': return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      default: return 'bg-slate-700 text-slate-300';
    }
  };

  return (
    <div className={`min-h-screen font-sans ${isDarkMode ? 'dark bg-[#0B0F17] text-slate-100' : 'bg-slate-50 text-slate-900'}`}>

      {/* HEADER */}
      <header className="h-16 px-6 border-b flex items-center justify-between sticky top-0 z-50 backdrop-blur-md bg-[#111827]/80 border-slate-800">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-all cursor-pointer"
          >
            ☰
          </button>
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/30">
              GX
            </div>
            <div>
              <h1 className="text-sm font-bold tracking-wide">Genome-X Suite</h1>
              <p className="text-[11px] text-slate-400 font-mono">Session: EColi_DnaK_Variant_01</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="p-2 rounded-lg border border-slate-700 bg-slate-800 hover:bg-slate-700 text-amber-400 transition-all cursor-pointer"
          >
            {isDarkMode ? '☀️ Light' : '🌙 Dark'}
          </button>
        </div>
      </header>

      {/* MAIN CONTAINER */}
      <div className="flex h-[calc(100vh-64px)] overflow-hidden">

        {/* SIDEBAR */}
        <aside className={`border-r border-slate-800 bg-[#111827] transition-all duration-300 flex flex-col overflow-y-auto ${sidebarOpen ? 'w-[320px] p-5' : 'w-0 p-0 overflow-hidden pointer-events-none'
          }`}>
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">Control Panel</h2>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">v1.2</span>
            </div>

            {/* FASTA Input Box */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-slate-300">Sequence Input (FASTA)</label>
                <button
                  onClick={handleLoadSample}
                  className="text-[11px] font-bold text-blue-400 bg-blue-500/10 hover:bg-blue-500/20 px-2.5 py-1 rounded-md transition-all border border-blue-500/30 cursor-pointer"
                >
                  Try Sample FASTA
                </button>
              </div>

              <textarea
                value={sequenceInput}
                onChange={(e) => setSequenceInput(e.target.value)}
                placeholder="Paste FASTA sequence here..."
                rows={5}
                className="w-full p-3 text-xs font-mono rounded-xl border border-slate-700 bg-[#0B0F17] text-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-none"
              />

              <div className="flex gap-2">
                <button onClick={handlePaste} className="flex-1 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg border border-slate-700 transition-all cursor-pointer">Paste</button>
                <button onClick={handleClear} className="py-1.5 px-3 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 text-xs font-semibold rounded-lg border border-rose-500/30 transition-all cursor-pointer">Clear</button>
              </div>
            </div>

            {/* Parameters */}
            <div className="space-y-4 pt-4 border-t border-slate-800">
              <h3 className="text-xs font-bold text-slate-300">Analysis Parameters</h3>
              <div>
                <label className="text-[11px] text-slate-400">E-Value Threshold</label>
                <input type="text" value={eValue} onChange={(e) => setEValue(e.target.value)} className="w-full px-3 py-1.5 text-xs font-mono rounded-lg border border-slate-700 bg-[#0B0F17] mt-1" />
              </div>
              <div>
                <div className="flex justify-between text-[11px] text-slate-400">
                  <span>Gap Penalty</span>
                  <span className="font-mono text-blue-400">{gapPenalty}</span>
                </div>
                <input type="range" min="1" max="25" value={gapPenalty} onChange={(e) => setGapPenalty(Number(e.target.value))} className="w-full accent-blue-500 cursor-pointer mt-1" />
              </div>
            </div>

            {/* Execute Button */}
            <button
              onClick={handleExecute}
              disabled={isLoading}
              className="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
            >
              {isLoading ? 'Running Analysis...' : '⚡ Execute Alignment'}
            </button>
          </div>
        </aside>

        {/* MAIN VIEWPORT */}
        <main className="flex-1 flex flex-col overflow-hidden bg-[#0B0F17] p-6 space-y-6 overflow-y-auto">

          {/* SUMMARY CARDS (AMR Risk Badges & SHAP Cards) */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl border border-slate-800 bg-[#111827] space-y-1">
              <span className="text-[11px] text-slate-400 font-semibold uppercase">AMR Risk Score</span>
              <div className="flex items-center justify-between">
                <span className="text-xl font-bold text-rose-400">HIGH (88.4%)</span>
                <span className="w-3 h-3 rounded-full bg-rose-500 animate-pulse"></span>
              </div>
            </div>

            <div className="p-4 rounded-xl border border-slate-800 bg-[#111827] space-y-1">
              <span className="text-[11px] text-slate-400 font-semibold uppercase">Target Gene</span>
              <p className="text-xl font-bold text-blue-400 font-mono">DnaK / GyrA</p>
            </div>

            <div className="p-4 rounded-xl border border-slate-800 bg-[#111827] space-y-1">
              <span className="text-[11px] text-slate-400 font-semibold uppercase">Mutation Count</span>
              <p className="text-xl font-bold text-amber-400 font-mono">2 Variants Detected</p>
            </div>

            <div className="p-4 rounded-xl border border-slate-800 bg-[#111827] space-y-1">
              <span className="text-[11px] text-slate-400 font-semibold uppercase">SHAP Feature Impact</span>
              <p className="text-xl font-bold text-emerald-400 font-mono">+0.42 (T6A Mutation)</p>
            </div>
          </div>

          {/* TABS NAVIGATION */}
          <div className="flex border-b border-slate-800 gap-4">
            <button
              onClick={() => setActiveView('alignment')}
              className={`pb-3 text-xs font-bold transition-all border-b-2 cursor-pointer ${activeView === 'alignment' ? 'border-blue-500 text-blue-400' : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
            >
              Sequence Alignment Viewer
            </button>
            <button
              onClick={() => setActiveView('3d')}
              className={`pb-3 text-xs font-bold transition-all border-b-2 cursor-pointer ${activeView === '3d' ? 'border-blue-500 text-blue-400' : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
            >
              3D Structural Canvas
            </button>
            <button
              onClick={() => setActiveView('jobs')}
              className={`pb-3 text-xs font-bold transition-all border-b-2 cursor-pointer ${activeView === 'jobs' ? 'border-blue-500 text-blue-400' : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
            >
              Job Logs
            </button>
          </div>

          {/* TAB 1: SEQUENCE ALIGNMENT VIEWER */}
          {activeView === 'alignment' && (
            <div className="p-6 rounded-2xl border border-slate-800 bg-[#111827] space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-sm font-bold text-slate-100">Nucleotide Sequence Alignment Visualizer</h3>
                  <p className="text-xs text-slate-400">WT Reference vs Query Strain Variant</p>
                </div>
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Alignment Done</span>
              </div>

              <div className="border border-slate-800 rounded-xl overflow-x-auto p-4 bg-[#0B0F17] space-y-3 font-mono">
                {/* Reference Sequence */}
                <div className="flex items-center gap-2">
                  <span className="w-20 text-xs font-bold text-slate-400 shrink-0">Ref (WT)</span>
                  <div className="flex gap-1">
                    {refSequence.map((base, i) => (
                      <span key={i} className={`w-7 h-8 flex items-center justify-center rounded font-bold border text-xs ${getBaseBadge(base)}`}>
                        {base}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Query Sequence with Mutation Highlight */}
                <div className="flex items-center gap-2">
                  <span className="w-20 text-xs font-bold text-slate-400 shrink-0">Query</span>
                  <div className="flex gap-1">
                    {querySequence.map((base, i) => {
                      const isMutated = base !== refSequence[i];
                      return (
                        <span key={i} className={`w-7 h-8 flex items-center justify-center rounded font-bold border text-xs ${isMutated ? 'bg-red-600 text-white border-red-500 ring-2 ring-red-400/50' : getBaseBadge(base)
                          }`}>
                          {base}
                        </span>
                      );
                    })}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: INTERACTIVE 3D PROTEIN CANVAS */}
          {activeView === '3d' && (
            <div className="flex-1 flex flex-col space-y-4">
              <div className="flex gap-3">
                <button
                  onClick={() => setDisplayMode('cartoon')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-all cursor-pointer ${displayMode === 'cartoon' ? 'bg-blue-600 text-white border-blue-500' : 'bg-slate-800 text-slate-300 border-slate-700'
                    }`}
                >
                  Ribbon Cartoon
                </button>
                <button
                  onClick={() => setDisplayMode('sphere')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-all cursor-pointer ${displayMode === 'sphere' ? 'bg-blue-600 text-white border-blue-500' : 'bg-slate-800 text-slate-300 border-slate-700'
                    }`}
                >
                  Molecular Surface / Sphere
                </button>
                <button
                  onClick={() => setDisplayMode('stick')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-all cursor-pointer ${displayMode === 'stick' ? 'bg-blue-600 text-white border-blue-500' : 'bg-slate-800 text-slate-300 border-slate-700'
                    }`}
                >
                  Ball & Stick
                </button>
              </div>

              {/* 3Dmol Container */}
              <div className="relative flex-1 min-h-[450px] bg-[#090D16] rounded-2xl border border-slate-800 overflow-hidden">
                <div ref={viewerRef} className="w-full h-full min-h-[450px] relative"></div>
                <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur px-3 py-1.5 rounded-lg border border-slate-700 text-[11px] text-slate-300">
                  💡 Mouse Left-Click: Rotate | Right-Click: Translate | Scroll: Zoom
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: JOB LOGS */}
          {activeView === 'jobs' && (
            <div className="p-6 rounded-2xl border border-slate-800 bg-[#111827] space-y-4">
              <h3 className="text-sm font-bold text-slate-100">Job Execution History</h3>
              <div className="p-4 rounded-xl border border-slate-800 bg-[#0B0F17] flex justify-between items-center">
                <div>
                  <p className="text-xs font-bold text-slate-200 font-mono">JOB-8821: EColi_DnaK_Variant_01</p>
                  <p className="text-[11px] text-slate-400 mt-0.5">Execution Time: 1.2s | E-Value: 0.001</p>
                </div>
                <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">SUCCESS</span>
              </div>
            </div>
          )}

        </main>

      </div>
    </div>
  );
}