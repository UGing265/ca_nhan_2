# utils/history_manager.py
# (Role: Frontend Logic) 
# Manages chat history persistence (load/save to JSON file)

import json
import streamlit as st
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


HISTORY_FILE = Path("data/review_history.json")


def init_history():
    """Initialize history in session state."""
    if "history" not in st.session_state:
        st.session_state.history = load_history()


def load_history() -> List[Dict]:
    """Load chat history from JSON file."""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")
    return []


def save_history(history: List[Dict]) -> bool:
    """Save chat history to JSON file."""
    try:
        HISTORY_FILE.parent.mkdir(exist_ok=True)  # Create data/ folder if not exists
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving history: {e}")
        return False


def add_to_history(code_input: str, review_results, repaired_code: Optional[str] = None) -> None:
    """Add new review session to history."""
    if "history" not in st.session_state:
        st.session_state.history = []
    
    history_item = {
        "timestamp": datetime.now().isoformat(),
        "code_input": code_input,
        "review_results": review_results,
        "repaired_code": repaired_code
    }
    
    st.session_state.history.append(history_item)
    
    # Auto-save after adding
    save_history(st.session_state.history)


def get_history() -> List[Dict]:
    """Get current history from session state."""
    return st.session_state.get("history", [])


def clear_history() -> bool:
    """Clear all history."""
    try:
        st.session_state.history = []
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        return True
    except Exception as e:
        print(f"Error clearing history: {e}")
        return False
