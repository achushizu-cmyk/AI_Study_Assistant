"""
prompts/prompt_templates.py
----------------------------
All Gemini prompt templates used across the application live here. Keeping
prompts centralized makes them easy to tune without touching business logic
in `utils/ai_engine.py`.
"""

MAX_CONTEXT_CHARS = 12000


def _truncate(text: str) -> str:
    """Prevent prompts from exceeding a safe context size."""
    if len(text) > MAX_CONTEXT_CHARS:
        return text[:MAX_CONTEXT_CHARS] + "\n\n...(content truncated)"
    return text


def simple_explanation_prompt(text: str) -> str:
    return f"""You are an expert teacher. Explain the following study material in
SIMPLE, EASY-TO-UNDERSTAND ENGLISH for a college student. Use short sentences,
everyday examples and break complex ideas into small parts. Use headings and
bullet points where helpful. Do not just repeat the text - genuinely explain it.

STUDY MATERIAL:
\"\"\"{_truncate(text)}\"\"\"

Now write the simple English explanation:"""


def tanglish_explanation_prompt(text: str) -> str:
    return f"""You are a friendly Tamil tutor. Explain the following study material in
TANGLISH (Tamil language, but written using English/Roman letters, the way
Tamil students chat casually). Keep it warm, conversational and easy to
understand, like explaining to a friend before an exam. Use simple technical
terms in English where there is no good Tamil equivalent.

STUDY MATERIAL:
\"\"\"{_truncate(text)}\"\"\"

Now write the Tanglish explanation:"""


def summary_prompt(text: str) -> str:
    return f"""Summarize the following study material into a clear, well-structured
summary of about 150-250 words. Capture the core ideas only, do not add
unrelated information.

STUDY MATERIAL:
\"\"\"{_truncate(text)}\"\"\"

Summary:"""


def key_points_prompt(text: str) -> str:
    return f"""Extract the most important KEY POINTS from the following study material.
Return them as a clean bullet list (using "-" ), each point being one short,
self-contained sentence. Produce between 6 and 12 points.

STUDY MATERIAL:
\"\"\"{_truncate(text)}\"\"\"

Key Points:"""


def important_topics_prompt(text: str) -> str:
    return f"""Identify the most IMPORTANT TOPICS / CONCEPTS covered in the following
study material. For each topic, give the topic name followed by a one-line
description of why it matters. Return as a bullet list. Produce between 5 and
10 topics.

STUDY MATERIAL:
\"\"\"{_truncate(text)}\"\"\"

Important Topics:"""


def mcq_prompt(text: str, count: int = 5) -> str:
    return f"""Based on the following study material, generate exactly {count} multiple
choice questions (MCQs) to test understanding.

Return ONLY valid JSON (no markdown fences, no extra commentary) in exactly
this structure:

{{
  "questions": [
    {{
      "question": "string",
      "options": {{"A": "string", "B": "string", "C": "string", "D": "string"}},
      "correct_option": "A",
      "explanation": "short explanation of why this is correct"
    }}
  ]
}}

STUDY MATERIAL:
\"\"\"{_truncate(text)}\"\"\"

JSON:"""


def subjective_questions_prompt(text: str, marks: int, count: int = 5) -> str:
    return f"""Based on the following study material, generate exactly {count}
{marks}-mark exam-style questions suitable for a university exam. The
questions should require answers of a depth appropriate for {marks} marks.

Return ONLY valid JSON (no markdown fences, no extra commentary) in exactly
this structure:

{{
  "questions": [
    {{
      "question": "string",
      "model_answer": "a complete model answer worth {marks} marks",
      "marks": {marks}
    }}
  ]
}}

STUDY MATERIAL:
\"\"\"{_truncate(text)}\"\"\"

JSON:"""


def answer_evaluation_prompt(question: str, model_answer: str, student_answer: str, max_marks: int) -> str:
    return f"""You are a strict but fair exam evaluator. Compare the STUDENT ANSWER
against the MODEL ANSWER for the given question, and award a mark out of
{max_marks}. Consider partial credit for partially correct answers.

Return ONLY valid JSON (no markdown fences) in exactly this structure:

{{
  "awarded_marks": number,
  "max_marks": {max_marks},
  "feedback": "short constructive feedback explaining the score",
  "is_correct": true or false
}}

QUESTION:
\"\"\"{question}\"\"\"

MODEL ANSWER:
\"\"\"{model_answer}\"\"\"

STUDENT ANSWER:
\"\"\"{student_answer if student_answer.strip() else "(no answer provided)"}\"\"\"

JSON:"""
