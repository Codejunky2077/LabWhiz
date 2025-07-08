import streamlit as st
import math
from PIL import Image
import datetime
import streamlit.components.v1 as components
from calculations import(simpledilution,serialdilution,molarity,drpdilution,md,wv,vv,cc,gdf,normality,molality)

#giving intuitive lab tips 
import random
from wisdom import insights
if "lab_tips" not in st.session_state:
    st.session_state.lab_tips = random.choice(insights)
lab_wisdom=st.session_state.lab_tips

#web traffic analytics
st.markdown("""
            <!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "00b3ac8e9b2f42feba7acd4d35d5969a"}'></script><!-- End Cloudflare Web Analytics -->
            """, unsafe_allow_html=True)

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

#main webapp LabWhiz
def LabWhiz():
    type = st.selectbox("Select the type of calculation needed...",[
        "",
        "Simple dilution",
        "Serial dilution",
        "General Dilution Factor",
        "Molarity",
        "Normality",
        "Molality",
        "Molarity Dilution",
        "Weight/Volume(%w/v)",
        "Volume/Volume (% v/v)",
        "DNA/RNA/Protein Dilution",
        "CFU / Cell Culture Calculation"],help="Use the type of calculation u want related to your lab work.")
    
    if type =="Simple dilution":
        st.header("Simple dilution")
        simpledilution()
    elif type =="Serial dilution":
        st.header("Serial dilution")
        serialdilution()
    elif type=="Molarity":
        st.header("Molarity")
        molarity()
    elif type=="Normality":
        st.header("Normality")
        normality()
    elif type=="Molality":
        st.header("Molality")
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
    with st.sidebar.markdown(f"""
            <img src="https://img.icons8.com/fluency/96/lab-items.png" width="48" style="margin-right:10px; vertical-align: middle;" />
            <span style="font-size: 32px; font-weight: 700;">LabWhiz</span>  
            <br><br>""",unsafe_allow_html=True):

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
                                📝 Takes less than a minute!""")
    
    LabWhiz()  
