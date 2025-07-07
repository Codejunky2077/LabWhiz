import streamlit as st
import math
from PIL import Image
import datetime
import streamlit.components.v1 as components

#giving tips 
import random

insights = [
    "📏 Always double-check units — μL and mL mistakes ruin entire preps.",
    "🧪 Mix solutions thoroughly — don’t assume it’s homogeneous after adding solute.",
    "🔬 Use dedicated tips and buffers for RNA work — RNases are everywhere.",
    "🧊 Keep enzymes on ice — activity drops fast even at room temp.",
    "🎯 Don’t trust pH alone — always verify ionic strength in sensitive buffers.",
    "💡 Label with date and initials — mystery tubes cost time and samples.",
    "🚿 Wipe pipettes regularly — cross-contamination is sneakier than you think.",
    "🧫 Vortex only when protocol says so — not all reagents tolerate agitation.",
    "🧯 Never microwave sealed tubes — pressure buildup can cause explosions.",
    "🧰 Pre-weigh chemicals over paper or boat — balances are sensitive to spills.",
    "📅 Make fresh working dilutions — avoid reusing week-old diluted reagents.",
    "👁️ Scan protocols fully before starting — assumptions = errors.",
    "♻️ Calibrate pipettes if they feel ‘off’ — accuracy degrades silently.",]

lab_wisdom = random.choice(insights)



#analytics
st.markdown("""
            <!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "00b3ac8e9b2f42feba7acd4d35d5969a"}'></script><!-- End Cloudflare Web Analytics -->
            """, unsafe_allow_html=True)

if "LabWhiz_history" not in st.session_state:
    st.session_state.LabWhiz_history = []
if "rerun_flag" not in st.session_state:
    st.session_state.rerun_flag = False

# ✅ Rerun trigger check
if st.session_state.rerun_flag:
    st.session_state.rerun_flag = False
    st.experimental_rerun()
#Tab appearance
st.set_page_config(page_title="LabWhiz by Bionika", page_icon=Image.open("Bionika_tablogo.png"), layout="wide")

#css inject for appearance
#text
st.markdown(f"""
<img src="https://img.icons8.com/fluency/96/lab-items.png" width="48" style="margin-right:10px; vertical-align: middle;" />
<span style="font-size: 32px; font-weight: 700;">LabWhiz</span>  
<span style="color: #9ca3af;">by Bionika</span>  
<br>

<div style="font-size: 19px; font-weight: 700; margin-top: 6px; margin-bottom: 14px;">
Fast lab calculations on your device — when precision matters, LabWhiz delivers.
</div>
            
<div style="font-size: 17px; line-height: 1.6">
LabWhiz is built to calculate and catch what your eye misses — precise, reliable, and scientifically accurate every single time.<br>
It meets you where you work — in quiet benches, busy labs, and every place science demands precision.
</div>

---
            
<div style="font-size: 15px; color: #00c09a;">
🧠 <b>Lab Wisdom:</b> {lab_wisdom}
</div>
""", unsafe_allow_html=True)


#theme
st.markdown("""
    <style>
      /* Root & typography */
      .stApp {
        background: #1e1e2f;
        color: #e0e0e0 !important;
        font-family: 'Inter', sans-serif !important;
      }

      /* Section cards */
      .stContainer, .stExpander {
        background: #2b2b3c !important;
        border-radius: 10px !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.5) !important;
        margin-bottom: 1rem !important;
        border: 2px solid #44475a !important;
      }

      /* Inputs & textareas */
      input, textarea {
        background: #1e1e2f !important;
        border: 2px solid #50505f !important;
        border-radius: 6px !important;
        padding: 0.5rem !important;
        color: #e0e0e0 !important;
        transition: box-shadow 0.2s ease !important;
      }
      input:focus, textarea:focus {
        border-color: #7dd3fc !important;
        outline: none !important;
        box-shadow: 0 0 4px rgba(125,211,252,0.5) !important;
      }

      /* Selectboxes – single outer box only */
      .stSelectbox > div {
        background: #1e1e2f !important;
        border: 2px solid #50505f !important;
        border-radius: 6px !important;
        padding: 0.4rem 0.6rem !important;
        color: #e0e0e0 !important;
      }
      .stSelectbox [role="combobox"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
      }
      .stSelectbox [role="combobox"] input {
        display: none !important;
      }
      .stSelectbox [role="combobox"] svg {
        fill: #e0e0e0 !important;
        pointer-events: none;
      }

      /* Buttons */
      .stButton > button {
        background: #7dd3fc !important;
        color: #1e1e2f !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.4) !important;
        transition: background 0.15s ease !important;
      }
      .stButton > button:hover {
        background: #38bdf8 !important;
      }

      /* Captions & info text */
      .stCaption, .stInfo {
        color: #b0b0b0 !important;
        font-size: 0.85rem !important;
      }

      /* Force all titles & headers to white */
      .stTitle > div,
      .stHeader > div,
      .stSubheader > div,
      .stMarkdown h1,
      .stMarkdown h2,
      .stMarkdown h3,
      .stApp h1,
      .stApp h2,
      .stApp h3 {
        color: #ffffff !important;
      }
    </style>
""", unsafe_allow_html=True)

