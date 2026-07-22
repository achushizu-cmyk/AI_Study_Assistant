"""
pages/settings.py
--------------------
Settings page: student profile, API key status check, and data management
(clearing history/uploads for the current student).
"""

import streamlit as st

from config import GEMINI_API_KEY, GEMINI_MODEL_NAME, APP_NAME


def render(db):
    st.title("⚙️ Settings")

    st.subheader("👤 Student Profile")
    name_input = st.text_input(
        "Your name",
        value=st.session_state.get("student_name", ""),
        placeholder="Enter your full name",
    )
    if st.button("💾 Save Name"):
        st.session_state["student_name"] = name_input.strip()
        if name_input.strip():
            db.ensure_student(name_input.strip())
            st.success(f"Saved! You are now logged in as **{name_input.strip()}**.")
        st.rerun()

    st.divider()

    st.subheader("🔑 AI Configuration")
    if GEMINI_API_KEY:
        st.success(f"Gemini API key detected. Using model: `{GEMINI_MODEL_NAME}`")
    else:
        st.error(
            "Gemini API key not found. Add `GEMINI_API_KEY` to your `.env` file "
            "(local) or to Streamlit secrets (cloud deployment)."
        )

    st.divider()

    st.subheader("🗑️ Data Management")
    student_name = st.session_state.get("student_name", "")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear My Quiz History", use_container_width=True):
            if student_name:
                db.clear_history(student_name)
                st.success("Quiz history cleared.")
            else:
                st.warning("Enter your name first.")
    with col2:
        if st.button("Clear My Uploads", use_container_width=True):
            if student_name:
                db.clear_uploads(student_name)
                st.success("Upload records cleared.")
            else:
                st.warning("Enter your name first.")

    st.divider()
    st.caption(f"{APP_NAME} — Settings are stored locally in your browser session and the app's SQLite database.")
