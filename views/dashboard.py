"""Dashboard: the first screen. One bold score hero, then quiet supporting detail."""
import plotly.graph_objects as go
import streamlit as st

from ui import components as c
from ui import nav, state, styles
from ui.courses import COURSES


def _greeting() -> str:
    h = state.now().hour
    return "Good morning" if h < 12 else "Good afternoon" if h < 17 else "Good evening"


def _headline(score: int, nxt) -> str:
    if score >= 100:
        return "You're fully compliant. Thanks for helping keep the company safe."
    if score == 0:
        return ("Four short courses and one assessment stand between you and full compliance. "
                "The first one takes about 15 minutes.")
    if nxt:
        return f"You're {score}% of the way to full compliance. Next up: {nxt['title'].lower()}."
    return f"You're {score}% of the way to full compliance. All courses done; the assessment is next."


def _gauge(score: int):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": "%", "font": {"size": 46, "color": "#FFFFFF", "family": styles.FONT}},
        gauge={
            "axis": {"range": [0, 100], "visible": False},
            "bar": {"color": styles.TEAL_BRIGHT, "thickness": 0.32},
            "bgcolor": "rgba(255,255,255,0.10)",
            "borderwidth": 0,
        },
    ))
    return styles.plotly_layout(fig, 200)


def _hero():
    s = st.session_state
    score = state.compliance_score()
    nxt = state.next_course()
    name = state.first_name()

    with st.container(key="hero"):
        left, right = st.columns([1.55, 1], vertical_alignment="center", gap="large")
        with left:
            greeting = f"{_greeting()}, {name}" if name else _greeting()
            c.render(f"<h1>{c.esc(greeting)}</h1><p>{c.esc(_headline(score, nxt))}</p>")
            b1, b2 = st.columns(2)
            with b1:
                if nxt:
                    label = "Continue learning" if state.lessons_done(nxt) else "Start learning"
                    if st.button(label, type="primary", icon=":material/play_arrow:", key="hero_primary"):
                        s.active_course = nxt["id"]
                        nav.go("library")
                elif not state.has_passed():
                    if st.button("Take the assessment", type="primary", icon=":material/quiz:", key="hero_primary"):
                        nav.go("assessment")
                else:
                    if st.button("View certificate", type="primary", icon=":material/workspace_premium:", key="hero_primary"):
                        nav.go("progress")
            with b2:
                if st.button("Ask the assistant", icon=":material/forum:", key="hero_ask"):
                    nav.go("assistant")
        with right:
            st.plotly_chart(_gauge(score), config=styles.PLOTLY_CONFIG, key="score_gauge")
            c.render('<div class="ciq-hero-meta">Compliance score. Courses count for 60%, '
                     'your best assessment for 40%.</div>')


def _name_prompt():
    s = st.session_state
    with st.container(key="card-name"):
        col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
        with col1:
            name = st.text_input(
                "What should we call you?", max_chars=30, placeholder="Your first name",
                help="Used on your dashboard and certificate. Kept only for this session and never sent to the AI.",
            )
        with col2:
            if st.button("Save name", key="save_name"):
                if state.NAME_PATTERN.fullmatch(name.strip()):
                    s.user_name = name.strip()
                    state.log("person", "Set up your profile")
                    st.rerun()
                else:
                    st.warning("Use English letters, spaces, dots, hyphens or apostrophes.")


def _stats():
    s = st.session_state
    done = state.courses_completed()
    deadlines = state.upcoming_deadlines()
    certs = s.certificates

    col1, col2, col3 = st.columns(3)
    with col1:
        remaining = len(COURSES) - done
        hint = "All courses complete." if not remaining else f"{remaining} left to finish."
        c.stat_card("Courses completed", f"{done} of {len(COURSES)}", hint, "school", "indigo")
    with col2:
        hint = (f"Next: {deadlines[0][0]['title']}, due {deadlines[0][1]:%d %b}"
                if deadlines else "Nothing due. You're all caught up.")
        c.stat_card("Upcoming deadlines", str(len(deadlines)), hint, "event", "amber")
    with col3:
        hint = (f"Latest issued {certs[-1]['date']:%d %b %Y}." if certs
                else "Pass the assessment to earn one.")
        c.stat_card("Certificates earned", str(len(certs)), hint, "workspace_premium", "teal")


def _courses_card():
    with st.container(key="card-mycourses"):
        c.section_title("Your courses")
        rows = []
        for course in COURSES:
            label, tone = state.course_status(course)
            rows.append(
                f'<div class="ciq-row"><div class="ciq-row-top">'
                f'<span class="name"><span class="ms ic-{course["tone"]}">{course["icon"]}</span>'
                f'{c.esc(course["title"])}</span>{c.pill(label, tone)}</div>'
                f'{c.bar(state.course_pct(course))}</div>'
            )
        c.render("".join(rows))
        if st.button("Open training library", icon=":material/school:", key="dash_library"):
            nav.go("library")


def _activity_card():
    s = st.session_state
    with st.container(key="card-activity"):
        c.section_title("Recent activity")
        if not s.activity:
            c.empty_state("history", "Nothing here yet",
                          "Lessons you finish, questions you ask and assessment results will appear here.")
            return
        items = []
        for a in s.activity[:6]:
            items.append(
                f'<div class="ciq-feed-item"><div class="ic ic-{a["tone"]}">{c.icon(a["icon"], 18)}</div>'
                f'<div><div class="txt">{c.esc(a["text"])}</div>'
                f'<div class="when">{state.time_ago(a["time"])}</div></div></div>'
            )
        c.render("".join(items))


def render():
    _hero()
    st.write("")
    if not st.session_state.user_name:
        _name_prompt()
        st.write("")
    _stats()
    st.write("")
    left, right = st.columns([1.4, 1], gap="medium")
    with left:
        _courses_card()
    with right:
        _activity_card()
    c.render('<div class="ciq-footnote">Deadlines are sample dates for this demo, counted from when you opened the app.</div>')
