"""
pages/history.py
-------------------
History page: lists all previous quiz attempts and uploads for the current
student, with a score-trend chart.
"""

import streamlit as st
import pandas as pd

from utils.helpers import format_score_percentage


def render(db):
    st.title("📚 History")

    student_name = st.session_state.get("student_name", "")
    if not student_name:
        st.warning("Enter your name in the sidebar to view your personal history.")
        return

    history = db.get_history(student_name)
    uploads = db.get_uploads(student_name)

    tab_quizzes, tab_uploads = st.tabs(["🎯 Quiz Attempts", "📄 Uploaded Documents"])

    with tab_quizzes:
        if not history:
            st.info("No quiz attempts yet. Go take a quiz!")
        else:
            df = pd.DataFrame(history)[
                ["quiz_date", "quiz_time", "file_name", "quiz_type", "total_questions", "correct_answers", "score"]
            ]
            df.columns = ["Date", "Time", "Document", "Quiz Type", "Total Qs", "Correct", "Score (%)"]
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("Score Trend")
            trend_df = pd.DataFrame(history).sort_values("id")[["id", "score"]]
            trend_df = trend_df.rename(columns={"id": "Attempt", "score": "Score (%)"}).set_index("Attempt")
            st.line_chart(trend_df)

            st.subheader("Review a Past Attempt")
            options = {
                f"#{h['id']} - {h['file_name']} ({h['quiz_type']}) - {format_score_percentage(h['score'])}": h
                for h in history
            }
            selected_label = st.selectbox("Select an attempt", list(options.keys()))
            if selected_label:
                selected = options[selected_label]
                st.session_state["quiz_result"] = {
                    "score_percent": selected["score"],
                    "total_questions": selected["total_questions"],
                    "correct_answers": selected["correct_answers"],
                    "details": selected["details"],
                }
                if st.button("🔍 Open in Results Page"):
                    st.session_state["_nav_target"] = "Results"
                    st.rerun()

            if st.button("🗑️ Clear My Quiz History"):
                db.clear_history(student_name)
                st.success("History cleared.")
                st.rerun()

    with tab_uploads:
        if not uploads:
            st.info("No documents uploaded yet.")
        else:
            df = pd.DataFrame(uploads)[["uploaded_date", "uploaded_time", "file_name", "file_type"]]
            df.columns = ["Date", "Time", "File Name", "Type"]
            st.dataframe(df, use_container_width=True, hide_index=True)
