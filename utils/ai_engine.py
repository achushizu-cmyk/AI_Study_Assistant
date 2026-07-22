"""
utils/ai_engine.py
--------------------
High-level AI operations built on top of `GeminiClient`. This is the module
that pages import - it hides prompt construction and JSON parsing behind
clean, typed function calls.
"""

import json
import re

from utils.gemini_client import get_gemini_client, GeminiClientError
from prompts import prompt_templates as pt
from config import DEFAULT_MCQ_COUNT, DEFAULT_SUBJECTIVE_COUNT


def _extract_json(raw_text: str) -> dict:
    """
    Gemini occasionally wraps JSON in markdown fences or adds stray text.
    This strips fences and extracts the first valid JSON object found.
    """
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned.strip(), flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned.strip()).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            raise GeminiClientError(f"Could not parse AI response as JSON: {exc}") from exc
    raise GeminiClientError("AI response did not contain valid JSON.")


def explain_simple_english(text: str) -> str:
    client = get_gemini_client()
    return client.generate(pt.simple_explanation_prompt(text))


def explain_tanglish(text: str) -> str:
    client = get_gemini_client()
    return client.generate(pt.tanglish_explanation_prompt(text))


def generate_summary(text: str) -> str:
    client = get_gemini_client()
    return client.generate(pt.summary_prompt(text))


def generate_key_points(text: str) -> str:
    client = get_gemini_client()
    return client.generate(pt.key_points_prompt(text))


def generate_important_topics(text: str) -> str:
    client = get_gemini_client()
    return client.generate(pt.important_topics_prompt(text))


def generate_mcqs(text: str, count: int = DEFAULT_MCQ_COUNT) -> list:
    client = get_gemini_client()
    raw = client.generate(pt.mcq_prompt(text, count), temperature=0.5)
    data = _extract_json(raw)
    return data.get("questions", [])


def generate_subjective_questions(text: str, marks: int, count: int = DEFAULT_SUBJECTIVE_COUNT) -> list:
    client = get_gemini_client()
    raw = client.generate(pt.subjective_questions_prompt(text, marks, count), temperature=0.5)
    data = _extract_json(raw)
    return data.get("questions", [])


def evaluate_subjective_answer(question: str, model_answer: str, student_answer: str, max_marks: int) -> dict:
    client = get_gemini_client()
    raw = client.generate(
        pt.answer_evaluation_prompt(question, model_answer, student_answer, max_marks),
        temperature=0.2,
    )
    data = _extract_json(raw)
    data.setdefault("awarded_marks", 0)
    data.setdefault("max_marks", max_marks)
    data.setdefault("feedback", "")
    data.setdefault("is_correct", False)
    return data
