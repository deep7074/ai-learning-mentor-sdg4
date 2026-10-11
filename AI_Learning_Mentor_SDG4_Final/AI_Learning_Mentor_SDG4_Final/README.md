# AI Learning Mentor – SDG 4 (Final Enhanced Version)

## Project
**SDG 4 – Quality Education**  
**Problem:** Student disengagement / dropout-related academic difficulties  
**AI Solution:** AI Learning Mentor

## What's new in this version

- Student login + demo authentication
- Student dashboard
- Admin/teacher dashboard
- LLM-powered mentor chat
- PDF upload
- RAG-style retrieval from uploaded notes
- AI revision-sheet generation
- Personalized AI study planner
- AI MCQ quiz generator
- SQLite progress tracking
- Transparent engagement-support indicator
- English interface
- Basic Bengali-ready interface selection
- Clear privacy/limitations notes

## Tech stack

Python • Streamlit • LLM (Ollama or OpenAI) • SQLite • PDF extraction • Prompt engineering

## Demo accounts

Student:
```text
username: student
password: student123
```

Admin:
```text
username: admin
password: admin123
```

Change these values in `.env` before any real deployment.

## Setup

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Install:
```bash
pip install -r requirements.txt
```

For local LLM:
```bash
ollama pull llama3.2
```

Run:
```bash
streamlit run app.py
```

## Optional OpenAI

Copy `.env.example` to `.env` and set:
```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-5-mini
```

## RAG workflow

1. Student uploads a PDF.
2. Text is extracted.
3. Text is stored in SQLite.
4. When the student asks a question, simple keyword retrieval finds relevant note content.
5. Retrieved content is sent to the LLM as context.
6. The mentor answers using the supplied study material.

This is a lightweight RAG-style prototype, not a production vector database.

## Important academic limitation

The engagement indicator is **not** a validated dropout prediction model. It is an explainable demonstration using simple rules. A real predictive system would require an approved dataset, model validation, fairness checks, privacy controls, and institutional review.

## Suggested demo order

1. Login as student.
2. Complete profile.
3. Show dashboard indicator.
4. Upload a Cyber Security PDF.
5. Ask: "Explain TCP three-way handshake from my notes."
6. Generate a revision sheet.
7. Generate a 5-question quiz.
8. Submit and show progress.
9. Logout and login as admin.
10. Show teacher/admin dashboard.

## Viva one-line explanation

> "Our project uses an LLM as a personalized learning mentor and a lightweight RAG pipeline to ground answers in uploaded study notes, while SQLite stores profiles and learning progress."
