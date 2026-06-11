import random
from Bio import SeqIO
from Bio.Seq import Seq
import Levenshtein


class GenomeXEngine:
    def __init__(self):
        self.dna = ""
        self.danger_codes = ["GATTACA", "TTAACCGG", "ATATATAT"]
        # Set ကိုသုံးခြင်းဖြင့် စစ်ဆေးနှုန်း မိုက်ခရိုစက္ကန့်ပိုင်းပဲ ကြာပါတော့တယ်
        self.ALLOWED_BASES = set(['A', 'T', 'C', 'G', 'N'])

    def _clean_and_validate(self, sequence_string, name="DNA"):
        """
        [Option 1 Centralized Logic] 
        ဒေတာများကို သန့်စင်ပြီး စစ်ဆေးပေးမည့် သီးသန့် Internal Helper ဖြစ်သည်။
        """
        if not sequence_string:
            raise ValueError(f"❌ {name} စာသား ဗလာဖြစ်နေပါသည်။")

        # Space များနှင့် Line breaks များကို တစ်ခါတည်း ရှင်းထုတ်ပစ်မည်
        cleaned = sequence_string.upper().strip().replace(
            " ", "").replace("\n", "").replace("\r", "")

        # ခွင့်မပြုထားသော အမှိုက်စာလုံးများကို ရှာဖွေခြင်း
        invalid_characters = {
            char for char in cleaned if char not in self.ALLOWED_BASES}
        if invalid_characters:
            raise ValueError(
                f"❌ {name} ထဲတွင် ခွင့်မပြုထားသော အမှိုက်စာလုံးများ ပါဝင်နေသည်: {invalid_characters}")

        # 'N' စာလုံးပါဝင်မှုကို Warning ထုတ်ပေးရန်
        n_count = cleaned.count('N')
        if n_count > 0:
            print(
                f"⚠️ [Warning]: {name} ထဲတွင် ဖတ်မရသော Unknown Base ('N') {n_count} ခု တွေ့ရှိရသည်။")

        return cleaned

    def load_sequence(self, sequence_string):
        """DNA စတင်ထည့်သွင်းကတည်းက တစ်ခါတည်း သန့်စင်စစ်ဆေးပစ်မည်"""
        try:
            self.dna = self._clean_and_validate(sequence_string, "Loaded DNA")
            print("✅ DNA Sequence Successfully Loaded & Validated.")
        except ValueError as e:
            print(e)
            self.dna = ""  # ဒေတာမမှန်လျှင် Empty လုပ်ပစ်မည်

    def calculate_gc(self):
        if not self.dna:
            return 0.0
        g_count = self.dna.count('G')
        c_count = self.dna.count('C')
        return (g_count + c_count) / len(self.dna) * 100

    def calculate_hamming_distance(self, other_sequence):
        if not self.dna:
            return "❌ လက်ရှိ Engine ထဲတွင် DNA ဒေတာမရှိပါ"

        try:
            # အဝင်အမျှင်အသစ်ကိုပါ တစ်ခါတည်း သန့်စင်စစ်ဆေးပစ်မည်
            other_dna = self._clean_and_validate(other_sequence, "Input DNA")

            if len(self.dna) != len(other_dna):
                return "❌ DNA အမျှင်နှစ်ခုစလုံး အရှည်တူညီရပါမည်"

            # ရှင်းလင်းပြီး ပိုမြန်ဆန်သော Hamming loop
            return sum(1 for i in range(len(self.dna)) if self.dna[i] != other_dna[i])

        except ValueError as e:
            return str(e)

    def extract_gene(self):
        if not self.dna:
            return "❌ No DNA Sequence Loaded"
        start_idx = self.dna.find('ATG')
        stop_idx = self.dna.find('TAA', start_idx)
        if start_idx == -1 or stop_idx == -1 or stop_idx < start_idx:
            return "❌ Gene ရှာမတွေ့ပါ"
        return self.dna[start_idx:stop_idx + 3]

    def calculate_variant_distance(self, other_dna):
        """Levenshtein Library သုံးပြီး အရှည်မတူသော DNA များ၏ Genetic Distance ကို တွက်ခြင်း"""
        if not self.dna:
            return "❌ No DNA Sequence Loaded"
        try:
            cleaned_other = self._clean_and_validate(
                other_dna, "Comparison DNA")
            total_distance = Levenshtein.distance(self.dna, cleaned_other)
            return f"🧬 Total Genetic Distance = {total_distance} mutations detected. (Levenshtein C-Engine Optimized)"
        except ValueError as e:
            return str(e)

    def find_all_orfs(self):
        """
        [Option 2 Logic]
        DNA Sequence ထဲကနေ ဇီဝဗေဒစည်းမျဉ်းအတိုင်း ၃ လုံးစီ (Codons) ခုန်ပြီး
        Valid ဖြစ်တဲ့ Open Reading Frames (ORFs) အားလုံးကို ရှာပေးမည့် စနစ်။
        """
        if not self.dna:
            return []

        orfs = []
        dna_len = len(self.dna)

        # ⚡ ဇီဝဗေဒအရ Reading Frames ၃ ခု (Frame 0, 1, 2) ရှိနိုင်လို့ အကုန်ပတ်ရှာမယ်
        for frame in range(3):
            i = frame
            while i < dna_len - 2:
                codon = self.dna[i:i+3]

                if codon == "ATG":  # Start Codon တွေ့ပြီ!
                    start_idx = i
                    found_stop = False

                    # Start Codon တွေ့တဲ့နေရာကနေ ၃ လုံးစီ ထပ်ခုန်ပြီး Stop Codon လိုက်ရှာမယ်
                    for j in range(start_idx + 3, dna_len - 2, 3):
                        next_codon = self.dna[j:j+3]

                        if next_codon in ["TAA", "TAG", "TGA"]:  # Stop Codons
                            stop_idx = j + 3
                            orf_sequence = self.dna[start_idx:stop_idx]

                            # တွေ့တဲ့ ORF ကို သိမ်းမယ် (ဘယ် Frame က ရှာတွေ့လဲပါ မှတ်မယ်)
                            orfs.append({
                                "frame": frame,
                                "start": start_idx,
                                "stop": stop_idx,
                                "sequence": orf_sequence
                            })

                            # အနီးဆုံး Stop Codon တွေ့ရင် ရပ်ပြီး နောက်ထပ် Start Codon အသစ် ထပ်ရှာမယ်
                            i = j
                            found_stop = True
                            break

                    if found_stop:
                        i += 3
                        continue

                i += 3  # ၃ လုံးစီ ခုန်ဖတ်ခြင်း (In-frame scanning)

        return orfs

    def calculate_codon_usage(self):
        if not self.dna:
            return {}
        codon_counts = {}
        total_codons = 0
        for i in range(0, len(self.dna) - 2, 3):
            codon = self.dna[i:i+3]

            codon_counts[codon] = codon_counts.get(codon, 0) + 1
            total_codons += 1
        if total_codons == 0:
            return {}
        codon_analysis = {}
        for codon, count in codon_counts.items():
            percentage = (count / total_codons) * 100
            codon_analysis[codon] = {
                "count": count,
                "percentage": round(percentage, 2)
            }
        return codon_analysis

    def translate_rna_to_protein(self, rna_sequence):
        # နေရာတကာ ထပ်မစစ်တော့ဘဲ ဝင်လာမည့် RNA ကို ရှင်းထုတ်ပြီး BioPython ဖြင့် တန်းမောင်းမည်
        rna_clean = rna_sequence.upper().strip().replace(' ', '').replace('\n', '')
        return str(Seq(rna_clean).translate(to_stop=True))

    def scan_security(self):
        if not self.dna:
            return "No DNA Sequence Loaded"
        for code in self.danger_codes:
            if code in self.dna:
                return f"🚨 Warning: Bio-Threat Detected! ({code} found)"
        return "✅ Sequence Safe. No threats found."

    def DNA_to_RNA(self):
        if not self.dna:
            return "No DNA Sequence Loaded"
        return str(Seq(self.dna).transcribe())

    def generate_mutation(self, mutation_count=1):
        if not self.dna:
            return "❌ No DNA Sequence Loaded"
        dna_list = list(self.dna)
        bases = ['A', 'T', 'G', 'C']
        mutated_indices = random.sample(
            range(len(self.dna)), min(mutation_count, len(self.dna)))
        for idx in mutated_indices:
            current_base = dna_list[idx]
            possible_bases = [b for b in bases if b != current_base]
            dna_list[idx] = random.choice(possible_bases)
        return "".join(dna_list)

    def read_fasta(self, file_path):
        print(f"📂 Reading FASTA file from: {file_path}\n")
        try:
            for record in SeqIO.parse(file_path, "fasta"):
                print(f"🆔 Gene ID        : {record.id}")
                print(f"Description    : {record.description}")
                print(f"🧬 Sequence Length : {len(record.seq)} bases")
                print(f"🧪 Transcribed RNA : {record.seq.transcribe()[:15]}...")
                print(
                    f"💊 Translated Prot : {record.seq.translate(to_stop=True)}")
                print("-" * 50)
        except FileNotFoundError:
            print("❌ Error: ဖိုင်ရှာမတွေ့ပါဗျာ။ File Path မှန်မမှန် ပြန်စစ်ပေးပါ။")

    def export_diagnostic_report(self, filename="genome_report.txt", other_sequence=None):
        """
        [Option 3 Logic]
        DNA ၏ အချက်အလက်များ၊ Security Status များနှင့် အသစ်ထည့်သွင်းထားသော 
        ORF (Protein) ခွဲခြမ်းစိတ်ဖြာမှု ရလဒ်အားလုံးကို ဖိုင်တွဲတစ်ခုတည်းအဖြစ် သိမ်းဆည်းပေးမည့်စနစ်။
        """
        if not self.dna:
            return "❌ Export လုပ်ရန် DNA ဒေတာမရှိသေးပါ"

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(
                    "==================================================\n")
                file.write(
                    "           GEONOME-X DIAGNOSTIC REPORT            \n")
                file.write(
                    "==================================================\n")
                file.write(f"Original DNA Sequence : {self.dna}\n")
                file.write(
                    f"GC Content Percentage : {self.calculate_gc():.2f}%\n")
                file.write(f"Bio-Security Status   : {self.scan_security()}\n")

                # 🧬 [ORF Analysis Integration]
                # အပေါ်ကရေးခဲ့တဲ့ ORF Finder ကို လှမ်းခေါ်ပြီး Report ထဲ ထည့်သွင်းခြင်း
                orfs = self.find_all_orfs()
                file.write(
                    "\n==================================================\n")
                file.write(
                    "        OPEN READING FRAME (ORF) ANALYSIS         \n")
                file.write(
                    "==================================================\n")
                file.write(
                    f"Total ORFs Detected   : {len(orfs)} frames found.\n")

                for index, orf in enumerate(orfs, 1):
                    file.write(f"\n▶️ ORF #{index} (Frame +{orf['frame']}):\n")
                    file.write(
                        f"  ↳ Position : {orf['start']} to {orf['stop']}\n")
                    file.write(f"  ↳ Sequence : {orf['sequence']}\n")

                    # RNA ပြောင်းပြီး Protein ထုတ်ယူမှု ရလဒ်ကိုပါ တစ်ခါတည်း တွက်ချက်သိမ်းဆည်းမည်
                    protein_product = self.translate_rna_to_protein(
                        orf['sequence'].replace('T', 'U'))
                    file.write(f"  ↳ Protein  : {protein_product}\n")

                # 🧬 [Mutation Analysis Section]
                if other_sequence:
                    if len(self.dna) == len(other_sequence):
                        distance = f"{self.calculate_hamming_distance(other_sequence)} mutations (Hamming)"
                    else:
                        distance = self.calculate_variant_distance(
                            other_sequence)

                    file.write(
                        "\n==================================================\n")
                    file.write(
                        "                MUTATION ANALYSIS                 \n")
                    file.write(
                        "==================================================\n")
                    file.write(
                        f"Compared Sequence     : {other_sequence.upper()}\n")
                    file.write(f"Result                : {distance}\n")

                file.write(
                    "\n==================================================\n")
                file.write(
                    "Report Generated Successfully by Genome-X Engine.\n")

            return f"✅ Report Officially Saved: '{filename}'"

        except Exception as e:
            return f"❌  (File Export Error): {str(e)}"


