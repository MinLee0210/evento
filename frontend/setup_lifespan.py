import streamlit as st


def setup_template():
    "Setup theme, style, etc."
    st.set_page_config(layout='wide', 
                       page_title="evento",
                       page_icon="⚡️")

# TODO: Make it read from a declarative file.
def set_session_state(): 
    # Initialize session state variables
    if 'expander_content' not in st.session_state:
        st.session_state['expander_content'] = None

    if 'copy_to_clipboard' not in st.session_state:
        st.session_state['copy_to_clipboard'] = None

    if 'selected_images' not in st.session_state:
        st.session_state['selected_images'] = {}

    if 'checkbox_states' not in st.session_state:
        st.session_state['checkbox_states'] = {}

    if 'search_results' not in st.session_state:
        st.session_state['search_results'] = None

    if 'top_k' not in st.session_state: 
        st.session_state['top_k'] = None

    if 'query' not in st.session_state: 
        st.session_state['query'] = None
    
    if 'high_performance' not in st.session_state: 
        st.session_state['high_performance'] = None