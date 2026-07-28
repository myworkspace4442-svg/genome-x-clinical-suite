import React from 'react';
import { ShieldAlert, Activity, Target, Zap } from 'lucide-react';

export const AMRPredictionTab: React.FC = () => {
    // SHAP Feature Attribution Mock Data
    const shapFeatures = [
        { gene: 'gyrA (S83L Mutation)', value: 0.48, impact: 'High Resistance Driver' },
        { gene: 'parC (S80I Mutation)', value: 0.32, impact: 'Secondary Hotspot' },
        { gene: 'qnrS1 (Plasmid Gene)', value: 0.12, impact: 'Moderate Resistance Effect' },
        { gene: 'acrB (Efflux Pump Overexpression)', value: 0.08, impact: 'Minor Contribution' },
    ];

    return (
        <div className="space-y-6">
            {/* 1. Header Section */}
            <div>
                <h2 className="text-2xl font-bold text-gray-900">AMR Phenotype Prediction Summary</h2>
                <p className="text-sm text-gray-500">Clinical-Grade Antimicrobial Resistance Prediction Platform</p>
            </div>

            {/* 2. Top Summary Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Card 1: Phenotype */}
                <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm relative overflow-hidden">
                    <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Predicted Phenotype</span>
                    <div className="text-3xl font-extrabold text-red-600 mt-2">RESISTANT</div>
                    <span className="inline-block mt-3 px-2.5 py-1 bg-red-100 text-red-700 text-xs font-bold rounded-md">
                        High Risk
                    </span>
                </div>

                {/* Card 2: Confidence */}
                <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                    <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Fusion Confidence</span>
                    <div className="text-3xl font-extrabold text-gray-900 mt-2">95.4%</div>
                    <span className="text-xs text-gray-500 mt-2 block">Late Fusion Model</span>
                </div>

                {/* Card 3: Primary Target */}
                <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                    <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Primary Target</span>
                    <div className="text-2xl font-bold text-gray-800 mt-2">gyrA_S83L</div>
                    <span className="text-xs text-gray-500 mt-2 block">QRDR Region</span>
                </div>

                {/* Card 4: Secondary Target */}
                <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                    <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Secondary Target</span>
                    <div className="text-2xl font-bold text-gray-800 mt-2">parC_S80I</div>
                    <span className="text-xs text-gray-500 mt-2 block">Secondary Hotspot</span>
                </div>
            </div>

            {/* 3. SHAP Feature Attribution Section */}
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                <h3 className="text-lg font-bold text-gray-900 mb-1">SHAP Feature Attribution</h3>
                <p className="text-xs text-gray-500 mb-6">Genomic features driving the neural decision towards resistance</p>

                <div className="space-y-4">
                    {shapFeatures.map((item, index) => (
                        <div key={index} className="space-y-1">
                            <div className="flex justify-between text-sm font-medium text-gray-700">
                                <span>{item.gene}</span>
                                <span className="font-mono text-red-600">+{item.value.toFixed(2)} SHAP</span>
                            </div>
                            <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
                                <div
                                    className="bg-red-500 h-full rounded-full transition-all duration-500"
                                    style={{ width: `${item.value * 100}%` }}
                                />
                            </div>
                            <span className="text-xs text-gray-400">{item.impact}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};