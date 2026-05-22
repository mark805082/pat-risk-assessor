import streamlit as st

st.set_page_config(page_title="PAT Risk Assessor Pro", page_icon="⚡", layout="centered")

st.title("⚡ PAT Risk Assessor Pro")
st.write("IET Code of Practice (5th Edition) Compliant Frequency Matrix")
st.markdown("---")

env = st.selectbox(
    "Step 1: Select the operational environment:",
    ["Low Risk (Office, clean shop)", 
     "Medium Risk (Schools, hotels, staff kitchens)", 
     "High Risk (Commercial kitchens, workshops, factories)", 
     "Extreme Risk (Construction sites, industrial yards)"]
)
env_scores = {"Low Risk": 1, "Medium Risk": 2, "High Risk": 4, "Extreme Risk": 6}
env_score = env_scores[env.split(" (")[0]]

handling = st.selectbox(
    "Step 2: How is the appliance handled?",
    ["Stationary (Rarely moves - e.g., PC, fridge)", 
     "Movable / Hand-held (Moved often/gripped - e.g., Kettle, Iron)"]
)
handling_score = 1 if "Stationary" in handling else 3

el_class = st.selectbox(
    "Step 3: What is the Electrical Class?",
    ["Class I (Earthed - Has metal casing/earth pin)", 
     "Class II (Double Insulated - Displays square-in-square [回] symbol)"]
)
class_score = 2 if "Class I" in el_class else 0

damage = st.selectbox(
    "Step 4: Is there a known history of damage?",
    ["No, it is well looked after.", 
     "Yes, it experiences heavy usage or rough treatment."]
)
damage_score = 0 if "No" in damage else 2

st.markdown("---")
total_score = env_score + handling_score + class_score + damage_score
st.subheader("📋 Assessment Report Summary")

if total_score <= 3:
    st.success("### RISK LEVEL: LOW")
    st.write("**Formal Visual Inspection:** Every 24 Months")
    st.write("**Combined Testing (PAT):** Not routinely required for Class II items.")
elif total_score <= 5:
    st.warning("### RISK LEVEL: MEDIUM")
    st.write("**Recommended Initial Frequency:** Every 12 Months")
    if "Class I" in el_class:
        st.info("💡 *Note: As a Class I earthed item, stick firmly to a 12-month cycle for safety.*")
elif total_score <= 8:
    st.error("### RISK LEVEL: HIGH")
    st.write("**Recommended Initial Frequency:** Every 6 to 12 Months")
    st.write("*High-use or hand-held items in this bracket should start strictly on a 6-month test regime.*")
else:
    st.error("### RISK LEVEL: EXTREME")
    st.write("**Recommended Initial Frequency:** Every 3 Months")
    st.write("*Mandatory documented daily/weekly visual checks required on-site.*")
    
st.caption("Legal Note: Frequencies are recommendations based on initial risk verification and should be reviewed dynamically alongside historical failure rates.")
