# /utils/ui_helpers.py

import streamlit as st
import difflib


def display_review_results(results):
    """Display review results as a table or list."""
    if not results:
        st.info("No issues found in the source code.")
        return

    st.subheader("🟢 Review Results:")
    for i, result in enumerate(results):
        with st.expander(f"Issue {i + 1}: {result['severity']} - {result['issue_type']}"):
            st.code(result['context'], language='python')
            st.write(f"**Line:** {result['line']}")
            st.markdown(f"**Description:** {result['description']}")
        with st.expander(f"Issue {i + 1}: {result.get('severity', 'N/A')} - {result.get('issue_type', 'General')} (Line {result.get('line', 'N/A')})"):
            st.code(result.get('context', 'No context provided'), language='python')
            st.markdown(f"**Description:** {result.get('description', 'No description.')}")


def display_code_diff(original_code, repaired_code):
    """Shows the difference between the original and modified code."""
    if not repaired_code:
        return

    st.subheader("🟢 Corrected code (Diff):")

    diff = list(difflib.unified_diff(
        original_code.splitlines(keepends=True),
        repaired_code.splitlines(keepends=True),
        lineterm=''
    ))

    # Display diff in a code box
    st.code("".join(diff), language='diff')