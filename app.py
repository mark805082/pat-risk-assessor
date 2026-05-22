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

# Calculate totals
cable_modifier = 2 if is_cable else 0
total_score = env_score + handling_score + class_score + damage_score + cable_modifier

st.subheader("📋 Assessment Report Summary")

if client_name or asset_id:
    st.markdown(f"**Client:** {client_name if client_name else 'N/A'} | **Asset:** {asset_id if asset_id else 'N/A'}")

# Setup evaluation conditions & matching color blocks for PDF rendering
risk_level = ""
visual_freq = ""
test_freq = ""
notes = ""
rgb_fill = (46, 204, 113) # Green default

if total_score <= 1:
    risk_level = "LOW"
    visual_freq = "Every 24 Months"
    test_freq = "Every 24 to 36 Months"
    notes = "Perfect for office PCs, monitors, and stationary earthed/double-insulated equipment."
    rgb_fill = (46, 204, 113) # Clean Green
    st.success(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Formal Visual Inspection:** {visual_freq}")
    st.write(f"**Combined Testing (PAT):** {test_freq}")
    st.info(f"💡 *{notes}*")
elif total_score <= 3:
    risk_level = "LOW-MEDIUM"
    visual_freq = "Every 12 Months"
    test_freq = "Every 12 to 24 Months"
    notes = "Standard cycle. For Class II items (like chargers) here, routine instrument testing is not required; visual checks are sufficient."
    rgb_fill = (52, 152, 219) # Business Blue
    st.success(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Formal Visual Inspection:** {visual_freq}")
    st.write(f"**Combined Testing (PAT):** {test_freq}")
    st.write(notes)
elif total_score <= 6:
    risk_level = "MEDIUM-HIGH"
    visual_freq = "Every 12 Months"
    test_freq = "Every 12 Months"
    notes = "Standard cycle for handheld Class I items (like kettles) or equipment in harsher environments."
    rgb_fill = (230, 126, 34) # Amber/Orange
    st.warning(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Recommended Initial Frequency:** {test_freq}")
    st.write(f"*{notes}*")
else:
    risk_level = "HIGH / EXTREME"
    visual_freq = "High Frequency (Daily/Weekly checks recommended on-site)"
    test_freq = "Every 3 to 6 Months"
    notes = "Mandatory high-frequency testing for construction sites, heavy tools, or heavily abused equipment."
    rgb_fill = (231, 76, 60) # High-Risk Red
    st.error(f"### RISK LEVEL: {risk_level}")
    st.write(f"**Recommended Initial Frequency:** {test_freq}")
    st.write(f"*{notes}*")

if is_cable:
    st.warning("⚠️ *Note: Risk increased due to item being a power lead/extension, as recommended by risk safety standards.*")

st.markdown("---")
st.subheader("📄 Export Report")

# --- EXECUTIVE DESIGN CUSTOM PDF ENGINE ---
class ProPDF(FPDF):
    def header(self):
        # Top Header Accent Bar
        self.set_fill_color(44, 62, 80) # Deep Slate
        self.rect(0, 0, 210, 8, 'F')
        self.ln(5)
        
        # Document Title Block
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(44, 62, 80)
        self.cell(w=0, h=10, text='ELECTRICAL EQUIPMENT RISK ASSESSMENT', align='L', new_x="LMARGIN", new_y="NEXT")
        
        self.set_font('Helvetica', '', 9)
        self.set_text_color(127, 140, 141)
        self.cell(w=0, h=4, text='In accordance with the IET Code of Practice 5th Edition Framework', align='L', new_x="LMARGIN", new_y="NEXT")
        
        # Clean Divider Line
        self.set_draw_color(189, 195, 199)
        self.set_thickness(0.5)
        self.line(10, 32, 200, 32)
        self.ln(12)
        
    def footer(self):
        self.set_y(-20)
        self.set_draw_color(189, 195, 199)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(127, 140, 141)
        self.cell(0, 10, 'Generated via PAT Risk Assessor Pro • Official Verification Document', align='C')

def generate_pdf():
    pdf = ProPDF()
    pdf.add_page()
    
    # 1. CLIENT & JOB IDENTIFICATION BOX
    pdf.set_font("Helvetica", 'B', 10)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(w=0, h=6, text="JOB & ASSET IDENTIFICATION", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_fill_color(248, 249, 250) # Light grey background grid
    pdf.set_draw_color(230, 233, 237)
    pdf.cell(w=190, h=22, text='', border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    
    # Fill text over the background box
    current_y = pdf.get_y()
    pdf.set_y(current_y - 20)
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(w=95, h=6, text=f" Client / Business:  {client_name if client_name else 'Unspecified'}")
    pdf.cell(w=95, h=6, text=f"Appliance ID / Tag:  {asset_id if asset_id else 'Unspecified'}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=190, h=6, text=f" Operational Environment:  {env}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_y(current_y + 6) # Reset position past the block
    
    # 2. MATRIX EVALUATION FACTORS
    pdf.set_font("Helvetica", 'B', 10)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(w=0, h=8, text="RISK MATRIX ASSESSMENT FACTOR BREAKDOWN", new_x="LMARGIN", new_y="NEXT")
    
    # Simple crisp list display
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(52, 73, 94)
    
    factors = [
        f"• Mechanical Handling Dynamics: {handling}",
        f"• Electrical Construction Profile: {el_class.split(' [')[0] if 'Class II' in el_class else el_class}",
        f"• Recorded Casing & Damage History: {damage}",
        f"• Detachable Cord / Extension Lead Factor: {'Yes (+2 Safety Penalty Applied)' if is_cable else 'No (Standard Profile)'}",
        f"• Total Computed Risk Evaluation Points: {total_score} Matrix Points"
    ]
    for factor in factors:
        pdf.cell(w=0, h=5.5, text=f"  {factor}", new_x="LMARGIN", new_y="NEXT")
        
    pdf.ln(6)
    
    # 3. THE OUTCOME BADGE (Dynamic colored box based on risk level)
    pdf.set_fill_color(*rgb_fill)
    pdf.rect(10, pdf.get_y(), 190, 12, 'F')
    
    pdf.set_font("Helvetica", 'B', 11)
    pdf.set_text_color(255, 255, 255) # White text
    pdf.cell(w=0, h=12, text=f"  EVALUATED RISK MATRIX STATUS: {risk_level}", align='L', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    # 4. TESTING FREQUENCY SCHEDULE BOX
    pdf.set_font("Helvetica", 'B', 10)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(w=0, h=8, text="RECOMMENDED MAINTENANCE TIMELINE SCHEDULE", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", '', 10)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(w=0, h=6, text=f"  Initial Formal Visual Inspection Interval:  {visual_freq}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", 'B', 10)
    pdf.cell(w=0, h=6, text=f"  Initial Combined Electrical Testing (PAT) Frequency:  {test_freq}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(4)
    pdf.set_font("Helvetica", 'I', 9.5)
    pdf.set_text_color(127, 140, 141)
    pdf.multi_cell(w=185, h=5, text=f"Framework Execution Directive: {notes}")
    
    # 5. CORPORATE SIGN-OFF BLOCK
    pdf.ln(12)
    pdf.set_draw_color(218, 223, 230)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Helvetica", 'B', 9.5)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(w=95, h=5, text="Assessed By:")
    pdf.cell(w=95, h=5, text="Authorized Client Sign-off:", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10) # Blank space for physical signature or stamp
    pdf.set_font("Helvetica", 'I', 9)
    pdf.cell(w=95, h=5, text="......................................................")
    pdf.cell(w=95, h=5, text="......................................................", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", '', 8.5)
    pdf.cell(w=95, h=4, text="Competent Electrical Inspector")
    pdf.cell(w=95, h=4, text="Premises / Duty Holder Representative", new_x="LMARGIN", new_y="NEXT")
    
    return bytes(pdf.output())

try:
    pdf_data = generate_pdf()
    
    st.download_button(
        label="📥 Download PDF Certificate",
        data=pdf_data,
        file_name=f"PAT_Risk_Report_{client_name.replace(' ', '_') if client_name else 'Asset'}.pdf",
        mime="application/pdf"
    )
except Exception as e:
    st.error("The PDF generator layout is formatting. Please refresh your browser window.")

st.caption("Legal Note: Frequencies are recommendations based on initial risk verification and should be reviewed dynamically alongside historical failure rates.")
