import random
import Levenshtein
from Bio import SeqIO
from Bio.Seq import Seq
import numpy as np


class GenomeXEngine:
    def __init__(self):
        self.dna = ""
        self.danger_codes = ["GATTACA", "TTAACCGG", "ATATATAT"]
        # Set ကိုသုံးခြင်းဖြင့် စစ်ဆေးနှုန်း မိုက်ခရိုစက္ကန့်ပိုင်းပဲ ကြာပါတော့တယ်
        self.ALLOWED_BASES = set(['A', 'T', 'C', 'G', 'N'])

    def _clean_and_validate(self, sequence_string, name="DNA"):
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
        dna_array = np.array(list(self.dna))

        # 'N' စာလုံးများကို ဖယ်ထုတ်ပြီးမှ တိကျသော အရေအတွက်ကို တွက်ချက်ခြင်း
        valid_dna = dna_array[dna_array != 'N']
        if len(valid_dna) == 0:
            return 0.0

        g_count = np.sum(valid_dna == 'G')
        c_count = np.sum(valid_dna == 'C')
        return (g_count + c_count) / len(valid_dna) * 100

    def calculate_hamming_distance(self, other_sequence):
        if not self.dna:
            return "❌ လက်ရှိ Engine ထဲတွင် DNA ဒေတာမရှိပါ"
        try:
            other_dna = self._clean_and_validate(other_sequence, "Input DNA")
            if len(self.dna) != len(other_dna):
                return "❌ DNA အမျှင်နှစ်ခုစလုံး အရှည်တူညီရပါမည်"

            # NumPy သုံးပြီး ပိုမိုမြန်ဆန်အောင် Vectorized Hamming Distance တွက်နည်းပြောင်းလဲခြင်း
            arr1 = np.array(list(self.dna))
            arr2 = np.array(list(other_dna))
            return int(np.sum(arr1 != arr2))
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
        if not self.dna:
            return []

        orfs = []
        dna_len = len(self.dna)

        for frame in range(3):
            i = frame
            while i < dna_len - 2:
                codon = self.dna[i:i+3]
                if codon == "ATG":  # Start Codon တွေ့ပြီ!
                    start_idx = i
                    found_stop = False

                    for j in range(start_idx + 3, dna_len - 2, 3):
                        next_codon = self.dna[j:j+3]
                        if next_codon in ["TAA", "TAG", "TGA"]:  # Stop Codons
                            stop_idx = j + 3
                            orf_sequence = self.dna[start_idx:stop_idx]

                            orfs.append({
                                "frame": frame,
                                "start": start_idx,
                                "stop": stop_idx,
                                "sequence": orf_sequence
                            })
                            i = j
                            found_stop = True
                            break

                    if found_stop:
                        i += 3
                        continue
                i += 3
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
        """BioPython SeqIO ဖြင့် သန့်ရှင်းသေသပ်စွာ ပြန်လည်ပြင်ဆင်ထားသော FASTA Reader"""
        print(f"📂 Reading FASTA file from: {file_path}\n")
        dna_sequence = ""
        try:
            # SeqIO သုံးပြီး ပေါ့ပေါ့ပါးပါး ဖတ်ရှုခြင်း
            for record in SeqIO.parse(file_path, "fasta"):
                print(f"🆔 Gene ID        : {record.id}")
                print(f"Description    : {record.description}")
                print(f"🧬 Sequence Length : {len(record.seq)} bases")
                print(f"🧪 Transcribed RNA : {record.seq.transcribe()[:15]}...")
                print(
                    f"💊 Translated Prot : {record.seq.translate(to_stop=True)[:15]}...")
                print("-" * 50)
                dna_sequence += str(record.seq)

            # ဖတ်လို့ရလာတဲ့ Sequence ကို Engine ရဲ့ self.dna ထဲကိုပါ တန်းထည့်ပေးလိုက်မယ်
            if dna_sequence:
                self.load_sequence(dna_sequence)
            return dna_sequence

        except FileNotFoundError:
            print("❌ Error: ဖိုင်ရှာမတွေ့ပါဗျာ။ File Path မှန်မမှန် ပြန်စစ်ပေးပါ။")
            return ""

    def export_diagnostic_report(self, filename="genome_report.txt", other_sequence=None):
        if not self.dna:
            return "❌ Export လုပ်ရန် DNA ဒေတာမရှိသေးပါ"
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(
                    "==================================================\n")
                file.write(
                    "            GEONOME-X DIAGNOSTIC REPORT            \n")
                file.write(
                    "==================================================\n")
                # တအားရှည်ရင် Report ကြည့်ရဆိုးလို့ အစပိုင်းပဲပြမယ်
                file.write(f"Original DNA Sequence : {self.dna[:100]}...\n")
                file.write(
                    f"GC Content Percentage : {self.calculate_gc():.2f}%\n")
                file.write(f"Bio-Security Status   : {self.scan_security()}\n")

                orfs = self.find_all_orfs()
                file.write(
                    "\n==================================================\n")
                file.write(
                    "        OPEN READING FRAME (ORF) ANALYSIS         \n")
                file.write(
                    "==================================================\n")
                file.write(
                    f"Total ORFs Detected   : {len(orfs)} frames found.\n")

                # Top 10 ကိုပဲ အရင်ထုတ်ပြမယ်
                for index, orf in enumerate(orfs[:10], 1):
                    file.write(f"\n▶️ ORF #{index} (Frame +{orf['frame']}):\n")
                    file.write(
                        f"  ↳ Position : {orf['start']} to {orf['stop']}\n")
                    file.write(f"  ↳ Sequence : {orf['sequence'][:50]}...\n")
                    protein_product = self.translate_rna_to_protein(
                        orf['sequence'].replace('T', 'U'))
                    file.write(f"  ↳ Protein  : {protein_product[:50]}...\n")

                if other_sequence:
                    if len(self.dna) == len(other_sequence):
                        distance = f"{self.calculate_hamming_distance(other_sequence)} mutations (Hamming)"
                    else:
                        distance = self.calculate_variant_distance(
                            other_sequence)

                    file.write(
                        "\n==================================================\n")
                    file.write(
                        "                  MUTATION ANALYSIS                \n")
                    file.write(
                        "==================================================\n")
                    file.write(f"Result                : {distance}\n")

                file.write(
                    "\n==================================================\n")
                file.write(
                    "Report Generated Successfully by Genome-X Engine.\n")
            return f"✅ Report Officially Saved: '{filename}'"
        except Exception as e:
            return f"❌ (File Export Error): {str(e)}"


