# PPT OUTLINE – AI LEARNING MENTOR

## Slide 1 – Title
**AI Learning Mentor**
SDG 4 – Quality Education

Presented by: Your Name  
Course: BCA  
College: Your College Name

## Slide 2 – SDG 4
- SDG 4 focuses on Quality Education.
- Education support should be accessible and continuous.
- Students need personalized guidance beyond classroom teaching.

## Slide 3 – Problem Statement
- Students struggle with difficult topics.
- Assignments can accumulate.
- Study routines may become irregular.
- Personal tutoring is not always available.
- Students may need quick revision support.

## Slide 4 – Proposed Solution
**AI Learning Mentor**
- LLM chatbot
- Personalized study plan
- AI quiz generator
- PDF notes + RAG
- Progress tracking
- Engagement-support indicator

## Slide 5 – Objectives
- Provide instant academic support.
- Personalize learning.
- Make revision easier.
- Ground AI answers in student notes.
- Track learning progress.

## Slide 6 – Technology Stack
- Python
- Streamlit
- Ollama / OpenAI LLM
- SQLite
- PyPDF
- Prompt Engineering

## Slide 7 – System Architecture
Student → Streamlit → LLM / RAG / Rule Engine → SQLite → Dashboard

## Slide 8 – RAG
**Retrieval-Augmented Generation**
1. Upload PDF.
2. Extract text.
3. Store text.
4. Retrieve relevant content.
5. Send context to LLM.
6. Generate grounded response.

## Slide 9 – Main Screens
Show screenshots of:
- Login
- Student dashboard
- AI Mentor
- Notes/RAG
- Study Plan
- Quiz
- Progress
- Admin dashboard

## Slide 10 – Engagement Support
Inputs:
- Attendance
- Study hours
- Pending assignments
- Quiz score

Output:
- Stable
- Watch
- Needs attention

**Important:** Not a validated dropout prediction system.

## Slide 11 – Demo
1. Login as student.
2. Save profile.
3. Upload Cyber Security PDF.
4. Ask about TCP three-way handshake.
5. Generate revision sheet.
6. Generate quiz.
7. Submit quiz.
8. Show progress.
9. Login as admin.

## Slide 12 – Advantages
- Personalized
- Interactive
- Affordable
- Easy to use
- Uses personal notes
- Tracks progress

## Slide 13 – Limitations
- LLM may make mistakes.
- Basic retrieval.
- PDF scanning limitations.
- Prototype authentication.
- Not a validated prediction model.

## Slide 14 – Future Scope
- Vector DB
- Semantic search
- Voice tutor
- Bengali/English
- LMS integration
- Teacher escalation
- Better analytics

## Slide 15 – Conclusion
AI can provide accessible, personalized academic support while keeping teachers involved in important decisions.

---

# VIVA QUESTIONS & SHORT ANSWERS

### 1. Why did you choose SDG 4?
Because the project uses AI to support accessible and personalized learning.

### 2. What is an LLM?
A Large Language Model is an AI model trained on large amounts of text that can understand and generate natural language.

### 3. Why use an LLM?
It allows students to ask questions naturally and receive personalized explanations.

### 4. What is RAG?
Retrieval-Augmented Generation retrieves relevant information from a knowledge source and provides it to the LLM as context before generating an answer.

### 5. Why did you use PDF notes?
Students often already have PDFs of their syllabus and study material. Using those notes makes answers more relevant.

### 6. Why SQLite?
SQLite is lightweight, easy to use and sufficient for a prototype.

### 7. Is this a real dropout prediction model?
No. It is a transparent engagement-support indicator. A real prediction model would need an approved dataset and validation.

### 8. What is Streamlit?
A Python framework for quickly building interactive data and AI web applications.

### 9. What happens if the LLM gives a wrong answer?
The application should treat AI output as assistance, not unquestionable truth. In a real system, trusted course material and teacher review should be used.

### 10. What is the future scope?
Semantic RAG, vector databases, voice support, Bengali/English support, LMS integration, stronger security, and validated analytics.
