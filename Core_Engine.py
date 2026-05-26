class GenomeXEngine:
    def __init__(self):
        self.dna = ""
        self.danger_codes = ["GATTACA", "TTAACCGG", "ATATATAT"]

    def load_sequence(self, sequence_string):

        self.dna = sequence_string.upper()

    def is_valid_dna(self):

        for letter in self.dna:
            if letter not in ['A', 'T', 'G', 'C']:
                return False

        return True if len(self.dna) > 0 else False

    def calculate_gc(self):
        """DNA စစ်မှန်ပါက GC Content (%) ကို တွက်ပေးမည်။ မစစ်မှန်ပါက Error ပြန်မည်။"""

        if not self.is_valid_dna():
            return "❌ Invalid DNA Sequence"

        g_count = self.dna.count('G')
        c_count = self.dna.count('C')
        total_len = len(self.dna)

        gc_percentage = (g_count + c_count) / total_len * \
            100 if total_len > 0 else 0
        return gc_percentage

    def calculate_hamming_distance(self, other_sequence):
        """လက်ရှိ DNA နှင့် အပြင်မှ ပေးလိုက်သော DNA နှစ်ခုကြားက Mutation အရေအတွက်ကို တွက်မည်"""
        other_dna = other_sequence.upper()

        # ၁။ Professional Error Handling အပိုင်း (ဒီတစ်ခါတော့ မင်းကိုယ်တိုင် ရေးရမယ်)
        # စစ်ဆေးရန် (က)- လက်ရှိ self.dna ကော၊ အပြင်ကဝင်လာတဲ့ other_dna ကော Valid ဖြစ်ရဲ့လား?
        # Hint: self.is_valid_dna() က False ဖြစ်နေရင် သို့မဟုတ် 'X' စာလုံးပါဝင်မှုကို စစ်ဆေးတဲ့ တခြားနည်းလမ်းတစ်ခုခု သုံးနိုင်ပါတယ်
        # (ဒါပေမယ့် ပိုလွယ်အောင် other_dna အတွက်ပါ စစ်ချင်ရင် self.dna နေရာမှာ other_dna ခေတ္တလဲပြီး စစ်ရမလို ဖြစ်နေမယ်)

        for letter in other_dna:
            if letter not in ['A', 'T', 'G', 'C']:
                return "❌ အဝင် DNA စာသား မမှန်ကန်ပါ"

        if not self.is_valid_dna():
            return "❌ လက်ရှိ DNA စာသား မမှန်ကန်ပါ"

        # စစ်ဆေးရန် (ခ)- DNA နှစ်ခုစလုံး အရှည်တူရဲ့လား? (မတူရင် Error ပြန်ပါ)
        if len(self.dna) != len(other_dna):
            return "❌ DNA အမျှင်နှစ်ခုစလုံး အရှည်တူညီရပါမည်"

        distance = 0

      # (loop ပတ်ပြီး distance တွက်ရန်) ---
        for i in range(len(self.dna)):
            if self.dna[i] != other_dna[i]:
                distance += 1
        return distance

    def extract_gene(self):
        """Start Codon (ATG) မှ Stop Codon (TAA) အထိ DNA အပိုင်းအစကို ဖြတ်ထုတ်ပေးရမည်"""

        if not self.is_valid_dna():
            return "❌ Invalid DNA Sequence"

        start_idx = self.dna.find('ATG')

        stop_idx = self.dna.find('TAA', start_idx)

        # (ATG သို့မဟုတ် TAA ရှာမတွေ့ရင် သို့မဟုတ် TAA က ရှေ့ရောက်နေရင်)
        if start_idx == -1 or stop_idx == -1 or stop_idx < start_idx:
            return "❌ Gene ရှာမတွေ့ပါ"

        gene = self.dna[start_idx:stop_idx + 3]

        return gene

    def translate_rna_to_protein(self, rna_sequence):
        """ဝင်လာသော RNA sequence ကို ၃ လုံးစီဖြတ်ပြီး Amino Acid အမည်များအဖြစ် ပြောင်းပေးမည်"""
        rna = rna_sequence.upper()

        # မျိုးဗီဇအဘိဓာန် (Genetic Code Dictionary)
        genetic_code = {
            'AUG': 'Methionine', 'GCA': 'Alanine',
            'GAA': 'Glutamic Acid', 'UAA': 'STOP'
        }

        protein_list = []

        # --- မင်းရဲ့ စစ်တလင်း စပြီ ---
        # တာဝန်: ၀ ကနေ စပြီး rna ရဲ့ အလျားအထိ ၃ လုံးစီ ခုန်ပြီး loop ပတ်ပါ
        for i in range(0, len(rna), 3):
            # ၁။ i ကနေစပြီး စာလုံး ၃ လုံး ကွက်တိ ဖြတ်ယူပါ (Slicing)
            codon = rna[i:i + 3]

            # ၂။ ဖြတ်ယူထားတဲ့ codon ကို အပေါ်က genetic_code ထဲမှာ ရှာဖွေပါ
            # Hint: ဇယားထဲမရှိတဲ့ စာလုံးဆိုရင် 'Unknown' လို့ ပြပေးဖို့ .get(codon, 'Unknown') သုံးနိုင်ပါတယ်
            amino_acid = genetic_code.get(codon, 'Unknown')

            # ၃။ ရလာတဲ့ amino_acid ကို protein_list ထဲသို့ ထည့်သွင်းပါ (.append)
            protein_list.append(amino_acid)

        return protein_list

    def scan_security(self):
        if not self.is_valid_dna():
            return "Invalid DNA Sequence!"

        for code in self.danger_codes:
            if code in self.dna:
                return f"🚨 Warning: Bio-Threat Detected! ({code} found)"

        return "✅ Sequence Safe. No threats found."


