import json

import streamlit as st

from components import setup_column_1, setup_column_2
from setup_lifespan import set_session_state

set_session_state()


with st.sidebar:

    url = st.text_input("Input backend url", value="http://103.20.97.119:8080")
    st.session_state["url"] = url

    with st.expander("Settings"):
        # Slider for K_neighbors
        K_neighbors = st.slider(
            "Number of Neighbors (K_neighbors)",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="Adjust the number of nearest neighbors to retrieve.",
            key="text_search",
        )
        st.session_state["top_k"] = K_neighbors

        # Checkbox for high_performance
        embed_model_list = ["CLIP", "BLIP"]
        high_performance = st.radio(
            "You can choose CLIP-based or BLIP-based",
            embed_model_list,
            index=embed_model_list.index("BLIP"),
        ).lower()
        print(high_performance)
        st.session_state["high_performance"] = high_performance

        mode = st.slider(
            "Mode of algorithm",
            min_value=0,
            max_value=8,
            step=1,
            help="Adjust mode the change the fuzzy matching algorithm.",
            key="ocr_search_fuzzy_matching",
        )
        st.session_state["mode"] = mode

    st.write("---")
    st.write("App created by AIO_TOP10")
# Title with gradient and centered
st.markdown(
    """
    <h1 style='text-align: center;'>Image Retrieval System - AIC2024</h1>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 2])

with col1:
    setup_column_1()

with col2:
    setup_column_2()

# Handle copying to clipboard
if st.session_state["copy_to_clipboard"]:
    js_button_label = json.dumps(st.session_state["copy_to_clipboard"])
    js_code = f"""
    <script>
    navigator.clipboard.writeText({js_button_label});
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)
    # Reset copy_to_clipboard after copying
    st.session_state["copy_to_clipboard"] = None
