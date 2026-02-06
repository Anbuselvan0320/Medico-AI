import streamlit as st
import google.generativeai as genai
import PIL.Image
import time

# --- 1. CLINICAL CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(
    page_title="MEDICO AI | Bio-Lab", 
    page_icon="🧬", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 🎨 UI THEME: ABYSSAL TEAL (ADVANCED ANIMATIONS)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* IMPORT TECH FONT */
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;600&display=swap');

    /* 1. MAIN APP BACKGROUND */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0f2027 0%, #203a43 50%, #000000 100%);
        color: #d4f1f4;
        font-family: 'Exo 2', sans-serif;
    }
    
    /* 2. INPUT FIELDS (Liquid Glass) */
    .stTextInput > div > div, 
    .stNumberInput > div > div, 
    .stSelectbox > div > div,
    .stTextArea > div > div {
        background-color: rgba(0, 40, 50, 0.4) !important;
        color: #75e6da !important;
        border: 1px solid rgba(117, 230, 218, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        color: #75e6da !important;
    }

    /* 3. FOCUS STATE (Synapse Fire Animation) */
    .stTextInput input:focus, 
    .stNumberInput input:focus, 
    .stTextArea textarea:focus, 
    .stSelectbox > div[data-baseweb="select"] > div:focus-within {
        border-color: #00d2ff !important; 
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.4) !important;
        background-color: rgba(0, 60, 70, 0.6) !important;
        animation: pulse-input 2s infinite;
    }

    @keyframes pulse-input {
        0% { box-shadow: 0 0 15px rgba(0, 210, 255, 0.3); }
        50% { box-shadow: 0 0 25px rgba(0, 210, 255, 0.6); }
        100% { box-shadow: 0 0 15px rgba(0, 210, 255, 0.3); }
    }

    /* 4. HEADERS */
    h1, h2, h3, span[data-testid="stHeaderActionElements"] {
        background: linear-gradient(to right, #43cea2, #185a9d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        text-shadow: 0 0 30px rgba(67, 206, 162, 0.2);
    }

    /* 5. SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: rgba(5, 20, 25, 0.85);
        border-right: 1px solid rgba(117, 230, 218, 0.1);
        backdrop-filter: blur(20px);
    }

    /* 6. DASHBOARD CARDS (Breathing Animation) */
    div[data-testid="stHorizontalBlock"] > div > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: rgba(5, 30, 40, 0.4);
        border: 1px solid rgba(117, 230, 218, 0.1);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        height: 100% !important; 
        min-height: 280px;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        
        /* Subtle Breathing Glow */
        animation: breathe 4s ease-in-out infinite;
    }

    @keyframes breathe {
        0% { border-color: rgba(117, 230, 218, 0.1); }
        50% { border-color: rgba(117, 230, 218, 0.3); box-shadow: 0 0 15px rgba(67, 206, 162, 0.1); }
        100% { border-color: rgba(117, 230, 218, 0.1); }
    }
    
    div[data-testid="stHorizontalBlock"] > div > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"]:hover {
        transform: translateY(-8px) scale(1.01);
        background-color: rgba(5, 40, 50, 0.7);
        border-color: #43cea2;
        box-shadow: 0 0 30px rgba(67, 206, 162, 0.3);
        animation: none; /* Stop breathing on hover to focus */
    }

    div[data-testid="stVerticalBlock"] h4 {
        margin-bottom: 15px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #75e6da !important;
        min-height: 2.4em;
    }

    div[data-testid="stVerticalBlock"] div[data-testid="stMarkdown"] p {
        color: #a4b0be !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        margin-bottom: auto !important;
        flex-grow: 1;
    }

    /* 7. HOLOGRAPHIC TABLES */
    div[data-testid="stMarkdown"] table {
        width: 100% !important;
        background-color: rgba(0, 20, 30, 0.5) !important;
        border: 1px solid rgba(117, 230, 218, 0.2) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
        color: #d4f1f4 !important;
    }
    div[data-testid="stMarkdown"] thead tr th {
        background-color: rgba(67, 206, 162, 0.2) !important;
        color: #75e6da !important;
        border-bottom: 1px solid rgba(117, 230, 218, 0.3) !important;
    }
    div[data-testid="stMarkdown"] tbody tr td {
        border-bottom: 1px solid rgba(117, 230, 218, 0.05) !important;
    }
    div[data-testid="stMarkdown"] tbody tr:hover {
        background-color: rgba(67, 206, 162, 0.1) !important;
    }

    /* 8. BUTTONS (Aqua Gradients) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 12px !important; 
        height: 3.2em !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin-top: 15px !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.7) !important;
        transform: scale(1.02) !important;
        color: white !important;
    }

    /* 9. SECONDARY BUTTONS */
    div.stButton > button[kind="secondary"] {
        color: #75e6da !important;
        border: 1px solid rgba(117, 230, 218, 0.3) !important;
        background: transparent !important;
        border-radius: 12px !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: rgba(117, 230, 218, 0.1) !important;
        border-color: #00d2ff !important;
    }

    /* 10. CHAT BUBBLES */
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 40, 50, 0.4) !important;
        border: 1px solid rgba(117, 230, 218, 0.1);
        border-radius: 15px !important;
    }
    div[data-testid="stChatMessage"] [data-testid="stImage"] {
        border-radius: 50% !important; 
        border: 2px solid #00d2ff;
    }

    /* 11. PROFILE CARD (SPACING FIXED) */
    .profile-card {
        background: linear-gradient(135deg, rgba(67, 206, 162, 0.1), rgba(24, 90, 157, 0.1));
        border: 1px solid rgba(117, 230, 218, 0.15);
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        margin-bottom: 25px; /* Added spacing to push logout button down */
        text-align: center;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    /* The Scanning Line */
    .profile-card::after {
        content: "";
        position: absolute;
        top: -50%;
        left: 0;
        width: 100%;
        height: 10px;
        background: linear-gradient(90deg, transparent, rgba(0, 210, 255, 0.5), transparent);
        animation: scan 4s linear infinite;
    }
    @keyframes scan {
        0% { top: -10%; }
        100% { top: 110%; }
    }
    
    .profile-name { color: #fff; font-size: 1.2rem; font-weight: 700; margin-bottom: 5px; }
    .profile-id { color: #43cea2; font-size: 0.8rem; letter-spacing: 1px; }
    .profile-stat { color: #75e6da; font-size: 0.85rem; margin-top: 8px; opacity: 0.7; }

    /* 12. COMPACT LOGOUT BUTTON (SPACING FIXED) */
    [data-testid="stSidebar"] div.stButton:last-of-type > button {
        padding: 8px 20px !important;
        width: 100% !important;
        color: rgba(117, 230, 218, 0.8) !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        background: rgba(0, 40, 50, 0.3) !important;
        border: 1px solid rgba(117, 230, 218, 0.2) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        margin-top: 0px !important; /* Relying on card margin-bottom now */
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] div.stButton:last-of-type > button:hover {
        background: rgba(0, 210, 255, 0.1) !important;
        border-color: #00d2ff !important;
        color: #fff !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3) !important;
    }

    /* 13. ANIMATIONS FOR FEATURES */
    
    /* Sonar Ripple for Status */
    @keyframes sonar {
        0% { box-shadow: 0 0 0 0 rgba(0, 210, 255, 0.7); }
        100% { box-shadow: 0 0 0 15px rgba(0, 210, 255, 0); }
    }
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #00d2ff;
        border-radius: 50%;
        margin-right: 8px;
        animation: sonar 1.5s infinite;
    }

    /* ECG Line Animation */
    .ecg-line {
        width: 100%;
        height: 2px;
        background: rgba(117, 230, 218, 0.1);
        margin: 30px 0;
        position: relative;
        overflow: hidden;
    }
    .ecg-line::after {
        content: "";
        position: absolute;
        top: 0;
        left: -100px;
        width: 150px;
        height: 100%;
        background: linear-gradient(90deg, transparent, #43cea2, #00d2ff, transparent);
        box-shadow: 0 0 15px #43cea2;
        animation: stream 3s ease-in-out infinite;
    }
    @keyframes stream {
        0% { left: -150px; }
        100% { left: 100%; }
    }

    /* SCROLLBARS */
    ::-webkit-scrollbar { width: 8px; background: #0f2027; }
    ::-webkit-scrollbar-thumb { background: #203a43; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #43cea2; }
    </style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------------------

# 🔑 API CONFIGURATION
api_key = "AIzaSyBnnNvpIWBo4Iz-vqUX1DkmUpO7gcSj3vU"
genai.configure(api_key=api_key)

# --- 2. SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_age' not in st.session_state:
    st.session_state.user_age = 25
if 'user_gender' not in st.session_state:
    st.session_state.user_gender = "Male"
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'user_allergies' not in st.session_state:
    st.session_state.user_allergies = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- 3. CORE UTILITIES ---
def get_working_model():
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        preferences = ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        for pref in preferences:
            if pref in available_models: return pref
        return available_models[0] if available_models else "models/gemini-pro"
    except:
        return "models/gemini-pro"

def go_home():
    st.session_state.page = 'home'

def logout():
    st.session_state.logged_in = False
    st.session_state.page = 'home'
    st.session_state.chat_history = [] 
    st.rerun()

# --- 4. LOGIN PORTAL ---
def show_login_page():
    st.markdown("# 🏥 MEDICO")
    st.markdown("### Clinical Intelligence System")
    st.caption("Secured Health Information Exchange Portal")
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container(border=True):
            st.markdown("#### 📝 PATIENT REGISTRATION")
            st.divider()
            with st.form("hospital_login"):
                name = st.text_input("FULL NAME", placeholder="Last Name, First Name")
                
                c_age, c_gen = st.columns(2)
                with c_age:
                    age = st.number_input("AGE *", min_value=0, max_value=120, value=st.session_state.user_age)
                with c_gen:
                    gender = st.selectbox("GENDER", ["Male", "Female", "Other"], index=0)
                
                c_code, c_phone = st.columns([1, 2])
                with c_code:
                    country_code = st.selectbox("CODE", ["+91", "+1", "+44", "+81"])
                with c_phone:
                    phone = st.text_input("CONTACT NUMBER *", max_chars=10, placeholder="10-digit mobile")
                
                allergies = st.text_input("KNOWN ALLERGIES", placeholder="e.g. Penicillin, Peanuts, Sulfa")
                
                st.write("")
                submit = st.form_submit_button("🚀 AUTHORIZE LOGIN", type="primary", use_container_width=True)

            if submit:
                if not name or len(phone) != 10 or not phone.isdigit():
                    st.error("ACCESS DENIED: Ensure name is provided and contact number is exactly 10 digits.")
                else:
                    st.session_state.user_name = name
                    st.session_state.user_age = age
                    st.session_state.user_gender = gender
                    st.session_state.user_allergies = allergies
                    st.session_state.logged_in = True
                    st.rerun()

# --- 5. CLINICAL FAQ ---
def show_clinical_faq():
    with st.sidebar.expander("❓ Clinical FAQ"):
        st.markdown("**1. Is this a real doctor?**")
        st.caption("No. This is an AI assistant. Always verify prescriptions with a licensed MD.")
        st.markdown("**2. What are 'Red Flags'?**")
        st.caption("Symptoms like chest pain or difficulty breathing that require immediate ER care.")

# --- 6. DASHBOARD (RE-ARRANGED & UNIFIED) ---
def show_home():
    st.markdown("## CLINICAL DASHBOARD")
    # UPDATED STATUS BADGE WITH SONAR RIPPLE
    st.markdown(f"""
    **Patient:** {st.session_state.user_name} | 
    <span style='background:rgba(0, 40, 50, 0.6); color:#75e6da; padding:4px 12px; border:1px solid #43cea2; border-radius:20px; font-weight:bold; display:inline-flex; align-items:center;'>
        <span class="status-dot"></span> Bio-Link Active
    </span>
    """, unsafe_allow_html=True)
    
    # 🌟 COSMIC STREAM ANIMATION
    st.markdown('<div class="ecg-line"></div>', unsafe_allow_html=True)
    st.write("")
    
    # ROW 1: DIAGNOSIS & ACTION
    col1, col2, col3, col4 = st.columns(4)
    
    # 1. Symptom Analyzer
    with col1:
        with st.container(border=True):
            st.markdown("""<h4 style="color: #00d2ff; margin:0;">🩺 SYMPTOM ANALYZER</h4>""", unsafe_allow_html=True)
            st.markdown("""<p>AI-powered diagnostic support & red-flag triage.</p>""", unsafe_allow_html=True)
            if st.button("Open Analyzer", key="btn_sym", type="primary", use_container_width=True):
                st.session_state.page = 'symptom_checker'
                st.rerun()

    # 2. Report Analyzer
    with col2:
        with st.container(border=True):
            st.markdown("""<h4 style="color: #43cea2; margin:0;">📄 REPORT ANALYZER</h4>""", unsafe_allow_html=True)
            st.markdown("""<p>Clinical OCR scanning for lab & radiology records.</p>""", unsafe_allow_html=True)
            if st.button("Open Lab Portal", key="btn_rep", type="primary", use_container_width=True):
                st.session_state.page = 'report_analyzer'
                st.rerun()

    # 3. Dosage Calculator
    with col3:
        with st.container(border=True):
            st.markdown("""<h4 style="color: #75e6da; margin:0;">💊 DOSAGE CALCULATOR</h4>""", unsafe_allow_html=True)
            st.markdown("""<p>Precision titration & allergy conflict safety checks.</p>""", unsafe_allow_html=True)
            if st.button("Open Calculator", key="btn_dos", type="primary", use_container_width=True):
                st.session_state.page = 'dosage_calculator'
                st.rerun()

    # 4. Interactions (DRUG-FOOD)
    with col4:
        with st.container(border=True):
            st.markdown("""<h4 style="color: #185a9d; margin:0;">🥦 DRUG-FOOD INTERACTION</h4>""", unsafe_allow_html=True)
            st.markdown("""<p>Check interactions between medicines and foods.</p>""", unsafe_allow_html=True)
            if st.button("Check Safety", key="btn_inter", type="primary", use_container_width=True):
                st.session_state.page = 'interaction_checker'
                st.rerun()

    st.write("") 

    # ROW 2: REFERENCE & SUPPORT
    st.markdown("#### 🧬 REFERENCE & SUPPORT")
    c_u1, c_u2, c_u3, c_u4 = st.columns(4)
    
    # 5. Mental Care
    with c_u1:
        with st.container(border=True):
            st.markdown("""<h4 style="color: #75e6da; font-size: 16px;">🧠 PSYCHOLOGICAL SUPPORT</h4>""", unsafe_allow_html=True)
            st.markdown("""<p>Cognitive triage & emotional care.</p>""", unsafe_allow_html=True)
            if st.button("Open Support", key="btn_mental", type="primary", use_container_width=True):
                st.session_state.page = 'mental_wellness'
                st.rerun()

    # 6. Pharma Guide
    with c_u2:
        with st.container(border=True):
            st.markdown("""<h4 style="color: #75e6da; font-size: 16px;">ℹ️ PHARMACOPOEIA</h4>""", unsafe_allow_html=True)
            st.markdown("""<p>Comprehensive database for drug safety & info.</p>""", unsafe_allow_html=True)
            if st.button("Open Med Guide", key="btn_med", type="primary", use_container_width=True):
                st.session_state.page = 'medicine_guide'
                st.rerun()

    # 7. Procedure Explainer
    with c_u3:
        with st.container(border=True):
            st.markdown("""<h4 style="color: #75e6da; font-size: 16px;">🩺 SURGICAL & PROCEDURE</h4>""", unsafe_allow_html=True)
            st.markdown("""<p>Understand surgeries, prep & recovery.</p>""", unsafe_allow_html=True)
            if st.button("Explain Procedure", key="btn_proc", type="primary", use_container_width=True):
                st.session_state.page = 'procedure_explainer'
                st.rerun()

    # 8. Jargon Decoder
    with c_u4:
        with st.container(border=True):
            st.markdown("""<h4 style="color: #75e6da; font-size: 16px;">📖 JARGON DECODER</h4>""", unsafe_allow_html=True)
            st.markdown("""<p>Translate medical terms to plain English.</p>""", unsafe_allow_html=True)
            if st.button("Open Translator", key="btn_trans", type="primary", use_container_width=True):
                st.session_state.page = 'jargon_decoder'
                st.rerun()

# --- 7. CORE MODULES ---

def show_symptom_checker():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("🏥 Symptom Checker & Red-Flag Triage")
    st.warning("⚠️ Disclaimer: This is an AI tool. Always consult a doctor for serious conditions.")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", value=st.session_state.user_age)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.user_gender))
    with col2:
        allergies = st.text_input("Allergies", value=st.session_state.user_allergies, placeholder="e.g. Penicillin")
        conditions = st.text_input("Chronic Conditions", placeholder="e.g. Diabetes, Hypertension")

    st.markdown("### Describe Symptoms")
    symptoms = st.text_area("What are you feeling?", height=100, placeholder="e.g. Crushing chest pain radiating to left arm...")

    c3, c4 = st.columns(2)
    with c3:
        duration = st.selectbox("Duration", ["< 24 hours", "1-3 days", "> 1 week"])
    with c4:
        severity = st.select_slider("Clinical Severity", options=["Very Mild", "Mild", "Moderate", "Severe", "Critical"], value="Moderate")

    if st.button("Initiate Clinical Triage", type="primary", use_container_width=True):
        if not symptoms: st.error("Please describe your symptoms.")
        else:
            try:
                model = genai.GenerativeModel(get_working_model())
                prompt = f"Act as a Triage Nurse. Patient: {age}yo {gender}. Symptoms: {symptoms} ({severity}, {duration}). History: {conditions}. Allergies: {allergies}. PROTOCOL: Check for Red Flags (Emergency). If found, start with '🚨 EMERGENCY RED FLAG WARNING'. Give DDx table and OTC advice if safe."
                with st.spinner("Analyzing Clinical Data..."):
                    response = model.generate_content(prompt)
                    if "EMERGENCY" in response.text.upper(): st.error("POTENTIAL CRITICAL CONDITION DETECTED")
                    st.markdown(response.text)
            except Exception as e: st.error(f"Error: {e}")

def show_dosage_calculator():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("💊 Precision Dosage Titration")
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("1. Patient")
        age = st.number_input("Age", value=st.session_state.user_age)
        weight = st.number_input("Weight (kg)", value=70.0)
    with c2:
        st.subheader("2. Medicine")
        drug = st.text_input("Agent Name", placeholder="e.g. Paracetamol / Acetaminophen")
        cv, cu = st.columns([2, 1])
        with cv: val = st.text_input("Strength", placeholder="e.g. 500")
        with cu: unit = st.selectbox("Unit", ["mg", "ml", "mcg", "g"])
    with c3:
        st.subheader("3. Condition")
        cond = st.text_input("Indication", placeholder="e.g. Post-operative pain")
        sev = st.select_slider("Clinical Severity", options=["Very Mild", "Mild", "Moderate", "Severe", "Critical"], value="Moderate")

    if st.button("Calculate Protocol", type="primary", use_container_width=True):
        if not drug or not val: st.error("Missing Data: Please enter Drug Name and Strength.")
        else:
            if st.session_state.user_allergies and drug.lower() in st.session_state.user_allergies.lower():
                st.error(f"🚨 ALLERGY CONFLICT: {drug} detected in your allergy profile!")
            with st.spinner("Calculating..."):
                model = genai.GenerativeModel(get_working_model())
                res = model.generate_content(f"Dosage for {age}yo, {weight}kg. Drug: {drug} {val}{unit} for {cond}. Severity: {sev}.")
                st.markdown("### 📋 Clinical Protocol")
                st.markdown(res.text)

def show_medicine_guide():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("ℹ️ AI Drug Guide")
    st.info("Identify uses, mechanisms, and safety warnings for pharmacological agents.")
    col1, col2 = st.columns(2)
    with col1: medicine_name = st.text_input("Enter Medicine Name", placeholder="e.g. Amoxicillin")
    with col2: my_allergies = st.text_input("Verify Allergies", value=st.session_state.user_allergies, placeholder="e.g. None")
    if st.button("Get Medicine Info", type="primary", use_container_width=True):
        if not medicine_name: st.error("Please enter a medicine name.")
        else:
            try:
                model = genai.GenerativeModel(get_working_model())
                with st.spinner("Searching..."):
                    result = model.generate_content(f"Pharmacist info for '{medicine_name}'. Allergies: '{my_allergies}'. Provide Uses, Mechanism, Side Effects, and Allergy Warnings.")
                    st.markdown("### 📋 Medicine Details")
                    st.markdown(result.text)
            except Exception as e: st.error(f"Error: {e}")

def show_report_analyzer():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("📄 Clinical Report Analysis")
    uploaded_file = st.file_uploader("Upload Lab Report", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = PIL.Image.open(uploaded_file)
        st.image(image, width=400)
        if st.button("Analyze Report", type="primary", use_container_width=True):
            try:
                model = genai.GenerativeModel(get_working_model())
                res = model.generate_content(["Interpret lab values professionally. Highlight abnormalities. No prescriptions.", image])
                st.markdown("### 🧬 Lab Interpretation")
                st.markdown(res.text)
            except Exception as e: st.error(f"Error: {e}")

def show_mental_wellness():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("🧠 Psychological Support Portal")
    st.info("Clinical-grade cognitive & emotional triage.")
    mood = st.select_slider("Current Emotional Baseline", options=["Distressed", "Anxious", "Neutral", "Stable", "Optimistic"])
    user_input = st.text_area("Clinical Notes / Subjective Feeling", placeholder="Describe current cognitive state or stressors...")
    if st.button("Initiate Consultation", type="primary", use_container_width=True):
        if not user_input: st.error("Please provide subjective notes.")
        else:
            try:
                model = genai.GenerativeModel(get_working_model())
                res = model.generate_content(f"Act as an empathetic clinical psychologist. User Mood: {mood}. Notes: {user_input}. Provide supportive clinical feedback and 1 evidence-based coping mechanism.")
                st.markdown("### 📋 Clinical Guidance")
                st.markdown(res.text)
            except Exception as e: st.error(f"Error: {e}")

def show_interaction_checker():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("⚔️ Drug–Food Interaction Checker")
    st.warning("⚠️ For informational purposes only. Consult a pharmacist.")
    c1, c2 = st.columns(2)
    with c1: drug1 = st.text_input("Medication Name", placeholder="e.g. Warfarin")
    with c2: food = st.text_input("Food / Beverage", placeholder="e.g. Grapefruit Juice")
    if st.button("Analyze Interaction", type="primary", use_container_width=True):
        if not drug1 or not food: st.error("Please enter both medicine and food item.")
        else:
            try:
                model = genai.GenerativeModel(get_working_model())
                res = model.generate_content(f"Act as a clinical pharmacist. Drug: {drug1}. Food: {food}. Provide: 1. Interaction severity. 2. Explanation. 3. Clinical recommendation.")
                st.markdown("### 🧬 Interaction Report")
                st.markdown(res.text)
            except Exception as e: st.error(f"Error: {e}")

def show_jargon_decoder():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("📖 Medical Jargon Decoder")
    term = st.text_input("Enter Medical Term or Phrase", placeholder="e.g. 'Idiopathic thrombocytopenia' or 'Prophylactic use'")
    if st.button("Translate to Plain English", type="primary", use_container_width=True):
        if not term: st.error("Please enter a term.")
        else:
            try:
                model = genai.GenerativeModel(get_working_model())
                res = model.generate_content(f"Translate this medical term to plain English for a patient: '{term}'. Explain what it means simply.")
                st.markdown("### 🗣️ Plain English Definition")
                st.markdown(res.text)
            except Exception as e: st.error(f"Error: {e}")

def show_procedure_explainer():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("🩺 Surgical & Procedure Explainer")
    st.info("Simple explanations for complex medical procedures.")
    procedure = st.text_input("Enter Procedure Name", placeholder="e.g. Laparoscopic Cholecystectomy, Root Canal, Endoscopy")
    if st.button("Explain Procedure", type="primary", use_container_width=True):
        if not procedure: st.error("Please enter a procedure name.")
        else:
            try:
                model = genai.GenerativeModel(get_working_model())
                res = model.generate_content(f"Explain the medical procedure '{procedure}' to a patient in simple, comforting language. Structure: 1. What is it? 2. How to Prepare? 3. Recovery? 4. Red flags.")
                st.markdown("### 📋 Procedure Guide")
                st.markdown(res.text)
            except Exception as e: st.error(f"Error: {e}")

# --- AI CHAT ASSISTANT MODULE ---
def show_ai_chat():
    st.button("← RETURN TO DASHBOARD", on_click=go_home, type="secondary")
    st.title("🤖 Medico AI Health Assistant")
    st.caption("Ask general health questions, clarify medical terms, or get wellness tips.")
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Ask Medico..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        try:
            model = genai.GenerativeModel(get_working_model())
            full_prompt = f"Act as a helpful medical assistant. You are speaking to {st.session_state.user_name}. User asks: {prompt}. Keep answers professional, concise, and safe. Always advise consulting a real doctor for serious issues."
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = model.generate_content(full_prompt)
                    st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e: st.error(f"Error: {e}")

# --- 8. MAIN ROUTER ---
if not st.session_state.logged_in:
    show_login_page()
else:
    with st.sidebar:
        # SMART DASHBOARD BUTTON
        if st.session_state.page != 'home':
            if st.button("🏠 DASHBOARD", use_container_width=True, type="primary"):
                st.session_state.page = 'home'
                st.rerun()
            
        st.title("MEDICO AI")
        st.divider()
        
        st.markdown("### 🤖 Assistant")
        if st.button("🤖 AI Health Assistant", use_container_width=True):
            st.session_state.page = 'ai_chat'
            st.rerun()

        st.divider()
        show_clinical_faq()
        
        st.markdown("---")
        
        st.markdown(f"""
            <div class="profile-card">
                <p class="profile-name">{st.session_state.user_name}</p>
                <p class="profile-id">ID: MED-{st.session_state.user_age}X99</p>
                <p class="profile-stat"><strong>Age:</strong> {st.session_state.user_age} | <strong>Gender:</strong> {st.session_state.user_gender}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user_allergies: st.warning(f"Allergies: {st.session_state.user_allergies}")
        
        # 🚀 GLASS PILL LOGOUT BUTTON
        if st.button("Logout", use_container_width=True, type="secondary", help="Securely end your session"): 
            logout()

    # Routing
    if st.session_state.page == 'home': show_home()
    elif st.session_state.page == 'symptom_checker': show_symptom_checker()
    elif st.session_state.page == 'report_analyzer': show_report_analyzer()
    elif st.session_state.page == 'dosage_calculator': show_dosage_calculator()
    elif st.session_state.page == 'medicine_guide': show_medicine_guide()
    elif st.session_state.page == 'mental_wellness': show_mental_wellness()
    elif st.session_state.page == 'interaction_checker': show_interaction_checker()
    elif st.session_state.page == 'jargon_decoder': show_jargon_decoder()
    elif st.session_state.page == 'procedure_explainer': show_procedure_explainer()
    elif st.session_state.page == 'ai_chat': show_ai_chat()
