"""
pages/explanation.py
-----------------------
AI Explanation page: turns uploaded content into a Simple English or
Tanglish explanation using Gemini.
"""

import streamlit as st

from utils import ai_engine
from utils.gemini_client import GeminiClientError


def render(db):
    st.title("🧠 AI Explanation")

    text = st.session_state.get("extracted_text", "")
    if not text:
        st.warning("No document loaded yet. Please upload a file first from the **Upload** page.")
        return

    st.caption(f"Explaining: **{st.session_state.get('current_file_name', 'your document')}**")

    tab_simple, tab_tanglish = st.tabs(["🇬🇧 Simple English", "🇮🇳 Tanglish"])

    with tab_simple:
        if st.button("✨ Generate Simple English Explanation", type="primary", key="btn_simple"):
            with st.spinner("Thinking in simple English..."):
                try:
                    explanation = ai_engine.explain_simple_english(text)
                    st.session_state["explanation_simple"] = explanation
                except GeminiClientError as exc:
                    st.error(str(exc))

        if st.session_state.get("explanation_simple"):
            st.markdown(st.session_state["explanation_simple"])

    with tab_tanglish:
        if st.button("✨ Generate Tanglish Explanation", type="primary", key="btn_tanglish"):
            with st.spinner("Explaining in Tanglish..."):
                try:
                    explanation = ai_engine.explain_tanglish(text)
                    st.session_state["explanation_tanglish"] = explanation
                except GeminiClientError as exc:
                    st.error(str(exc))

        if st.session_state.get("explanation_tanglish"):
            st.markdown(st.session_state["explanation_tanglish"])
