import json
import streamlit as st

from components import setup_column_2, setup_column_1
from setup_lifespan import set_session_state

set_session_state()

st.sidebar.write("App created by AIO_TOP10")

# Title with gradient and centered
st.markdown("""
    <h1 style='text-align: center;'>Image Retrieval System - AIC2024</h1>
    """, unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    setup_column_1()

with col2:
    setup_column_2()

# Handle copying to clipboard
if st.session_state['copy_to_clipboard']:
    js_button_label = json.dumps(st.session_state['copy_to_clipboard'])
    js_code = f"""
    <script>
    navigator.clipboard.writeText({js_button_label});
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)
    # Reset copy_to_clipboard after copying
    st.session_state['copy_to_clipboard'] = None
