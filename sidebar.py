import streamlit as st


def side_barfunc():
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
