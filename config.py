"""
config.py
---------
Centralized configuration for the AI Study Assistant application.

All environment variables, file paths, model settings and application
constants are defined here so that every other module can import a single
source of truth instead of scattering magic values across the codebase.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file if present (local development).
load_dotenv()

# --------------------------------------------------------------------------
# Base paths
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
HISTORY_DIR = BASE_DIR / "history"
ASSETS_DIR = BASE_DIR / "assets"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------
DB_PATH = str(BASE_DIR / "study_assistant.db")

# --------------------------------------------------------------------------
# Gemini AI configuration
# --------------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.6"))
GEMINI_MAX_OUTPUT_TOKENS = int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "4096"))

# --------------------------------------------------------------------------
# Application constants
# --------------------------------------------------------------------------
APP_NAME = "AI Study Assistant"
APP_ICON = "🎓"
APP_TAGLINE = "Learn Smarter. Understand Faster. Score Higher."

SUPPORTED_EXTENSIONS = {
    "pdf": "document",
    "docx": "document",
    "pptx": "document",
    "txt": "document",
    "jpg": "image",
    "jpeg": "image",
    "png": "image",
}

MAX_FILE_SIZE_MB = 25

QUIZ_TYPES = ["MCQ", "2 Mark Questions", "5 Mark Questions", "10 Mark Questions"]

DEFAULT_MCQ_COUNT = 5
DEFAULT_SUBJECTIVE_COUNT = 5

# --------------------------------------------------------------------------
# UI Theme
# --------------------------------------------------------------------------
PRIMARY_COLOR = "#6C63FF"
SECONDARY_COLOR = "#00C2A8"
BACKGROUND_COLOR = "#0E1117"
CARD_COLOR = "#161B22"