# --- Unit Conversion Maps --- #
CONCENTRATION_UNITS = {
    "ng/μL": 1,
    "μg/μL": 1000,
    "mg/mL": 1000,
    "μg/mL": 1,
    "ng/mL": 0.001,
    "M": 1e9,
    "mM": 1e6,
    "μM": 1e3,
    "nM": 1,
    }

VOLUME_UNITS = {
    "μL": 1,
    "mL": 1000,
    "L": 1_000_000
    }

# --- Conversion Functions --- #
def convert_conc(value, from_unit, to_base=True):
    factor = CONCENTRATION_UNITS[from_unit]
    return value * factor if to_base else value / factor

def convert_vol(value, from_unit, to_base=True):
    factor = VOLUME_UNITS[from_unit]
    return value * factor if to_base else value / factor


#different calculation functions
def simpledilution():
    st.info("Use: To dilute a stock solution to a lower concentration directly. Common in buffer prep, reagent dilution, etc.")
    col1, col2 = st.columns(2)

    with col1:
        C1_str = st.text_input("Original Concentration (C₁)", placeholder="e.g. 50", key="c1_input")
        C1_unit = st.selectbox("C₁ Unit", list(CONCENTRATION_UNITS))
    with col2:
        C2_str = st.text_input("Target Concentration (C₂)", placeholder="e.g. 10", key="c2_input")
        C2_unit = st.selectbox("C₂ Unit", list(CONCENTRATION_UNITS))

    V2_str = st.text_input("Final Volume (V₂)", placeholder="e.g. 100", key="v2_input")
    V2_unit = st.selectbox("V₂ Unit", list(VOLUME_UNITS))

    output_unit = st.selectbox("Output Volume Unit (V₁)", list(VOLUME_UNITS), help="You can change unit of solution you need which is possible in your lab.")

    calculate = st.button("🚀 Get needed Volume (V₁)")

    if calculate:
        try:
            C1 = float(C1_str)
            C2 = float(C2_str)
            V2 = float(V2_str)
        except (ValueError, TypeError):
            st.error("Please enter valid numerical values for C₁, C₂, and V₂.")
            return

        if C1 <= 0 or C2 <= 0 or V2 <= 0:
            st.error("Parameter values must be greater than 0.")
        elif C2 > C1:
            st.error("Target concentration (C₂) cannot exceed original concentration (C₁).")
        else:
            try:
                C1_u = convert_conc(C1, C1_unit)
                C2_u = convert_conc(C2, C2_unit)
                V2_u = convert_vol(V2, V2_unit)
                V1_uL = (C2_u * V2_u) / C1_u
                V1_converted = convert_vol(V1_uL, output_unit, to_base=False)

                # History must update BEFORE success message
                result_text = f"Simple dilution \nC1={C1:.2f} {C1_unit} →C2={C2:.2f} {C2_unit} in V2={V2:.2f} {V2_unit} → need V1={V1_converted:.2f} {output_unit}"
                st.session_state.LabWhiz_history.insert(0, result_text)
                st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

                st.success(f"✅ Needed Volume (V₁): {V1_converted:.2f} {output_unit}")
                st.caption(f"Pipette {V1_converted:.2f} {output_unit} of {C1:.2f} {C1_unit} stock and dilute to {V2:.2f} {V2_unit} to get {C2:.2f} {C2_unit}.")

            except Exception as e:
                st.error(f"Error in dilution calculation please use numericals only.")