# ==========================================
# 🎯 တကယ့် စမ်းသပ်မောင်းနှင်ချက်များ (Test Runs)
# ==========================================
engine = GenomeXEngine()

# စမ်းသပ်ချက် (၁)


# စမ်းသပ်ချက် (၂) - အရှည်မတူတဲ့ ကောင်တွေကို Distance တွက်ခြင်း (အသစ်ထည့်ထားတဲ့ Matrix စနစ်စမ်းသပ်မှု)
engine.load_sequence("GAGCCTACTAACGGGAT")
test_sequence = "CATCGTAATGACGGCAT"
print(f"Hamming Distance: {engine.calculate_hamming_distance(test_sequence)}")

# အရှည်မတူတဲ့ DNA နဲ့ စမ်းသပ်မယ် (ဒါဆိုရင် Matrix ကောင် အလုပ်လုပ်လိမ့်မယ်)
long_sequence = "GAGCCTACTAACGGGATTTTT"
print(
    f"Variant Distance (Matrix): {engine.calculate_variant_distance(long_sequence)}")

# စမ်းသပ်ချက် (၃) - Gene Extraction & Translation
engine.load_sequence("CCCGGGATGAGCTAAAGCT")
print(f"Extracted Gene: {engine.extract_gene()}")

rna_sample = "AUGGCAGAAUAA"
print(f"Translated Proteins: {engine.translate_rna_to_protein(rna_sample)}")

