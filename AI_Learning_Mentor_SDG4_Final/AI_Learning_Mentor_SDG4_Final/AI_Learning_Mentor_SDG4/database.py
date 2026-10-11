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

def load_chats(limit=30):
    conn = get_conn()
    rows = conn.execute(
        "SELECT role, content FROM chats ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]

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
