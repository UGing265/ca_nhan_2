# \ca_nhan_2\streamlit_app.py
import streamlit as st
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from utils.config import Config
from utils.session_manager import initialize_session_state, get_session_data, set_session_data
from utils.ui_helpers import display_review_results, display_code_diff
from agents.workflow import run_code_review_workflow
import io

initialize_session_state()
st.set_page_config(page_title=Config.APP_TITLE, layout="wide")
st.header("🔍 Code Review & Repair Agent")
st.markdown("AI-powered code analysis and automatic bug fixing")
st.image("static/fighting_chicks.jpg", width=100)
st.subheader("1. Input Source Code")

input_tabs = st.tabs(["📝 Paste Code", "📤 Upload File"])

# TAB 1: PASTE CODE
with input_tabs[0]:
    language_paste = st.selectbox(
        "Select Language:",
        ["python", "javascript", "typescript", "java", "c++", "csharp", "go", "rust", "Auto-detect"],
        key="language_paste_select",
        index=0,
        help="Choose the programming language of your code"
    )
    code_input_paste = st.text_area(
        "Paste your code here:",
        height=300,
        key="code_paste_area"
    )
    if st.button("🚀 Analyze Pasted Code", key='run_paste', use_container_width=True):
        if not code_input_paste.strip():
            st.error("❌ Please paste some code first!")
        else:
            final_language = language_paste
            if final_language=="Auto-detect":
                try:
                    final_language = guess_lexer(code_input_paste).aliases[0]
                    st.info(f"Detected language: {final_language}")
                except ClassNotFound:
                    final_language = 'python'
                    st.warning("Could not auto-detect language. Falling back to Python.")
            with st.spinner(f"🔍 Analyzing {final_language} code..."):
                review_results, repaired_code = run_code_review_workflow(code_input_paste, final_language)
                set_session_data('review_results', review_results)
                set_session_data('repaired_code', repaired_code)
                set_session_data('final_language', final_language)
                set_session_data('current_code_for_display', code_input_paste)

# TAB 2: UPLOAD FILE
with input_tabs[1]:
    uploaded_file = st.file_uploader(
        "Upload a code file (e.g., .py, .js, .java) 📁",
        type=["py", "js", "ts", "java", "cpp", "cs", "go", "rs"],
        key="file_uploader_widget"
    )
    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        file_ext = uploaded_file.name.split('.')[-1].lower()
        ext_to_lang = {
            'py': 'python', 'js': 'javascript', 'ts': 'typescript',
            'java': 'java', 'cpp': 'c++', 'cs': 'csharp', 'go': 'go', 'rs': 'rust'
        }
        detected_language = ext_to_lang.get(file_ext, 'text')
        st.info(f"📄 File loaded: `{uploaded_file.name}` (Language: {detected_language})")
        st.code(file_content, language=detected_language, line_numbers=True)
        if st.button("🚀 Analyze Uploaded File", key='run_file', use_container_width=True):
            with st.spinner(f"🔍 Analyzing {detected_language} code..."):
                review_results, repaired_code = run_code_review_workflow(file_content, detected_language)
                set_session_data('review_results', review_results)
                set_session_data('repaired_code', repaired_code)
                set_session_data('final_language', detected_language)
                set_session_data('current_code_for_display', file_content)
    else:
        st.markdown("""
        <p style='text-align: center; color: gray; margin-top: 2rem;'>
        Drag & Drop or Click to upload your code file for analysis.
        </p>
        """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("2. Analysis Results")

review_results = get_session_data('review_results')
repaired_code = get_session_data('repaired_code')
final_language = get_session_data('final_language') or 'text'
current_code_for_display = get_session_data('current_code_for_display')

if review_results is None:
    st.info("👋 No analysis run yet. Paste or upload your code above and click 'Analyze' to get started!")
else:
    if review_results:
        # Case 1: ERRORS FOUND
        display_review_results(review_results)
        # Display the fix if available
        if repaired_code:
            display_code_diff(current_code_for_display, repaired_code)
        else:
            st.warning("⚠️ Issues were found, but the Repair Agent could not generate a fix.")
    else:
        # Case 2: NO ERRORS FOUND
        st.success("🎉 Your code passed the review. **No issues found!**")
        st.subheader("✔️ Original Code:")
        st.code(current_code_for_display, language=final_language)