def serialdilution():
    st.info("Use: When you need very high dilutions (e.g., 1:10000), which are impractical in one step. Common in microbiology and pharmacology.")
    
    col1, col2 = st.columns(2)
    with col1:
        C1_str = st.text_input("Initial Concentration (C₁)", placeholder="e.g. 100", key="serial_c1")
        C1_unit = st.selectbox("C₁ Unit", list(CONCENTRATION_UNITS))
    with col2:
        C2_str = st.text_input("Desired Final Concentration (C₂)", placeholder="e.g. 0.01", key="serial_c2")
        C2_unit = st.selectbox("C₂ Unit", list(CONCENTRATION_UNITS))

    dilution_factor_str = st.text_input("Dilution Ratio per Step (e.g., 1:10 → enter 10)", placeholder="e.g. 10", key="serial_ratio")
    volume_stock_str = st.text_input("Volume taken per Step (µL)", placeholder="e.g. 100", key="serial_vstock")
    volume_diluent_str = st.text_input("Diluent Volume per Step (µL)", placeholder="e.g. 900", key="serial_vdiluent")

    if st.button("🚀Calculate number of steps"):
        try:
            # Parse and validate inputs
            C1 = float(C1_str)
            C2 = float(C2_str)
            dilution_factor = float(dilution_factor_str)
            volume_stock = float(volume_stock_str)
            volume_diluent = float(volume_diluent_str)

            if any(x <= 0 for x in [C1, C2, dilution_factor, volume_stock, volume_diluent]):
                st.error("All inputs must be greater than zero.")
                return

            C1_u = convert_conc(C1, C1_unit)
            C2_u = convert_conc(C2, C2_unit)

            if C2_u >= C1_u:
                st.error("Desired concentration must be lower than starting concentration.")
                return

            total_dilution = C1_u / C2_u
            epsilon = 1e-9  # Prevent floating point mismatch
            steps_needed = math.ceil(math.log(total_dilution + epsilon, dilution_factor))

            # Calculate final actual concentration
            actual_final = C1_u / (dilution_factor ** steps_needed)
            actual_final_user_unit = convert_conc(actual_final, C2_unit, to_base=False)

            # Save result to history first
            result_text = f"Serial Dilution\n C1={C1:.2f} {C1_unit} → C2≈{actual_final_user_unit:.4f} {C2_unit} in {steps_needed} steps (1:{dilution_factor} each)"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

            st.success(f"✅You need {steps_needed} serial dilution step(s) to reach ~{actual_final_user_unit:.4f} {C2_unit} from {C1:.2f} {C1_unit}")
            st.caption(f"Each step: {volume_stock:.2f} µL + {volume_diluent:.2f} µL diluent (1:{dilution_factor:.1f} dilution)")

        except ValueError:
            st.error("Please enter valid numerical values in all fields.")
        except Exception as e:
            st.error(f"Error in serial dilution please use numericals only.")
def molarity():
    st.info("Use: Quickly calculate how much solute is needed to make a solution of desired molarity. Common in: solution prep, reagents, buffers, and media preparation.")

    molarity_str = st.text_input("Desired molarity (mol/L)", placeholder="e.g. 0.1", key="mol_molarity")
    volume_str = st.text_input("Enter volume", placeholder="e.g. 1000", key="mol_volume")
    volume_unit = st.selectbox("Enter the unit of volume", list(VOLUME_UNITS))
    mw_str = st.text_input("Enter Molecular weight (g/mol)", placeholder="e.g. 58.44", key="mol_mw")

    if st.button("🎯Calculate required mass"):
        try:
            molarity = float(molarity_str)
            volume = float(volume_str)
            mw = float(mw_str)

            if molarity <= 0 or volume <= 0 or mw <= 0:
                st.error("All input values must be greater than zero.")
                return

            volume_in_L = volume * VOLUME_UNITS[volume_unit] / 1_000_000  # μL-based to L
            moles = molarity * volume_in_L
            mass = moles * mw  # in grams

            unit = "mg" if mass < 1 else "g"
            mass_out = mass * 1000 if unit == "mg" else mass

            st.success(f"✅You need to weigh **{mass_out:.3f} {unit}** of the compound.")
            st.caption(f"To make {volume:.2f} {volume_unit} of a {molarity:.4f} M solution with MW {mw:.2f} g/mol.")

            # Add to history
            result_text = f"Molarity={molarity:.4f} M × Vol={volume:.2f} {volume_unit} with g/mol={mw:.2f} → {mass_out:.3f} {unit}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in molarity calculation please use numericals only.")
