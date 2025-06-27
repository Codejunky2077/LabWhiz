import streamlit as st
import math

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

# --- Streamlit App --- #
st.title("🧬BufferBuddy")
st.header("Welcome to BufferBuddy")
st.write("Most simplistic calculator especially designed for wet lab fellas for their daily shenanigans.")
def BufferBuddy():
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
        "General Dilution Factor"])
    
    if type =="Simple dilution":
        simpledilution()
    elif type =="Serial dilution":
        serialdilution()
    elif type=="Molarity":
        molarity()
    elif type=="Weight/Volume(%w/v)":
        wv()
    elif type=="Volume/Volume (% v/v)":
        vv()
    elif type=="Molarity Dilution":
        md()
    elif type=="DNA/RNA/Protein Dilution":
        drpdilution()
    elif type=="CFU / Cell Culture Calculation":
        cc()
    elif type=="General Dilution Factor":
        gdf()


if __name__ == '__main__':
    BufferBuddy()  


#different calculation functions
def simpledilution():
    st.info("Use: To dilute a stock solution to a lower concentration directly.Common in buffer prep, reagent dilution, etc.")

    C1 = st.number_input("Original Concentration (C₁)", min_value=0.0, step=0.1, format="%.4f")
    C1_unit = st.selectbox("C₁ Unit", list(CONCENTRATION_UNITS))

    C2 = st.number_input("Target Concentration (C₂)", min_value=0.0, step=0.1, format="%.4f")
    C2_unit = st.selectbox("C₂ Unit", list(CONCENTRATION_UNITS))

    V2 = st.number_input("Final Volume (V₂)", min_value=0.0, step=0.1, format="%.4f")
    V2_unit = st.selectbox("V₂ Unit", list(VOLUME_UNITS))

    output_unit = st.selectbox("Output Volume Unit (V₁)", list(VOLUME_UNITS))

    if st.button("Get needed Volume (V₁)"):
        if C1 == 0 or C2 == 0 or V2 == 0:
            st.error("Parameter values must be greater than 0.")
        elif C2 > C1:
            st.error("Target concentration (C₂) cannot exceed original concentration (C₁).")
        else:
            C1_u = convert_conc(C1, C1_unit)
            C2_u = convert_conc(C2, C2_unit)
            V2_u = convert_vol(V2, V2_unit)

            V1_uL = (C2_u * V2_u) / C1_u
            V1_converted = convert_vol(V1_uL, output_unit, to_base=False)

            st.success(f"Needed Volume (V₁): {V1_converted:.2f} {output_unit}")
            st.caption(f"Pipette {V1_converted:.2f} {output_unit} of {C1:.2f} {C1_unit} stock and dilute to {V2:.2f} {V2_unit} to get {C2:.2f} {C2_unit}.")
def serialdilution():
    st.info("Use: When you need very high dilutions (e.g., 1:10000), which are impractical in one step.Common in microbiology and pharmacology.")

    C1 = st.number_input("Initial Concentration (C₁)", min_value=0.0, step=0.1, format="%.4f")
    C1_unit = st.selectbox("C₁ Unit", list(CONCENTRATION_UNITS))

    C2 = st.number_input("Desired Final Concentration (C₂)", min_value=0.0, step=0.1, format="%.4f")
    C2_unit = st.selectbox("C₂ Unit", list(CONCENTRATION_UNITS))

    dilution_factor = st.number_input("Dilution Ratio per Step (e.g., 1:10 → enter 10)", min_value=1.0, step=1.0)

    volume_stock = st.number_input("Volume taken per Step (µL)", min_value=0.0, step=0.1, format="%.4f")
    volume_diluent = st.number_input("Diluent Volume per Step (µL)", min_value=0.0, step=0.1, format="%.4f")

    if st.button("Calculate number of steps"):
        C1_u = convert_conc(C1, C1_unit)
        C2_u = convert_conc(C2, C2_unit)

        if C2_u >= C1_u:
            st.error("Desired concentration must be lower than starting concentration.")
        else:
            total_dilution = C1_u / C2_u
            steps_needed = math.ceil(math.log(total_dilution, dilution_factor))
            actual_final = C1_u / (dilution_factor ** steps_needed)
            actual_final_user_unit = convert_conc(actual_final, C2_unit, to_base=False)

            st.success(f"You need {steps_needed} serial dilution step(s) to reach ~{actual_final_user_unit:.4f} {C2_unit} from {C1} {C1_unit}")
            st.caption(f"Each step: {volume_stock} µL + {volume_diluent} µL diluent (1:{dilution_factor} dilution)")
