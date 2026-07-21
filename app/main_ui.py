from datetime import datetime
import importlib  # 👈 Formatter ကို ဉာဏ်ဆင်ဖို့ ဒါလေးလိုပါတယ်
import os
import streamlit as st
import sys
import pandas as pd

# ၁။ Runtime Paths တွေကို အရင်သတ်မှတ်မယ် (ဒါကို Formatter က မရွှေ့ပါဘူး)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# ၂။ 💥 Formatter တွေ လုံးဝ မရွှေ့နိုင်အောင် အသွင်ပြောင်းပြီး Import လုပ်နည်း
try:
    core_module = importlib.import_module("engine.core_engine")
except ModuleNotFoundError:
    core_module = importlib.import_module("app.engine.core_engine")

# 🚀 Engine ကို ခေါ်ယူအသုံးပြုခြင်း
GenomeXEngine = core_module.GenomeXEngine

# 🏢 Web App Layout အကျယ်ကို Wide Mode သတ်မှတ်ခြင်း
st.set_page_config(page_title="Genome-X Clinical Suite Pro",
                   page_icon="🧬", layout="wide")

# 🧠 ၃။ SESSION STATE INITIALIZATION (Rerun ဖြစ်ရင် ဒေတာမပျောက်အောင် ထိန်းခြင်း)
if "scan_status" not in st.session_state:
    st.session_state.scan_status = "🟢 Standing By..."
if "action_type" not in st.session_state:
    st.session_state.action_type = "SYSTEM_READY"
if "is_threat" not in st.session_state:
    st.session_state.is_threat = False

