"""
utils/helpers.py
-------------------
Small, reusable helper functions shared across pages: file saving, CSS
loading, timestamp formatting and text truncation for UI previews.
"""

import os
import uuid
from datetime import datetime

import streamlit as st

from config import UPLOAD_DIR, ASSETS_DIR


def save_uploaded_file(uploaded_file) -> str:
    """
    Persist a Streamlit `UploadedFile` to disk under UPLOAD_DIR with a unique
    prefix to avoid collisions, and return the absolute path.
    """
    file_extension = uploaded_file.name.split(".")[-1].lower()
    unique_name = f"{uuid.uuid4().hex[:8]}_{uploaded_file.name}"
    destination = UPLOAD_DIR / unique_name
    with open(destination, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(destination)


def load_css(filename: str = "style.css"):
    """Inject a custom CSS file into the Streamlit app."""
    css_path = ASSETS_DIR / filename
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_chars: int = 600) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + " ..."


def format_score_percentage(value: float) -> str:
    return f"{value:.1f}%"


def score_badge(score_percent: float) -> str:
    """Return an emoji badge appropriate for a score percentage."""
    if score_percent >= 85:
        return "🏆 Excellent"
    if score_percent >= 65:
        return "👍 Good"
    if score_percent >= 40:
        return "📘 Needs Practice"
    return "⚠️ Needs Improvement"
