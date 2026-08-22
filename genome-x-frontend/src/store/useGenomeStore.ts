import { create } from 'zustand';

export interface AMRData {
  predicted_phenotype: string;
  confidence: number;
  primary_target: string;
  secondary_target: string;
  shap_features: Array<{ gene: string; value: number; impact: string }>;
}

interface GenomeStore {
  amrData: AMRData | null;
  loading: boolean;
  fetchAMRPrediction: (sequence: string) => Promise<void>;
}

export const useGenomeStore = create<GenomeStore>((set) => ({
  amrData: null,
  loading: false,

  fetchAMRPrediction: async (sequence: string) => {
    set({ loading: true });
    try {
      const response = await fetch('http://localhost:8000/api/v1/predict-amr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sequence }),
      });

      if (!response.ok) {
        throw new Error('Backend API မမိပါ။');
      }

      const data = await response.json();
      set({ amrData: data, loading: false });
    } catch (error) {
      console.error('Fetch Error:', error);
      set({ loading: false });
    }
  },
}));