import random
import Levenshtein
import numpy as np
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
# အခြား import များရဲ့ အောက်မှာ ထည့်ပါ
from engine.cache_manager import LocalCacheEngine
import re

# =====================================================================
# 📚 KNOWLEDGE BASE MODULE
# =====================================================================


class GeneticKnowledgeBase:
    def __init__(self):

        # ညီမလေး ရှာဖွေပြီး ထည့်သွင်းထားတဲ့ ဒေတာစနစ်
        self.rules = {
            "E_coli": [
                {
                    "mutation_pattern": "ATATATAT",
                    "antibiotic": "Ampicillin",
                    "probability": 0.75,
                    "environmental_factor": "Low pH"
                },
                {
                    "mutation_pattern": "AAAAA",
                    "antibiotic": "Penicillin",
                    "probability": 0.70,
                    "environmental_factor": "Acidic"
                }
            ]
        }

# =====================================================================
# 🧬 GENOME_X_SUITE: INTEGRATED CORE ENGINE
# =====================================================================


class GenomeXEngine:
    def __init__(self):
        self.dna = ""

        self.danger_codes = ["GATTACA", "TTAACCGG", "ATATATAT"]
        self.ALLOWED_BASES = set(['A', 'T', 'C', 'G', 'N'])
        Entrez.email = "genomex_user@example.com"
        self.kb = GeneticKnowledgeBase()

        # 💥 ဒီစာကြောင်းလေး အသစ်ဝင်လာပါပြီ
        self.cache = LocalCacheEngine()

    def _clean_and_validate(self, sequence_string, name="DNA"):
        if not sequence_string:
            raise ValueError(f"❌ {name} စာသား ဗလာဖြစ်နေပါသည်။")

        cleaned = sequence_string.upper().strip().replace(
            " ", "").replace("\n", "").replace("\r", "")

        invalid_characters = {
            char for char in cleaned if char not in self.ALLOWED_BASES}
        if invalid_characters:
            raise ValueError(
                f"❌ {name} ထဲတွင် ခွင့်မပြုထားသော အမှိုက်စာလုံးများ ပါဝင်နေသည်: {invalid_characters}")

        n_count = cleaned.count('N')
        if n_count > 0:
            print(
                f"⚠️ [Warning]: {name} ထဲတွင် ဖတ်မရသော Unknown Base ('N') {n_count} ခု တွေ့ရှိရသည်။")

        return cleaned

    def load_sequence(self, sequence_string):
        try:
            self.dna = self._clean_and_validate(sequence_string, "Loaded DNA")
            print("✅ DNA Sequence Successfully Loaded & Validated.")
        except ValueError as e:
            print(e)
            self.dna = ""

    def fetch_from_ncbi(self, accession_id):
        """အင်တာနက်မသွားခင် စက်ထဲက Local Cache ကို အရင်စစ်ဆေးမည့် စနစ်သစ်"""

        # ၁။ စက်ထဲမှာ သိမ်းထားတာ ရှိမရှိ အရင်စစ်မယ်
        cached_dna = self.cache.get_from_cache(accession_id)
        if cached_dna:
            self.dna = cached_dna  # တွေ့ရင် အင်ဂျင်ထဲ တန်းထည့်မယ်
            return self.dna

        # ၂။ စက်ထဲမှာ မရှိမှသာ အင်တာနက်ကနေ ဒေါင်းလုဒ်ဆွဲမယ် (NCBI ခေါ်ယူခြင်း)
        print(
            f"🌐 [NCBI Fetch]: {accession_id} ကို အင်တာနက်မှ စတင် ဒေါင်းလုဒ်ဆွဲနေပါသည်...")
        try:
            handle = Entrez.efetch(
                db="nucleotide", id=accession_id, rettype="fasta", retmode="text")
            fasta_data = handle.read()
            handle.close()

            lines = fasta_data.strip().split("\n")
            dna_sequence = "".join(
                [line for line in lines if not line.startswith(">")])
            self.dna = dna_sequence.upper()

            # ၃။ အင်တာနက်က အောင်မြင်စွာ ဆွဲလို့ရသွားပြီဆိုတာနဲ့ နောက်တစ်ခါအတွက် စက်ထဲကို ချက်ချင်း သိမ်းထားလိုက်မယ် 💥
            if self.dna:
                self.cache.save_to_cache(accession_id, self.dna)

            return self.dna

        except Exception as e:
            print(f"NCBI Fetch Error: {str(e)}")
            return None

    def calculate_gc(self):
        if not self.dna:
            return 0.0
        dna_array = np.array(list(self.dna))
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
                if codon == "ATG":
                    start_idx = i
                    found_stop = False

                    for j in range(start_idx + 3, dna_len - 2, 3):
                        next_codon = self.dna[j:j+3]
                        if next_codon in ["TAA", "TAG", "TGA"]:
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
        print(f"📂 Reading FASTA file from: {file_path}\n")
        dna_sequence = ""
        try:
            for record in SeqIO.parse(file_path, "fasta"):
                print(f"🆔 Gene ID        : {record.id}")
                print(f"Description    : {record.description}")
                print(f"🧬 Sequence Length : {len(record.seq)} bases")
                print(f"🧪 Transcribed RNA : {record.seq.transcribe()[:15]}...")
                print(
                    f"💊 Translated Prot : {record.seq.translate(to_stop=True)[:15]}...")
                print("-" * 50)
                dna_sequence += str(record.seq)

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
                file.write(f"Original DNA Sequence : {self.dna[:100]}...\n")
                file.write(
                    f"GC Content Percentage : {self.calculate_gc():.2f}%\n")
                file.write(f"Bio-Security Status   : {self.scan_security()}\n")

                orfs = self.find_all_orfs()
                file.write(
                    "\n==================================================\n")
                file.write(
                    "        OPEN READING FRAME (ORF) ANALYSIS          \n")
                file.write(
                    "==================================================\n")
                file.write(
                    f"Total ORFs Detected   : {len(orfs)} frames found.\n")

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

    # 💥 [FIXED MODULES]: `something` Class ထဲက Function များကို ဤနေရာသို့ ရွှေ့ပြောင်းပေါင်းစပ်လိုက်ပါပြီ
    def analyze_drug_resistance(self, organism_name, dna_sequence, current_environment):
        """အသစ်ထည့်သွင်းလိုက်သော ဆေးယဉ်ပါးမှု စစ်ဆေးသည့် စနစ်"""
        if organism_name not in self.kb.rules:
            return None

        detected_risks = []
        organism_rules = self.kb.rules[organism_name]

        for rule in organism_rules:
            if rule["mutation_pattern"] in dna_sequence and rule["environmental_factor"] == current_environment:
                detected_risks.append({
                    "antibiotic": rule["antibiotic"],
                    "confidence": f"{rule['probability'] * 100}%",
                    "reason": f"ဗီဇပုံစံ {rule['mutation_pattern']} က {current_environment} တွင် DNA Update ဖြစ်သွားခြင်း ဖြစ်သည်။"
                })
        return detected_risks

    def generate_realtime_report(self, organism, sequence, environment):
        """Terminal တွင် Real-Time Analysis ရလဒ်ကို လှပစွာ ထုတ်ပြပေးမည့် Function"""
        # လက်ရှိ Engine ရဲ့ self.dna ထဲသို့ ဒေတာ အရင်သွင်းယူပြီး သန့်စင်စစ်ဆေးမည်
        self.load_sequence(sequence)

        gc = self.calculate_gc()
        security = self.scan_security()
        orfs = len(self.find_all_orfs())
        risks = self.analyze_drug_resistance(organism, self.dna, environment)

        print("\n========================================")
        print("        GENOMEX ENGINE REAL-TIME ANALYSIS       ")
        print("========================================")
        print(f" Organism Under Test  : 🧫 {organism}")
        print(f" Section GC Content   : {gc:.2f}%")
        print(f" 🛡️ Bio-Security Scan  : {security}")
        print(f" 🧬 Open Reading Frames: {orfs} frames detected")
        print(f" 🌍 Environment Cond.  : 🌡️ {environment}")

        print("\n----------------------------------------")
        print(" 💊 DRUG RESISTANCE (MUTATION) ANALYSIS ")
        print("----------------------------------------")

        if risks:
            for r in risks:
                print(
                    f" 🚨 Warning : {r['antibiotic']} ဆေးမတိုးနိုင်ခြေ ({r['confidence']}) ရှိနေပါသည်။")
                print(f" 📝 Reason  : {r['reason']}")
        else:
            print(
                " ✅ Status  : မျိုးဗီဇအရ ဆေးယဉ်ပါးမှုအန္တရာယ် မရှိပါ။ စိတ်ချစွာ ကုသနိုင်ပါသည်။")
        print("========================================\n")


