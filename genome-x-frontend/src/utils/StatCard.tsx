import React from 'react';

interface StatCardProps {
    title: string;
    value: string | number;
    icon: React.ReactNode;
}

export default function StatCard({ title, value, icon }: StatCardProps) {
    return (
        <div className="p-4 rounded-xl border border-slate-700 bg-slate-900/50 backdrop-blur-md space-y-2 shadow-sm">
            <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                    {title}
                </span>
                <div className="p-2 rounded-lg bg-slate-800/80">
                    {icon}
                </div>
            </div>
            <p className="text-2xl font-bold font-mono text-white">
                {value}
            </p>
        </div>
    );
}