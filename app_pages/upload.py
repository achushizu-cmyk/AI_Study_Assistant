"""
pages/upload.py
-----------------
Upload page: accepts PDF/DOCX/PPTX/TXT/JPG/PNG files, extracts text
(using OCR for images / handwritten pages) and stores the result in both
session state and the database.
"""

import os
import streamlit as st

from utils.file_parser import extract_text
from utils.helpers import save_uploaded_file, truncate_text
from config import SUPPORTED_EXTENSIONS, MAX_FILE_SIZE_MB


def render(db):
    st.title("📤 Upload Study Material")
    st.caption("Supported formats: PDF, DOCX, PPTX, TXT, JPG, PNG (including handwritten notes)")

    student_name = st.session_state.get("student_name", "")
    if not student_name:
        st.warning("Please enter your name in the sidebar first so we can save your progress.")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=list(SUPPORTED_EXTENSIONS.keys()),
        accept_multiple_files=False,
        help=f"Maximum file size: {MAX_FILE_SIZE_MB} MB",
    )

    if uploaded_file is not None:
        size_mb = uploaded_file.size / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            st.error(f"File too large ({size_mb:.1f} MB). Maximum allowed is {MAX_FILE_SIZE_MB} MB.")
            return

        file_extension = uploaded_file.name.split(".")[-1].lower()
        file_kind = SUPPORTED_EXTENSIONS.get(file_extension, "document")

        st.markdown(f"**File:** {uploaded_file.name}  \n**Type:** {file_kind.title()} (`.{file_extension}`)")

        if file_kind == "image":
            st.image(uploaded_file, caption="Preview", use_container_width=True)

        if st.button("🚀 Extract & Process", type="primary", use_container_width=True):
            with st.spinner("Saving file..."):
                file_path = save_uploaded_file(uploaded_file)

            progress = st.progress(0, text="Starting extraction...")
            try:
                progress.progress(30, text="Reading content (this may take a moment for OCR)...")
                extracted = extract_text(file_path, file_extension)
                progress.progress(80, text="Finalizing...")

                if not extracted.strip():
                    st.error("No text could be extracted from this file. Try a clearer scan or a different file.")
                    progress.empty()
                    return

                st.session_state["extracted_text"] = extracted
                st.session_state["current_file_name"] = uploaded_file.name

                if student_name:
                    db.add_upload(student_name, uploaded_file.name, file_extension, extracted)

                progress.progress(100, text="Done!")
                progress.empty()

                st.success("✅ Text extracted successfully!")
                with st.expander("📄 Preview Extracted Text", expanded=True):
                    st.text_area(
                        "Extracted content",
                        value=truncate_text(extracted, 3000),
                        height=280,
                        disabled=True,
                    )

                st.info("Now go to **AI Explanation**, **Summary** or **Quiz** from the sidebar to continue.")
            except Exception as exc:  # noqa: BLE001
                progress.empty()
                st.error(f"Something went wrong while processing the file: {exc}")
            finally:
                if os.path.exists(file_path) and file_kind == "document" and file_extension == "pdf":
                    pass  # keep original file for potential re-use

    if "extracted_text" in st.session_state and uploaded_file is None:
        st.divider()
        st.caption(f"Currently loaded document: **{st.session_state.get('current_file_name', 'Unknown')}**")
        if st.button("🗑️ Clear loaded document"):
            st.session_state.pop("extracted_text", None)
            st.session_state.pop("current_file_name", None)
            st.rerun()
