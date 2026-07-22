"""
pages/summary.py
-------------------
Summary page: generates a concise summary, key points and important topics
for the currently loaded document.
"""

import streamlit as st

from utils import ai_engine
from utils.gemini_client import GeminiClientError


def render(db):
    st.title("📝 Summary & Key Points")

    text = st.session_state.get("extracted_text", "")
    if not text:
        st.warning("No document loaded yet. Please upload a file first from the **Upload** page.")
        return

    st.caption(f"Summarizing: **{st.session_state.get('current_file_name', 'your document')}**")

    tab_summary, tab_points, tab_topics = st.tabs(["📄 Summary", "🔑 Key Points", "⭐ Important Topics"])

    with tab_summary:
        if st.button("✨ Generate Summary", type="primary", key="btn_summary"):
            with st.spinner("Summarizing content..."):
                try:
                    st.session_state["summary_text"] = ai_engine.generate_summary(text)
                except GeminiClientError as exc:
                    st.error(str(exc))
        if st.session_state.get("summary_text"):
            st.markdown(st.session_state["summary_text"])

    with tab_points:
        if st.button("✨ Generate Key Points", type="primary", key="btn_points"):
            with st.spinner("Extracting key points..."):
                try:
                    st.session_state["key_points_text"] = ai_engine.generate_key_points(text)
                except GeminiClientError as exc:
                    st.error(str(exc))
        if st.session_state.get("key_points_text"):
            st.markdown(st.session_state["key_points_text"])

    with tab_topics:
        if st.button("✨ Generate Important Topics", type="primary", key="btn_topics"):
            with st.spinner("Identifying important topics..."):
                try:
                    st.session_state["topics_text"] = ai_engine.generate_important_topics(text)
                except GeminiClientError as exc:
                    st.error(str(exc))
        if st.session_state.get("topics_text"):
            st.markdown(st.session_state["topics_text"])
