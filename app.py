from flask import Flask, render_template, request
from Core_Engine import GenomeXEngine
from database import save_history, get_history

app = Flask(__name__)
engine = GenomeXEngine()


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    is_error = False
    result_type = None

    if request.method == "POST":
        user_dna = request.form.get("dna_input")
        # ဘယ်ခလုတ်ကို နှိပ်လိုက်လဲဆိုတာ ဖမ်းတာ
        action = request.form.get("action")

        engine.load_sequence(user_dna)

        # ၁။ တကယ်လို့ GC Content တွက်တဲ့ ခလုတ်ကို နှိပ်ခဲ့ရင်
        if action == "gc_content":
            result_type = "GC Content Analysis"
            calculated_gc = engine.calculate_gc()
            if type(calculated_gc) == float:
                result = f"🧬 GC Ratio = {calculated_gc:.2f}%"
                is_error = False
            else:
                result = calculated_gc
                is_error = True

        # ၂။ တကယ်လို့ Bio-Security Scan ဖတ်တဲ့ ခလုတ်ကို နှိပ်ခဲ့ရင်
        elif action == "bio_scan":
            result_type = "Bio-Security Scan"
            scan_result = engine.scan_security()
            if "Warning" in scan_result:
                result = scan_result
                is_error = True  # Warning ဖြစ်လို့ အနီရောင် Box နဲ့ ပြမယ်
            else:
                result = scan_result
                is_error = False  # Safe ဖြစ်ရင် သာမန် Box နဲ့ ပြမယ်

        # 💾 ဘာပဲလုပ်လုပ် ရလဒ်ကို ဒေတာဘေ့စ်ထဲ လှမ်းသိမ်းမယ်
        save_history(user_dna, result_type, result)

    db_history = get_history()
    db_history = [list(row) for row in db_history]
    return render_template("index.html", calculation_result=result, is_error=is_error, history_list=db_history)


if __name__ == "__main__":
    app.run(debug=True)
