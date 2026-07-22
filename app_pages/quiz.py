"""
pages/quiz.py
---------------
Interactive quiz page. Supports MCQ, 2-mark, 5-mark and 10-mark question
types. MCQs are graded instantly (locally); subjective answers are graded by
Gemini. Results are stored in the database and also handed off to the
Results page via session state.
"""

import streamlit as st

from utils import quiz_engine
from utils.gemini_client import GeminiClientError
from config import QUIZ_TYPES, DEFAULT_MCQ_COUNT, DEFAULT_SUBJECTIVE_COUNT


def _reset_quiz_state():
    for key in ["quiz_questions", "quiz_type", "quiz_submitted", "quiz_result"]:
        st.session_state.pop(key, None)


def render(db):
    st.title("🎯 Interactive Quiz")

    text = st.session_state.get("extracted_text", "")
    file_name = st.session_state.get("current_file_name", "Untitled Document")
    student_name = st.session_state.get("student_name", "")

    if not text:
        st.warning("No document loaded yet. Please upload a file first from the **Upload** page.")
        return

    if not student_name:
        st.warning("Please enter your name in the sidebar so your quiz result can be saved.")

    st.caption(f"Quiz source: **{file_name}**")

    with st.expander("⚙️ Quiz Settings", expanded="quiz_questions" not in st.session_state):
        quiz_type = st.selectbox("Question type", QUIZ_TYPES, key="selected_quiz_type")
        count = st.slider(
            "Number of questions",
            min_value=3,
            max_value=10,
            value=DEFAULT_MCQ_COUNT if quiz_type == "MCQ" else DEFAULT_SUBJECTIVE_COUNT,
        )
        if st.button("🎲 Generate Quiz", type="primary", use_container_width=True):
            _reset_quiz_state()
            with st.spinner("Generating quiz questions with AI..."):
                try:
                    if quiz_type == "MCQ":
                        questions = quiz_engine.build_mcq_quiz(text, count)
                    else:
                        marks = int(quiz_type.split()[0])
                        questions = quiz_engine.build_subjective_quiz(text, marks, count)

                    if not questions:
                        st.error("The AI did not return any questions. Please try again.")
                    else:
                        st.session_state["quiz_questions"] = questions
                        st.session_state["quiz_type"] = quiz_type
                        st.session_state["quiz_submitted"] = False
                except GeminiClientError as exc:
                    st.error(str(exc))

    questions = st.session_state.get("quiz_questions")
    quiz_type = st.session_state.get("quiz_type")

    if not questions:
        return

    st.divider()
    st.subheader(f"{quiz_type} Quiz ({len(questions)} questions)")

    if not st.session_state.get("quiz_submitted"):
        with st.form("quiz_form"):
            user_answers = {}
            for idx, q in enumerate(questions):
                st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
                st.markdown(f"**Q{idx + 1}. {q.get('question', '')}**")

                if quiz_type == "MCQ":
                    options = q.get("options", {})
                    option_labels = [f"{key}. {value}" for key, value in options.items()]
                    choice = st.radio(
                        "Select an answer",
                        options=list(options.keys()) or ["A", "B", "C", "D"],
                        format_func=lambda k, opts=options: f"{k}. {opts.get(k, '')}",
                        key=f"mcq_{idx}",
                        index=None,
                    )
                    user_answers[str(idx)] = choice or ""
                else:
                    answer = st.text_area(
                        f"Your answer ({q.get('marks', '')} marks)",
                        key=f"subjective_{idx}",
                        height=120,
                    )
                    user_answers[str(idx)] = answer

                st.markdown("</div>", unsafe_allow_html=True)

            submitted = st.form_submit_button("✅ Submit Quiz", type="primary", use_container_width=True)

        if submitted:
            with st.spinner("Evaluating your answers..."):
                try:
                    if quiz_type == "MCQ":
                        result = quiz_engine.grade_mcq_quiz(questions, user_answers)
                        score_percent = result["score_percent"]
                    else:
                        marks = int(quiz_type.split()[0])
                        result = quiz_engine.grade_subjective_quiz(questions, user_answers)
                        score_percent = result["score_percent"]

                    if student_name:
                        db.save_quiz_result(
                            student_name=student_name,
                            file_name=file_name,
                            quiz_type=quiz_type,
                            total_questions=result["total_questions"],
                            correct_answers=result["correct_answers"],
                            score=score_percent,
                            details=result["details"],
                        )

                    st.session_state["quiz_result"] = result
                    st.session_state["quiz_submitted"] = True
                    st.rerun()
                except GeminiClientError as exc:
                    st.error(str(exc))
    else:
        st.success("Quiz submitted! See the **Results** page for your detailed score and explanations.")
        if st.button("🔁 Start a New Quiz"):
            _reset_quiz_state()
            st.rerun()
