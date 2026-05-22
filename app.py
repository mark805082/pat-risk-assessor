import streamlit as st

st.set_page_config(page_title="PAT Risk Assessor Pro", page_icon="⚡", layout="centered")

st.title("⚡ PAT Risk Assessor Pro")
st.write("IET Code of Practice (5th Edition) Compliant Frequency Matrix")
st.markdown("---")

# 1. ENVIRONMENT (Recalibrated for lower baseline office risk)
env = st.selectbox(
    "Step 1: Select the operational environment:",
    ["Low Risk (Office, clean shop)", 
     "Medium Risk (Schools, hotels, staff kitchens)", 
     "High Risk (Commercial kitchens, workshops, factories)", 
     "Extreme Risk (Construction sites, industrial yards)"]
)
env_scores = {"Low Risk": 0, "Medium Risk": 2, "High Risk": 4, "Extreme Risk": 6}
env_score = env_scores[env.split(" (")[0]]

# 2. HANDLING
handling = st.selectbox(
    "Step 2: How is the appliance handled?",
    ["Stationary (Rarely moves - e.g., PC, printer, fridge)", 
     "Movable / Hand-held (Moved often/gripped - e.g., Kettle, Iron)"]
)
handling_score = 0 if "Stationary" in handling else 3

# 3. ELECTRICAL CLASS
el_class = st.selectbox(
    "Step 3: What is the Electrical Class?",
    ["Class I (Earthed - Has metal casing/earth pin)", 
     "Class II (Double Insulated - Displays square-in-square [回] symbol)"]
)
class_score = 1 if "Class I" in el_class else 0

# 4. DAMAGE HISTORY
damage = st.selectbox(
    "Step 4: Is there a known history of damage?",
    ["No, it is well looked after.", 
     "Yes, it experiences heavy usage or rough treatment."]
)
damage_score = 0 if "No" in damage else 2

st.markdown("---")
total_score = env_score + handling_score + class_score + damage_score
st.subheader("📋 Assessment Report Summary")

# NEW RECALIBRATED LOGIC BRACKETS
if total_score <= 1:
    st.success("### RISK LEVEL: LOW")
    st.write("**Formal Visual Inspection:** Every 24 Months")
    st.write("**Combined Testing (PAT):** Every 24 to 36 Months")
    st.info("💡 *Perfect for office PCs, monitors, and stationary earthed/double-insulated equipment.*")
elif total_score <= 3:
    st.success("### RISK LEVEL: LOW-MEDIUM")
    st.write("**Formal Visual Inspection:** Every 12 Months")
    st.write("**Combined Testing (PAT):** Every 12 to 24 Months")
    if "Class II" in el_class:
        st.write("**Note:** For Class II items (like chargers) in this bracket, routine instrument testing is not required; visual checks are sufficient.")
elif total_score <= 6:
    st.warning("### RISK LEVEL: MEDIUM-HIGH")
    st.write("**Recommended Initial Frequency:** Every 12 Months")
    st.write("*Standard cycle for handheld Class I items (like kettles) or equipment in harsher environments.*")
else:
    st.error("### RISK LEVEL: HIGH / EXTREME")
    st.write("**Recommended Initial Frequency:** Every 3 to 6 Months")
    st.write("*Mandatory high-frequency testing for construction sites or heavily abused equipment.*")
    
st.caption("Legal Note: Frequencies are recommendations based on initial risk verification and should be reviewed dynamically alongside historical failure rates.")
