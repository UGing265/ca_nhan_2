# streamlit_app.py

import streamlit as st
from utils.config import Config
from utils.session_manager import initialize_session_state, get_session_data, set_session_data
from utils.ui_helpers import display_review_results, display_code_diff, render_chat_history_sidebar
from utils.history_manager import init_history, add_to_history
from agents.workflow import run_code_review_workflow

# Initialize session state
initialize_session_state()
init_history()

st.set_page_config(page_title=Config.APP_TITLE, layout="wide")

st.title(Config.APP_TITLE)
# st.image("static/logo.png", width=100)

# Render history sidebar
render_chat_history_sidebar()

# --- Input Section ---
st.header("1. Enter Source Code")

code_input = st.text_area(
    "Paste the Python code to be reviewed here:",
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
            review_results, repaired_code = run_code_review_workflow(code_input)

            # Update session state
            set_session_data('review_results', review_results)
            set_session_data('repaired_code', repaired_code)
            
            # Add to history
            add_to_history(code_input, review_results, repaired_code)
            
            st.success("✅ Review completed and saved to history!")

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
    st.code(repaired_code, language='python')