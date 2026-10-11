import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).with_name("mentor.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            role TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT,
            course TEXT,
            attendance REAL,
            study_hours REAL,
            pending INTEGER,
            quiz_score REAL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            score REAL,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def ensure_demo_users():
    conn = get_conn()
    users = [
        ("student", "student"),
        ("admin", "admin"),
    ]
    for username, role in users:
        conn.execute(
            "INSERT OR IGNORE INTO users(username, role, created_at) VALUES (?, ?, ?)",
            (username, role, datetime.now().isoformat(timespec="seconds"))
        )
    conn.commit()
    conn.close()

def save_profile(name, course, attendance, study_hours, pending, quiz_score):
    conn = get_conn()
    conn.execute("""
        INSERT INTO profile (id, name, course, attendance, study_hours, pending, quiz_score)
        VALUES (1, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            course=excluded.course,
            attendance=excluded.attendance,
            study_hours=excluded.study_hours,
            pending=excluded.pending,
            quiz_score=excluded.quiz_score
    """, (name, course, attendance, study_hours, pending, quiz_score))
    conn.commit()
    conn.close()

def load_profile():
    conn = get_conn()
    row = conn.execute("SELECT * FROM profile WHERE id=1").fetchone()
    conn.close()
    return dict(row) if row else {}

def save_chat(role, content):
    conn = get_conn()
    conn.execute(
        "INSERT INTO chats(role, content, created_at) VALUES (?, ?, ?)",
        (role, content, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

def load_chats(limit=40):
    conn = get_conn()
    rows = conn.execute(
        "SELECT role, content, created_at FROM chats ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]

def clear_chats():
    conn = get_conn()
    conn.execute("DELETE FROM chats")
    conn.commit()
    conn.close()

def save_progress(topic, score):
    conn = get_conn()
    conn.execute(
        "INSERT INTO progress(topic, score, created_at) VALUES (?, ?, ?)",
        (topic, score, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

def load_progress():
    conn = get_conn()
    rows = conn.execute(
        "SELECT topic AS Topic, score AS Score, created_at AS Date "
        "FROM progress ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_note(filename, content):
    conn = get_conn()
    conn.execute(
        "INSERT INTO notes(filename, content, created_at) VALUES (?, ?, ?)",
        (filename, content, datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

def load_notes():
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, filename, content, created_at FROM notes ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_note(note_id):
    conn = get_conn()
    conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()

def dashboard_stats():
    conn = get_conn()
    chats = conn.execute("SELECT COUNT(*) FROM chats").fetchone()[0]
    quizzes = conn.execute("SELECT COUNT(*) FROM progress").fetchone()[0]
    avg = conn.execute("SELECT AVG(score) FROM progress").fetchone()[0]
    notes = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    conn.close()
    return {
        "chat_messages": chats,
        "quiz_attempts": quizzes,
        "avg_quiz_score": round(avg, 1) if avg is not None else 0,
        "notes": notes,
    }
