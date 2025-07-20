#imports 
import streamlit as st
import math
from PIL import Image
import datetime
import streamlit.components.v1 as components
from calculations import(simpledilution,serialdilution,molarity,Biomolecule_Dilution,md,wv,vv,cc,gdf,normality,molality)
from sidebar import side_barfunc

#adding download 
# Inject the manifest and meta tags
components.html("""
                <link rel="manifest" href="https://raw.githubusercontent.com/Codejunky2077/LabWhiz/refs/heads/main/manifest.json">
                <meta name="theme-color" content="#4CAF50"/>
                <link rel="icon" href="https://raw.githubusercontent.com/Codejunky2077/LabWhiz/main/lab-items.png" type="image/png">
                """, height=0)

#web analytics
components.html(
    """<script defer data-domain="labwhiz.streamlit.app" src="https://plausible.io/js/script.outbound-links.pageview-props.tagged-events.js"></script>
    <script>window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }</script>
    """,height=0)

#giving intuitive lab tips 
import random
from wisdom import insights
if "lab_tips" not in st.session_state:
    st.session_state.lab_tips = random.choice(insights)
lab_wisdom=st.session_state.lab_tips


#history pre-setting 
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
🧠 <b>Science Wisdom/Quotes:</b> {lab_wisdom}
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

#main webapp LabWhiz
def LabWhiz():
    type = st.selectbox("Select the type of calculation needed...",[
        "",
        "Simple dilution",
        "Serial dilution",
        "General Dilution Factor",
        "Molarity(M)",
        "Normality(N)",
        "Molality(m)",
        "Molarity Dilution",
        "Weight/Volume(%w/v)",
        "Volume/Volume (% v/v)",
        "Biomolecule Dilution/Mass",
        "CFU / Cell Culture Calculation"],help="Use the type of calculation u want related to your lab work.")
    
    if type =="Simple dilution":
        st.header("Simple dilution")
        simpledilution()
    elif type =="Serial dilution":
        st.header("Serial dilution")
        serialdilution()
    elif type=="Molarity(M)":
        st.header("Molarity(M)")
        molarity()
    elif type=="Normality(N)":
        st.header("Normality(N)")
        normality()
    elif type=="Molality(m)":
        st.header("Molality(m)")
        molality()
    elif type=="Weight/Volume(%w/v)":
        st.header("Weight/Volume(%w/v)")
        wv()
    elif type=="Volume/Volume (% v/v)":
        st.header("Volume/Volume (% v/v)")
        vv()
    elif type=="Molarity Dilution":
        st.header("Molarity Dilution")
        md()
    elif type=="Biomolecule Dilution/Mass":
        st.header("Biomolecule Dilution/Mass")
        Biomolecule_Dilution()
    elif type=="CFU / Cell Culture Calculation":
        st.header("CFU / Cell Culture Calculation")
        cc()
    elif type=="General Dilution Factor":
        st.header("General Dilution Factor")
        gdf()

if __name__ == '__main__':
  side_barfunc()         
  LabWhiz()  
