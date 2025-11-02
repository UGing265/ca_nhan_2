# \ca_nhan_2\utils\ui_helpers.py

import streamlit as st
import difflib


def display_review_results(results):
    """Display detailed review results, focusing on line and reason."""
    if not results:
        st.info("No issues found in the source code. ✅")
        return

    st.subheader("⚠️ Review Results (Issues Found):")

    # Display issues summary table
    summary_data = [
        {"Severity": res.get('severity', 'N/A'), "Line": res.get('line', 'N/A'),
         "Issue Type": res.get('issue_type', 'General')}
        for res in results
    ]
    st.dataframe(summary_data, use_container_width=True, hide_index=True)

    # Display detailed issues
    for i, result in enumerate(results):
        # Clearly state the issue line and type
        header_text = f"🚨 Issue {i + 1}: {result.get('severity', 'N/A')} - {result.get('issue_type', 'General')} (Line: {result.get('line', 'N/A')})"

        with st.expander(header_text):
            # Display Reason
            st.markdown(f"**Reason:** {result.get('description', 'No description.')}")
            st.markdown("**Context Code:**")
            # Display Context Code
            st.code(result.get('context', 'No context provided'), language='python')


def display_code_diff(original_code, repaired_code):
    """Shows the difference (Fix) between the original and modified code."""
    if not repaired_code:
        st.error("❌ Review Agent found issues, but Repair Agent could not propose a fix.")
        return

    # Display the Fix (Diff)
    st.subheader("🛠️ Repaired Code (Diff/Fix):")

    diff = list(difflib.unified_diff(
        original_code.splitlines(keepends=True),
        repaired_code.splitlines(keepends=True),
        lineterm=''
    ))

    # Display diff in a code box
    st.code("".join(diff), language='diff')

    # Display the final fixed code
    st.subheader("✔️ Complete Fixed Code:")
    st.code(repaired_code, language=st.session_state.get('final_language', 'text'))