def wv():
    st.info("Use: To prepare a solution where a solid is dissolved in a liquid (e.g., NaCl, glucose).")

    percent_str = st.text_input("Enter desired concentration (% w/v)", placeholder="e.g. 5", key="wv_percent")
    volume_str = st.text_input("Enter total volume", placeholder="e.g. 250", key="wv_volume")
    volume_unit = st.selectbox("Select volume unit", list(VOLUME_UNITS.keys()))  # μL, mL, L

    if st.button("🚀Calculate required mass"):
        try:
            percent = float(percent_str)
            volume = float(volume_str)

            if percent <= 0 or volume <= 0:
                st.error("Concentration and volume must be greater than zero.")
                return

            # ✅ Convert volume to mL safely (assuming convert_vol returns µL)
            volume_uL = convert_vol(volume, volume_unit, to_base=True)  # e.g., 250 mL → 250,000 µL
            volume_mL = volume_uL / 1000  # µL → mL

            # ✅ Calculate mass in grams
            mass_g = (percent / 100) * volume_mL

            # ✅ Format output unit smartly
            if mass_g >= 1:
                mass_out = mass_g
                unit = "g"
            elif mass_g >= 0.001:
                mass_out = mass_g * 1000
                unit = "mg"
            else:
                mass_out = mass_g * 1_000_000
                unit = "µg"

            st.success(f"✅You need to weigh **{mass_out:.3f} {unit}** of solute.")
            st.caption(f"To make {volume:.2f} {volume_unit} of a {percent:.2f}% w/v solution.")

            # Add to history
            result_text = f"W/V\n {percent:.2f}% in Vol={volume:.2f} {volume_unit} → Mass={mass_out:.3f} {unit}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in w/v calculation please use numericals only.")
def vv():
    st.info("Note: Use for mixing two liquids, like ethanol or acetic acid in water. Example: making 70% ethanol = 70 mL ethanol in 100 mL solution.")

    percent_str = st.text_input("Enter desired concentration (% v/v)", placeholder="e.g. 70", key="vv_percent")
    volume_str = st.text_input("Enter total solution volume", placeholder="e.g. 100", key="vv_volume")
    volumeunit = st.selectbox("Choose volume unit", list(VOLUME_UNITS))

    if st.button("🎯Calculate required solute volume"):
        try:
            percent = float(percent_str)
            volume = float(volume_str)

            if percent <= 0 or volume <= 0:
                st.error("Concentration and volume must be greater than zero.")
                return

            # Convert input volume to µL
            total_volume_uL = convert_vol(volume, volumeunit, to_base=True)

            # Calculate solute volume in µL
            solute_volume_uL = (percent / 100) * total_volume_uL

            # Decide best output unit
            if solute_volume_uL >= 1_000_000:
                solute_volume_out = solute_volume_uL / 1_000_000
                unit = "L"
            elif solute_volume_uL >= 1000:
                solute_volume_out = solute_volume_uL / 1000
                unit = "mL"
            else:
                solute_volume_out = solute_volume_uL
                unit = "μL"

            st.success(f"✅You need **{solute_volume_out:.2f} {unit}** of liquid solute.")
            st.caption(f"To make {volume:.2f} {volumeunit} of a {percent:.2f}% v/v solution.")

            # Add to history
            result_text = f"v/v\n {percent:.2f}% in Vol={volume:.2f} {volumeunit} → soluteVol={solute_volume_out:.2f} {unit}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in v/v calculation please use numericals only.")