def molarity():
    st.info("Use: Quickly calculate how much solute is needed to make a solution of desired molarity.Common in: solution prep, reagents, buffers, and media preparation.")
    molarity=st.number_input("Desired molarity(mol/L)",min_value=0.0, step=0.001, format="%.4f")
    volume=st.number_input("Enter volume",min_value=0.0, step=0.01, format="%.2f")
    volume_unit=st.selectbox("Enter the unit of volume",list(VOLUME_UNITS))
    mw=st.number_input("Enter Molecular weight(g/mol)",min_value=0.0, step=0.001, format="%.4f")

    if st.button("Calculate required mass"):
        if molarity==0 or volume==0 or mw==0:
            st.error("Parameter given must not be zero.\nCheck values again.")
        else:
            volume_in_L = volume * VOLUME_UNITS[volume_unit] / 1_000_000  # μL-based to L
                    # Calculate moles and mass
            moles = molarity * volume_in_L
            mass = moles * mw  # in grams

            unit = "mg" if mass < 1 else "g"
            mass_out = mass * 1000 if unit == "mg" else mass

            st.success(f"You need to weigh **{mass_out:.3f} {unit}** of the compound.")
            st.caption(f"To make {volume:.2f} {volume_unit} of a {molarity:.4f} M solution with MW {mw:.2f} g/mol.")
def wv():
    st.info("Use:To prepare a solution where a solid is dissolved in a liquid (e.g., NaCl, glucose).")
    percent = st.number_input("Enter desired concentration (% w/v)", min_value=0.0, step=0.01, format="%.2f")
    volume = st.number_input("Enter total volume", min_value=0.0, step=0.1, format="%.2f")
    volume_unit = st.selectbox("Select volume unit", list(VOLUME_UNITS.keys()))  # μL, mL, L

    if st.button("Calculate required mass"):
        if percent == 0 or volume == 0:
            st.error("Concentration and volume must be greater than zero.")
        else:
                    # Convert volume to mL
            volume_ml = convert_vol(volume, volume_unit, to_base=True) / 1000  # μL to mL

                    # Calculate required mass in grams
            mass = (percent * volume_ml) / 100  # g

            unit = "mg" if mass < 1 else "g"
            mass_out = mass * 1000 if unit == "mg" else mass

            st.success(f"You need to weigh **{mass_out:.3f} {unit}** of solute.")
            st.caption(f"To make {volume:.2f} {volume_unit} of a {percent:.2f}% w/v solution.")
def vv():
    st.info("Note:Use for mixing two liquids, like ethanol or acetic acid in water.Example: making 70%" "ethanol = 70 mL ethanol in 100 mL solution.")
        
    percent=st.number_input("Enter desired concentration(%v/v)",min_value=0.0,step=0.01,format="%.2f")
    volume=st.number_input("Enter total solution volume",min_value=0.0,step=0.01,format="%.2f")
    volumeunit=st.selectbox("Choose volume unit",list(VOLUME_UNITS))

    if st.button("Calculate required solute volume"):
        if percent == 0 or volume == 0:
            st.error("Concentration and volume must be greater than zero.")
        else:
            
            total_volume_mL = convert_vol(volume, volumeunit, to_base=True) / 1000  # μL to mL

            
            solute_volume_mL = (percent * total_volume_mL) / 100

            # Choose best output unit
            unit = "μL" if solute_volume_mL < 0.001 else "mL"
            solute_volume_out = solute_volume_mL * 1000 if unit == "μL" else solute_volume_mL

            st.success(f"You need **{solute_volume_out:.2f} {unit}** of liquid solute.")
            st.caption(f"To make {volume:.2f} {volumeunit} of a {percent:.2f}% v/v solution.")
def md():
    st.info("Use:\nDilute a molar solution from a concentrated stock.\nCommon in buffer preparation, titrations, and chemical reactions.")

    M1 = st.number_input("Initial Molarity (M₁)", min_value=0.0, step=0.001, format="%.4f")
    M2 = st.number_input("Target Molarity (M₂)", min_value=0.0, step=0.001, format="%.4f")

    V2 = st.number_input("Final Volume (V₂)", min_value=0.0, step=0.01, format="%.4f")
    V2_unit = st.selectbox("V₂ Unit", list(VOLUME_UNITS.keys()))

    output_unit = st.selectbox("Output Volume Unit (V₁)", list(VOLUME_UNITS.keys()))

    if st.button("Calculate needed Volume (V₁)"):
        if M1 == 0 or M2 == 0 or V2 == 0:
            st.error("All parameters must be greater than zero.")
        elif M2 > M1:
            st.error("Target molarity (M₂) cannot exceed starting molarity (M₁).")
        else:
            V2_uL = convert_vol(V2, V2_unit)  # Convert to µL
            V1_uL = (M2 * V2_uL) / M1         # µL by default
            V1_out = convert_vol(V1_uL, output_unit, to_base=False)

            st.success(f"You need to pipette **{V1_out:.2f} {output_unit}** of {M1} M solution.")
            st.caption(f"Dilute to {V2:.2f} {V2_unit} to get {M2:.2f} M.")
