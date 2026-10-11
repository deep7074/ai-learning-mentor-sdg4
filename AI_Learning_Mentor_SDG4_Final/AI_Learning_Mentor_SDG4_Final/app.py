import os
import streamlit as st
from dotenv import load_dotenv

from database import (
    init_db, ensure_demo_users, save_profile, load_profile,
    save_chat, load_chats, clear_chats, save_progress,
    load_progress, save_note, load_notes, delete_note, dashboard_stats
)
from llm import mentor_answer, generate_study_plan, generate_quiz, generate_revision_summary
from risk import engagement_indicator
from rag import extract_pdf_text, clean_text, retrieve_context

load_dotenv()
init_db()
ensure_demo_users()

st.set_page_config(
    page_title="AI Learning Mentor | SDG 4",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Styling ----------
st.markdown("""
<style>
.main-title {font-size: 2.3rem; font-weight: 800;}
.subtitle {color: #64748b; font-size: 1.05rem;}
.card {
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,.2);
    margin-bottom: .8rem;
}
.small {font-size: .88rem; color: #64748b;}
</style>
""", unsafe_allow_html=True)

# ---------- Authentication ----------
def login_screen():
    st.markdown('<div class="main-title">🎓 AI Learning Mentor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">SDG 4 – Quality Education</div>', unsafe_allow_html=True)
    st.write("")
    st.info("Demo login: **student / student123** or **admin / admin123**")

    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        student_user = os.getenv("DEMO_STUDENT_USER", "student")
        student_pass = os.getenv("DEMO_STUDENT_PASSWORD", "student123")
        admin_user = os.getenv("DEMO_ADMIN_USER", "admin")
        admin_pass = os.getenv("DEMO_ADMIN_PASSWORD", "admin123")

        if username == student_user and password == student_pass:
            st.session_state.logged_in = True
            st.session_state.role = "student"
            st.rerun()
        elif username == admin_user and password == admin_pass:
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.rerun()
        else:
            st.error("Invalid demo credentials.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_screen()
    st.stop()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🎓 AI Learning Mentor")
    st.caption("SDG 4 • Quality Education")
    st.write(f"Logged in as: **{st.session_state.role.title()}**")

    language = st.selectbox("Interface language", ["English", "বাংলা"])
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.divider()

profile = load_profile()
if not profile:
    profile = {
        "name": "Student",
        "course": "BCA",
        "attendance": 75,
        "study_hours": 8,
        "pending": 1,
        "quiz_score": 60,
    }

# ---------- Admin ----------
if st.session_state.role == "admin":
    st.title("🛡️ Admin / Teacher Dashboard")
    st.caption("Demo dashboard for project presentation. Real deployments need authentication, authorization and privacy controls.")

    stats = dashboard_stats()
    a, b, c, d = st.columns(4)
    a.metric("Chat messages", stats["chat_messages"])
    b.metric("Quiz attempts", stats["quiz_attempts"])
    c.metric("Average quiz score", f"{stats['avg_quiz_score']}%")
    d.metric("Uploaded note files", stats["notes"])

    st.subheader("Student Profile Snapshot")
    st.json(profile)

    progress = load_progress()
    if progress:
        st.subheader("Quiz Performance")
        st.dataframe(progress, use_container_width=True, hide_index=True)

    st.subheader("Uploaded Study Materials")
    notes = load_notes()
    if notes:
        for note in notes:
            with st.expander(note["filename"]):
                st.write(note["content"][:1500] + ("..." if len(note["content"]) > 1500 else ""))
                if st.button(f"Delete {note['filename']}", key=f"del_{note['id']}"):
                    delete_note(note["id"])
                    st.rerun()
    else:
        st.info("No study materials uploaded yet.")

    st.divider()
    st.success("For your viva: explain that the dashboard is a prototype and real student data must be protected.")
    st.stop()

# ---------- Student profile ----------
st.markdown('<div class="main-title">🎓 AI Learning Mentor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your LLM-powered academic companion for SDG 4 – Quality Education.</div>', unsafe_allow_html=True)

with st.expander("👤 Student Profile", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Name", profile.get("name", "Student"))
        course = st.text_input("Course / Class", profile.get("course", "BCA"))
        attendance = st.slider("Attendance (%)", 0, 100, int(profile.get("attendance", 75)))
    with c2:
        study_hours = st.number_input("Study hours per week", 0.0, 80.0, float(profile.get("study_hours", 8)), 0.5)
        pending = st.number_input("Pending assignments", 0, 30, int(profile.get("pending", 1)))
        quiz_score = st.slider("Recent quiz score (%)", 0, 100, int(profile.get("quiz_score", 60)))

    if st.button("💾 Save Profile", use_container_width=True):
        save_profile(name, course, attendance, study_hours, pending, quiz_score)
        st.success("Profile saved.")
        st.rerun()

profile = {
    "name": name if 'name' in locals() else profile["name"],
    "course": course if 'course' in locals() else profile["course"],
    "attendance": attendance if 'attendance' in locals() else profile["attendance"],
    "study_hours": study_hours if 'study_hours' in locals() else profile["study_hours"],
    "pending": pending if 'pending' in locals() else profile["pending"],
    "quiz_score": quiz_score if 'quiz_score' in locals() else profile["quiz_score"],
}

indicator, reasons = engagement_indicator(profile)

# ---------- Dashboard ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Attendance", f"{profile['attendance']}%")
c2.metric("Study / week", f"{profile['study_hours']:g} h")
c3.metric("Pending work", profile["pending"])
c4.metric("Quiz score", f"{profile['quiz_score']}%")

if indicator == "Needs attention":
    st.warning("🟠 Your current pattern suggests that extra academic support may be useful.")
elif indicator == "Watch":
    st.info("🟡 You are doing reasonably well, but a few habits could be strengthened.")
else:
    st.success("🟢 Your current study pattern looks stable.")

if reasons:
    with st.expander("Why am I seeing this indicator?"):
        for r in reasons:
            st.write("• " + r)

st.caption("This is a transparent academic-support indicator, not a clinical or scientifically validated dropout prediction.")

tabs = st.tabs(["💬 AI Mentor", "📚 My Notes / RAG", "🗓️ Study Plan", "📈 Progress"])

# ---------- Chat ----------
with tabs[0]:
    st.subheader("💬 Ask your AI Mentor")
    st.write("Examples: *Explain TCP/IP simply*, *Help me revise Java in 5 days*, *Explain this topic from my notes*.")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = load_chats()

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    col_a, col_b = st.columns([3, 1])
    with col_b:
        if st.button("Clear chat"):
            clear_chats()
            st.session_state.chat_messages = []
            st.rerun()

    prompt = st.chat_input("Type your study question...")
    if prompt:
        notes = load_notes()
        context = retrieve_context(prompt, notes)

        save_chat("user", prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI Mentor is thinking..."):
                answer = mentor_answer(profile, prompt, context)
            st.markdown(answer)

        save_chat("assistant", answer)
        st.session_state.chat_messages.append({"role": "assistant", "content": answer})

# ---------- Notes / RAG ----------
with tabs[1]:
    st.subheader("📚 Upload Your Study Notes")
    st.write("Upload PDF notes. The mentor can retrieve relevant text and use it as context when answering.")

    uploaded = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded is not None:
        if st.button("Add PDF to My Knowledge Base"):
            try:
                text = clean_text(extract_pdf_text(uploaded.getvalue()))
                if text:
                    save_note(uploaded.name, text)
                    st.success(f"Added {uploaded.name} to your study knowledge base.")
                    st.rerun()
                else:
                    st.error("No readable text was found in this PDF.")
            except Exception as e:
                st.error(f"Could not read the PDF: {e}")

    notes = load_notes()
    if notes:
        st.write("**Saved materials:**")
        for note in notes:
            st.write(f"📄 {note['filename']}")

        topic = st.text_input("Topic for an AI revision sheet", "Networking")
        if st.button("Generate Revision Sheet"):
            combined = retrieve_context(topic, notes, max_chars=9000)
            if not combined:
                st.warning("No relevant note text found.")
            else:
                with st.spinner("Creating revision sheet..."):
                    summary = generate_revision_summary(topic, combined)
                st.markdown(summary)
    else:
        st.info("Upload your syllabus/notes PDF to activate the RAG-style study assistant.")

# ---------- Study plan ----------
with tabs[2]:
    st.subheader("🗓️ Personalized Study Plan")
    days = st.slider("Plan length (days)", 3, 14, 7)
    subjects = st.text_input("Subjects / topics", "Cyber Security, Research Methodology, Java, Networking")

    if st.button("Generate AI Study Plan"):
        with st.spinner("Creating your plan..."):
            plan = generate_study_plan(profile, subjects, days)
        st.markdown(plan)

# ---------- Progress ----------
with tabs[3]:
    st.subheader("📈 Learning Progress")
    progress = load_progress()
    if progress:
        st.dataframe(progress, use_container_width=True, hide_index=True)
        scores = [float(x["Score"]) for x in progress]
        st.line_chart(scores)
    else:
        st.info("No quiz attempts saved yet.")

st.divider()
st.caption("AI Learning Mentor • SDG 4 • BCA Project Prototype")
