"""
app.py
-------
Main entry point for the AI Study Assistant Streamlit application.

Responsible for:
    - Page configuration and global styling
    - Session-state initialization
    - Sidebar navigation between feature pages
    - Wiring the shared database instance into every page

Run with:  streamlit run app.py
"""

import streamlit as st

from config import APP_NAME, APP_ICON
from database import StudyDatabase
from utils.helpers import load_css

from app_pages import home, upload, explanation, summary, quiz, results, history, settings, about


# ----------------------------------------------------------------------
# Page configuration (must be the first Streamlit command)
# ----------------------------------------------------------------------
st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css("style.css")


# ----------------------------------------------------------------------
# Shared resources
# ----------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_database() -> StudyDatabase:
    return StudyDatabase()


db = get_database()

# ----------------------------------------------------------------------
# Session state defaults
# ----------------------------------------------------------------------
if "student_name" not in st.session_state:
    st.session_state["student_name"] = ""

# ----------------------------------------------------------------------
# Navigation configuration
# ----------------------------------------------------------------------
NAV_ITEMS = {
    "Home": ("🏠", home),
    "Upload": ("📤", upload),
    "AI Explanation": ("🧠", explanation),
    "Summary": ("📝", summary),
    "Quiz": ("🎯", quiz),
    "Results": ("📊", results),
    "History": ("📚", history),
    "Settings": ("⚙️", settings),
    "About": ("ℹ️", about),
}

with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_NAME}")
    st.text_input(
        "Student name",
        key="student_name",
        placeholder="Enter your name",
        help="Used to save your uploads and quiz history.",
    )
    st.divider()

    # Allow other pages to programmatically redirect navigation.
    default_page = st.session_state.pop("_nav_target", "Home")
    labels = list(NAV_ITEMS.keys())
    default_index = labels.index(default_page) if default_page in labels else 0

    selected_page = st.radio(
        "Navigate",
        options=labels,
        format_func=lambda label: f"{NAV_ITEMS[label][0]}  {label}",
        index=default_index,
        label_visibility="collapsed",
    )

    st.divider()
    if st.session_state.get("current_file_name"):
        st.caption(f"📄 Active document: **{st.session_state['current_file_name']}**")
    st.caption("Built with Streamlit + Gemini AI")

# ----------------------------------------------------------------------
# Render selected page
# ----------------------------------------------------------------------
_, page_module = NAV_ITEMS[selected_page]
page_module.render(db)
