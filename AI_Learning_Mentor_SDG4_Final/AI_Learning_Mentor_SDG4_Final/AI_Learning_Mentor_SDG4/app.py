import os
import json
import streamlit as st
from dotenv import load_dotenv

from database import init_db, save_profile, load_profile, save_chat, load_chats, save_progress, load_progress
from llm import ask_llm, generate_study_plan, generate_quiz, evaluate_answer
from risk import engagement_indicator

load_dotenv()
init_db()

st.set_page_config(
    page_title="AI Learning Mentor | SDG 4",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Learning Mentor")
st.caption("SDG 4 – Quality Education | An LLM-powered student support prototype")

with st.sidebar:
    st.header("Student Profile")
    existing = load_profile()

    name = st.text_input("Name", existing.get("name", "Student"))
    course = st.text_input("Course / Class", existing.get("course", "BCA"))
    attendance = st.slider("Attendance (%)", 0, 100, int(existing.get("attendance", 75)))
    study_hours = st.number_input("Study hours per week", 0.0, 80.0, float(existing.get("study_hours", 8.0)), 0.5)
    pending = st.number_input("Pending assignments", 0, 30, int(existing.get("pending", 1)))
    quiz_score = st.slider("Recent quiz score (%)", 0, 100, int(existing.get("quiz_score", 60)))

    if st.button("Save Profile", use_container_width=True):
        save_profile(name, course, attendance, study_hours, pending, quiz_score)
        st.success("Profile saved.")

    st.divider()
    st.info(
        "This prototype is an educational support tool. "
        "The engagement indicator is not a clinical or official dropout prediction."
    )

profile = {
    "name": name,
    "course": course,
    "attendance": attendance,
    "study_hours": study_hours,
    "pending": pending,
    "quiz_score": quiz_score,
}

indicator, reasons = engagement_indicator(profile)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Attendance", f"{attendance}%")
c2.metric("Study / week", f"{study_hours:g} h")
c3.metric("Pending work", pending)
c4.metric("Quiz score", f"{quiz_score}%")

st.subheader("📊 Engagement Support Indicator")
if indicator == "Needs attention":
    st.warning("Your current pattern suggests that extra academic support may be useful.")
elif indicator == "Watch":
    st.info("You are doing reasonably well, but a few habits could be strengthened.")
else:
    st.success("Your current study pattern looks stable.")

if reasons:
    st.write("Possible factors:")
    for r in reasons:
        st.write(f"• {r}")

tabs = st.tabs(["💬 AI Mentor", "🗓️ Study Plan", "🧠 AI Quiz", "📈 Progress"])

with tabs[0]:
    st.subheader("Ask your AI Learning Mentor")
    st.write("Examples: *Explain TCP/IP simply*, *I have an exam in 7 days*, *Help me make a study routine*.")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = load_chats()

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Type your study question...")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        save_chat("user", prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        context = f"""
Student profile:
Name: {name}
Course: {course}
Attendance: {attendance}%
Study hours/week: {study_hours}
Pending assignments: {pending}
Recent quiz score: {quiz_score}%

Be a supportive academic mentor. Explain concepts in simple language.
Do not shame the student or make medical/psychological diagnoses.
Give practical next steps when useful.
"""
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_llm(context, prompt)
            st.markdown(answer)
        save_chat("assistant", answer)
        st.session_state.chat_messages.append({"role": "assistant", "content": answer})

with tabs[1]:
    st.subheader("🗓️ Personalized Study Plan")
    days = st.slider("Plan length (days)", 3, 14, 7)
    subjects = st.text_input("Subjects / topics", "Cyber Security, Research Methodology, Java, Networking")

    if st.button("Generate AI Study Plan"):
        with st.spinner("Creating your plan..."):
            plan = generate_study_plan(profile, subjects, days)
        st.markdown(plan)

with tabs[2]:
    st.subheader("🧠 AI Practice Quiz")
    topic = st.text_input("Quiz topic", "Networking fundamentals")
    difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    num_q = st.slider("Number of questions", 3, 10, 5)

    if st.button("Generate Quiz"):
        with st.spinner("Generating questions..."):
            quiz = generate_quiz(topic, difficulty, num_q)
        st.session_state.quiz = quiz

    if "quiz" in st.session_state and st.session_state.quiz:
        quiz = st.session_state.quiz
        answers = {}
        for i, q in enumerate(quiz, start=1):
            st.markdown(f"**Q{i}. {q['question']}**")
            options = q.get("options", [])
            answers[i] = st.radio(
                "Choose one:",
                options,
                key=f"q_{i}",
                index=None,
                label_visibility="collapsed"
            )

        if st.button("Check Quiz"):
            score = 0
            for i, q in enumerate(quiz, start=1):
                correct = q.get("answer", "")
                if answers[i] == correct:
                    score += 1
            percent = round(score / len(quiz) * 100)
            st.success(f"Score: {score}/{len(quiz)} ({percent}%)")
            save_progress(topic, percent)

            if percent < 50:
                st.info("Let's review the basics and try another short quiz.")
            elif percent < 80:
                st.info("Good progress. Review the questions you missed.")
            else:
                st.success("Excellent! Try a harder topic next.")

with tabs[3]:
    st.subheader("📈 Saved Quiz Progress")
    progress = load_progress()
    if progress:
        st.dataframe(progress, use_container_width=True, hide_index=True)
    else:
        st.info("No quiz attempts saved yet.")
