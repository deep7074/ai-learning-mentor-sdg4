# PROJECT REPORT
# AI Learning Mentor for Student Engagement
## SDG 4 – Quality Education

### 1. Introduction

Quality education is not only about access to classes; students also need continuous academic support, feedback, revision opportunities, and guidance. Many learners face difficulty understanding technical topics, organizing study time, completing assignments, and preparing for examinations.

This project proposes an **AI Learning Mentor**, an LLM-powered educational web application designed to provide personalized academic assistance. The system combines a conversational AI mentor, AI-generated study plans, AI-generated quizzes, PDF-based study-note retrieval, progress tracking, and a transparent engagement-support indicator.

### 2. SDG Connection

The project is aligned with **United Nations Sustainable Development Goal 4 – Quality Education**.

The application supports the goal by making personalized learning assistance more accessible and by encouraging continuous learning and revision.

### 3. Problem Statement

Students may:
- struggle with difficult subjects,
- have limited access to personal tutoring,
- postpone assignments,
- study irregularly,
- need last-minute exam guidance,
- have difficulty identifying the most important points in long notes.

A conversational AI mentor can provide immediate support while allowing students to use their own study material.

### 4. Objectives

1. Build a web-based AI Learning Mentor.
2. Use an LLM for natural-language tutoring.
3. Generate personalized study schedules.
4. Generate practice MCQs.
5. Allow students to upload PDF notes.
6. Retrieve relevant content from uploaded notes.
7. Generate revision material from the retrieved content.
8. Store learning progress in SQLite.
9. Provide a transparent engagement-support indicator.
10. Demonstrate a teacher/admin dashboard.

### 5. Proposed System

The system has two main roles.

#### Student
- Login
- Profile management
- AI mentor
- PDF study-note upload
- RAG-style note retrieval
- AI revision sheet
- AI study plan
- AI quiz
- Progress dashboard

#### Admin/Teacher
- Login
- Student profile snapshot
- Chat/quiz/note statistics
- Quiz performance table
- Uploaded material overview

### 6. System Architecture

```text
                         ┌──────────────────┐
                         │     Student      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Streamlit Web UI │
                         └────────┬─────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
      │ LLM Service │      │ RAG Module  │      │ Rule Engine │
      │ Ollama/API  │      │ PDF + Search│      │ Engagement  │
      └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                         ┌──────────────────┐
                         │  SQLite Database │
                         └──────────────────┘
                                  ▲
                                  │
                         ┌────────┴─────────┐
                         │ Admin Dashboard  │
                         └──────────────────┘
```

### 7. Major Modules

#### Module 1 – Authentication
A demonstration login separates student and admin views.

#### Module 2 – Student Profile
Stores:
- name,
- course,
- attendance,
- weekly study hours,
- pending assignments,
- recent quiz score.

#### Module 3 – LLM Mentor
The user asks questions in natural language. The system creates a prompt containing student context and relevant study-note context.

#### Module 4 – RAG-style Study Assistant

RAG means **Retrieval-Augmented Generation**.

The prototype workflow is:

```text
PDF Upload
   ↓
Text Extraction
   ↓
SQLite Storage
   ↓
Question
   ↓
Keyword-based Retrieval
   ↓
Relevant Note Context
   ↓
LLM Prompt
   ↓
Grounded Answer
```

This makes the project more advanced than a simple chatbot.

#### Module 5 – AI Study Planner
The LLM creates a day-by-day plan based on:
- subjects,
- available study time,
- pending assignments,
- recent quiz performance.

#### Module 6 – AI Quiz
The LLM generates four-option MCQs in JSON format. The application checks the selected answers and stores the percentage.

#### Module 7 – Progress Analytics
Quiz scores are stored and displayed as a table and line chart.

#### Module 8 – Engagement Support Indicator
The application uses transparent rules based on:
- attendance,
- study hours,
- pending assignments,
- quiz performance.

The output is:
- Stable
- Watch
- Needs attention

**This is not a validated dropout prediction model.**

### 8. LLM Prompt Engineering

The mentor uses instructions such as:

```text
You are an AI Learning Mentor for college students.
Explain concepts clearly and accurately using simple English.
Use the student's uploaded notes when relevant.
Do not shame students.
Give practical next steps.
```

Quiz generation requires strict JSON so that the application can parse the result.

### 9. Database

#### users
Stores demo username and role.

#### profile
Stores the student's learning profile.

#### chats
Stores mentor conversation history.

#### progress
Stores quiz topic, score and date.

#### notes
Stores uploaded study-note text.

### 10. Algorithm

The support indicator is intentionally explainable.

| Factor | Condition | Points |
|---|---|---:|
| Attendance | <60% | +2 |
| Attendance | 60–74% | +1 |
| Study time | <4 h/week | +2 |
| Study time | 4–6.99 h/week | +1 |
| Pending assignments | 5+ | +2 |
| Pending assignments | 2–4 | +1 |
| Quiz score | <40% | +2 |
| Quiz score | 40–59% | +1 |

Interpretation:

```text
0–1   → Stable
2–3   → Watch
4+    → Needs attention
```

### 11. Advantages

- Personalized academic support.
- Natural-language interaction.
- Uses student's own study notes.
- Generates study plans automatically.
- Generates practice questions.
- Tracks learning progress.
- Local LLM option can reduce API cost.
- Transparent support rules.
- Easy-to-demonstrate web interface.

### 12. Limitations

- LLMs can generate incorrect information.
- PDF extraction may fail on scanned/image-only PDFs.
- Keyword retrieval is basic and can be improved.
- The engagement indicator is not scientifically validated.
- Demo authentication is not production-grade.
- Real student data requires strong privacy and security.

### 13. Future Scope

1. Vector database such as FAISS/Chroma.
2. Embedding-based semantic retrieval.
3. Bengali + English voice mentor.
4. Teacher dashboard with authorized access.
5. College LMS/attendance integration.
6. Calendar and reminder integration.
7. Strong authentication and role-based access control.
8. Human teacher escalation.
9. Learning analytics and validated prediction models.
10. Evaluation with approved educational datasets.

### 14. Ethical Considerations

- Do not label a student as a "dropout".
- Use indicators only to offer support.
- Protect student data.
- Obtain consent where required.
- Keep human teachers involved in important decisions.
- Evaluate model accuracy and fairness before institutional deployment.

### 15. Conclusion

The AI Learning Mentor demonstrates how LLMs can be applied to SDG 4 by giving students personalized and accessible academic assistance. The combination of LLM tutoring, RAG-style study-note grounding, study planning, AI quizzes, progress tracking, and transparent engagement support makes the prototype suitable for a BCA final-year demonstration.

The project focuses on **supporting students rather than judging them**, which is an important principle for responsible educational AI.
