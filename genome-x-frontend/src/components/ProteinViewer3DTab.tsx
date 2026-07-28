import React, { useEffect, useRef } from 'react';

declare const $3Dmol: any;

export const ProteinViewer3DTab: React.FC = () => {
    const viewerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        // 3Dmol CDN Script ကို Dynamic ရယူခြင်း
        const script = document.createElement('script');
        script.src = 'https://3Dmol.org/build/3Dmol-min.js';
        script.async = true;
        script.onload = () => {
            if (viewerRef.current) {
                viewerRef.current.innerHTML = '';
                const config = { backgroundColor: 'black' };
                const viewer = $3Dmol.createViewer(viewerRef.current, config);

                // PDB: 1KZN (Protein Structure) ကို ရယူပြီး 3D Render လုပ်ခြင်း
                $3Dmol.download('pdb:1KZN', viewer, {}, () => {
                    viewer.setStyle({}, { cartoon: { color: 'spectrum' } });
                    viewer.zoomTo();
                    viewer.render();
                });
            }
        };
        document.head.appendChild(script);
    }, []);

    return (
        <div className="w-full bg-slate-900 p-4 rounded-xl border border-slate-700">
            <div
                ref={viewerRef}
                style={{ width: '100%', height: '500px', position: 'relative' }}
            />
        </div>
    );
};