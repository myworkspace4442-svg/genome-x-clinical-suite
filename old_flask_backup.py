
from report_generator import generate_clinical_pdf
from flask import Flask, render_template, request
from Core_Engine import GenomeXEngine
import database

app = Flask(__name__)
engine = GenomeXEngine()


@app.route("/", methods=["GET", "POST"])
def home():
    action = request.form.get("action") if request.method == "POST" else None
    user_dna = request.form.get("dna_input", "")
    result_type = "SYSTEM_READY"
    scan_result = ""
    result = ""
    is_error = False
    history_data = []

    if request.method == "POST":
        if action == "alignment":
            is_error = True
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
            database.save_history(user_dna, result_type, result)

        elif action == "export_report":
            from flask import make_response
            user_dna_2 = request.form.get("dna_input_2")
            report_content = engine.export_diagnostic_report(
                other_sequence=user_dna_2)
            response = make_response(report_content)
            response.headers["Content-Disposition"] = "attachment; filename=genome_x_diagnostic_report.txt"
            response.headers["Content-Type"] = "text/plain"
            return response

    try:
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
    dna_seq = request.form.get('dna_input', '').strip()
    if not dna_seq:
        dna_seq = 'N/A'
        gc_ratio = '0.00%'
        security_status = 'Unknown'
        mutations = '0'
    else:
        engine.load_sequence(dna_seq)
        gc_ratio = f"{engine.calculate_gc():.2f}%"
        security_status = engine.scan_security()
        user_dna_2 = request.form.get("dna_input_2", "").strip()
        if user_dna_2:
            mutations = str(engine.calculate_hamming_distance(user_dna_2))
        else:
            mutations = '0 mutations found'

    pdf_filename = "GenomeX_Lab_Report.pdf"
    generate_clinical_pdf(pdf_filename, dna_seq, gc_ratio,
                          security_status, mutations)
    return send_file(pdf_filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