# 🎨 ၄။ ADVANCED CSS (Streamlit core element တွေကိုပါ Animation ထည့်ခြင်း)
st.markdown("""
<style>
    @keyframes pulse-red {
        0% { background-color: rgba(248, 81, 73, 0.02); border-color: rgba(248, 81, 73, 0.4); }
        50% { background-color: rgba(248, 81, 73, 0.12); border-color: rgba(248, 81, 73, 1.0); }
        100% { background-color: rgba(248, 81, 73, 0.02); border-color: rgba(248, 81, 73, 0.4); }
    }
    /* Streamlit Container ကို Threat ဖြစ်တဲ့အခါ ကပ်တွယ်မယ့် Class */
    .element-container:has(.threat-active) + div, 
    [data-testid="stVerticalBlock"]:has(.threat-active) {
        animation: pulse-red 2s infinite;
        border: 2px solid #f85149 !important;
        padding: 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(248, 81, 73, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Engine Instance ဆောက်ခြင်း
try:
    engine = GenomeXEngine()
except Exception as e:
    engine = None

# 🛠️ ၅။ SIDEBAR TOOLS
with st.sidebar:
    st.title("🧬 Genome-X Pro")
    st.subheader("Input DNA Sequence (Target)")

    # Input Box
    raw_dna = st.text_area("Enter ATGC sequence...",
                           value="ATGCGTACGTTAGC", height=150)

    # Live Input Validation (Python Optimization)
    cleaned_dna = "".join([char for char in raw_dna.upper() if char in "ATGC"])

    # Action Buttons
    bio_scan_btn = st.button(
        "⚡ Run Bio-Scan", type="primary", use_container_width=True)
    st.markdown("---")
    export_btn = st.button("🖨️ Export Lab Report", use_container_width=True)

# 🖨️ ၆။ WORKSPACE REPORT VIEWER
st.header("Genome-X Clinical Diagnostic Report")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"System Time: {current_time} | Status: Active Suite")
st.markdown("---")


# ==========================================
# 💊 Antimicrobial Resistance (AMR) Report Section
# ==========================================
st.markdown("---")
st.subheader("💊 Antimicrobial Resistance (AMR) Findings")

amr_file_path = "amr_results.txt"

if os.path.exists(amr_file_path):
    try:
        # amr_results.txt ကို ဖတ်ယူခြင်း
        amr_df = pd.read_csv(amr_file_path, sep="\t", header=None, names=[
                             "AMR Gene", "Mapped Reads"])

        # Mapped reads > 0 ရှိသော တကယ့် ဆေးယဉ်ပါး ဗီဇများကို စစ်ထုတ်ခြင်း
        detected_amr = amr_df[amr_df["Mapped Reads"] > 0]

        if not detected_amr.empty:
            st.error("⚠️ High Risk: Antibiotic Resistance Gene(s) Detected!")
            st.dataframe(detected_amr, use_container_width=True)
        else:
            st.success("🟢 No Antimicrobial Resistance Genes Detected.")
    except Exception as e:
        st.info("Waiting for pipeline output processing...")
else:
    st.info("💡 Run BWA pipeline to view AMR Detection Results.")
st.title("🧬 Genome-X AMR Analysis Result")

amr_file = "amr_results.txt"

if os.path.exists(amr_file):
    # Data ဖတ်ယူခြင်း
    df = pd.read_csv(amr_file, sep="\t", header=None, names=[
                     "AMR_Gene_Header", "Mapped_Reads"])

    if not df.empty:
        st.success("🎯 Antibiotic Resistance Genes Detected!")

        # Streamlit Table အဖြစ် လှပစွာ ပြသခြင်း
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No Resistant Genes Detected.")
else:
    st.warning("Waiting for FASTQ/FASTA file input...")
# ⚡ SCAN BUTTON LOGIC (ဒေတာတွေကို Session State ထဲ သိမ်းမယ်)
if bio_scan_btn:
    st.session_state.action_type = "Bio-Security Scan"

    if engine:
        try:
            scan_result = engine.scan_security()
        except AttributeError:
            scan_result = "Warning: Unverified Foreign Element Detected"
    else:
        # Core Engine မရှိသေးပါက Demo ပြရန်
        scan_result = "Warning: Unverified Foreign Element Detected"

    if "Warning" in scan_result or "Danger" in scan_result:
        st.session_state.scan_status = f"⚠️ Danger: {scan_result}"
        st.session_state.is_threat = True
    else:
        st.session_state.scan_status = f"✅ Clean: {scan_result}"
        st.session_state.is_threat = False

    def display_amr_results(amr_data):
        st.subheader("💊 Antimicrobial Resistance (AMR) Analysis")

    # Sample Output Data Format
    df = pd.DataFrame([
        {"Gene / Mutation": "rpoB (S531L)", "Drug Class": "Rifamycins",
         "Resistant Drug": "Rifampicin", "Status": "RESISTANT 🔴"},
        {"Gene / Mutation": "katG (S315T)", "Drug Class": "Isonicotinamides",
         "Resistant Drug": "Isoniazid", "Status": "RESISTANT 🔴"},
        {"Gene / Mutation": "embB (M306V)", "Drug Class": "Ethambutol",
         "Resistant Drug": "Ethambutol", "Status": "SUSCEPTIBLE 🟢"}
    ])

    st.dataframe(df, use_container_width=True)
# 🎛️ ၇။ DYNAMIC REPORT CONTAINER INTERFACE
report_box = st.container()

with report_box:
    # Danger ဖြစ်ခဲ့ရင် Custom CSS Trigger လုပ်ဖို့ HTML anchor တစ်ခုချန်ခဲ့မယ်
    if st.session_state.is_threat:
        st.markdown('<div class="threat-active"></div>',
                    unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Current Action Executed",
                  value=st.session_state.action_type)
        st.markdown(f"**Bio-Security Status:** {st.session_state.scan_status}")

    with col2:
        mutation_text = "1 mutations found" if st.session_state.is_threat else "0 mutations found"
        st.metric(label="Mutation Distance (Hamming)", value=mutation_text)

    st.markdown("---")
    st.subheader("Processed DNA Sequence Target")

    if cleaned_dna:
        st.code(cleaned_dna, language="dna")
    else:
        st.info("No DNA sequence loaded.")

# 🖨️ EXPORT REPORT LOGIC (Rerun ဖြစ်သွားလည်း အပေါ်က Result တွေ မပျောက်တော့ပါ)
if export_btn:
    st.toast("Generating PDF Clinical Report... 🖨️")
    # TODO: နောက်ပရောဂျက်အဆင့်များတွင် PDF Generation Engine နှင့် ချိတ်ဆက်ရန်