# စမ်းသပ်ချက် (၄) - Mutation & Report Export
engine.load_sequence("CGTTAGATTACACTG")
mutated_dna = engine.generate_mutation(mutation_count=3)
report_status = engine.export_diagnostic_report(
    "clinical_result.txt", other_sequence=mutated_dna)
print(report_status)
# အင်ဂျင်ကို ခေါ်သုံးခြင်း
# သို့မဟုတ် မင်းပေးထားတဲ့ Class နာမည်

# မိမိဆောက်ခဲ့သော ဖိုင်ကို လှမ်းဖတ်ခိုင်းခြင်း
engine.read_fasta("sample.fasta")
# --- Engine ကို အသက်သွင်းခြင်း ---
engine = GenomeXEngine()

# စမ်းသပ်ဖို့ DNA ထည့်မယ် (ဒီထဲမှာ frame 0 ရော frame 1 မှာပါ ORF တွေ မြှုပ်ထားတယ်)
test_sequence = "ATGAAATAAgATGCCCCCTGA"
engine.load_sequence(test_sequence)

# ORF ရှာခိုင်းမယ်
found_orfs = engine.find_all_orfs()
# ၁။ Engine ကို အသက်သွင်းပြီး ဒေတာ ထည့်မယ်
engine = GenomeXEngine()
# Space တွေရော၊ စာလုံးအသေးတွေရော ပါတယ်
engine.load_sequence("  atgaaataag atgccccctga  ")

# ၂။ ခွဲခြမ်းစိတ်ဖြာမှု အစီရင်ခံစာကို ထုတ်ယူမယ်
# (ဒီမှာ Mutation စစ်ဖို့ အမျှင်တစ်ခုပါ တစ်ခါတည်း ထည့်စမ်းထားပါတယ်)
status_message = engine.export_diagnostic_report(
    filename="genome_report.txt",
    other_sequence="ATGAAATAAGATGCCCCCTGG"
)

print(status_message)
engine = GenomeXEngine()
# စမ်းသပ်ဖို့ Codon တချို့ကို အထပ်ထပ် ထည့်ထားတဲ့ DNA
engine.load_sequence("ATGATGATGTTTTTTCCCGGG")

usage_report = engine.calculate_codon_usage()

print("\n📊 [CODON USAGE BIAS REPORT]")
print("-" * 35)
for codon, data in usage_report.items():
    print(
        f"🧬 Codon: {codon} | Count: {data['count']} ကြိမ် | Percentage: {data['percentage']}%")
