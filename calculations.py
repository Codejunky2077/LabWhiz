#imports
import streamlit as st
import math
from unit import CONCENTRATION_UNITS,VOLUME_UNITS,convert_vol,convert_conc
from Molarmass import compoundmass
from normality_dic import chemical_data

#different calculation functions
def simpledilution():
    st.info("💡 Fill any 3 of C₁, V₁, C₂, V₂ to get the 4th value. *Leave both value and unit empty for the one you want to calculate.*")

    # --- Input Change Tracking ---
    for key in ("C1", "V1", "C2", "V2"):
        if st.session_state.get(key) != st.session_state.get(f"_prev_{key}", None):
            st.session_state.result_value = None
            st.session_state.result_type = None
            st.session_state.missing_key = None
            st.session_state[f"_prev_{key}"] = st.session_state.get(key)

    # --- INPUT GRID ---
    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            c1_col1, c1_col2 = st.columns([2, 1])
            C1 = c1_col1.text_input("Initial Concentration (C₁)", key="C1")
            with c1_col2:
                st.caption("C₁ unit")
                C1_unit = st.selectbox("", CONCENTRATION_UNITS, key="C1_unit", label_visibility="collapsed")

        with st.container():
            v1_col1, v1_col2 = st.columns([2, 1])
            V1 = v1_col1.text_input("Stock Volume (V₁)", key="V1")
            with v1_col2:
                st.caption("V₁ unit")
                V1_unit = st.selectbox("", VOLUME_UNITS, key="V1_unit", label_visibility="collapsed")

    with col2:
        with st.container():
            c2_col1, c2_col2 = st.columns([2, 1])
            C2 = c2_col1.text_input("Final Concentration (C₂)", key="C2")
            with c2_col2:
                st.caption("C₂ unit")
                C2_unit = st.selectbox("", CONCENTRATION_UNITS, key="C2_unit", label_visibility="collapsed")

        with st.container():
            v2_col1, v2_col2 = st.columns([2, 1])
            V2 = v2_col1.text_input("Final Volume (V₂)", key="V2")
            with v2_col2:
                st.caption("V₂ unit")
                V2_unit = st.selectbox("", VOLUME_UNITS, key="V2_unit", label_visibility="collapsed")

    # --- VALIDATION ---
    inputs = {"C1": C1, "V1": V1, "C2": C2, "V2": V2}
    filled = [k for k, v in inputs.items() if v.strip() != ""]
    if len(filled) < 3:
        st.info("👈 Fill any 3 fields to find the missing one.")
        return
    if len(filled) > 3:
        st.warning("⚠️ Please fill exactly 3 fields, leaving the 4th blank.")
        return

    missing = [k for k in inputs if k not in filled][0]
    st.success(f"Click 'Calculate' to find value of: **{missing}**")

    # --- CALCULATION ---
    if st.button("🚀 Calculate"):
        try:
            if "C1" not in (missing,):
                C1_val = float(C1.strip())
                if C1_val <= 0:
                    raise ValueError("C₁ must be > 0")
                C1_u = convert_conc(C1_val, C1_unit)

            if "C2" not in (missing,):
                C2_val = float(C2.strip())
                if C2_val <= 0:
                    raise ValueError("C₂ must be > 0")
                C2_u = convert_conc(C2_val, C2_unit)

            if "V1" not in (missing,):
                V1_val = float(V1.strip())
                if V1_val <= 0:
                    raise ValueError("V₁ must be > 0")
                V1_u = convert_vol(V1_val, V1_unit)

            if "V2" not in (missing,):
                V2_val = float(V2.strip())
                if V2_val <= 0:
                    raise ValueError("V₂ must be > 0")
                V2_u = convert_vol(V2_val, V2_unit)
        except ValueError:
            st.error("❌ Input error: fill valid numericals.")
            return
        except Exception:
            st.error("❌ Unexpected input error. Check your values.")
            return

        # Warnings (not errors)
        if "C1" not in (missing,) and "C2" not in (missing,) and C2_u > C1_u:
            st.warning("⚠️ You're concentrating the solution (C₂ > C₁). This is not a dilution.")
        if "V1" not in (missing,) and "V2" not in (missing,) and V2_u < V1_u:
            st.warning("⚠️ You're concentrating the solution (V₂ < V₁). This is not a dilution.")

        # Compute missing value
        try:
            if missing == "C1":
                raw = (C2_u * V2_u) / V1_u
                result_type = "conc"
            elif missing == "C2":
                raw = (C1_u * V1_u) / V2_u
                result_type = "conc"
            elif missing == "V1":
                raw = (C2_u * V2_u) / C1_u
                result_type = "vol"
            elif missing == "V2":
                raw = (C1_u * V1_u) / C2_u
                result_type = "vol"

            st.session_state.result_value = raw
            st.session_state.result_type = result_type
            st.session_state.missing_key = missing
        except ZeroDivisionError as zde:
            st.error(f"❌ Math error: {zde}")
            return
        except:
            st.error("❌ Calculation failed unexpectedly.")
            return

    # --- DISPLAY RESULT ---
    if st.session_state.get("result_value") is not None:
        if st.session_state.result_type == "conc":
            unit = st.selectbox("Select concentration unit", CONCENTRATION_UNITS, key="out_u")
            display = convert_conc(st.session_state.result_value, unit, to_base=False)
        else:
            unit = st.selectbox("Select volume unit", VOLUME_UNITS, key="out_u")
            display = convert_vol(st.session_state.result_value, unit, to_base=False)

        st.success(f"✅ **{st.session_state.missing_key} = {display:.4f} {unit}**")
        st.markdown(r"**Formula:** $C_1 \cdot V_1 = C_2 \cdot V_2$")

        # --- HISTORY ---
        try:
            known = {
                "C1": (C1, C1_unit),
                "V1": (V1, V1_unit),
                "C2": (C2, C2_unit),
                "V2": (V2, V2_unit)
            }
            known_values = [float(known[k][0]) for k in known if k != missing]
            known_units = [known[k][1] for k in known if k != missing]
            known_labels = [k for k in known if k != missing]

            result_text = f"Simple Dilution → {known_labels[0]}={known_values[0]:.2f} {known_units[0]}, {known_labels[1]}={known_values[1]:.2f} {known_units[1]} → {missing}={display:.2f} {unit}"

            if "LabWhiz_history" not in st.session_state:
                st.session_state.LabWhiz_history = []
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]
        except:
            pass  # Silent fail on history
