import React, { useState, useEffect, useRef, } from 'react';
import { parseFASTA, ParsedFastaResult } from './components/fastaParser';
import StatCard from './utils/StatCard';
import { Dna, Activity } from 'lucide-react';
import { detectMutations } from './utils/mutationDetector';
// Component ထဲမှာ သုံးပုံ

declare const $3Dmol: any;

export default function App() {
  // Navigation & Theme States
  const [isDarkMode, setIsDarkMode] = useState<boolean>(true);
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(true);
  const [activeView, setActiveView] = useState<'alignment' | '3d' | 'jobs'>('alignment');
  // Parsed Data များကို သိမ်းဆည်းရန် State
  const [parsedData, setParsedData] = useState<ParsedFastaResult | null>(null);
  // Input States
  const sampleFasta = `>sp|P0A6Y8|DNAK_ECOLI Chaperone protein DnaK\nATGGCAGCAAAAGACGTAAAATTCGGTAACGACGCTCGTGACAAAATG\nTCGCGTCACGGTGTATTCGTACTTGATGTTCAGCAAGCTTGCCG`;
  const [sequenceInput, setSequenceInput] = useState<string>(sampleFasta);
  const [eValue, setEValue] = useState<string>('0.001');
  const [gapPenalty, setGapPenalty] = useState<number>(11);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // 3D Visualizer States & Controls
  const [displayMode, setDisplayMode] = useState<'cartoon' | 'sphere' | 'stick' | 'surface'>('cartoon');
  const [colorScheme, setColorScheme] = useState<'spectrum' | 'chain' | 'secondary' | 'residue'>('spectrum');
  const [isSpinning, setIsSpinning] = useState<boolean>(false);
  const [activePdb, setActivePdb] = useState<string>('1KZN');

  const viewerRef = useRef<HTMLDivElement>(null);
  const molViewerInstance = useRef<any>(null);

  // Sample Alignment Sequence Data
  const refSequence = ['A', 'T', 'G', 'C', 'G', 'T', 'A', 'C', 'T', 'G', 'A', 'C', 'C', 'G', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A'];
  // Line 33 ကို ဒီလို ပြောင်းပေးပါ:
  const [querySequence, setQuerySequence] = useState<string[]>([
    'A', 'T', 'G', 'C', 'G', 'A', 'A', 'C', 'T', 'G', 'A', 'C', 'C', 'G', 'T', 'A', 'G', 'C'
  ]);

  // Dynamic Theme Helpers
  const cardBg = isDarkMode ? 'bg-[#111827] border-slate-800' : 'bg-white border-slate-200 shadow-sm';
  const innerBg = isDarkMode ? 'bg-[#0B0F17] border-slate-800' : 'bg-slate-50 border-slate-200';
  const textPrimary = isDarkMode ? 'text-slate-100' : 'text-slate-900';
  const textMuted = isDarkMode ? 'text-slate-400' : 'text-slate-500';
  const borderTheme = isDarkMode ? 'border-slate-800' : 'border-slate-200';

  // Load 3Dmol Engine Script
  useEffect(() => {
    if (!window.hasOwnProperty('$3Dmol')) {
      const script = document.createElement('script');
      script.src = 'https://3Dmol.org/build/3Dmol-min.js';
      script.async = true;
      script.onload = () => {
        if (activeView === '3d') init3DViewer();
      };
      document.head.appendChild(script);
    }
  }, []);
  const handleExecute = () => {
    setIsLoading(true);

    // 1. FASTA Text ကို Parse လုပ်သည်
    const result = parseFASTA(sequenceInput);

    if (!result.isValid) {
      alert(result.errorMessage);
      setIsLoading(false);
      return;
    }

    setParsedData(result);
    setQuerySequence(result.sequence.split(''));

    // ==========================================
    // 2. ဤနေရာတွင် Mutation Detector ကို ထည့်သွင်းပါ
    // ==========================================
    const mutations = detectMutations(refSequence.join(''), result.sequence);
    console.log("Detected Mutations:", mutations);
    // (နောက်ပိုင်းတွင် ဤ mutations များကို State ထဲ သိမ်းပြီး Card ပေါ် ပြသပါမည်)

    setTimeout(() => {
      setIsLoading(false);
      setActiveView('alignment');
    }, 300);
  };
  // Re-render 3D view when tab, display mode, color, theme or PDB structure changes
  useEffect(() => {
    if (activeView === '3d') {
      const timer = setTimeout(() => {
        init3DViewer();
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [activeView, displayMode, colorScheme, activePdb, isDarkMode]);

  // Apply Styles and Color Schemes
  const applyStyles = (viewer: any) => {
    if (!viewer) return;
    viewer.setStyle({}, {}); // Clear existing style

    let colorObj: any = {};
    if (colorScheme === 'spectrum') colorObj = { color: 'spectrum' };
    else if (colorScheme === 'chain') colorObj = { colorscheme: 'chain' };
    else if (colorScheme === 'secondary') colorObj = { colorscheme: 'ssPyMOL' };
    else if (colorScheme === 'residue') colorObj = { colorscheme: 'amino' };

    if (displayMode === 'cartoon') viewer.setStyle({}, { cartoon: colorObj });
    else if (displayMode === 'sphere') viewer.setStyle({}, { sphere: colorObj });
    else if (displayMode === 'stick') viewer.setStyle({}, { stick: colorObj });
    else if (displayMode === 'surface') {
      viewer.setStyle({}, { cartoon: colorObj });
      viewer.addSurface($3Dmol.SurfaceType.VDW, { opacity: 0.65, color: 'spectrum' });
    }

    viewer.render();
  };

  const init3DViewer = () => {
    if (viewerRef.current && typeof $3Dmol !== 'undefined') {
      viewerRef.current.innerHTML = '';
      const config = { backgroundColor: isDarkMode ? '#090D16' : '#FFFFFF' };
      const viewer = $3Dmol.createViewer(viewerRef.current, config);
      molViewerInstance.current = viewer;

      $3Dmol.download(`pdb:${activePdb}`, viewer, {}, () => {
        applyStyles(viewer);
        viewer.zoomTo();
        viewer.render();
      });
    }
  };

  // 3D Interactive Control Actions
  const handleZoomIn = () => {
    if (molViewerInstance.current) molViewerInstance.current.zoom(1.2, 200);
  };

  const handleZoomOut = () => {
    if (molViewerInstance.current) molViewerInstance.current.zoom(0.8, 200);
  };

  const handleResetView = () => {
    if (molViewerInstance.current) {
      molViewerInstance.current.zoomTo();
      molViewerInstance.current.render();
    }
  };

  const toggleSpin = () => {
    if (molViewerInstance.current) {
      molViewerInstance.current.spin(!isSpinning);
      setIsSpinning(!isSpinning);
    }
  };

  const handleScreenshot = () => {
    if (molViewerInstance.current) {
      const imgData = molViewerInstance.current.png();
      const link = document.createElement('a');
      link.href = imgData;
      link.download = `${activePdb}_structure.png`;
      link.click();
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



  // Color Mapping for Bases
  const getBaseBadge = (base: string) => {
    switch (base) {
      case 'A': return 'bg-rose-500/20 text-rose-500 border-rose-500/40';
      case 'T': return 'bg-emerald-500/20 text-emerald-600 border-emerald-500/40';
      case 'C': return 'bg-sky-500/20 text-sky-600 border-sky-500/40';
      case 'G': return 'bg-amber-500/20 text-amber-600 border-amber-500/40';
      default: return isDarkMode ? 'bg-slate-700 text-slate-300' : 'bg-slate-200 text-slate-700';
    }
  };

  return (
    <div className={`min-h-screen font-sans transition-colors duration-200 ${isDarkMode ? 'dark bg-[#0B0F17] text-slate-100' : 'bg-slate-100 text-slate-900'}`}>

      {/* HEADER */}
      <header className={`h-16 px-6 border-b flex items-center justify-between sticky top-0 z-50 backdrop-blur-md transition-colors duration-200 ${isDarkMode ? 'bg-[#111827]/80 border-slate-800' : 'bg-white/80 border-slate-200'}`}>
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className={`p-2 rounded-lg border transition-all cursor-pointer ${isDarkMode ? 'bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700' : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border-slate-300'}`}
          >
            ☰
          </button>
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/30">
              GX
            </div>
            <div>
              <h1 className="text-sm font-bold tracking-wide">Genome-X Suite</h1>
              <p className={`text-[11px] font-mono ${textMuted}`}>Session: EColi_DnaK_Variant_01</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className={`p-2 rounded-lg border transition-all cursor-pointer text-xs font-semibold ${isDarkMode ? 'border-slate-700 bg-slate-800 hover:bg-slate-700 text-amber-400' : 'border-slate-300 bg-slate-100 hover:bg-slate-200 text-indigo-600'}`}
          >
            {isDarkMode ? '☀️ Light' : '🌙 Dark'}
          </button>
        </div>
      </header>

      {/* MAIN CONTAINER */}
      <div className="flex h-[calc(100vh-64px)] overflow-hidden">

        {/* SIDEBAR */}
        <aside className={`border-r transition-all duration-300 flex flex-col overflow-y-auto ${isDarkMode ? 'border-slate-800 bg-[#111827]' : 'border-slate-200 bg-white'} ${sidebarOpen ? 'w-[320px] p-5' : 'w-0 p-0 overflow-hidden pointer-events-none'}`}>
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className={`text-xs font-bold uppercase tracking-wider ${textMuted}`}>Control Panel</h2>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-500 border border-blue-500/30">v1.2</span>
            </div>

            {/* FASTA Input Box */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className={`text-xs font-bold ${textPrimary}`}>Sequence Input (FASTA)</label>
                <button
                  onClick={handleLoadSample}
                  className="text-[11px] font-bold text-blue-500 bg-blue-500/10 hover:bg-blue-500/20 px-2.5 py-1 rounded-md transition-all border border-blue-500/30 cursor-pointer"
                >
                  Try Sample FASTA
                </button>
              </div>

              <textarea
                value={sequenceInput}
                onChange={(e) => setSequenceInput(e.target.value)}
                placeholder="Paste FASTA sequence here..."
                rows={5}
                className={`w-full p-3 text-xs font-mono rounded-xl border transition-colors resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/50 ${isDarkMode ? 'border-slate-700 bg-[#0B0F17] text-slate-200' : 'border-slate-300 bg-slate-50 text-slate-800'}`}
              />

              <div className="flex gap-2">
                <button onClick={handlePaste} className={`flex-1 py-1.5 text-xs font-semibold rounded-lg border transition-all cursor-pointer ${isDarkMode ? 'bg-slate-800 hover:bg-slate-700 border-slate-700 text-slate-200' : 'bg-slate-100 hover:bg-slate-200 border-slate-300 text-slate-700'}`}>Paste</button>
                <button onClick={handleClear} className="py-1.5 px-3 bg-rose-500/10 hover:bg-rose-500/20 text-rose-500 text-xs font-semibold rounded-lg border border-rose-500/30 transition-all cursor-pointer">Clear</button>
              </div>
            </div>

            {/* Parameters */}
            <div className={`space-y-4 pt-4 border-t ${borderTheme}`}>
              <h3 className={`text-xs font-bold ${textPrimary}`}>Analysis Parameters</h3>
              <div>
                <label className={`text-[11px] ${textMuted}`}>E-Value Threshold</label>
                <input type="text" value={eValue} onChange={(e) => setEValue(e.target.value)} className={`w-full px-3 py-1.5 text-xs font-mono rounded-lg border mt-1 ${isDarkMode ? 'border-slate-700 bg-[#0B0F17] text-slate-200' : 'border-slate-300 bg-slate-50 text-slate-800'}`} />
              </div>
              <div>
                <div className={`flex justify-between text-[11px] ${textMuted}`}>
                  <span>Gap Penalty</span>
                  <span className="font-mono text-blue-500">{gapPenalty}</span>
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
        <main className={`flex-1 flex flex-col overflow-hidden p-6 space-y-6 overflow-y-auto ${isDarkMode ? 'bg-[#0B0F17]' : 'bg-slate-100'}`}>

          {/* SUMMARY CARDS */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">

            {/* 1. Sequence Length (Dynamic) */}
            {/* 1. Sequence Length StatCard */}
            <StatCard
              title="Sequence Length"
              value={parsedData ? `${parsedData.length} bp` : "0 bp"}
              icon={<Dna className="w-5 h-5 text-indigo-400" />}
            />
            {/* 2. GC Content (Dynamic) */}
            <StatCard
              title="GC Content"
              value={parsedData ? `${parsedData.gcContent}%` : "0%"}
              icon={<Activity className="w-5 h-5 text-emerald-400" />}
            />

            {/* 3. Target Gene (Dynamic) */}
            <div className={`p-4 rounded-xl border ${cardBg} space-y-1`}>
              <span className={`text-[11px] font-semibold uppercase ${textMuted}`}>Target Gene</span>
              <p className="text-xl font-bold text-blue-500 font-mono truncate">
                {parsedData?.header ? parsedData.header.split(' ')[0] : "DnaK / GyrA"}
              </p>
            </div>

            {/* 4. AMR Risk Score (Grid ထဲမှာပဲ ရှိရပါမည်) */}
            <div className={`p-4 rounded-xl border ${cardBg} space-y-1`}>
              <span className={`text-[11px] font-semibold uppercase ${textMuted}`}>AMR Risk Score</span>
              <div className="flex items-center justify-between">
                <span className="text-xl font-bold text-rose-500">HIGH (88.4%)</span>
                <span className="w-3 h-3 rounded-full bg-rose-500 animate-pulse"></span>
              </div>
            </div>

          </div> {/* Grid Container ပိတ်သည့် div */}

          {/* TABS NAVIGATION */}

          {/* TABS NAVIGATION */}
          <div className={`flex border-b gap-4 ${borderTheme}`}>
            <button
              onClick={() => setActiveView('alignment')}
              className={`pb-3 text-xs font-bold transition-all border-b-2 cursor-pointer ${activeView === 'alignment' ? 'border-blue-500 text-blue-500' : `border-transparent ${textMuted} hover:text-blue-400`}`}
            >
              Sequence Alignment Viewer
            </button>
            <button
              onClick={() => setActiveView('3d')}
              className={`pb-3 text-xs font-bold transition-all border-b-2 cursor-pointer ${activeView === '3d' ? 'border-blue-500 text-blue-500' : `border-transparent ${textMuted} hover:text-blue-400`}`}
            >
              3D Structural Canvas
            </button>
            <button
              onClick={() => setActiveView('jobs')}
              className={`pb-3 text-xs font-bold transition-all border-b-2 cursor-pointer ${activeView === 'jobs' ? 'border-blue-500 text-blue-500' : `border-transparent ${textMuted} hover:text-blue-400`}`}
            >
              Job Logs
            </button>
          </div>

          {/* TAB 1: SEQUENCE ALIGNMENT VIEWER */}
          {
            activeView === 'alignment' && (
              <div className={`p-6 rounded-2xl border ${cardBg} space-y-6`}>
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className={`text-sm font-bold ${textPrimary}`}>Nucleotide Sequence Alignment Visualizer</h3>
                    <p className={`text-xs ${textMuted}`}>WT Reference vs Query Strain Variant</p>
                  </div>
                  <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">Alignment Done</span>
                </div>

                <div className={`border rounded-xl overflow-x-auto p-4 space-y-3 font-mono ${innerBg}`}>
                  {/* Reference Sequence */}
                  <div className="flex items-center gap-2">
                    <span className={`w-20 text-xs font-bold shrink-0 ${textMuted}`}>Ref (WT)</span>
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
                    <span className={`w-20 text-xs font-bold shrink-0 ${textMuted}`}>Query</span>
                    <div className="flex gap-1">
                      {querySequence.map((base, i) => {
                        const isMutated = base !== refSequence[i];
                        return (
                          <span key={i} className={`w-7 h-8 flex items-center justify-center rounded font-bold border text-xs ${isMutated ? 'bg-red-600 text-white border-red-500 ring-2 ring-red-400/50' : getBaseBadge(base)}`}>
                            {base}
                          </span>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>
            )
          }

          {/* TAB 2: INTERACTIVE 3D PROTEIN CANVAS WITH ADVANCED CONTROLS */}
          {
            activeView === '3d' && (
              <div className="flex-1 flex flex-col space-y-4">

                {/* TOP TOOLBAR CONTROLS */}
                <div className={`flex flex-wrap items-center justify-between gap-3 p-3 rounded-xl border ${cardBg}`}>
                  <div className="flex items-center space-x-2 flex-wrap gap-2">

                    {/* Structure Model Selector */}
                    <select
                      value={activePdb}
                      onChange={(e) => setActivePdb(e.target.value)}
                      className={`text-xs font-semibold border rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 ${isDarkMode ? 'bg-slate-800 text-slate-200 border-slate-700' : 'bg-slate-100 text-slate-800 border-slate-300'}`}
                    >
                      <option value="1KZN">1KZN (GyrA Complex)</option>
                      <option value="1TSR">1TSR (DnaK Protein)</option>
                      <option value="4HHB">4HHB (Hemoglobin)</option>
                    </select>

                    {/* Representation Modes */}
                    <div className={`flex p-1 rounded-lg border ${isDarkMode ? 'bg-slate-900 border-slate-800' : 'bg-slate-100 border-slate-200'}`}>
                      {(['cartoon', 'sphere', 'stick', 'surface'] as const).map((mode) => (
                        <button
                          key={mode}
                          onClick={() => setDisplayMode(mode)}
                          className={`px-3 py-1 text-xs font-bold rounded-md capitalize transition-all cursor-pointer ${displayMode === mode ? 'bg-blue-600 text-white shadow' : `${textMuted} hover:text-blue-500`}`}
                        >
                          {mode}
                        </button>
                      ))}
                    </div>

                    {/* Color Scheme Dropdown */}
                    <select
                      value={colorScheme}
                      onChange={(e: any) => setColorScheme(e.target.value)}
                      className={`text-xs font-semibold border rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500 ${isDarkMode ? 'bg-slate-800 text-slate-200 border-slate-700' : 'bg-slate-100 text-slate-800 border-slate-300'}`}
                    >
                      <option value="spectrum">Spectrum Color</option>
                      <option value="chain">Chain Color</option>
                      <option value="secondary">Secondary Structure</option>
                      <option value="residue">Amino Acid Type</option>
                    </select>
                  </div>

                  <span className="text-xs font-bold px-2.5 py-1 bg-blue-500/10 text-blue-500 rounded-full border border-blue-500/30">
                    PDB: {activePdb}
                  </span>
                </div>

                {/* 3Dmol CANVAS CONTAINER */}
                <div className={`relative flex-1 min-h-[480px] rounded-2xl border overflow-hidden shadow-2xl ${isDarkMode ? 'bg-[#090D16] border-slate-800' : 'bg-white border-slate-200'}`}>

                  {/* FLOATING ACTION CONTROL BUTTONS */}
                  <div className={`absolute top-4 right-4 z-20 flex flex-col border rounded-xl p-1.5 space-y-1 shadow-2xl backdrop-blur ${isDarkMode ? 'bg-slate-900/90 border-slate-800' : 'bg-white/90 border-slate-200'}`}>
                    <button onClick={handleZoomIn} title="Zoom In (+)" className={`w-8 h-8 flex items-center justify-center font-bold rounded-lg transition-all cursor-pointer text-base ${isDarkMode ? 'text-slate-300 hover:text-white hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-100'}`}>+</button>
                    <button onClick={handleZoomOut} title="Zoom Out (-)" className={`w-8 h-8 flex items-center justify-center font-bold rounded-lg transition-all cursor-pointer text-base ${isDarkMode ? 'text-slate-300 hover:text-white hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-100'}`}>-</button>
                    <button onClick={handleResetView} title="Reset View" className={`w-8 h-8 flex items-center justify-center font-bold rounded-lg transition-all cursor-pointer text-xs ${isDarkMode ? 'text-slate-300 hover:text-white hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-100'}`}>↺</button>
                    <button onClick={toggleSpin} title={isSpinning ? "Stop Rotation" : "Auto Rotate"} className={`w-8 h-8 flex items-center justify-center font-bold rounded-lg transition-all cursor-pointer text-xs ${isSpinning ? 'bg-blue-600 text-white animate-spin' : isDarkMode ? 'text-slate-300 hover:text-white hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-100'}`}>⚙</button>
                    <hr className={borderTheme} />
                    <button onClick={handleScreenshot} title="Download Screenshot" className={`w-8 h-8 flex items-center justify-center font-bold text-emerald-500 hover:bg-emerald-500/10 rounded-lg transition-all cursor-pointer text-xs`}>📷</button>
                  </div>

                  {/* Actual 3D Container Node */}
                  <div ref={viewerRef} className="w-full h-full min-h-[480px] relative"></div>

                  {/* Footer Controls Overlay Guide */}
                  <div className={`absolute bottom-4 left-4 backdrop-blur px-3.5 py-2 rounded-xl border text-[11px] shadow-lg flex items-center space-x-3 ${isDarkMode ? 'bg-slate-900/90 border-slate-800 text-slate-300' : 'bg-white/90 border-slate-200 text-slate-700'}`}>
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span><strong>Mouse Controls:</strong> Left-Click: Rotate | Right-Click: Pan | Scroll: Zoom</span>
                  </div>
                </div>

              </div>
            )
          }

          {/* TAB 3: JOB LOGS */}
          {
            activeView === 'jobs' && (
              <div className={`p-6 rounded-2xl border ${cardBg} space-y-4`}>
                <h3 className={`text-sm font-bold ${textPrimary}`}>Job Execution History</h3>
                <div className={`p-4 rounded-xl border flex justify-between items-center ${innerBg}`}>
                  <div>
                    <p className={`text-xs font-bold font-mono ${textPrimary}`}>JOB-8821: EColi_DnaK_Variant_01</p>
                    <p className={`text-[11px] mt-0.5 ${textMuted}`}>Execution Time: 1.2s | E-Value: 0.001</p>
                  </div>
                  <span className="text-xs font-bold text-emerald-500 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">SUCCESS</span>
                </div>
              </div>
            )
          }

        </main >

      </div>
    </div>
  );
}