def md():
    st.info("Use:\nDilute a molar solution from a concentrated stock.\nCommon in buffer preparation, titrations, and chemical reactions.")

    M1_str = st.text_input("Initial Molarity (M₁)", placeholder="e.g. 1.0", key="md_m1")
    M2_str = st.text_input("Target Molarity (M₂)", placeholder="e.g. 0.1", key="md_m2")

    V2_str = st.text_input("Final Volume (V₂)", placeholder="e.g. 100", key="md_v2")
    V2_unit = st.selectbox("V₂ Unit", list(VOLUME_UNITS.keys()))

    output_unit = st.selectbox("Output Volume Unit (V₁)", list(VOLUME_UNITS.keys()))

    if st.button("🚀Calculate needed Volume (V₁)"):
        try:
            M1 = float(M1_str)
            M2 = float(M2_str)
            V2 = float(V2_str)

            if M1 <= 0 or M2 <= 0 or V2 <= 0:
                st.error("All parameters must be greater than zero.")
                return

            if M2 > M1:
                st.error("Target molarity (M₂) cannot exceed starting molarity (M₁).")
                return

            V2_uL = convert_vol(V2, V2_unit)  # Convert to µL
            V1_uL = (M2 * V2_uL) / M1
            V1_out = convert_vol(V1_uL, output_unit, to_base=False)

            st.success(f"✅You need to pipette **{V1_out:.2f} {output_unit}** of {M1:.2f} M solution.")
            st.caption(f"Dilute to {V2:.2f} {V2_unit} to get {M2:.2f} M.")

            # Add to history
            result_text = f"Molarity Dilution\n M1={M1:.2f} M → M2={M2:.2f} M in V2={V2:.2f} {V2_unit} → need V1={V1_out:.2f} {output_unit}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in molarity dilution please use numericals only.")
def drpdilution():
    st.info("Use:\nDilute nucleic acids or proteins to desired working concentrations.\nCommon in PCR, gel loading, extractions, assays.")
    calc_type = st.radio("Choose what you want to calculate:", ["Dilution Volume (C₁×V₁ = C₂×V₂)", "Mass in Given Volume"], help="Two types of problem arise from wet lab here both types are given.")

    if calc_type == "Dilution Volume (C₁×V₁ = C₂×V₂)":
        col1, col2, col3 = st.columns(3)
        with col1:
            C1_str = st.text_input("Stock Concentration (C₁)", placeholder="e.g. 100", key="drp_c1")
            C1_unit = st.selectbox("C₁ Unit", list(CONCENTRATION_UNITS.keys()))
        with col2:
            C2_str = st.text_input("Target Concentration (C₂)", placeholder="e.g. 10", key="drp_c2")
            C2_unit = st.selectbox("C₂ Unit", list(CONCENTRATION_UNITS.keys()))
        with col3:
            V2_str = st.text_input("Final Volume (V₂)", placeholder="e.g. 500", key="drp_v2")
            V2_unit = st.selectbox("V₂ Unit", list(VOLUME_UNITS.keys()))

        output_unit = st.selectbox("Output Volume Unit (V₁)", list(VOLUME_UNITS.keys()))

        if st.button("🧬Calculate Volume (V₁)"):
            try:
                C1 = float(C1_str)
                C2 = float(C2_str)
                V2 = float(V2_str)

                if C1 <= 0 or C2 <= 0 or V2 <= 0:
                    st.error("All values must be greater than zero.")
                    return

                if C2 > C1:
                    st.error("Target concentration cannot exceed stock concentration.")
                    return

                C1_base = convert_conc(C1, C1_unit)
                C2_base = convert_conc(C2, C2_unit)
                V2_base = convert_vol(V2, V2_unit)

                V1_uL = (C2_base * V2_base) / C1_base
                V1_out = convert_vol(V1_uL, output_unit, to_base=False)

                st.success(f"✅You need {V1_out:.2f} {output_unit} of {C1:.2f} {C1_unit} solution.")
                st.caption(f"Dilute it to {V2:.2f} {V2_unit} to get {C2:.2f} {C2_unit}.")

                result_text = f"DRP Dilution\n C1={C1:.2f} {C1_unit} → C2={C2:.2f} {C2_unit} in V2={V2:.2f} {V2_unit} → need V1={V1_out:.2f} {output_unit}"
                st.session_state.LabWhiz_history.insert(0, result_text)
                st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

            except Exception as e:
                st.error(f"Error in biomolecule dilution please use numericals only.")

    elif calc_type == "Mass in Given Volume":
        conc_str = st.text_input("Concentration", placeholder="e.g. 50", key="drp_conc")
        conc_unit = st.selectbox("Concentration Unit", list(CONCENTRATION_UNITS.keys()))

        vol_str = st.text_input("Volume", placeholder="e.g. 20", key="drp_vol")
        vol_unit = st.selectbox("Volume Unit", list(VOLUME_UNITS.keys()))

        if st.button("🧪Calculate Mass"):
            try:
                conc = float(conc_str)
                vol = float(vol_str)

                if conc <= 0 or vol <= 0:
                    st.error("Values given must be greater than zero.")
                    return

                conc_base = convert_conc(conc, conc_unit)  # ng/μL
                vol_base = convert_vol(vol, vol_unit)      # μL

                mass_ng = conc_base * vol_base

                unit = "ng"
                if mass_ng >= 1e6:
                    mass = mass_ng / 1e6
                    unit = "mg"
                elif mass_ng >= 1000:
                    mass = mass_ng / 1000
                    unit = "μg"
                else:
                    mass = mass_ng

                st.success(f"✅Mass: {mass:.3f} {unit}")
                st.caption(f"From {conc:.2f} {conc_unit} × {vol:.2f} {vol_unit}")

                result_text = f"DRP Mass\n con={conc:.2f} {conc_unit} × vol={vol:.2f} {vol_unit} → mass={mass:.3f} {unit}"
                st.session_state.LabWhiz_history.insert(0, result_text)
                st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

            except Exception as e:
                st.error(f"Error in mass calculation please use numericals only.")
