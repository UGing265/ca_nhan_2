# streamlit_app.py

import streamlit as st
from utils.config import Config
from utils.session_manager import initialize_session_state, get_session_data, set_session_data
from utils.ui_helpers import display_review_results, display_code_diff
from agents.workflow import run_code_review_workflow

# Initialize session state
initialize_session_state()

st.set_page_config(page_title=Config.APP_TITLE)

st.title(Config.APP_TITLE)
# st.image("static/logo.png", width=100)

# --- Input Section ---
st.header("1.Enter Source Code")

# Language selection
supported_languages = ["python", "javascript", "java", "csharp", "cpp", "go", "ruby", "typescript", "php", "swift"]
# Ensure 'selected_language' is initialized in session state
if 'selected_language' not in st.session_state:
    st.session_state['selected_language'] = 'python'

selected_language = st.selectbox(
    "Select the programming language:",
    options=supported_languages,
    index=supported_languages.index(get_session_data('selected_language')) # Default to Python
)
set_session_data('selected_language', selected_language)


code_input = st.text_area(
    f"Paste the {selected_language} code to be reviewed here:",
    height=300,
    value=get_session_data('code_input')
)
set_session_data('code_input', code_input)

if st.button("🚀 Run Review & Repair"):
    if not code_input.strip():
        st.error("Please enter the source code to run the review.")
    else:
        with st.spinner("Running Review Agent and Repair Agent..."):
            # Run the entire stream
            review_results, repaired_code = run_code_review_workflow(code_input, selected_language)

            # Update session state
            set_session_data('review_results', review_results)
            set_session_data('repaired_code', repaired_code)

# --- Output Section ---
st.header("2. Result")

review_results = get_session_data('review_results')
repaired_code = get_session_data('repaired_code')

if review_results:
    display_review_results(review_results)

if repaired_code:
    display_code_diff(code_input, repaired_code)

    # Show last repaired code
    st.subheader("The code has been completely repaired.:")
    st.code(repaired_code, language=selected_language)