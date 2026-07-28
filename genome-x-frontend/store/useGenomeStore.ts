import { create } from 'zustand';

interface GenomeState {
  sequence: string;
  selectedPosition: number | null;
  selectedResidue: string | null;
  amrResult: {
    gene: string;
    resistanceRisk: string;
    probability: number;
    mutation: string;
  } | null;
  isLoading: boolean;
  setSequence: (seq: string) => void;
  setSelectedPosition: (pos: number | null, residue?: string | null) => void;
  setAmrResult: (result: any) => void;
  setIsLoading: (loading: boolean) => void;
}

export const useGenomeStore = create<GenomeState>((set) => ({
  sequence: 'ATGCGTACTGACCGTAGCTAGCTAGCTAGCTAGCTAGCTA',
  selectedPosition: 5,
  selectedResidue: 'T',
  amrResult: {
    gene: 'rpoB_S531L',
    resistanceRisk: 'HIGH RISK',
    probability: 0.94,
    mutation: 'Ser531Leu (Rifampicin Resistance)'
  },
  isLoading: false,
  setSequence: (sequence) => set({ sequence }),
  setSelectedPosition: (position, residue = null) =>
    set({ selectedPosition: position, selectedResidue: residue }),
  setAmrResult: (amrResult) => set({ amrResult }),
  setIsLoading: (isLoading) => set({ setIsLoading: () => set({ isLoading }) }),
}));