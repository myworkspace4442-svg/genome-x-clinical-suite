import React from 'react';
import { Download, FileSpreadsheet } from 'lucide-react';

interface AuditLog {
    runId: string;
    timestamp: string;
    pathogen: string;
    antibiotic: string;
    result: 'RESISTANT' | 'SENSITIVE';
    confidence: string;
    keyMutation: string;
}

export const AuditHistoryTab: React.FC = () => {
    const historyLogs: AuditLog[] = [
        { runId: 'RUN-1092', timestamp: '2026-07-27 19:20', pathogen: 'E. coli', antibiotic: 'Ciprofloxacin', result: 'RESISTANT', confidence: '95.4%', keyMutation: 'gyrA_S83L' },
        { runId: 'RUN-1091', timestamp: '2026-07-26 14:12', pathogen: 'S. aureus', antibiotic: 'Rifampicin', result: 'SENSITIVE', confidence: '98.1%', keyMutation: 'Wildtype' },
        { runId: 'RUN-1090', timestamp: '2026-07-25 09:45', pathogen: 'E. coli', antibiotic: 'Ciprofloxacin', result: 'RESISTANT', confidence: '91.2%', keyMutation: 'parC_S80I' },
        { runId: 'RUN-1089', timestamp: '2026-07-24 16:30', pathogen: 'K. pneumoniae', antibiotic: 'Meropenem', result: 'RESISTANT', confidence: '97.8%', keyMutation: 'blaKPC-2' },
    ];

    // CSV Export Functionality
    const exportToCSV = () => {
        const headers = ["Run ID,Timestamp,Pathogen,Antibiotic,Result,Confidence,Key Mutation"];
        const rows = historyLogs.map(log => `${log.runId},${log.timestamp},${log.pathogen},${log.antibiotic},${log.result},${log.confidence},${log.keyMutation}`);
        const csvContent = "data:text/csv;charset=utf-8," + [headers, ...rows].join("\n");
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "genome_x_prediction_history.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm space-y-6">
            {/* Title */}
            <div>
                <h2 className="text-2xl font-bold text-gray-900">Prediction History & Clinical Audit Trail</h2>
                <p className="text-sm text-gray-500">Historical database of analyzed genomic samples</p>
            </div>

            {/* Table */}
            <div className="overflow-x-auto border border-gray-200 rounded-lg">
                <table className="w-full text-left text-sm text-gray-600">
                    <thead className="bg-gray-50 text-xs font-semibold text-gray-500 uppercase tracking-wider border-b">
                        <tr>
                            <th className="py-3 px-4">Run ID</th>
                            <th className="py-3 px-4">Timestamp</th>
                            <th className="py-3 px-4">Pathogen</th>
                            <th className="py-3 px-4">Antibiotic</th>
                            <th className="py-3 px-4">Result</th>
                            <th className="py-3 px-4">Confidence</th>
                            <th className="py-3 px-4">Key Mutation</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {historyLogs.map((log) => (
                            <tr key={log.runId} className="hover:bg-gray-50">
                                <td className="py-3 px-4 font-mono font-medium text-gray-900">{log.runId}</td>
                                <td className="py-3 px-4 text-xs text-gray-500">{log.timestamp}</td>
                                <td className="py-3 px-4 italic">{log.pathogen}</td>
                                <td className="py-3 px-4">{log.antibiotic}</td>
                                <td className="py-3 px-4">
                                    <span className={`px-2.5 py-1 rounded-md text-xs font-bold ${log.result === 'RESISTANT' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                                        }`}>
                                        {log.result}
                                    </span>
                                </td>
                                <td className="py-3 px-4 font-semibold text-gray-800">{log.confidence}</td>
                                <td className="py-3 px-4 font-mono text-xs">{log.keyMutation}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Export Button */}
            <div>
                <button
                    onClick={exportToCSV}
                    className="flex items-center space-x-2 px-4 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-semibold rounded-lg border border-gray-300 transition-all"
                >
                    <Download size={14} />
                    <span>Export History (CSV)</span>
                </button>
            </div>
        </div>
    );
};