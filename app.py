from flask import send_file  # send_file မရှိသေးရင် flask import ထဲမှာ ထည့်ပါ
from report_generator import generate_clinical_pdf


from flask import Flask, render_template, request
from Core_Engine import GenomeXEngine
# 🧹 လိုအပ်တဲ့ function များကို သေသေချာချာ import လုပ်ထားပါတယ်
from database import save_history, get_history, clear_all_history, delete_history_by_id

app = Flask(__name__)
engine = GenomeXEngine()


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    is_error = False
    result_type = None

    if request.method == "POST":
        user_dna = request.form.get("dna_input")
        action = request.form.get("action")

        # 🧹 ၁။ မှတ်တမ်းအားလုံး ပြောင်ရှင်းပစ်ခြင်း
        if action == "clear_logs":
            clear_all_history()
            result = "🧹 All diagnostic history logs have been cleared successfully."
            is_error = False

        # ❌ ၂။ ရွေးချယ်ထားသော အတန်းတစ်ခုတည်းကို ကွက်ဖျက်ခြင်း
        elif action == "delete_row":
            target_id = request.form.get("row_id")
            delete_history_by_id(target_id)
            result = "❌ Selected history log has been removed."
            is_error = False

        # 🧬 DNA စစ်ဆေးခြင်း နှင့် Report ထုတ်ခြင်း (DNA Box ထဲက စာသား လိုအပ်သော အပိုင်းများ)
        else:
            engine.load_sequence(user_dna)

            # 📊 (က) GC Content တွက်ခြင်း
            if action == "gc_content":
                result_type = "GC Content Analysis"
                calculated_gc = engine.calculate_gc()
                if type(calculated_gc) == float:
                    result = f"🧬 GC Ratio = {calculated_gc:.2f}%"
                    is_error = False
                else:
                    result = calculated_gc
                    is_error = True
                # 💾 တွက်ချက်မှု အောင်မြင်မှ ဒေတာဘေ့စ်ထဲ သိမ်းမည်
                save_history(user_dna, result_type, result)

            # 🛡️ (ခ) Bio-Security Scan ဖတ်ခြင်း
            elif action == "bio_scan":
                result_type = "Bio-Security Scan"
                scan_result = engine.scan_security()
                if "Warning" in scan_result:
                    result = scan_result
                    is_error = True
                else:
                    result = scan_result
                    is_error = False
                # 💾 စကင်ဖတ်မှု ရလဒ်ကို ဒေတာဘေ့စ်ထဲ သိမ်းမည်
                save_history(user_dna, result_type, result)

            # 📥 (ဂ) Lab Report စာသားဖိုင် ထုတ်ယူခြင်း (ဒုတိယ DNA လက်ခံရန် အချောသပ်လိုက်ပါပြီ)
            elif action == "export_report":
                from flask import make_response  # ဖိုင်ထုတ်ပေးရန် Flask ရဲ့ library ကို သုံးပါမယ်

                user_dna_2 = request.form.get("dna_input_2")
                report_content = engine.export_diagnostic_report(
                    other_sequence=user_dna_2)

                # 📄 တကယ့် စာသားဖိုင် (Text File) တစ်ခု ဖန်တီးလိုက်ခြင်း
                response = make_response(report_content)
                response.headers["Content-Disposition"] = "attachment; filename=genome_diagnostic_report.txt"
                response.headers["Content-Type"] = "text/plain"

                return response
                # Note: Report ထုတ်တာကို database ထဲ မှတ်တမ်းအသစ်အနေနဲ့ ထပ်မသိမ်းတော့ပါ

    # 🔄 နောက်ဆုံးပေါ် သမိုင်းကြောင်းကို ဆွဲထုတ်ပြီး ဇယားကွက်ပြရန် ပို့ပေးခြင်း
# 🔄 နောက်ဆုံးပေါ် သမိုင်းကြောင်းကို ဒေတာဘေ့စ်ကနေ သန့်သန့်ရှင်းရှင်း ဆွဲထုတ်မယ်
    db_history = get_history()  # ဒေတာဘေ့စ်ထဲက စာရင်းကို ယူတယ်

    # ဒေတာတွေ ပုံစံမှန်အောင် Clean တဲ့ အဆင့်ပါ
    clean_history = []
    for row in db_history:
        clean_history.append(list(row))

    return render_template("index.html", calculation_result=result, is_error=is_error, history_list=clean_history)


if __name__ == "__main__":
    app.run(debug=True)


@app.route('/export_report', methods=['POST'])
def export_report():
    # ၁။ လက်ရှိ ဓာတ်ခွဲခန်းထဲမှာ စစ်ဆေးထားတဲ့ ရလဒ်တွေကို Form ထဲကနေ လှမ်းယူမယ်
    dna_seq = request.form.get('dna_sequence', 'N/A')
    gc_ratio = request.form.get('gc_ratio', '0.00%')
    security_status = request.form.get('security_status', 'Unknown')
    mutations = request.form.get('mutations', '0')

    pdf_filename = "GenomeX_Lab_Report.pdf"

    # ၂။ PDF ထုတ်ပေးမယ့် Function ကို လှမ်းခေါ်မယ်
    generate_clinical_pdf(pdf_filename, dna_seq, gc_ratio,
                          security_status, mutations)

    # ၃။ ထွက်လာတဲ့ PDF ဖိုင်ကို အသုံးပြုသူရဲ့ စက်ထဲကို Download ချပေးလိုက်မယ်
    return send_file(pdf_filename, as_attachment=True)