def validate_dna_sequence(sequence: str) -> tuple[bool, str]:
    """
    Sequence တကယ် ဟုတ်၊ မဟုတ် စစ်ဆေးပေးသော Function
    """
    # နေရာလွတ်နှင့် Enter ခေါက်ချက်များ ဖျက်ခြင်း
    clean_seq = sequence.strip().upper()

    if not clean_seq:
        return False, "❌ Empty input provided."

    # FASTQ / FASTA Header ပါပါက ဖျက်ပြီး Base စာသားကိုပဲ စစ်ဆေးခြင်း
    lines = clean_seq.splitlines()
    bases = "".join([line for line in lines if not line.startswith(
        '>') and not line.startswith('@')])

    # A, T, C, G, N သာ ပါဝင်ရမည် (Command များ၊ ကိန်းဂဏန်းများ သို့မဟုတ် လမ်းကြောင်းများ လက်မခံပါ)
    pattern = r'^[ATCGN]+$'

    if re.match(pattern, bases):
        return True, "Valid DNA Sequence"
    else:
        return False, "❌ Invalid Genomic Sequence! Only DNA bases (A, T, C, G) are allowed. Commands like 'docker compose up -d' are rejected."


# --- စမ်းသပ်မောင်းနှင်ခြင်း ---
if __name__ == "__main__":
    engine = GenomeXEngine()

    # စမ်းသပ်ရန် နမူနာ (E_coli DNA) - ထဲတွင် ညီမလေး သတ်မှတ်ထားသော ATATATAT ပါဝင်သည်
    fetched_dna = "ATATATATGGCCAAATTTTCCGG"
    current_env = "Low pH"

    # Report ထုတ်ခိုင်းခြင်း
    engine.generate_realtime_report("E_coli", fetched_dna, current_env)
