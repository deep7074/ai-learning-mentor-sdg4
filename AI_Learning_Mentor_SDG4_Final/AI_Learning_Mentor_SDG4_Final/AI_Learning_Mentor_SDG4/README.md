# AI Learning Mentor – SDG 4 Project

## 1. Project idea

**SDG:** SDG 4 – Quality Education  
**Problem:** Student disengagement and dropout risk  
**AI Solution:** AI Learning Mentor

This project is a prototype of an LLM-powered academic support assistant. It helps a student by:
- answering study questions,
- creating personalized study plans,
- generating practice quizzes,
- saving quiz progress,
- showing a simple engagement-support indicator.

> Important: The indicator is NOT a scientifically validated dropout prediction model. It is a transparent rule-based demonstration for an academic project.

## 2. Technology stack

- Python
- Streamlit
- LLM: Ollama + a local model (default: `llama3.2`)
- Optional: OpenAI API
- SQLite
- Requests
- python-dotenv

## 3. Folder structure

```text
AI_Learning_Mentor_SDG4/
├── app.py
├── llm.py
├── database.py
├── risk.py
├── requirements.txt
├── .env.example
├── PROJECT_REPORT.md
├── PRESENTATION_OUTLINE.md
└── README.md
```

The SQLite database `mentor.db` is created automatically after first run.

## 4. Installation

### Step A – Install Python
Use Python 3.10+.

### Step B – Create a virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step C – Install packages

```bash
pip install -r requirements.txt
```

### Step D – Install Ollama

Install Ollama from its official website, then download a model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running.

### Step E – Run

```bash
streamlit run app.py
```

The application opens in the browser.

## 5. Optional OpenAI setup

Copy `.env.example` to `.env` and change:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-5-mini
```

Then run:

```bash
streamlit run app.py
```

## 6. Demo flow

1. Enter a student profile.
2. Click **Save Profile**.
3. Show the engagement-support indicator.
4. Ask the AI mentor a question.
5. Generate a 7-day study plan.
6. Generate a quiz.
7. Submit the quiz and show the saved progress.

## 7. Why this is an LLM project

The LLM is used for:
- natural-language tutoring,
- personalized planning,
- question generation,
- conversational support.

The application layer handles user data, UI, storage, and transparent engagement rules.

## 8. Future improvements

- Add teacher dashboard.
- Add multilingual Bengali/English tutoring.
- Add email/SMS reminders with consent.
- Add attendance integration.
- Add retrieval-augmented generation (RAG) from college notes.
- Add stronger privacy/security controls.
- Evaluate the system with real student feedback and approved datasets.