def drpdilution():
    st.info("Use:\nDilute nucleic acids or proteins to desired working concentrations.\nCommon in PCR, gel loading, extractions, assays.")

    calc_type = st.radio("Choose what you want to calculate:", ["Dilution Volume (C₁×V₁ = C₂×V₂)", "Mass in Given Volume"])

    if calc_type == "Dilution Volume (C₁×V₁ = C₂×V₂)":
        C1 = st.number_input("Stock Concentration (C₁)", min_value=0.0, step=0.1, format="%.4f")
        C1_unit = st.selectbox("C₁ Unit", list(CONCENTRATION_UNITS.keys()))

        C2 = st.number_input("Target Concentration (C₂)", min_value=0.0, step=0.1, format="%.4f")
        C2_unit = st.selectbox("C₂ Unit", list(CONCENTRATION_UNITS.keys()))

        V2 = st.number_input("Final Volume (V₂)", min_value=0.0, step=0.1, format="%.4f")
        V2_unit = st.selectbox("V₂ Unit", list(VOLUME_UNITS.keys()))

        output_unit = st.selectbox("Output Volume Unit (V₁)", list(VOLUME_UNITS.keys()))

        if st.button("Calculate Volume (V₁)"):
            if C1 == 0 or C2 == 0 or V2 == 0:
                st.error("All values must be greater than zero.")
            elif C2 > C1:
                st.error("Target concentration cannot exceed stock concentration.")
            else:
                C1_base = convert_conc(C1, C1_unit)
                C2_base = convert_conc(C2, C2_unit)
                V2_base = convert_vol(V2, V2_unit)

                V1_uL = (C2_base * V2_base) / C1_base
                V1_out = convert_vol(V1_uL, output_unit, to_base=False)

                st.success(f"You need {V1_out:.2f} {output_unit} of {C1} {C1_unit} solution.")
                st.caption(f"Dilute it to {V2:.2f} {V2_unit} to get {C2:.2f} {C2_unit}.")

    elif calc_type == "Mass in Given Volume":
        conc = st.number_input("Concentration", min_value=0.0, step=0.1, format="%.4f")
        conc_unit = st.selectbox("Concentration Unit", list(CONCENTRATION_UNITS.keys()))

        vol = st.number_input("Volume", min_value=0.0, step=0.1, format="%.4f")
        vol_unit = st.selectbox("Volume Unit", list(VOLUME_UNITS.keys()))

        if st.button("Calculate Mass"):
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

            st.success(f"Mass: {mass:.3f} {unit}")
            st.caption(f"From {conc:.2f} {conc_unit} × {vol:.2f} {vol_unit}")
def cc():
    st.info("Use:\nEstimate bacterial concentration in original sample after plating.\nCommon in: microbiology, antibiotic testing, fermentation.")

    colonies = st.number_input("Number of Colonies Counted", min_value=0, step=1)
    dilution_factor = st.number_input("Dilution Factor (e.g., 1:1000 → enter 1000)", min_value=1.0, step=1.0)
    plated_volume = st.number_input("Volume Plated (in mL)", min_value=0.0001, step=0.0001, format="%.4f")

    if st.button("Calculate CFU/mL"):
        if colonies == 0 or plated_volume == 0:
            st.error("Colony count and volume plated must be greater than zero.")
        else:
            cfu_per_mL = (colonies * dilution_factor) / plated_volume
            st.success(f"Estimated concentration: **{cfu_per_mL:.2e} CFU/mL**")
            st.caption(f"Based on {colonies} colonies at 1:{int(dilution_factor)} dilution and {plated_volume} mL plated.")
def gdf():
    st.info("Use:\nCalculate how much dilution occurred based on initial volume and final total volume.\nCommon in: buffer prep, enzyme assays, reagent use.")

    stock_volume = st.number_input("Volume of Stock Used", min_value=0.0001, step=0.1, format="%.4f")
    final_volume = st.number_input("Final Volume after Dilution", min_value=0.0001, step=0.1, format="%.4f")
    unit = st.selectbox("Select Unit", list(VOLUME_UNITS.keys()))  # Uses your unified volume unit map

    if st.button("Calculate Dilution Factor"):
        stock_vol_uL = convert_vol(stock_volume, unit)
        final_vol_uL = convert_vol(final_volume, unit)

        if final_vol_uL <= stock_vol_uL:
            st.error("Final volume must be greater than stock volume to indicate dilution.")
        else:
            dilution_factor = final_vol_uL / stock_vol_uL
            st.success(f"Dilution Factor: **1:{dilution_factor:.2f}**")
            st.caption(f"You diluted {stock_volume:.2f} {unit} up to {final_volume:.2f} {unit}, giving a 1:{dilution_factor:.2f} dilution.")