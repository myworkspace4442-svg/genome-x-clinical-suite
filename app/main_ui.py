from flask import send_file  # send_file မရှိသေးရင် flask import ထဲမှာ ထည့်ပါ
from report_generator import generate_clinical_pdf


from flask import Flask, render_template, request
from Core_Engine import GenomeXEngine
# 🧹 လိုအပ်တဲ့ function များကို သေသေချာချာ import လုပ်ထားပါတယ်
import database

app = Flask(__name__)
engine = GenomeXEngine()


@app.route("/", methods=["GET", "POST"])
# app.py ရဲ့ def home(): အပိုင်းကို ဒီလိုလေး ပြင်ပေးပါ
def home():
    # 💡 [ADDED] စာမျက်နှာစဖွင့်ချင်း Error မတက်အောင် variable တွေကို default တန်ဖိုး ကြိုပေးထားမယ်
    action = request.form.get("action") if request.method == "POST" else None
    # Form က တောင်းတဲ့ DNA Input Name အတိုင်းပေးပါ
    user_dna = request.form.get("dna_input", "")
    result_type = "SYSTEM_READY"
    scan_result = ""
    result = ""
    is_error = False
    history_data = []

    # --- ဒီအောက်ကနေစပြီး ညီမလေးရဲ့ မူရင်း logic တွေ (လိုင်း ၇၃ ကနေစတဲ့ ကုဒ်တွေ) ပြန်လာပါမယ် ---
    # ညီမလေး လက်ရှိ ရေးထားတဲ့ အပိုင်း-
    if request.method == "POST":
        if action == "alignment":
            is_error = True
            # 💾 တွက်ချက်မှု အောင်မြင်မှ ဒေတာဘေ့စ်ထဲ သိမ်းမည်
            database.save_history(user_dna, result_type, result)

        elif action == "bio_scan":
            result_type = "Bio-Security Scan"
            scan_result = engine.scan_security()
            if "Warning" in scan_result:
                result = scan_result
                is_error = True
            else:
                result = scan_result
                is_error = False
            # 💾 ကောင်မွန်မှု ရလဒ်ကို ဒေတာဘေ့စ်ထဲ သိမ်းမည်
            database.save_history(user_dna, result_type, result)

            # 🎯 (ဂ) Lab Report စာသားဖိုင် ထုတ်ယူခြင်း (ဒုတိယ DNA လက်ခံရန် အရေးကြီးလှပါပြီ)
        elif action == "export_report":
            from flask import make_response  # ဖိုင်ထုတ်ပေးရန် Flask ရဲ့ library ကို သုံးပါမယ်

            # Form ထဲက ဒုတိယ DNA Input တန်ဖိုးကို ယူမယ်
            user_dna_2 = request.form.get("dna_input_2")

            # Core_Engine ထဲက Report ထုတ်ပေးတဲ့ Function ကို လှမ်းခေါ်မယ်
            report_content = engine.export_diagnostic_report(
                other_sequence=user_dna_2)

            # Browser ကနေ ဖိုင်ကို တိုက်ရိုက် Download ဆွဲချနိုင်အောင် Response ဖန်တီးပေးတာ
            response = make_response(report_content)
            response.headers["Content-Disposition"] = "attachment; filename=genome_x_diagnostic_report.txt"
            response.headers["Content-Type"] = "text/plain"
            return response

    # 💡 [ADDED] HTML ဘက်ကို ဒေတာတွေအကုန်လုံး လှမ်းပို့ပေးဖို့ return statement ထဲမှာ ထည့်ပေးရမယ်
    # (ညီမလေးရဲ့ အောက်ဆုံး return line ကို ဒါမျိုးလေး ဖြစ်အောင် စစ်ပေးပါ)
    try:
        # database.py က function အသစ်ကို လှမ်းခေါ်တာ
        history_data = database.get_history()
    except:
        history_data = []

    return render_template("index.html",
                           action=action,
                           user_dna=user_dna,
                           result_type=result_type,
                           scan_result=scan_result,
                           is_error=is_error,
                           history=history_data)


@app.route('/export_report', methods=['POST'])
def export_report():
    # ၁။ HTML Form ဘက်က name="dna_input" ဆိုတဲ့ သေတ္တာထဲက စာသားကို တိုက်ရိုက်ဆွဲယူမယ်
    dna_seq = request.form.get('dna_input', '').strip()

    # အကယ်၍ DNA စာသား ထည့်မထားဘူးဆိုရင် Error မတက်အောင် default 'N/A' ပေးမယ်
    if not dna_seq:
        dna_seq = 'N/A'
        gc_ratio = '0.00%'
        security_status = 'Unknown'
        mutations = '0'
    else:
        # 🚀 အဓိက အဆင့် - ဒီနေရာမှာ တိုက်ရိုက် Analysis တွက်ချက်မှုကို နောက်ကွယ်ကနေ အရင်မောင်းလိုက်မယ်
        engine.load_sequence(dna_seq)
        gc_ratio = f"{engine.calculate_gc():.2f}%"
        security_status = engine.scan_security()

        # ဒုတိယ DNA သေတ္တာထဲမှာ စာသားရှိရင် Mutation ပါ တစ်ခါတည်း တွက်မယ်
        user_dna_2 = request.form.get("dna_input_2", "").strip()
        if user_dna_2:
            mutations = str(engine.calculate_hamming_distance(user_dna_2))
        else:
            mutations = '0 mutations found'

    pdf_filename = "GenomeX_Lab_Report.pdf"

    # ၂။ လတ်လတ်ဆတ်ဆတ် ရလာတဲ့ Dynamic Data တွေနဲ့ PDF ဖိုင်အသစ်စက်စက်ကို လှမ်းဆောက်မယ်
    generate_clinical_pdf(pdf_filename, dna_seq, gc_ratio,
                          security_status, mutations)

    # ၃။ အသစ်ထွက်လာတဲ့ PDF ကို အသုံးပြုသူဆီ တန်းပြီး ဒေါင်းလုဒ် ချပေးမယ်
    return send_file(pdf_filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