# ==========================================
# 🎯 တကယ့် စမ်းသပ်မောင်းနှင်ချက်များ (Test Runs)
# ==========================================
engine = GenomeXEngine()

# စမ်းသပ်ချက် (၁)


# စမ်းသပ်ဖို့ Codon တချို့ကို အထပ်ထပ် ထည့်ထားတဲ့ DNA
engine.load_sequence("ATGATGATGTTTTTTCCCGGG")

usage_report = engine.calculate_codon_usage()

print("\n📊 [CODON USAGE BIAS REPORT]")
print("-" * 35)
for codon, data in usage_report.items():
    print(
        f"🧬 Codon: {codon} | Count: {data['count']} times/time | Percentage: {data['percentage']}%")
# ၁။ Engine ကို စတင်သက်သွင်းမယ်
# ၂။ Covid ဖိုင်ကို လှမ်းဖတ်ပြီး Engine ထဲကို Data သွင်းမယ်
fasta_file = "covid_19.fasta"
engine.read_fasta(fasta_file)

# ၃။ ဒေတာဝင်သွားပြီဆိုရင် ခွဲခြမ်းစိတ်ဖြာမှုတွေ တန်းလုပ်မယ်
if engine.dna:
    print("\n" + "="*40)
    print("        GENOMEX ENGINE REAL-TIME ANALYSIS       ")
    print("="*40)

    # GC Content တွက်ချက်ခြင်း
    gc_percent = engine.calculate_gc()
    print(f"📊 COVID-19 Section GC Content : {gc_percent:.2f}%")

    # ဇီဝလုံခြုံရေး စစ်ဆေးခြင်း
    security_status = engine.scan_security()
    print(f"🛡️ Bio-Security Scan Status   : {security_status}")

    # Open Reading Frames (ORFs) ဘယ်နှစ်ခုရှာတွေ့လဲ စစ်ခြင်း
    orfs_found = engine.find_all_orfs()
    print(f"🧬 Open Reading Frames Found  : {len(orfs_found)} frames")

    # ၄။ ရလဒ်အားလုံးကို Text Report ဖိုင်အဖြစ် သိမ်းဆည်းခြင်း
    report_file = "covid_analysis_report.txt"
    export_status = engine.export_diagnostic_report(report_file)
    print(f"\n📝 Report Status: {export_status}")
