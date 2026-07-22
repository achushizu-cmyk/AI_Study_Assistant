"""
pages/home.py
--------------
Landing/dashboard page: hero banner, feature overview and quick stats
pulled from the database for the current student.
"""

import streamlit as st

from config import APP_NAME, APP_TAGLINE


def render(db):
    student_name = st.session_state.get("student_name", "")

    st.markdown(
        f"""
        <div class="hero-container">
            <h1>🎓 {APP_NAME}</h1>
            <p style="font-size:1.1rem; color:#B0B3C0;">{APP_TAGLINE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------
    # Quick stats
    # ------------------------------------------------------------
    uploads = db.get_uploads(student_name) if student_name else []
    history = db.get_history(student_name) if student_name else []
    avg_score = round(sum(h["score"] for h in history) / len(history), 1) if history else 0.0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="metric-card"><div class="value">{len(uploads)}</div>'
            f'<div class="label">Documents Uploaded</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="metric-card"><div class="value">{len(history)}</div>'
            f'<div class="label">Quizzes Attempted</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="metric-card"><div class="value">{avg_score}%</div>'
            f'<div class="label">Average Score</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.subheader("What you can do")

    features = [
        ("📄", "Multi-Format Upload", "Upload PDF, DOCX, PPTX, TXT, JPG or PNG - including handwritten notes."),
        ("🔎", "OCR for Handwriting", "EasyOCR reads scanned pages and handwritten notes automatically."),
        ("🧠", "AI Explanations", "Get content explained in Simple English or friendly Tanglish."),
        ("📝", "Smart Summaries", "Auto-generated summaries, key points and important topics."),
        ("❓", "Question Bank", "MCQs, 2-mark, 5-mark and 10-mark questions generated instantly."),
        ("🎯", "Interactive Quiz", "Attempt quizzes in-app with automatic AI evaluation and scoring."),
        ("📊", "History & Analytics", "Track every attempt with scores, dates and detailed review."),
        ("⚡", "Fast & Free Stack", "Built entirely on Streamlit + Gemini for instant deployment."),
    ]

    cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 4]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div style="font-size:1.8rem;">{icon}</div>
                    <div style="font-weight:700; margin-top:0.4rem;">{title}</div>
                    <div style="color:#9CA3AF; font-size:0.85rem; margin-top:0.3rem;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")

    st.write("")
    if not student_name:
        st.info("👋 Enter your name in the sidebar to start tracking your uploads and quiz history.")
    else:
        st.success(f"Welcome back, **{student_name}**! Head to **Upload** to add new study material.")
