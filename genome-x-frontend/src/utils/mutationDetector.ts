export interface MutationResult {
    position: number;
    refBase: string;
    queryBase: string;
    type: 'substitution' | 'insertion' | 'deletion';
}

/**
 * Reference DNA နှင့် Query DNA ကို နှိုင်းယှဉ်ပြီး Mutation များကို ရှာဖွေပေးခြင်း
 */
export function detectMutations(reference: string, query: string): MutationResult[] {
    const mutations: MutationResult[] = [];
    const minLength = Math.min(reference.length, query.length);

    for (let i = 0; i < minLength; i++) {
        const refBase = reference[i];
        const queryBase = query[i];

        if (refBase !== queryBase) {
            mutations.push({
                position: i + 1, // ၁ စဉ်မှ စရေတွက်ရန်
                refBase,
                queryBase,
                type: 'substitution', // တစ်လုံးတည်း အစားထိုးခံရခြင်း
            });
        }
    }

    return mutations;
}