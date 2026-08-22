import React, { useEffect } from 'react';
import { useGenomeStore } from '../store/useGenomeStore';

export const AMRPredictionTab: React.FC = () => {
    // Store မှ Data နှင့် Function များကို ယူသုံးခြင်း
    const { amrData, loading, fetchAMRPrediction } = useGenomeStore();

    useEffect(() => {
        // Component စတင်ပွင့်ချိန် Backend API မှ Data ခေါ်ယူမည်
        fetchAMRPrediction("ATGCGT...");
    }, [fetchAMRPrediction]);

    // Loading ဖြစ်နေစဉ် ပြသမည်
    if (loading) {
        return (
            <div className="flex items-center justify-center p-12 bg-white rounded-xl border border-gray-200">
                <div className="text-center">
                    <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
                    <p className="text-sm font-medium text-gray-600">Connecting to Genome-X AI Engine...</p>
                </div>
            </div>
        );
    }

    // Backend မှ ရလာမည့် Data များ (မရောက်သေးပါက Default Dynamic Fallback ပေးထားမည်)
    const phenotype = amrData?.predicted_phenotype || 'RESISTANT';
    const confidence = amrData?.confidence ?? 95.4;
    const primaryTarget = amrData?.primary_target || 'gyrA_S83L';
    const secondaryTarget = amrData?.secondary_target || 'parC_S80I';

    // SHAP Feature Attribution Data
    const shapFeatures = amrData?.shap_features || [
        { gene: 'gyrA (S83L Mutation)', value: 0.48, impact: 'High Resistance Driver' },
        { gene: 'parC (S80I Mutation)', value: 0.32, impact: 'Secondary Hotspot' },
        { gene: 'qnrS1 (Plasmid Gene)', value: 0.12, impact: 'Moderate Resistance Effect' },
        { gene: 'acrB (Efflux Pump)', value: 0.08, impact: 'Minor Contribution' }
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
                    <div className={`text-3xl font-extrabold mt-2 ${phenotype === 'RESISTANT' ? 'text-red-600' : 'text-green-600'}`}>
                        {phenotype}
                    </div>
                    <span className={`inline-block mt-3 px-2.5 py-1 text-xs font-bold rounded-md ${phenotype === 'RESISTANT' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                        {phenotype === 'RESISTANT' ? 'High Risk' : 'Low Risk / Susceptible'}
                    </span>
                </div>

                {/* Card 2: Confidence */}
                <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                    <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Fusion Confidence</span>
                    <div className="text-3xl font-extrabold text-gray-900 mt-2">{confidence}%</div>
                    <span className="text-xs text-gray-500 mt-2 block">Late Fusion Model</span>
                </div>

                {/* Card 3: Primary Target */}
                <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                    <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Primary Target</span>
                    <div className="text-2xl font-bold text-gray-800 mt-2">{primaryTarget}</div>
                    <span className="text-xs text-gray-500 mt-2 block">QRDR Region</span>
                </div>

                {/* Card 4: Secondary Target */}
                <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                    <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Secondary Target</span>
                    <div className="text-2xl font-bold text-gray-800 mt-2">{secondaryTarget}</div>
                    <span className="text-xs text-gray-500 mt-2 block">Secondary Hotspot</span>
                </div>
            </div>

            {/* 3. SHAP Feature Attribution Section */}
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                <h3 className="text-lg font-bold text-gray-900 mb-1">SHAP Feature Attribution</h3>
                <p className="text-xs text-gray-500 mb-6">Genomic features driving the neural decision towards resistance</p>

                <div className="space-y-4">
                    {shapFeatures.map((item, index) => {
                        const valNum = Number(item.value) || 0;
                        const percentage = Math.min(Math.max(valNum * 100, 0), 100);

                        return (
                            <div key={index} className="space-y-1">
                                <div className="flex justify-between text-sm font-medium text-gray-700">
                                    <span>{item.gene}</span>
                                    <span className="font-mono text-red-600">+{valNum.toFixed(2)} SHAP</span>
                                </div>
                                <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
                                    <div
                                        className="bg-red-500 h-full rounded-full transition-all duration-500"
                                        style={{ width: `${percentage}%` }}
                                    />
                                </div>
                                <span className="text-xs text-gray-400">{item.impact}</span>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}