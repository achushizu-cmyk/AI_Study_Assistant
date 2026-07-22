"""
pages/results.py
-------------------
Results page: shows the score and a detailed, question-by-question
breakdown (with correct-answer explanations) for the most recently
submitted quiz.
"""

import streamlit as st

from utils.helpers import format_score_percentage, score_badge


def render(db):
    st.title("📊 Quiz Results")

    result = st.session_state.get("quiz_result")
    if not result:
        st.info("No quiz has been submitted yet. Go to the **Quiz** page to attempt one.")
        return

    score_percent = result.get("score_percent", 0.0)
    total = result.get("total_questions", 0)
    correct = result.get("correct_answers", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="metric-card"><div class="value">{format_score_percentage(score_percent)}</div>'
            f'<div class="label">Score</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="metric-card"><div class="value">{correct}/{total}</div>'
            f'<div class="label">Correct Answers</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="metric-card"><div class="value">{score_badge(score_percent)}</div>'
            f'<div class="label">Performance</div></div>',
            unsafe_allow_html=True,
        )

    st.progress(min(int(score_percent), 100) / 100)
    st.divider()
    st.subheader("Detailed Review")

    for idx, item in enumerate(result.get("details", []), start=1):
        is_correct = item.get("is_correct", False)
        icon = "✅" if is_correct else "❌"

        with st.expander(f"{icon} Question {idx}: {item.get('question', '')[:80]}", expanded=False):
            st.markdown(f"**Question:** {item.get('question', '')}")

            if "options" in item:  # MCQ
                for key, value in item.get("options", {}).items():
                    prefix = "👉" if key == item.get("selected_option") else "  "
                    tag = " ✅ correct" if key == item.get("correct_option") else ""
                    st.markdown(f"{prefix} **{key}.** {value}{tag}")
                st.markdown(f"**Your answer:** {item.get('selected_option') or 'Not answered'}")
                st.markdown(f"**Correct answer:** {item.get('correct_option', '')}")
                if item.get("explanation"):
                    st.info(f"💡 Explanation: {item['explanation']}")
            else:  # Subjective
                st.markdown(f"**Your answer:** {item.get('student_answer') or '_No answer provided_'}")
                st.markdown(f"**Model answer:** {item.get('model_answer', '')}")
                st.markdown(f"**Marks awarded:** {item.get('awarded_marks', 0)} / {item.get('marks', 0)}")
                if item.get("feedback"):
                    st.info(f"💡 Feedback: {item['feedback']}")

    st.divider()
    if st.button("📚 View Full History"):
        st.session_state["_nav_target"] = "History"
        st.rerun()
