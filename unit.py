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
    "μL (micro liters)": 1,
    "mL (mili liters)": 1000,
    "L (Liters)": 1_000_000
    }

# --- Conversion Functions --- #
def convert_conc(value, from_unit, to_base=True):
    factor = CONCENTRATION_UNITS[from_unit]
    return value * factor if to_base else value / factor

def convert_vol(value, from_unit, to_base=True):
    factor = VOLUME_UNITS[from_unit]
    return value * factor if to_base else value / factor