def molarity():
    st.info("Use: Quickly calculate how much solute is needed to make a solution of desired molarity. Common in: solution prep, reagents, buffers, and media preparation.")

    molarity_str = st.text_input("Desired molarity (mol/L)", placeholder="e.g. 0.2M of NaOH", key="mol_molarity")
    volume_str = st.text_input("Enter volume", placeholder="e.g. 1000", key="mol_volume")
    volume_unit = st.selectbox("Enter the unit of volume", list(VOLUME_UNITS))
    compound = st.selectbox("Choose compound to enter Molecular weight(g/mol)", list(compoundmass.keys()), index=0)
    if compound !="Custom":
        mw_str=compoundmass[compound]
    else:
        mw_str = st.text_input("Enter Molecular weight (g/mol)", placeholder="e.g. 58.44 g/mol of NaCl", key="mol_mw")

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
            st.markdown(r"**Formula:**$ M = \dfrac{\text{moles}}{\text{liters of solution}}$")

            # Add to history
            result_text = f"Molarity={molarity:.4f} M × Vol={volume:.2f} {volume_unit} with g/mol={mw:.2f} → {mass_out:.3f} {unit}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in molarity calculation please use numericals.")
def wv():
    st.info("Use: To prepare a solution where a solid is dissolved in a liquid (e.g., NaCl, glucose).")

    percent_str = st.text_input("Enter desired concentration (% w/v)", placeholder="e.g. 68 ", key="wv_percent")
    volume_str = st.text_input("Enter total volume", placeholder="e.g. 250 ml of solution", key="wv_volume")
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
            st.markdown(r"**Formula:** $\text{Mass (g)} = \dfrac{\%\ \text{w/v} \times \text{Volume (mL)}}{100}$")

            # Add to history
            result_text = f"W/V\n {percent:.2f}% in Vol={volume:.2f} {volume_unit} → Mass={mass_out:.3f} {unit}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in w/v calculation please use numericals.")
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
            st.markdown(r"**Formula:** $\text{Solute Volume} = \dfrac{\%\ \text{v/v} \times \text{Total Volume}}{100}$")

            # Add to history
            result_text = f"v/v\n {percent:.2f}% in Vol={volume:.2f} {volumeunit} → soluteVol={solute_volume_out:.2f} {unit}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in v/v calculation please use numericals.")
