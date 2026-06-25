from flask import send_file  # send_file မရှိသေးရင် flask import ထဲမှာ ထည့်ပါ
from report_generator import generate_clinical_pdf


from flask import Flask, render_template, request
from Core_Engine import GenomeXEngine
# 🧹 လိုအပ်တဲ့ function များကို သေသေချာချာ import လုပ်ထားပါတယ်
import database

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
            # Use getattr to avoid static-analyzer errors if the function is not present
            clear_fn = getattr(database, "clear_all_history", None)
            if clear_fn:
                clear_fn()
                result = "🧹 All diagnostic history logs have been cleared successfully."
                is_error = False
            else:
                # try alternative common names for clearing history
                alt_clear = getattr(database, "clear_history", None) or getattr(
                    database, "delete_all_history", None)
                if alt_clear:
                    alt_clear()
                    result = "🧹 All diagnostic history logs have been cleared successfully (using fallback)."
                    is_error = False
                else:
                    result = "🧹 Clear operation not available: database module lacks a clear function."
                    is_error = True

        # ❌ ၂။ ရွေးချယ်ထားသော အတန်းတစ်ခုတည်းကို ကွက်ဖျက်ခြင်း
        elif action == "delete_row":
            target_id = request.form.get("row_id")
            # call a delete function if the database module provides one (use getattr to avoid static analyzer no-member)
            delete_fn = getattr(database, "delete_history_by_id", None)
            if not delete_fn:
                delete_fn = getattr(database, "delete_history", None)
            if delete_fn:
                delete_fn(target_id)
                result = "❌ Selected history log has been removed."
                is_error = False
            else:
                # no suitable delete function found in database module
                result = "❌ Unable to delete: delete function not implemented in database module."
                is_error = True

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
                # 💾 တွတ်ချက်မှု အောင်မြင်မှ ဒေတာဘေ့စ်ထဲ သိမ်းမည်
                database.save_history(user_dna, result_type, result)

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
                database.save_history(user_dna, result_type, result)

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
    db_history = database.get_history()  # ဒေတာဘေ့စ်ထဲက စာရင်းကို ယူတယ်

    # ဒေတာတွေ ပုံစံမှန်အောင် Clean တဲ့ အဆင့်ပါ
    clean_history = []
    for row in db_history:
        clean_history.append(list(row))

    return render_template("index.html", calculation_result=result, is_error=is_error, history_list=clean_history)


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
