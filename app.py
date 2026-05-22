import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="PAT Risk Assessor Pro", page_icon="⚡", layout="centered")

st.title("⚡ PAT Risk Assessor Pro")
st.write("IET Code of Practice (5th Edition) Compliant Frequency Matrix")
st.markdown("---")

# FEATURE 1: Client and Asset Logging Inputs
st.subheader("📁 Job Identification")
col1, col2 = st.columns(2)

with col1:
    client_name = st.text_input("Client / Business Name:", placeholder="e.g., Acme Corp")

with col2:
    asset_id = st.text_input("Appliance ID / Asset Tag:", placeholder="e.g., ASSET-001")

st.markdown("---")

# FEATURE 3: Cables & Extension Leads Toggle
is_cable = st.checkbox("🔌 Is this an extension lead or a detachable mains cable?", 
                       help="Extension leads and trailing cables face significantly higher mechanical stress and wear.")

# 1. ENVIRONMENT 
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
     "Class II (Double Insulated - Displays double-square symbol)"]
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

# Calculate totals
cable_modifier = 2 if is_cable else 0
total_score = env_score + handling_score + class_score + damage_score + cable_modifier

st.subheader("📋 Assessment Report Summary")

if client_name or asset_id:
    st.markdown(f"**Client:** {client_name if client_name else 'N/A'} | **Asset:** {asset_id if asset_id else 'N/A'}")

# Setup evaluation conditions & descriptions
risk_level = ""
visual_freq = ""
test_freq = ""
notes = ""

if total_score <= 1:
    risk_level = "LOW"
    visual_freq = "Every 24 Months"
    test_freq = "Every 24 to 36 Months"
    notes = "Perfect for office PCs, monitors, and stationary equipment."
    st.success(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Formal Visual Inspection:** {visual_freq}")
    st.write(f"**Combined Testing (PAT):** {test_freq}")
    st.info(f"💡 *{notes}*")
elif total_score <= 3:
    risk_level = "LOW-MEDIUM"
    visual_freq = "Every 12 Months"
    test_freq = "Every 12 to 24 Months"
    notes = "Standard cycle. For Class II items here, routine instrument testing is not required; visual checks are sufficient."
    st.success(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Formal Visual Inspection:** {visual_freq}")
    st.write(f"**Combined Testing (PAT):** {test_freq}")
    st.write(notes)
elif total_score <= 6:
    risk_level = "MEDIUM-HIGH"
    visual_freq = "Every 12 Months"
    test_freq = "Every 12 Months"
    notes = "Standard cycle for handheld Class I items or equipment in harsher environments."
    st.warning(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Recommended Initial Frequency:** {test_freq}")
    st.write(f"*{notes}*")
else:
    risk_level = "HIGH / EXTREME"
    visual_freq = "High Frequency (Daily/Weekly checks recommended on-site)"
    test_freq = "Every 3 to 6 Months"
    notes = "Mandatory high-frequency testing for construction sites or heavily abused equipment."
    st.error(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Recommended Initial Frequency:** {test_freq}")
    st.write(f"*{notes}*")

if is_cable:
    st.warning("⚠️ *Note: Risk increased due to item being a power lead/extension.*")

st.markdown("---")