def md():
    st.info("Use:\nDilute a molar solution from a concentrated stock.\nCommon in buffer preparation, titrations, and chemical reactions.")

    M1_str = st.text_input("Initial Molarity (M₁)", placeholder="e.g. 3.0M of NaCl", key="md_m1")
    M2_str = st.text_input("Target Molarity (M₂)", placeholder="e.g. 0.1M of NaCl", key="md_m2")

    V2_str = st.text_input("Final Volume (V₂)", placeholder="e.g. 100 ml of volume", key="md_v2")
    V2_unit = st.selectbox("V₂ Unit", list(VOLUME_UNITS.keys()))

    output_unit = st.selectbox("Initial needed Volume Unit (V₁)", list(VOLUME_UNITS.keys()))

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
            st.markdown(r"**Formula:**$ V_1 = \dfrac{M_2 \times V_2}{M_1}$")

            # Add to history
            result_text = f"Molarity Dilution\n M1={M1:.2f} M → M2={M2:.2f} M in V2={V2:.2f} {V2_unit} → need V1={V1_out:.2f} {output_unit}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in molarity dilution please use numericals.")
def Biomolecule_Dilution():
    st.info("Use:\nDilute nucleic acids or proteins to desired working concentrations.\nCommon in PCR, gel loading, extractions, assays.")
    calc_type = st.radio("Choose what you want to calculate:", ["Dilution Volume (C₁×V₁ = C₂×V₂)", "Mass in Given Volume"], help="Two types of problem arise from wet lab here both types are given.")

    if calc_type == "Dilution Volume (C₁×V₁ = C₂×V₂)":
        col1, col2, col3 = st.columns(3)
        with col1:
            C1_str = st.text_input("Stock Concentration (C₁)", placeholder="e.g. 4", key="drp_c1")
            C1_unit = st.selectbox("C₁ Unit", list(CONCENTRATION_UNITS.keys()))
        with col2:
            C2_str = st.text_input("Target Concentration (C₂)", placeholder="e.g. 1.23", key="drp_c2")
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
                st.markdown(r"**Formula:**$ V_1 = \dfrac{C_2 \times V_2}{C_1}$")


                result_text = f"DRP Dilution\n C1={C1:.2f} {C1_unit} → C2={C2:.2f} {C2_unit} in V2={V2:.2f} {V2_unit} → need V1={V1_out:.2f} {output_unit}"
                st.session_state.LabWhiz_history.insert(0, result_text)
                st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

            except Exception as e:
                st.error(f"Error in biomolecule dilution please use numericals.")

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
                st.markdown(r"**Formula:**$ \text{Mass} = \text{Concentration} \times \text{Volume}$")


                result_text = f"DRP Mass\n con={conc:.2f} {conc_unit} × vol={vol:.2f} {vol_unit} → mass={mass:.3f} {unit}"
                st.session_state.LabWhiz_history.insert(0, result_text)
                st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

            except Exception as e:
                st.error("Error in mass calculation please use numericals.")
def cc():
    st.info("Use:\nEstimate bacterial concentration in original sample after plating.\nCommon in: microbiology, antibiotic testing, fermentation.")

    colonies_str = st.text_input("Number of Colonies Counted", placeholder="e.g. 87 number of Streptococcus pneumoniae colonies", key="cc_colonies")
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
            st.markdown(r"**Formula:**$ \text{CFU/mL} = \dfrac{\text{Colonies} \times \text{Dilution Factor}}{\text{Volume Plated (mL)}}$")

            result_text = f"CFU Count\n {colonies} colonies at 1:{int(dilution_factor)} → {cfu_per_mL:.2e} CFU/mL"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Error in CFU calculation please use numericals.")
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
                st.markdown(r"**Formula:** $\text{DF} = \dfrac{\text{Final Volume}}{\text{Stock Volume}}$")

                # Save to history
                result_text = f"Dilution Factor\n stock={stock_volume:.2f} {unit} → final={final_volume:.2f} {unit} → 1:{dilution_factor:.2f}"
                st.session_state.LabWhiz_history.insert(0, result_text)
                st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except (ValueError, TypeError):
            st.error("Please enter valid numerical values.")
        except Exception as e:
            st.error(f"Error in dilution factor calculation please use numericals.")
