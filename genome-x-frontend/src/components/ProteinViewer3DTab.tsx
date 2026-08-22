import React, { useEffect, useRef, useState } from 'react';
import {
    ZoomIn, ZoomOut, RefreshCw, RotateCw, Camera,
    Activity
} from 'lucide-react';

declare global {
    interface Window {
        $3Dmol: any;
    }
}

interface ProteinViewer3DTabProps {
    pdbId?: string;
    mutationResidue?: string;
}

export const ProteinViewer3DTab: React.FC<ProteinViewer3DTabProps> = ({
    pdbId = '1TSR',
    mutationResidue = 'T6A'
}) => {
    const viewerRef = useRef<HTMLDivElement>(null);
    const viewerInstance = useRef<any>(null);

    const [loading, setLoading] = useState<boolean>(true);
    const [style, setStyle] = useState<'cartoon' | 'stick' | 'sphere' | 'surface'>('cartoon');
    const [colorScheme, setColorScheme] = useState<'spectrum' | 'chain' | 'secondary' | 'residue'>('spectrum');
    const [isSpinning, setIsSpinning] = useState<boolean>(false);
    const [activePdb, setActivePdb] = useState<string>(pdbId);

    useEffect(() => {
        if (!window.$3Dmol) {
            const script = document.createElement('script');
            script.src = 'https://3Dmol.org/build/3Dmol-min.js';
            script.async = true;
            script.onload = () => initViewer();
            document.head.appendChild(script);
        } else {
            initViewer();
        }
    }, [activePdb]);

    const initViewer = () => {
        if (!viewerRef.current || !window.$3Dmol) return;

        setLoading(true);
        viewerRef.current.innerHTML = '';

        const element = viewerRef.current;
        const config = { backgroundColor: 'rgb(15, 23, 42)' };
        const viewer = window.$3Dmol.createViewer(element, config);
        viewerInstance.current = viewer;

        window.$3Dmol.download(`pdb:${activePdb}`, viewer, {}, () => {
            applyStyles(viewer, style, colorScheme);
            viewer.zoomTo();
            viewer.render();
            setLoading(false);
        });
    };

    const applyStyles = (v: any, currentStyle: string, currentScheme: string) => {
        if (!v) return;

        v.setStyle({}, {});

        let colorObj = {};
        if (currentScheme === 'spectrum') colorObj = { color: 'spectrum' };
        else if (currentScheme === 'chain') colorObj = { colorscheme: 'chain' };
        else if (currentScheme === 'secondary') colorObj = { colorscheme: 'ssPyMOL' };
        else if (currentScheme === 'residue') colorObj = { colorscheme: 'amino' };

        if (currentStyle === 'cartoon') v.setStyle({}, { cartoon: colorObj });
        else if (currentStyle === 'stick') v.setStyle({}, { stick: colorObj });
        else if (currentStyle === 'sphere') v.setStyle({}, { sphere: colorObj });
        else if (currentStyle === 'surface') {
            v.setStyle({}, { cartoon: colorObj });
            v.addSurface(window.$3Dmol.SurfaceType.VDW, { opacity: 0.6, color: 'spectrum' });
        }

        v.setStyle({ resn: 'ALA' }, { stick: { color: 'red', radius: 0.4 } });
        v.render();
    };

    useEffect(() => {
        if (viewerInstance.current) {
            applyStyles(viewerInstance.current, style, colorScheme);
        }
    }, [style, colorScheme]);

    const handleZoomIn = () => {
        if (viewerInstance.current) viewerInstance.current.zoom(1.2, 200);
    };

    const handleZoomOut = () => {
        if (viewerInstance.current) viewerInstance.current.zoom(0.8, 200);
    };

    const handleReset = () => {
        if (viewerInstance.current) {
            viewerInstance.current.zoomTo();
            viewerInstance.current.render();
        }
    };

    const toggleSpin = () => {
        if (viewerInstance.current) {
            viewerInstance.current.spin(!isSpinning);
            setIsSpinning(!isSpinning);
        }
    };

    const handleScreenshot = () => {
        if (viewerInstance.current) {
            const imgData = viewerInstance.current.png();
            const link = document.createElement('a');
            link.href = imgData;
            link.download = `${activePdb}_3d_structure.png`;
            link.click();
        }
    };

    return (
        <div className="flex flex-col h-full bg-slate-900 text-slate-100 rounded-xl border border-slate-800 shadow-xl overflow-hidden">
            {/* Control Toolbar */}
            <div className="flex flex-wrap items-center justify-between p-4 bg-slate-800/80 backdrop-blur border-b border-slate-700/60 gap-3">
                <div className="flex items-center space-x-3">
                    <Activity className="w-5 h-5 text-cyan-400" />
                    <h3 className="font-semibold text-lg text-slate-100">3D Protein Structural Canvas</h3>
                    <span className="px-2.5 py-0.5 text-xs font-medium bg-cyan-500/20 text-cyan-300 rounded-full border border-cyan-500/30">
                        PDB: {activePdb}
                    </span>
                </div>

                {/* Action Controls */}
                <div className="flex items-center space-x-2 flex-wrap gap-1">
                    <select
                        value={activePdb}
                        onChange={(e) => setActivePdb(e.target.value)}
                        className="bg-slate-700 text-xs text-slate-200 border border-slate-600 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                    >
                        <option value="1TSR">1TSR (DnaK/GyrA Complex)</option>
                        <option value="1PDB">1PDB (Protein Variant)</option>
                        <option value="4HHB">4HHB (Hemoglobin)</option>
                    </select>

                    <div className="flex bg-slate-900/80 p-1 rounded-lg border border-slate-700/80">
                        {(['cartoon', 'stick', 'sphere', 'surface'] as const).map((mode) => (
                            <button
                                key={mode}
                                onClick={() => setStyle(mode)}
                                className={`px-2.5 py-1 text-xs font-medium rounded-md capitalize transition-all ${style === mode
                                    ? 'bg-cyan-500 text-slate-950 font-semibold shadow'
                                    : 'text-slate-400 hover:text-slate-200'
                                    }`}
                            >
                                {mode}
                            </button>
                        ))}
                    </div>

                    <select
                        value={colorScheme}
                        onChange={(e: any) => setColorScheme(e.target.value)}
                        className="bg-slate-700 text-xs text-slate-200 border border-slate-600 rounded-lg px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-cyan-500"
                    >
                        <option value="spectrum">Spectrum Color</option>
                        <option value="chain">Chain Color</option>
                        <option value="secondary">Secondary Structure</option>
                        <option value="residue">Amino Acid Type</option>
                    </select>
                </div>
            </div>

            {/* Main 3D Canvas */}
            <div className="relative flex-1 min-h-[450px] bg-slate-950">
                {loading && (
                    <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/80 z-20 backdrop-blur-sm">
                        <div className="w-10 h-10 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
                        <p className="mt-3 text-sm text-cyan-400 font-medium">Fetching 3D Structural Data...</p>
                    </div>
                )}

                {/* Floating Controls (Zoom / Rotate / Screenshot) */}
                <div className="absolute top-4 right-4 z-10 flex flex-col bg-slate-800/90 border border-slate-700/80 rounded-xl p-1.5 space-y-1 shadow-2xl backdrop-blur">
                    <button
                        onClick={handleZoomIn}
                        title="Zoom In"
                        className="p-2 text-slate-300 hover:text-cyan-400 hover:bg-slate-700/60 rounded-lg transition"
                    >
                        <ZoomIn className="w-4 h-4" />
                    </button>
                    <button
                        onClick={handleZoomOut}
                        title="Zoom Out"
                        className="p-2 text-slate-300 hover:text-cyan-400 hover:bg-slate-700/60 rounded-lg transition"
                    >
                        <ZoomOut className="w-4 h-4" />
                    </button>
                    <button
                        onClick={handleReset}
                        title="Reset View"
                        className="p-2 text-slate-300 hover:text-cyan-400 hover:bg-slate-700/60 rounded-lg transition"
                    >
                        <RefreshCw className="w-4 h-4" />
                    </button>
                    <button
                        onClick={toggleSpin}
                        title={isSpinning ? "Stop Rotation" : "Auto Rotate"}
                        className={`p-2 rounded-lg transition ${isSpinning ? 'text-cyan-400 bg-cyan-500/20' : 'text-slate-300 hover:text-cyan-400 hover:bg-slate-700/60'
                            }`}
                    >
                        <RotateCw className={`w-4 h-4 ${isSpinning ? 'animate-spin' : ''}`} />
                    </button>
                    <hr className="border-slate-700 my-1" />
                    <button
                        onClick={handleScreenshot}
                        title="Download Screenshot"
                        className="p-2 text-slate-300 hover:text-green-400 hover:bg-slate-700/60 rounded-lg transition"
                    >
                        <Camera className="w-4 h-4" />
                    </button>
                </div>

                <div ref={viewerRef} className="w-full h-full min-h-[450px]" />

                <div className="absolute bottom-4 left-4 z-10 bg-slate-900/90 border border-slate-800 rounded-lg p-3 backdrop-blur shadow-lg flex items-center space-x-3">
                    <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse" />
                    <div>
                        <p className="text-xs font-semibold text-slate-200">Active Mutation Variant</p>
                        <p className="text-xs text-slate-400">Residue: <span className="text-red-400 font-mono font-bold">{mutationResidue}</span> (High Impact)</p>
                    </div>
                </div>
            </div>
        </div>
    );
};
