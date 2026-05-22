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

# Calculate totals (Including Feature 3 modifier if checked)
cable_modifier = 2 if is_cable else 0
total_score = env_score + handling_score + class_score + damage_score + cable_modifier

st.subheader("📋 Assessment Report Summary")

# Display the logged details
if client_name or asset_id:
    st.markdown(f"**Client:** {client_name if client_name else 'N/A'} | **Asset:** {asset_id if asset_id else 'N/A'}")

# Define variables for results output
risk_level = ""
visual_freq = ""
test_freq = ""
notes = ""

if total_score <= 1:
    risk_level = "LOW"
    visual_freq = "Every 24 Months"
    test_freq = "Every 24 to 36 Months"
    notes = "Perfect for office PCs, monitors, and stationary earthed/double-insulated equipment."
    st.success(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Formal Visual Inspection:** {visual_freq}")
    st.write(f"**Combined Testing (PAT):** {test_freq}")
    st.info(f"💡 *{notes}*")
elif total_score <= 3:
    risk_level = "LOW-MEDIUM"
    visual_freq = "Every 12 Months"
    test_freq = "Every 12 to 24 Months"
    notes = "Standard cycle. For Class II items (like chargers) here, routine instrument testing is not required; visual checks are sufficient."
    st.success(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Formal Visual Inspection:** {visual_freq}")
    st.write(f"**Combined Testing (PAT):** {test_freq}")
    st.write(notes)
elif total_score <= 6:
    risk_level = "MEDIUM-HIGH"
    visual_freq = "Every 12 Months"
    test_freq = "Every 12 Months"
    notes = "Standard cycle for handheld Class I items (like kettles) or equipment in harsher environments."
    st.warning(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Recommended Initial Frequency:** {test_freq}")
    st.write(f"*{notes}*")
else:
    risk_level = "HIGH / EXTREME"
    visual_freq = "High Frequency (Daily/Weekly checks recommended on-site)"
    test_freq = "Every 3 to 6 Months"
    notes = "Mandatory high-frequency testing for construction sites, heavy tools, or heavily abused equipment."
    st.error(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Recommended Initial Frequency:** {test_freq}")
    st.write(f"*{notes}*")

if is_cable:
    st.warning("⚠️ *Note: Risk increased due to item being a power lead/extension, as recommended by risk safety standards.*")

# FEATURE 2: PDF Generation Logic
st.markdown("---")
st.subheader("📄 Export Report")

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(w=0, h=10, text='PAT RISK ASSESSMENT COMPLIANCE REPORT', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # CRITICAL FIX: Strip the special character [回] out before generating the PDF text string
    clean_class_string = el_class.split(" [")[0] if "Class II" in el_class else el_class
    
    # Metadata Block
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(w=0, h=6, text=f"Client / Business: {client_name if client_name else 'Unspecified'}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=6, text=f"Appliance ID / Tag: {asset_id if asset_id else 'Unspecified'}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=10)
    pdf.cell(w=0, h=6, text=f"Environment: {env}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Assessment Variables Box
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(w=0, h=8, text="Risk Assessment Matrix Factors", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)
    pdf.cell(w=0, h=6, text=f" - Handling Dynamics: {handling}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=6, text=f" - Equipment Construction: {clean_class_string}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=6, text=f" - Condition/Damage Profiles: {damage}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=6, text=f" - Cord/Extension Lead Factor: {'Yes (+2 Risk)' if is_cable else 'No'}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=6, text=f" - Calculated Core Matrix Evaluation Score: {total_score}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Results Box
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(w=0, h=8, text=f"EVALUATED RISK MATRIX OUTCOME: {risk_level}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(w=0, h=6, text=f"Initial Formal Visual Inspection Requirement: {visual_freq}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=6, text=f"Initial Combined Instrument Testing Cycle: {test_freq}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.multi_cell(w=0, h=5, text=f"Operational Direction: {notes}")
    
    return bytes(pdf.output())

# Execute download generation stream safely
try:
    pdf_data = generate_pdf()
    
    st.download_button(
        label="📥 Download PDF Certificate",
        data=pdf_data,
        file_name=f"PAT_Report_{client_name.replace(' ', '_') if client_name else 'Asset'}.pdf",
        mime="application/pdf"
    )
except Exception as e:
    st.error("The PDF generator is warming up. Please make sure your GitHub configuration matches correctly.")

st.caption("Legal Note: Frequencies are recommendations based on initial risk verification and should be reviewed dynamically alongside historical failure rates.")
