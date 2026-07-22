"""
database.py
-----------
SQLite persistence layer for the AI Study Assistant.

This module exposes a single class, `StudyDatabase`, which wraps all
database access behind a clean API. No other module should touch SQLite
directly - everything goes through this class so the storage layer can be
swapped later (e.g. to Postgres) without touching business logic.
"""

import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

from config import DB_PATH


class StudyDatabase:
    """Encapsulates all SQLite operations for the application."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_tables()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_tables(self):
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS uploads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    extracted_text TEXT,
                    uploaded_date TEXT NOT NULL,
                    uploaded_time TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS quiz_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    quiz_type TEXT NOT NULL,
                    total_questions INTEGER NOT NULL,
                    correct_answers INTEGER NOT NULL,
                    score REAL NOT NULL,
                    details TEXT,
                    quiz_date TEXT NOT NULL,
                    quiz_time TEXT NOT NULL
                )
                """
            )

    # ----------------------------------------------------------------
    # Students
    # ----------------------------------------------------------------
    def ensure_student(self, name: str):
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO students (name, created_at) VALUES (?, ?)",
                (name, datetime.now().isoformat()),
            )

    def get_students(self):
        with self._get_connection() as conn:
            rows = conn.execute("SELECT name FROM students ORDER BY name").fetchall()
            return [r["name"] for r in rows]

    # ----------------------------------------------------------------
    # Uploads
    # ----------------------------------------------------------------
    def add_upload(self, student_name: str, file_name: str, file_type: str, extracted_text: str) -> int:
        self.ensure_student(student_name)
        now = datetime.now()
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO uploads (student_name, file_name, file_type, extracted_text, uploaded_date, uploaded_time)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    student_name,
                    file_name,
                    file_type,
                    extracted_text,
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                ),
            )
            return cursor.lastrowid

    def get_uploads(self, student_name: str = None):
        with self._get_connection() as conn:
            if student_name:
                rows = conn.execute(
                    "SELECT * FROM uploads WHERE student_name = ? ORDER BY id DESC",
                    (student_name,),
                ).fetchall()
            else:
                rows = conn.execute("SELECT * FROM uploads ORDER BY id DESC").fetchall()
            return [dict(r) for r in rows]

    # ----------------------------------------------------------------
    # Quiz history
    # ----------------------------------------------------------------
    def save_quiz_result(
        self,
        student_name: str,
        file_name: str,
        quiz_type: str,
        total_questions: int,
        correct_answers: int,
        score: float,
        details: list,
    ) -> int:
        self.ensure_student(student_name)
        now = datetime.now()
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO quiz_history
                (student_name, file_name, quiz_type, total_questions, correct_answers, score, details, quiz_date, quiz_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student_name,
                    file_name,
                    quiz_type,
                    total_questions,
                    correct_answers,
                    score,
                    json.dumps(details),
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                ),
            )
            return cursor.lastrowid

    def get_history(self, student_name: str = None):
        with self._get_connection() as conn:
            if student_name:
                rows = conn.execute(
                    "SELECT * FROM quiz_history WHERE student_name = ? ORDER BY id DESC",
                    (student_name,),
                ).fetchall()
            else:
                rows = conn.execute("SELECT * FROM quiz_history ORDER BY id DESC").fetchall()
            results = []
            for r in rows:
                item = dict(r)
                try:
                    item["details"] = json.loads(item["details"]) if item["details"] else []
                except (json.JSONDecodeError, TypeError):
                    item["details"] = []
                results.append(item)
            return results

    def get_last_quiz_result(self, student_name: str):
        history = self.get_history(student_name)
        return history[0] if history else None

    def clear_history(self, student_name: str = None):
        with self._get_connection() as conn:
            if student_name:
                conn.execute("DELETE FROM quiz_history WHERE student_name = ?", (student_name,))
            else:
                conn.execute("DELETE FROM quiz_history")

    def clear_uploads(self, student_name: str = None):
        with self._get_connection() as conn:
            if student_name:
                conn.execute("DELETE FROM uploads WHERE student_name = ?", (student_name,))
            else:
                conn.execute("DELETE FROM uploads")
