from Bio.Seq import Seq

# ၁။ DNA Sequence တစ်ခု သတ်မှတ်ခြင်း
my_dna = Seq("CCCGGGATGAGCTAAAGCT")
print(f"🧬 Original DNA      : {my_dna}")

# ၂။ DNA မှ RNA သို့ ပြောင်းခြင်း (Manual ရေးတုန်းက .replace('T', 'U') လုပ်ခဲ့ရတဲ့အပိုင်း)
my_rna = my_dna.transcribe()
print(f"🧪 Transcribed RNA   : {my_rna}")

# ၃။ Protein သို့ တိုက်ရိုက် ဘာသာပြန်ခြင်း (Loop ပတ်ပြီး Dict ထဲ ရှာခဲ့ရတဲ့အပိုင်း)
my_protein = my_dna.translate()
print(f"💊 Translated Protein: {my_protein}")
