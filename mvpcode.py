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

       # --- Simple Dilution --- #
    if type == "Simple dilution":
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
    elif type == "Serial dilution": # --- Serial Dilution --- #
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
    elif type =="Molarity":#--Molarity--#
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

if __name__ == '__main__':
    BufferBuddy()