def molality():
    st.info("Use: Calculate molality (mol/kg solvent). Useful when temperature affects volume — like in boiling point elevation or freezing point depression.")

    moles_str = st.text_input("Amount of solute (in moles)", placeholder="e.g. 0.5 moles of HCl", key="molality_moles")
    solvent_mass_str = st.text_input("Mass of solvent (in kg)", placeholder="e.g. 0.2kg of distilled water", key="molality_solvent")

    if st.button("🧪 Calculate Molality"):
        try:
            moles = float(moles_str)
            solvent_mass = float(solvent_mass_str)

            if moles <= 0 or solvent_mass <= 0:
                st.error("Both values must be greater than zero.")
                return

            molality_value = moles / solvent_mass
            st.success(f"✅ Molality: {molality_value:.4f} mol/kg")
            st.caption(f"Molality = Moles of solute ÷ kg of solvent = {moles:.4f} ÷ {solvent_mass:.4f}")
            st.markdown(r"**Formula:** $ molality= \dfrac{\text{moles of solute}}{\text{kg of solvent}}$")


            result_text = f"Molality\n Moles={moles:.4f}, Solvent={solvent_mass:.4f} kg → Molality={molality_value:.4f} mol/kg"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error("Error in molality calculation enter valid numericals.")
def normality():
    st.info("Use: Calculate normality (N) from molarity (M) and equivalent weight. Based on actual chemistry.")

    molarity_str = st.text_input("Enter Molarity (mol/L)", placeholder="e.g. 0.5 for 0.5M HCl", key="norm_m")
    compound = st.selectbox("Select compound from list", list(chemical_data.keys()), index=0, help="Select and autofill compounds from list and all parameters will be autofilled or give specific inputs through custom.")

    valid_custom_inputs = True

    if compound != "Custom":
        molar_mass = chemical_data[compound]["molar_mass"]
        n_factor = chemical_data[compound]["n_factor"]

        if n_factor > 0:
            equivalent_weight = molar_mass / n_factor
            st.markdown(f"""
            **Selected Compound:** `{compound}`  
            • Molar Mass = `{molar_mass} g/mol`  
            • n-factor = `{n_factor}`  
            • Equivalent Weight = `{equivalent_weight:.3f} g/mol`
            """)
        else:
            st.error("⚠️ n-factor must be greater than 0.")
            return

    else:
        custom_mm = st.text_input("Enter Molar Mass (g/mol)", placeholder="e.g. 40.00 for NaOH", key="custom_mm")
        custom_nf = st.text_input("Enter n-factor", placeholder="e.g. 1 for NaOH", key="custom_nf")

        try:
            if not custom_mm.strip() or not custom_nf.strip():
                valid_custom_inputs = False
                raise ValueError

            molar_mass = float(custom_mm)
            n_factor = float(custom_nf)

            if molar_mass <= 0 or n_factor <= 0:
                st.error("⚠️ Molar mass and n-factor must be greater than 0.")
                return

            equivalent_weight = molar_mass / n_factor
            st.markdown(f"**Equivalent Weight (Custom):** {equivalent_weight:.3f} g/mol")

        except ValueError:
            st.info("Please enter numerical values for molar mass and n-factor.")
            return

    if st.button("🧪 Calculate Normality"):
        try:
            if not molarity_str.strip():
                st.warning("Please enter a valid molarity value.")
                return

            molarity = float(molarity_str)

            if molarity <= 0 or equivalent_weight <= 0:
                st.error("All values must be greater than zero.")
                return

            normality = molarity * n_factor

            st.success(f"✅ Normality: {normality:.3f} N")
            st.caption(f"Computed using: N = M / (Eq. Wt) = {molarity:.3f} / ({molar_mass:.3f} / {n_factor}) = {normality:.3f}")
            st.markdown(r"**Formula:** $N = \frac{M}{\frac{Molar\ Mass}{n\text{-}factor}}$")

            result_text = f"Normality of {compound}: M={molarity:.3f}, EqW={equivalent_weight:.3f} → N={normality:.3f}"
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except ValueError:
            st.error("⚠️ Invalid molarity input. Please enter a valid number.")

