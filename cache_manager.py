import json
import os


class LocalCacheEngine:
    def __init__(self, cache_file="genome_cache.json"):
        self.cache_file = cache_file
        # အစပြုချိန်တွင် စက်ထဲ၌ cache ဖိုင် ရှိမရှိ စစ်ဆေးပြီး ရှိလျှင် ဒေတာများကို ဖတ်ယူထားမည်
        self.cache_data = self._load_cache()

    def _load_cache(self):

        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as file:
                return json.load(file)
        return {}

    def save_to_cache(self, accession_id, dna_sequence):
        """အင်တာနက်မှ ရလာသော DNA ကို စက်ထဲသို့ အမြဲတမ်း သိမ်းဆည်းမည့် Function"""
        # Dictionary ထဲသို့ ID ကို Key အဖြစ်၊ DNA ကို Value အဖြစ် ထည့်မည်
        self.cache_data[accession_id] = dna_sequence

        # ပြီးလျှင် .json ဖိုင်ထဲသို့ ရေးသွင်းသိမ်းဆည်းမည်
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache_data, file, indent=4)
        print(
            f"💾 [Cache Status]: ID {accession_id} ကို စက်ထဲသို့ သိမ်းဆည်းပြီးပါပြီ။")

    def get_from_cache(self, accession_id):
        """စက်ထဲမှာ ID ရှိမရှိ စစ်ဆေးပြီး ရှိလျှင် DNA ကို ချက်ချင်း ပြန်ထုတ်ပေးမည့် Function"""
        if accession_id in self.cache_data:
            print(
                f"⚡ [Cache Hit]: ID {accession_id} ကို စက်ထဲမှ ချက်ချင်း ရှာတွေ့ပါသည်။ (Offline)")
            return self.cache_data[accession_id]
        print(
            f"🌐 [Cache Miss]: ID {accession_id} ကို စက်ထဲတွင် မရှိပါ။ အင်တာနက်မှ ဆွဲရပါမည်။")
        return None


if __name__ == "__main__":
    # ၁။ ငါတို့ ဆောက်ထားတဲ့ အင်ဂျင်ကို သုံးမယ်ဆိုပြီး နှိုးလိုက်မယ်
    cache_engine = LocalCacheEngine()

    # ၂။ စမ်းသပ်ဖို့အတွက် ID နဲ့ DNA နမူနာ သတ်မှတ်မယ်
    sample_id = "NM_000546"
    sample_dna = "ATGCGTACGTAGCTAGCTAGCTAG"

    print("--- 💾 အဆင့် (၁): ဒေတာကို စက်ထဲ သိမ်းဆည်းခြင်း ---")
    cache_engine.save_to_cache(sample_id, sample_dna)

    print("\n--- ⚡ အဆင့် (၂): သိမ်းထားတဲ့ ဒေတာကို ပြန်ထုတ်ယူခြင်း ---")
    retrieved_dna = cache_engine.get_from_cache(sample_id)
    print(f"🔬 ပြန်ရလာတဲ့ DNA: {retrieved_dna}")
