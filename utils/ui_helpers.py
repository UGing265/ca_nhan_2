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


def render_chat_history_sidebar():
    """Render chat history in sidebar with save/clear options."""
    from utils.history_manager import get_history, save_history, clear_history
    from datetime import datetime
    
    st.sidebar.header("📜 Review History")
    
    history = get_history()
    
    if not history:
        st.sidebar.info("No history yet. Run a review to start!")
        return
    
    # Display history count
    st.sidebar.markdown(f"**Total Sessions:** {len(history)}")
    
    # Show recent items (last 5)
    st.sidebar.subheader("Recent Sessions:")
    recent_history = list(reversed(history[-5:]))
    
    for idx, item in enumerate(recent_history):
        session_num = len(history) - idx
        timestamp = item.get('timestamp', 'Unknown')
        
        # Parse timestamp for better display
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M")
        except:
            time_str = timestamp
        
        with st.sidebar.expander(f"Session #{session_num} - {time_str}"):
            # Show code preview
            code_preview = item.get('code_input', '')[:100]
            st.markdown(f"**Code Preview:**\n```python\n{code_preview}...\n```")
            
            # Show issues count
            review_results = item.get('review_results', [])
            if review_results:
                st.markdown(f"**Issues Found:** {len(review_results)}")
            else:
                st.success("✅ No issues")
            
            # Show if repaired
            if item.get('repaired_code'):
                st.info("🔧 Code was repaired")
            
            # Button to load this session
            if st.button(f"Load Session #{session_num}", key=f"load_{session_num}"):
                load_history_session(item)
    
    # Action buttons
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("💾 Save", key="save_history"):
            if save_history(history):
                st.sidebar.success("✅ Saved!")
            else:
                st.sidebar.error("❌ Save failed")
    
    with col2:
        if st.button("🗑️ Clear", key="clear_history"):
            if clear_history():
                st.sidebar.success("✅ Cleared!")
                st.rerun()
            else:
                st.sidebar.error("❌ Clear failed")


def load_history_session(session_item):
    """Load a history session into current session state."""
    from utils.session_manager import set_session_data
    
    set_session_data('code_input', session_item.get('code_input', ''))
    set_session_data('review_results', session_item.get('review_results', None))
    set_session_data('repaired_code', session_item.get('repaired_code', None))
    
    st.success("✅ History session loaded!")
    st.rerun()