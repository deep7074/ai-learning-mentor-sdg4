# PROJECT REPORT
# AI Learning Mentor for Student Engagement
## SDG 4 – Quality Education

### 1. Abstract

Student disengagement can make it difficult for learners to keep up with classes, assignments, revision, and examinations. This project presents an AI Learning Mentor that uses a Large Language Model (LLM) to provide personalized academic assistance. The system allows students to ask questions, receive explanations, generate study plans, practice through AI-generated quizzes, and view their learning progress. A simple transparent engagement-support indicator uses attendance, study time, pending assignments, and quiz performance to highlight when additional academic support may be useful.

The project is designed as an educational prototype rather than a validated dropout prediction system. Its main goal is to demonstrate how generative AI can support students before academic difficulties become severe.

### 2. SDG Mapping

**SDG 4 – Quality Education**

The project supports:
- accessible learning assistance,
- personalized study guidance,
- continuous practice,
- improved academic engagement.

### 3. Problem Statement

Many students struggle because they do not have continuous access to a personal tutor. They may postpone assignments, study irregularly, have difficulty understanding technical topics, or not know how to organize preparation before examinations.

A digital AI mentor can provide immediate, personalized support at low cost.

### 4. Objectives

1. Build an AI-based academic mentor.
2. Use an LLM for natural-language tutoring.
3. Generate personalized study plans.
4. Generate practice quizzes.
5. Store learning progress.
6. Provide a transparent engagement-support indicator.
7. Create a simple web interface suitable for students.

### 5. Proposed Solution

The system has four main modules:

#### Module 1 – Student Profile
The student enters:
- name,
- course,
- attendance,
- weekly study hours,
- pending assignments,
- recent quiz score.

#### Module 2 – AI Mentor
The student asks questions in natural language. The LLM generates a simple explanation and practical study advice.

#### Module 3 – Personalized Study Planner
The system sends the student profile, subjects, and requested duration to the LLM. The LLM returns a realistic study plan.

#### Module 4 – AI Quiz and Progress
The LLM generates multiple-choice questions. The application checks answers and stores the score in SQLite.

### 6. System Architecture

```text
                 ┌─────────────────────┐
                 │      Student        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Streamlit Web UI   │
                 └──────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
     ┌─────────────────┐         ┌─────────────────┐
     │ Engagement Rules│         │   LLM Service   │
     │ Attendance etc. │         │ Ollama / OpenAI │
     └────────┬────────┘         └────────┬────────┘
              │                           │
              └─────────────┬─────────────┘
                            ▼
                   ┌─────────────────┐
                   │ SQLite Database │
                   └─────────────────┘
```

### 7. LLM Prompting

The system uses structured prompts.

Example mentor instruction:

```text
You are an AI learning mentor for college students.
Explain concepts in simple language.
Do not shame the student.
Give practical next steps when useful.
```

For quiz generation, the model is instructed to return JSON with:
- question,
- four options,
- correct answer.

### 8. Algorithm for Engagement Support

The prototype does not claim to predict actual dropout.

A simple score is calculated:

- Attendance below 60% → +2
- Attendance 60–74% → +1
- Study time below 4 hours/week → +2
- Study time 4–6.99 hours/week → +1
- 5+ pending assignments → +2
- 2–4 pending assignments → +1
- Quiz score below 40% → +2
- Quiz score 40–59% → +1

Interpretation:
- 0–1 → Stable
- 2–3 → Watch
- 4+ → Needs attention

This rule-based component is intentionally transparent and easy to explain.

### 9. Database Design

#### Profile table

| Field | Description |
|---|---|
| id | Primary key |
| name | Student name |
| course | Course/class |
| attendance | Attendance percentage |
| study_hours | Weekly study time |
| pending | Pending assignments |
| quiz_score | Recent quiz score |

#### Chats table

| Field | Description |
|---|---|
| id | Message ID |
| role | user/assistant |
| content | Message |
| created_at | Timestamp |

#### Progress table

| Field | Description |
|---|---|
| id | Attempt ID |
| topic | Quiz topic |
| score | Percentage |
| created_at | Timestamp |

### 10. Advantages

- Personalized assistance.
- Immediate response.
- Easy-to-use interface.
- Local LLM option can reduce API cost.
- Quiz progress is saved.
- Transparent support indicator.
- Can be expanded into a college-level system.

### 11. Limitations

- LLM answers can occasionally be incorrect.
- The engagement indicator is not a validated prediction model.
- Local LLM quality depends on the selected model and computer hardware.
- The prototype does not automatically access college attendance systems.
- Student privacy must be protected in a real deployment.

### 12. Future Scope

1. RAG using college notes and syllabus.
2. Bengali + English tutoring.
3. Teacher/admin dashboard.
4. Attendance API integration.
5. Calendar integration.
6. Personalized notifications with consent.
7. Learning analytics.
8. Secure authentication.
9. Human counselor/teacher escalation for serious academic difficulties.
10. Evaluation using an approved dataset and measurable outcomes.

### 13. Expected Outcome

The project demonstrates how an LLM can act as a personal learning mentor. It can reduce friction in studying by answering questions, planning revision, generating practice, and tracking progress.

### 14. Conclusion

The AI Learning Mentor is a practical SDG 4 project that combines LLM technology, a web application, and a small database. Instead of treating students as a prediction problem, the prototype focuses on providing useful academic support and early encouragement. With stronger evaluation, privacy controls, institutional integration, and teacher involvement, the system could be developed into a more complete educational support platform.
