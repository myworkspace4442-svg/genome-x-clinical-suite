import matplotlib.pyplot as plt

# ၁။ စမ်းသပ်မည့် DNA စာသား
dna_sequence = "ATGGCTTAA"

# ၂။ စာလုံးတစ်လုံးချင်းစီကို လှမ်းရေတွက်မယ်
counts = {
    "Adenine (A)": dna_sequence.count("A"),
    "Thymine (T)": dna_sequence.count("T"),
    "Cytosine (C)": dna_sequence.count("C"),
    "Guanine (G)": dna_sequence.count("G")
}

bases = list(counts.keys())    # X-axis အတွက် နာမည်များ
values = list(counts.values())  # Y-axis အတွက် အရေအတွက်များ
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # လှပတဲ့ ကာလာစုံလေးတွေ
# ပထမဆုံး 'A' အပိုင်းလေးကို အပြင်နည်းနည်း ထွက်နေအောင် ဖြတ်ထုတ်ပြတာပါ
explode = (0.05, 0, 0, 0)

# ၄။ Pie Chart ကို စဆွဲမယ်
# autopct='%1.1f%%' ဆိုတာ ရာခိုင်နှုန်း (%) အလိုအလျောက် တွက်ချက်ပြီး ပြခိုင်းတာပါ
plt.pie(values, explode=explode, labels=bases, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

# ၅။ စက်ဝိုင်းပုံစံ အချိုးအစား မှန်အောင် ထိန်းညှိခြင်း
plt.axis('equal')
plt.title("DNA Base Ratio Percentage Analysis", fontsize=14, fontweight='bold')

# ၆။ ပုံကားချပ် ထုတ်ပြမယ်
plt.show()
