"""Session state: everything the app remembers during one browser session.
Nothing is written to disk, so closing or refreshing the tab starts fresh."""
import re
from datetime import datetime, timedelta, timezone

import streamlit as st

from ui.courses import COURSES

IST = timezone(timedelta(hours=5, minutes=30))
PASS_MARK = 0.8
NAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z .'\-]{1,49}")


def now() -> datetime:
    return datetime.now(IST)


def init():
    s = st.session_state
    s.setdefault("user_name", "")
    s.setdefault("started_at", now())
    s.setdefault("messages", [])            # chat history
    s.setdefault("chip_round", 0)           # resets the suggestion chips after use
    s.setdefault("completed_lessons", set())
    s.setdefault("course_completed_at", {}) # course id -> datetime
    s.setdefault("lesson_pos", {})          # course id -> current lesson index
    s.setdefault("lesson_summaries", {})    # lesson id -> AI-written lesson
    s.setdefault("active_course", None)
    s.setdefault("quiz", None)
    s.setdefault("quiz_idx", 0)
    s.setdefault("quiz_results", [])
    s.setdefault("quiz_checked", False)
    s.setdefault("quiz_attempts", [])
    s.setdefault("certificates", [])
    s.setdefault("activity", [])


def log(icon_name: str, text: str, tone: str = "indigo"):
    feed = st.session_state.activity
    feed.insert(0, {"icon": icon_name, "text": text, "tone": tone, "time": now()})
    del feed[30:]


def first_name() -> str:
    name = st.session_state.user_name.strip()
    return name.split()[0] if name else ""


def time_ago(dt: datetime) -> str:
    secs = int((now() - dt).total_seconds())
    if secs < 60:
        return "Just now"
    if secs < 3600:
        return f"{secs // 60} min ago"
    if secs < 86400:
        return f"{secs // 3600} hr ago"
    return dt.strftime("%d %b")


# ---------- course progress ----------

def lessons_done(course: dict) -> int:
    return sum(l["id"] in st.session_state.completed_lessons for l in course["lessons"])


def course_pct(course: dict) -> int:
    return round(100 * lessons_done(course) / len(course["lessons"]))


def is_complete(course: dict) -> bool:
    return lessons_done(course) == len(course["lessons"])


def courses_completed() -> int:
    return sum(is_complete(c) for c in COURSES)


def total_lessons() -> int:
    return sum(len(c["lessons"]) for c in COURSES)


def total_lessons_done() -> int:
    return sum(lessons_done(c) for c in COURSES)


def next_course():
    return next((c for c in COURSES if not is_complete(c)), None)


def due_date(course: dict):
    """Demo deadlines, counted from when this session started."""
    return (st.session_state.started_at + timedelta(days=course["due_days"])).date()


def upcoming_deadlines() -> list:
    return sorted(((c, due_date(c)) for c in COURSES if not is_complete(c)), key=lambda x: x[1])


def course_status(course: dict) -> tuple[str, str]:
    if is_complete(course):
        return "Completed", "success"
    if due_date(course) < now().date():
        return "Overdue", "danger"
    if lessons_done(course):
        return "In progress", "indigo"
    return "Not started", "neutral"


# ---------- assessment & score ----------

def best_quiz_pct() -> int:
    return max((a["pct"] for a in st.session_state.quiz_attempts), default=0)


def has_passed() -> bool:
    return any(a["passed"] for a in st.session_state.quiz_attempts)


def compliance_score() -> int:
    """Courses count for 60%, the best assessment score for 40%."""
    lesson_pct = 100 * total_lessons_done() / total_lessons()
    return round(0.6 * lesson_pct + 0.4 * best_quiz_pct())
