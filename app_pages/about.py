"""
pages/about.py
-----------------
About page: project description, tech stack and credits. Useful for final
year project demonstrations and viva sessions.
"""

import streamlit as st

from config import APP_NAME, APP_TAGLINE


def render(db):
    st.title("ℹ️ About This Project")

    st.markdown(
        f"""
        ### {APP_NAME}
        _{APP_TAGLINE}_

        **{APP_NAME}** is an AI-powered learning companion built as a Final Year
        Project. It helps students turn raw study material - typed or
        handwritten - into structured, exam-ready knowledge: explanations,
        summaries, key points, and auto-graded quizzes.

        #### 🎯 Core Objective
        Reduce the time students spend manually summarizing notes and
        preparing questions before exams, by automating the entire pipeline
        from raw file to graded quiz.

        #### 🧩 How It Works
        1. **Upload** a PDF, DOCX, PPTX, TXT, JPG or PNG (including handwritten notes).
        2. The app **extracts text** using PyMuPDF / python-docx / python-pptx,
           or **EasyOCR** for images and scanned/handwritten pages.
        3. **Gemini AI** explains the content in Simple English and Tanglish,
           and generates summaries, key points, important topics and questions.
        4. Students attempt an **interactive quiz** (MCQ or subjective), which is
           **auto-graded** - MCQs instantly, subjective answers via AI evaluation.
        5. Every attempt is saved to a **SQLite database**, viewable in **History**.

        #### 🛠️ Tech Stack
        - **Frontend / App Framework:** Streamlit
        - **AI Engine:** Google Gemini API
        - **OCR:** EasyOCR
        - **Document Parsing:** PyMuPDF, python-docx, python-pptx
        - **Data Handling:** Pandas
        - **Image Handling:** Pillow
        - **Database:** SQLite
        - **Version Control & Hosting:** GitHub + Streamlit Community Cloud

        #### 👨‍🎓 Academic Note
        This project demonstrates practical application of Generative AI,
        OCR, document processing and full-stack Python web development in a
        single, deployable system - suitable for Final Year Project
        submission and viva demonstration.
        """
    )

    st.divider()
    st.caption("Built with ❤️ using Python and Streamlit.")
