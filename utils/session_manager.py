# \ca_nhan_2\utils\session_manager.py

import streamlit as st

def initialize_session_state():
    """Initializes Streamlit session state variables."""
    if 'code_input' not in st.session_state:
        st.session_state['code_input'] = ""
    if 'review_results' not in st.session_state:
        st.session_state['review_results'] = []
    if 'repaired_code' not in st.session_state:
        st.session_state['repaired_code'] = None
    if 'selected_language' not in st.session_state:
        st.session_state['selected_language'] = "python"

def get_session_data(key):
    """Get data from session state."""
    return st.session_state.get(key)

def set_session_data(key, value):
    """Write data to session state."""
    st.session_state[key] = value