def serialdilution():
    st.info("Use: When very high dilutions (e.g., 1:10000) are needed via multiple steps. Common in microbiology/pharmacology.")

    col1, col2 = st.columns(2)
    with col1:
        C1_str = st.text_input("Initial Concentration (C₁)", placeholder="e.g. 100", key="serial_c1")
        C1_unit = st.selectbox("C₁ Unit", list(CONCENTRATION_UNITS.keys()))
    with col2:
        C2_str = st.text_input("Desired Final Concentration (C₂)", placeholder="e.g. 0.01", key="serial_c2")
        C2_unit = st.selectbox("C₂ Unit", list(CONCENTRATION_UNITS.keys()))

    dilution_factor_str = st.text_input("Dilution Ratio per Step (e.g., 1:10 → enter 10)", placeholder="e.g. 10", key="serial_ratio")
    volume_stock_str = st.text_input("Volume taken per Step (µL)", placeholder="e.g. 100", key="serial_vstock")
    volume_diluent_str = st.text_input("Diluent Volume per Step (µL)", placeholder="e.g. 900", key="serial_vdiluent")

    if st.button("🚀 Calculate number of steps"):
        try:
            # --- Input checks ---
            inputs = [C1_str, C2_str, dilution_factor_str, volume_stock_str, volume_diluent_str]
            if any(x.strip() == "" for x in inputs):
                st.error("All fields are required.")
                return

            try:
                C1_val = float(C1_str.strip())
                C2_val = float(C2_str.strip())
                dilution_factor = float(dilution_factor_str)
                volume_stock = float(volume_stock_str)
                volume_diluent = float(volume_diluent_str)
            except ValueError:
                st.error("Please enter valid numbers in all fields.")
                return

            try:
                C1_norm = convert_conc(C1_val, C1_unit)
                C2_norm = convert_conc(C2_val, C2_unit)
            except Exception as e:
                st.error(f"Unit conversion error: {e}")
                return

            if any(x <= 0 for x in [C1_norm, C2_norm, dilution_factor, volume_stock, volume_diluent]):
                st.error("All inputs must be greater than zero.")
                return
            if C2_norm >= C1_norm:
                st.error("Final concentration must be lower than starting concentration.")
                return

            # --- Ratio check ---
            try:
                actual_ratio = (volume_stock + volume_diluent) / volume_stock
                if abs(actual_ratio - dilution_factor) > 0.05:
                    st.warning(f"⚠️ Volume-based ratio {actual_ratio:.2f} ≠ entered ratio {dilution_factor:.2f}. Fix for accuracy.")
            except ZeroDivisionError:
                st.error("Stock volume cannot be zero.")
                return

            # --- Step math ---
            total_dilution = C1_norm / C2_norm
            exact_steps = math.log(total_dilution) / math.log(dilution_factor)
            floor_steps = math.floor(exact_steps)
            ceil_steps = math.ceil(exact_steps)

            conc_floor = C1_norm / (dilution_factor ** floor_steps) if floor_steps >= 0 else None
            conc_ceil = C1_norm / (dilution_factor ** ceil_steps) if ceil_steps >= 0 else None

            # Pick closer outcome
            options = []
            if conc_floor: options.append((floor_steps, conc_floor))
            if conc_ceil: options.append((ceil_steps, conc_ceil))
            steps_needed, nearest_conc = min(options, key=lambda x: abs(x[1] - C2_norm))

            # --- Tolerance & correction ---
            tolerance = 0.05  # ±5% allowed
            if abs(nearest_conc - C2_norm) / C2_norm <= tolerance:
                # Close enough → no correction
                actual_final_user = nearest_conc / CONCENTRATION_UNITS[C2_unit]
                st.success(f"✅ Do {steps_needed} step(s) of 1:{dilution_factor}. Final ≈ {actual_final_user:.4f} {C2_unit} (target {C2_val} {C2_unit}).")
                st.caption(f"Each step: {volume_stock:.0f} µL + {volume_diluent:.0f} µL diluent")
            else:
                # Needs correction dilution
                correction_factor = nearest_conc / C2_norm  # overall dilution required
                # Example pipetting volumes (scale from volume_stock)
                corr_stock = volume_stock
                corr_diluent = corr_stock * (correction_factor - 1)

                actual_final_user = C2_norm / CONCENTRATION_UNITS[C2_unit]
                st.success(
                    f"✅ Do {steps_needed} step(s) of 1:{dilution_factor} → {nearest_conc/CONCENTRATION_UNITS[C2_unit]:.4f} {C2_unit}.\n"
                    f"Then correct with a final 1:{correction_factor:.2f} dilution to hit {actual_final_user:.4f} {C2_unit}."
                )
                st.caption(
                    f"Correction step: {corr_stock:.0f} µL stock + {corr_diluent:.0f} µL diluent"
                )

            # --- History log ---
            result_text = (
                f"Serial Dilution: {C1_val:.2f} {C1_unit} → target {C2_val:.4f} {C2_unit} "
                f"(step factor {dilution_factor}, stock {volume_stock} µL, diluent {volume_diluent} µL)"
            )
            st.session_state.LabWhiz_history.insert(0, result_text)
            st.session_state.LabWhiz_history = st.session_state.LabWhiz_history[:5]

        except Exception as e:
            st.error(f"Unexpected error: {e}")
