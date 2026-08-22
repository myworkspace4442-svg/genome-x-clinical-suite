// utils/fastaParser.ts

export interface ParsedFastaResult {
    header: string;
    sequence: string;
    length: number;
    gcContent: number;
    baseCounts: {
        A: number;
        T: number;
        C: number;
        G: number;
        Other: number;
    };
    isValid: boolean;
    errorMessage?: string;
}

/**
 * Raw FASTA စာသားကို Parse လုပ်ပေးသည့် Engine Function
 */
export function parseFASTA(fastaText: string): ParsedFastaResult {
    const trimmedText = fastaText.trim();

    // 1. Validate Basic FASTA Format
    if (!trimmedText || !trimmedText.startsWith('>')) {
        return {
            header: '',
            sequence: '',
            length: 0,
            gcContent: 0,
            baseCounts: { A: 0, T: 0, C: 0, G: 0, Other: 0 },
            isValid: false,
            errorMessage: 'Invalid FASTA: Sequence must start with ">"',
        };
    }

    // 2. Separate Header and Sequence Lines
    const lines = trimmedText.split(/\r?\n/);
    const header = lines[0].substring(1).trim(); // '>' ကို ဖယ်ထုတ်သည်

    // Header မဟုတ်သော အောက်လိုင်းများကို ပေါင်းစပ်ပြီး စာလုံးကြီးပြောင်းသည်
    const sequenceLines = lines.slice(1).filter((line) => !line.startsWith('>'));
    const cleanedSequence = sequenceLines.join('').toUpperCase().replace(/[^A-Z-]/g, '');

    if (cleanedSequence.length === 0) {
        return {
            header,
            sequence: '',
            length: 0,
            gcContent: 0,
            baseCounts: { A: 0, T: 0, C: 0, G: 0, Other: 0 },
            isValid: false,
            errorMessage: 'FASTA Header found, but Sequence content is empty.',
        };
    }

    // 3. Base Composition & GC Content Calculation
    let countA = 0, countT = 0, countC = 0, countG = 0, countOther = 0;

    for (let i = 0; i < cleanedSequence.length; i++) {
        const base = cleanedSequence[i];
        switch (base) {
            case 'A': countA++; break;
            case 'T': countT++; break;
            case 'C': countC++; break;
            case 'G': countG++; break;
            default: countOther++; break; // Gaps (-) သို့မဟုတ် တခြား Unknown Bases (N)
        }
    }

    const totalLength = cleanedSequence.length;
    // GC Content တွက်ချက်ခြင်း (%)
    const gcContent = parseFloat((((countG + countC) / totalLength) * 100).toFixed(2));

    return {
        header,
        sequence: cleanedSequence,
        length: totalLength,
        gcContent,
        baseCounts: {
            A: countA,
            T: countT,
            C: countC,
            G: countG,
            Other: countOther,
        },
        isValid: true,
    };
}