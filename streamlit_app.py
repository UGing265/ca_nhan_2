# streamlit_app.py

import streamlit as st
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
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
st.header("1.Enter Source Code")

# Language selection
supported_languages = ["Auto-detect", "python", "javascript", "java", "csharp", "cpp", "go", "ruby", "typescript", "php", "swift"]
# Ensure 'selected_language' is initialized in session state
if 'selected_language' not in st.session_state:
    st.session_state['selected_language'] = 'Auto-detect'

# Choose language:
selected_language_option = st.selectbox(
    "Select the programming language:",
    options=supported_languages,
    index=supported_languages.index(get_session_data('selected_language')) # Default to Auto-detect
)
set_session_data('selected_language', selected_language_option)

st.header("1. Enter Source Code")

code_input = st.text_area(
    f"Paste the code to be reviewed here:",
    height=300,
    value=get_session_data('code_input')
)
set_session_data('code_input', code_input)

if st.button("🚀 Run Review & Repair"):
    if not code_input.strip():
        st.error("Please enter the source code to run the review.")
    else:
        with st.spinner("Running Review Agent and Repair Agent..."):
            language_to_use = selected_language_option
            if language_to_use == "Auto-detect":
                try:
                    lexer = guess_lexer(code_input)
                    language_to_use = lexer.aliases[0]
                    st.info(f"Detected language: {language_to_use}")
                except ClassNotFound:
                    language_to_use = "python" # fallback to python
                    st.warning("Could not auto-detect language. Falling back to Python. Please select the language manually for better results.")

            # Run the entire stream
            review_results, repaired_code = run_code_review_workflow(code_input, language_to_use)

            # Update session state
            set_session_data('review_results', review_results)
            set_session_data('repaired_code', repaired_code)
            set_session_data('final_language', language_to_use)
            
            # Add to history
            add_to_history(code_input, review_results, repaired_code)
            
            st.success("✅ Review completed and saved to history!")

# --- Output Section ---
st.header("2. Result")

review_results = get_session_data('review_results')
repaired_code = get_session_data('repaired_code')
final_language = get_session_data('final_language') or get_session_data('selected_language') or 'text'

# If no review run yet, guide the user
if review_results is None:
    st.info("No review has been run yet. Paste your code above and click 'Run Review & Repair'.")
else:
    # If there are findings, display them
    if review_results:
        display_review_results(review_results)
    else:
        # Announce success when there are no issues
        st.success("✅ No issues found. The code looks correct.")
        st.subheader("Original Code:")
        st.code(code_input or get_session_data('code_input') or "", language=final_language)

    # If repair produced a result, show the diff and final code
    if repaired_code:
        display_code_diff(code_input, repaired_code)

        # Show last repaired code
        st.subheader("The code has been completely repaired:")
        st.code(repaired_code, language=final_language)