engine = GenomeXEngine()

# စမ်းသပ်ချက် (၁) - DNA အမှန်
engine.load_sequence("ATGCATGC")
print(f"Test 1 (Valid DNA?): {engine.is_valid_dna()}")  # True ထွက်ရမည်

# စမ်းသပ်ချက် (၂) - DNA အတု (X ပါနေသည်)
engine.load_sequence("ATGCXATC")
print(f"Test 2 (Valid DNA?): {engine.is_valid_dna()}")  # False ထွက်ရမည်

engine.load_sequence("ATGCATGC")
print(f"Test 1 - GC Content: {engine.calculate_gc()}")


engine.load_sequence("ATGCXATC")
print(f"Test 2 - GC Content: {engine.calculate_gc()}")
engine = GenomeXEngine()

# လက်ရှိ DNA ကို အခြေချမယ်
engine.load_sequence("GAGCCTACTAACGGGAT")

# အရှည်တူပြီး စာလုံး ၇ လုံး ကွဲလွဲတဲ့ DNA တစ်ခုနဲ့ စမ်းယှဉ်မယ်
test_sequence = "CATCGTAATGACGGCAT"

print(f"Mutation Count: {engine.calculate_hamming_distance(test_sequence)}")
# အဖြေမှန်က 7 ထွက်လာရပါမယ်။

# စမ်းသပ်ချက် (၁) - Gene အမှန် ပါဝင်သော DNA (အဖြေက 'ATGAGCTAA' ထွက်ရမည်)
engine.load_sequence("CCCGGGATGAGCTAAAGCT")
print(f"Test 1 - Extracted Gene: {engine.extract_gene()}")

# စမ်းသပ်ချက် (၂) - DNA အတု ဖြစ်နေပါက (Error စာသား ထွက်ရမည်)
engine.load_sequence("CCCGGGATGAGCXAAAGCT")
print(f"Test 2 - Extracted Gene: {engine.extract_gene()}")


rna_sample = "AUGGCAGAAUAA"
print(f"Translated Proteins: {engine.translate_rna_to_protein(rna_sample)}")
# အဖြေမှန်က ['Methionine', 'Alanine', 'Glutamic Acid', 'STOP'] ထွက်ရပါမယ်။