def cc():
    st.info("Use:\nEstimate bacterial concentration in original sample after plating.\nCommon in: microbiology, antibiotic testing, fermentation.")

    colonies_str = st.text_input("Number of Colonies Counted", placeholder="e.g. 87", key="cc_colonies")
    dilution_str = st.text_input("Dilution Factor (e.g., 1:1000 → enter 1000)", placeholder="e.g. 1000", key="cc_dilution")
    plated_vol_str = st.text_input("Volume Plated (in mL)", placeholder="e.g. 0.1", key="cc_volume")

    if st.button("🦠Calculate CFU/mL"):
        try:
            colonies = int(colonies_str)
            dilution_factor = float(dilution_str)
            plated_volume = float(plated_vol_str)

            if colonies <= 0 or plated_volume <= 0 or dilution_factor <= 0:
                st.error("Colony count, volume plated, and dilution must be greater than zero.")
                return

            cfu_per_mL = (colonies * dilution_factor) / plated_volume

            st.success(f"✅Estimated concentration: **{cfu_per_mL:.2e} CFU/mL**")
            st.caption(f"Based on {colonies} colonies at 1:{int(dilution_factor)} dilution and {plated_volume:.4f} mL plated.")

            result_text = f"CFU Count\n {colonies} colonies at 1:{int(dilution_factor)} → {cfu_per_mL:.2e} CFU/mL"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in CFU calculation please use numericals only.")
def gdf():
    st.info("Use:\nCalculate how much dilution occurred based on initial volume and final total volume.\nCommon in: buffer prep, enzyme assays, reagent use.")

    col1, col2 = st.columns([2, 1])
    with col1:
        stock_volume_str = st.text_input("Volume of initial stock used", placeholder="e.g. 100", key="gdf_stock")
    with col2:
        unit = st.selectbox("Unit", list(VOLUME_UNITS.keys()), key="gdf_unit")

    final_volume_str = st.text_input("Final volume after dilution", placeholder="e.g. 1000", key="gdf_final")

    if st.button("🧪 Calculate Dilution Factor"):
        try:
            stock_volume = float(stock_volume_str)
            final_volume = float(final_volume_str)

            if stock_volume <= 0 or final_volume <= 0:
                st.error("Both volumes must be greater than zero.")
                return

            stock_vol_uL = convert_vol(stock_volume, unit)
            final_vol_uL = convert_vol(final_volume, unit)

            if final_vol_uL <= stock_vol_uL:
                st.error("Final volume must be greater than stock volume to indicate dilution.")
            else:
                dilution_factor = final_vol_uL / stock_vol_uL
                st.success(f"✅ Dilution Factor: **1:{dilution_factor:.2f}**")
                st.caption(f"You diluted {stock_volume:.2f} {unit} up to {final_volume:.2f} {unit}, giving a 1:{dilution_factor:.2f} dilution.")

                # Save to history
                result_text = f"Dilution Factor\n stock={stock_volume:.2f} {unit} → final={final_volume:.2f} {unit} → 1:{dilution_factor:.2f}"
                st.session_state.LabWhiz_history.insert(0, result_text)
                st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except (ValueError, TypeError):
            st.error("Please enter valid numerical values.")
        except Exception as e:
            st.error(f"Error in dilution factor calculation please use numericals only.")


