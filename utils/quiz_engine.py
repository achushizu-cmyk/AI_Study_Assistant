"""
utils/quiz_engine.py
----------------------
Quiz orchestration logic: building quiz sessions, grading MCQs locally, and
grading subjective answers via the AI engine. Keeping this separate from the
Streamlit page code means the quiz logic is independently testable.
"""

from utils import ai_engine


def build_mcq_quiz(text: str, count: int) -> list:
    """Return a list of MCQ question dicts ready to render."""
    questions = ai_engine.generate_mcqs(text, count)
    for q in questions:
        q.setdefault("options", {})
        q.setdefault("correct_option", "")
        q.setdefault("explanation", "")
    return questions


def build_subjective_quiz(text: str, marks: int, count: int) -> list:
    """Return a list of subjective question dicts ready to render."""
    questions = ai_engine.generate_subjective_questions(text, marks, count)
    for q in questions:
        q.setdefault("model_answer", "")
        q.setdefault("marks", marks)
    return questions


def grade_mcq_quiz(questions: list, user_answers: dict) -> dict:
    """
    Grade an MCQ quiz.

    Args:
        questions: list of question dicts as produced by build_mcq_quiz.
        user_answers: mapping of question index (str) -> selected option letter.

    Returns:
        dict with total, correct, score_percent and per-question details.
    """
    details = []
    correct_count = 0

    for idx, q in enumerate(questions):
        selected = user_answers.get(str(idx), "")
        is_correct = selected == q.get("correct_option", "")
        if is_correct:
            correct_count += 1
        details.append(
            {
                "question": q.get("question", ""),
                "options": q.get("options", {}),
                "selected_option": selected,
                "correct_option": q.get("correct_option", ""),
                "is_correct": is_correct,
                "explanation": q.get("explanation", ""),
                "marks": 1,
                "awarded_marks": 1 if is_correct else 0,
            }
        )

    total = len(questions)
    score_percent = round((correct_count / total) * 100, 2) if total else 0.0

    return {
        "total_questions": total,
        "correct_answers": correct_count,
        "score_percent": score_percent,
        "details": details,
    }


def grade_subjective_quiz(questions: list, user_answers: dict) -> dict:
    """
    Grade a subjective (2/5/10 mark) quiz using AI evaluation for each answer.

    Args:
        questions: list of question dicts as produced by build_subjective_quiz.
        user_answers: mapping of question index (str) -> student's free-text answer.

    Returns:
        dict with total marks, awarded marks, score_percent and per-question details.
    """
    details = []
    total_marks = 0
    awarded_marks_total = 0
    correct_count = 0

    for idx, q in enumerate(questions):
        student_answer = user_answers.get(str(idx), "")
        max_marks = int(q.get("marks", 0)) or 1
        evaluation = ai_engine.evaluate_subjective_answer(
            question=q.get("question", ""),
            model_answer=q.get("model_answer", ""),
            student_answer=student_answer,
            max_marks=max_marks,
        )
        awarded = float(evaluation.get("awarded_marks", 0))
        total_marks += max_marks
        awarded_marks_total += awarded
        if evaluation.get("is_correct"):
            correct_count += 1

        details.append(
            {
                "question": q.get("question", ""),
                "model_answer": q.get("model_answer", ""),
                "student_answer": student_answer,
                "marks": max_marks,
                "awarded_marks": awarded,
                "feedback": evaluation.get("feedback", ""),
                "is_correct": bool(evaluation.get("is_correct", False)),
            }
        )

    score_percent = round((awarded_marks_total / total_marks) * 100, 2) if total_marks else 0.0

    return {
        "total_questions": len(questions),
        "correct_answers": correct_count,
        "total_marks": total_marks,
        "awarded_marks": awarded_marks_total,
        "score_percent": score_percent,
        "details": details,
    }
