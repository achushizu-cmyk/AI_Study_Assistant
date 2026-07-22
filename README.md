# 🎓 AI Study Assistant

> Learn Smarter. Understand Faster. Score Higher.

An AI-powered study companion, built as a production-style Final Year
Project. Upload any study material — typed or handwritten — and get instant
explanations, summaries, question banks, and auto-graded quizzes powered by
Google Gemini.

---

## ✨ Features

- **Multi-format upload:** PDF, DOCX, PPTX, TXT, JPG, PNG
- **OCR for handwritten notes** using EasyOCR (also used as a fallback for
  scanned PDF pages with no embedded text)
- **AI explanations** in Simple English and Tanglish (Tamil in English letters)
- **Summary generator:** summary, key points, and important topics
- **Question generator:** MCQs, 2-mark, 5-mark, and 10-mark questions
- **Interactive quiz** with instant MCQ grading and AI-evaluated subjective grading
- **Score dashboard** with detailed, per-question review and correct-answer explanations
- **Quiz history** stored in SQLite, with score-trend charts
- **Modern, sidebar-driven dashboard UI**

---

## 🧱 Tech Stack

| Layer            | Technology                                  |
|------------------|----------------------------------------------|
| UI / App         | Streamlit                                    |
| AI               | Google Gemini API (`google-generativeai`)    |
| OCR              | EasyOCR                                      |
| PDF parsing      | PyMuPDF (`fitz`)                             |
| DOCX parsing     | python-docx                                  |
| PPTX parsing     | python-pptx                                  |
| Data handling    | Pandas                                       |
| Image handling   | Pillow                                       |
| Database         | SQLite (via Python's built-in `sqlite3`)     |
| Hosting          | Streamlit Community Cloud                    |
| Version control  | GitHub                                       |

---

## 📁 Project Structure

```
AI_Study_Assistant/
├── app.py                     # Main entry point + sidebar navigation
├── config.py                  # Central configuration & constants
├── database.py                # SQLite persistence layer (StudyDatabase)
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── assets/
│   └── style.css              # Premium custom theme
│
├── app_pages/                  # Feature pages (see note below)
│   ├── home.py
│   ├── upload.py
│   ├── explanation.py
│   ├── summary.py
│   ├── quiz.py
│   ├── results.py
│   ├── history.py
│   ├── settings.py
│   └── about.py
│
├── utils/
│   ├── file_parser.py          # PDF / DOCX / PPTX / TXT / image → text
│   ├── ocr_engine.py            # EasyOCR wrapper
│   ├── gemini_client.py         # Gemini API wrapper
│   ├── ai_engine.py              # High-level AI operations
│   ├── quiz_engine.py           # Quiz building & grading logic
│   └── helpers.py               # Misc reusable helpers
│
├── prompts/
│   └── prompt_templates.py      # All Gemini prompt templates
│
├── uploads/                     # Uploaded files land here (gitignored)
└── history/                     # Reserved for exported history/reports
```

> **Why `app_pages/` instead of `pages/`?** Streamlit automatically turns any
> folder literally named `pages/` next to `app.py` into its own native
> multi-page navigation. Since this project implements a fully custom
> sidebar (with icons, active-document indicator, and student profile), the
> feature modules were named `app_pages/` to avoid a conflicting, duplicate
> navigation menu. Functionally, it plays the exact role of the `pages/`
> folder described in the project spec.

---

## ⚙️ Setup (Local Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/AI_Study_Assistant.git
   cd AI_Study_Assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Gemini API key (get one free at
   [Google AI Studio](https://aistudio.google.com/app/apikey)):
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app opens at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Community Cloud

1. Push this project to a **public GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select your repository, branch, and set the main file
   path to `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_actual_key_here"
   ```
5. Click **Deploy**. Streamlit Cloud will install `requirements.txt`
   automatically and launch the app.

> **Note:** `python-generativeai`/EasyOCR/PyMuPDF are pure-Python-installable
> and work on Streamlit Community Cloud without extra system packages. First
> load may take a little longer while EasyOCR downloads its model weights —
> this is expected and only happens once per deployment (cached afterward).

---

## 🗄️ Database Schema

SQLite database file: `study_assistant.db` (auto-created on first run).

- **students** — `id, name, created_at`
- **uploads** — `id, student_name, file_name, file_type, extracted_text, uploaded_date, uploaded_time`
- **quiz_history** — `id, student_name, file_name, quiz_type, total_questions, correct_answers, score, details (JSON), quiz_date, quiz_time`

---

## 🧭 How to Use

1. Enter your name in the sidebar (used to save your history).
2. Go to **Upload**, choose a file, and click **Extract & Process**.
3. Visit **AI Explanation** for Simple English / Tanglish explanations.
4. Visit **Summary** for a summary, key points, and important topics.
5. Visit **Quiz**, pick a question type and count, and generate a quiz.
6. Answer the questions and submit — MCQs grade instantly, subjective
   answers are graded by Gemini.
7. Check **Results** for a full breakdown with correct-answer explanations.
8. Check **History** to review all past attempts and score trends.

---

## 🎓 Academic Notes

This project was designed to demonstrate, in a single deployable system:

- Practical use of a modern LLM (Gemini) for content understanding and
  generation, including structured JSON output parsing.
- OCR-based digitization of handwritten/scanned material.
- Multi-format document parsing (PDF, DOCX, PPTX).
- A clean, modular Python architecture separating configuration, data
  access, business logic (utils/), and presentation (app_pages/).
- A relational data model for tracking learning progress over time.

---

## 📄 License

This project is provided for educational purposes as part of a Final Year
Project submission.