#main webapp LabWhiz
def LabWhiz():
    type = st.selectbox("Select the type of calculation needed...",[
        "",
        "Simple dilution",
        "Serial dilution",
        "Molarity",
        "Weight/Volume(%w/v)",
        "Volume/Volume (% v/v)",
        "Molarity Dilution",
        "DNA/RNA/Protein Dilution",
        "CFU / Cell Culture Calculation",
        "General Dilution Factor"],help="Use the type of calculation u want related to your lab work.")
    
    if type =="Simple dilution":
        st.header("Simple dilution")
        simpledilution()
    elif type =="Serial dilution":
        st.header("Serial dilution")
        serialdilution()
    elif type=="Molarity":
        st.header("Molarity")
        molarity()
    elif type=="Weight/Volume(%w/v)":
        st.header("Weight/Volume(%w/v)")
        wv()
    elif type=="Volume/Volume (% v/v)":
        st.header("Volume/Volume (% v/v)")
        vv()
    elif type=="Molarity Dilution":
        st.header("Molarity Dilution")
        md()
    elif type=="DNA/RNA/Protein Dilution":
        st.header("DNA/RNA/Protein Dilution")
        drpdilution()
    elif type=="CFU / Cell Culture Calculation":
        st.header("CFU / Cell Culture Calculation")
        cc()
    elif type=="General Dilution Factor":
        st.header("General Dilution Factor")
        gdf()
if __name__ == '__main__':
     #sidebar ui
    with st.sidebar.expander("📤 Share LabWhiz", expanded=False):
        st.markdown("""
                    <br><small>Send it to your labmates:</small><br>
                    - <a href="https://api.whatsapp.com/send?text=LabWhiz%20%E2%80%94%20Built%20for%20life%20science%20lab%20people%20who%20hate%20messy%20calculations.%0A%0ANo%20more%20unit%20confusion%20or%20endless%20Googling.%0A%F0%9F%93%B1%20Works%20on%20mobile.%20No%20login.%20No%20clutter.%0A%F0%9F%92%A1%20The%20smart%20ones%20are%20already%20using%20it.%0A%0A%F0%9F%91%87%20Try%20it%20once%20%E2%80%94%20you%E2%80%99ll%20wish%20you%20had%20it%20earlier%3A%0Ahttps%3A%2F%2Flabwhiz.streamlit.app%2F" target="_blank">WhatsApp</a><br>
                    - <a href="https://twitter.com/intent/tweet?text=Try%20LabWhiz%20%E2%80%94%20The%20fastest%20lab%20calculator.%20https://labwhiz.streamlit.app/" target="_blank">🕊️X</a><br>
                    - <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://labwhiz.streamlit.app/" target="_blank">💼LinkedIn</a><br>
                    - <a href="mailto:?subject=Try%20LabWhiz%20%E2%80%94%20Fastest%20Lab%20Calculator&body=LabWhiz%20is%20a%20mobile-friendly%20lab%20calculator%20built%20for%20life%20science%20students.%0A%0Ahttps://labwhiz.streamlit.app/" target="_blank">📨 Email</a>
                    """, unsafe_allow_html=True)

    with st.sidebar.expander("🧾 Recent Calculations", expanded=False):
        if st.session_state.LabWhiz_history:
            for item in st.session_state.LabWhiz_history:
                st.markdown(f"- {item}")
        else:
            st.caption("No calculations yet.")
    with st.sidebar.expander("💬 Send Feedback",expanded=False):
        st.markdown("""
        We'd love your feedback on LabWhiz — bug reports, feature requests, or just thoughts.
        👉 [Click here to open the feedback form](https://forms.gle/mBd51Fpz4Ly4tbUE6)  
        📝 Takes less than a minute!
        """)
    LabWhiz()  
