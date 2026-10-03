"""Training library and course viewer. Lessons show the real policy text they're built on."""
import streamlit as st

from ui import components as c
from ui import state
from ui.courses import COMING_SOON, COURSES, explain_lesson, get_course, lesson_excerpts

QUOTE_CHARS = 650


@st.cache_data(show_spinner=False)
def _excerpts(course_id: str, lesson_id: str) -> list[dict]:
    course = get_course(course_id)
    lesson = next(l for l in course["lessons"] if l["id"] == lesson_id)
    return lesson_excerpts(course, lesson)


def _course_card(course: dict):
    s = st.session_state
    pct = state.course_pct(course)
    label, tone = state.course_status(course)
    done = state.is_complete(course)
    due = "Completed" if done else f"Due {state.due_date(course):%d %b}"

    with st.container(key=f"card-course-{course['id']}"):
        c.render(
            f'<div class="ciq-course"><div class="ciq-course-ic ic-{course["tone"]}">{c.icon(course["icon"], 24)}</div>'
            f'<h3>{c.esc(course["title"])}</h3><p>{c.esc(course["summary"])}</p>'
            f'<div class="meta"><span>{len(course["lessons"])} lessons, about {course["minutes"]} min</span>'
            f'{c.pill(label, tone)}</div>{c.bar(pct)}<div class="due">{due}</div></div>'
        )
        button = "Review course" if done else "Continue" if pct else "Start course"
        if st.button(button, key=f"open_{course['id']}", type="secondary" if done else "primary"):
            s.active_course = course["id"]
            st.rerun()


def _library():
    c.page_header("Training library",
                  "Short courses built from the company's own policies. Every lesson shows the policy text it's based on.")
    cols = st.columns(2, gap="medium")
    for i, course in enumerate(COURSES):
        with cols[i % 2]:
            _course_card(course)
            st.write("")

    c.section_title("Coming soon")
    cols = st.columns(2, gap="medium")
    for i, soon in enumerate(COMING_SOON):
        with cols[i % 2]:
            c.render(
                f'<div class="ciq-soon"><div class="ciq-course-ic ic-neutral" style="margin:0">{c.icon(soon["icon"], 24)}</div>'
                f'<div><div class="t">{c.esc(soon["title"])}</div><div class="ciq-small">{c.esc(soon["summary"])}</div></div></div>'
            )


def _stepper(course: dict, pos: int):
    s = st.session_state
    steps = []
    for i, lesson in enumerate(course["lessons"]):
        done = lesson["id"] in s.completed_lessons
        cls = ("done " if done else "") + ("current" if i == pos else "")
        num = c.icon("check", 16) if done and i != pos else str(i + 1)
        steps.append(f'<div class="ciq-step {cls}"><span class="num">{num}</span>'
                     f'<span class="label">{c.esc(lesson["title"])}</span></div>')
    c.render(f'<div class="ciq-stepper">{"".join(steps)}</div>')


def _mark_complete(course: dict, lesson: dict):
    s = st.session_state
    s.completed_lessons.add(lesson["id"])
    state.log("task_alt", f"Completed lesson: {lesson['title']}", "teal")
    if state.is_complete(course):
        s.course_completed_at[course["id"]] = state.now()
        state.log("school", f"Finished course: {course['title']}", "indigo")
        st.toast(f"Course complete: {course['title']}", icon=":material/celebration:")


def _viewer(course: dict):
    s = st.session_state
    lessons = course["lessons"]
    pos = s.lesson_pos.get(course["id"], 0)
    lesson = lessons[pos]
    done = lesson["id"] in s.completed_lessons

    if st.button("Back to library", icon=":material/arrow_back:", key="back_to_library"):
        s.active_course = None
        st.rerun()
    c.page_header(course["title"], course["summary"])
    _stepper(course, pos)

    main, side = st.columns([2.3, 1], gap="large")
    with main:
        with st.container(key="card-lesson"):
            c.render(f'<div class="ciq-lesson-kicker">Lesson {pos + 1} of {len(lessons)}</div>'
                     f'<h2 class="ciq-lesson-title">{c.esc(lesson["title"])}</h2>')
            excerpts = _excerpts(course["id"], lesson["id"])

            summary = s.lesson_summaries.get(lesson["id"])
            if summary:
                st.markdown(summary.replace("$", "\\$"))
                st.caption("Written by AI from the policy text below. Check the source if anything looks off.")
            else:
                c.render('<p class="ciq-muted">Get a short, plain-language lesson written from the policy text below.</p>')
                if st.button("Explain this lesson", type="primary", icon=":material/auto_awesome:",
                             key=f"explain_{lesson['id']}"):
                    with st.spinner("Writing your lesson from the policy..."):
                        try:
                            s.lesson_summaries[lesson["id"]] = explain_lesson(lesson, excerpts)
                            st.rerun()
                        except RuntimeError:
                            st.warning("The AI service is busy right now. The policy text below covers the same "
                                       "material; try again in a minute.")

            st.write("")
            c.section_title("From the policy")
            for h in excerpts:
                text = h["text"] if len(h["text"]) <= QUOTE_CHARS else h["text"][:QUOTE_CHARS].rsplit(" ", 1)[0] + "..."
                c.render(f'<div class="ciq-quote">{c.esc(text)}'
                         f'<div class="src">{c.esc(h["source"])}, page {h["page"]}</div></div>')

    with side:
        with st.container(key="card-lessonnav"):
            c.render(c.pill("Lesson completed", "success", "check_circle") if done
                     else c.pill("Not completed yet", "neutral"))
            st.write("")
            c.render(c.bar(state.course_pct(course)) +
                     f'<div class="ciq-muted ciq-small" style="margin-top:8px">'
                     f'{state.lessons_done(course)} of {len(lessons)} lessons done</div>')
            st.write("")
            if not done and st.button("Mark as complete", type="primary", icon=":material/check:",
                                      key=f"done_{lesson['id']}"):
                _mark_complete(course, lesson)
                st.rerun()
            prev_col, next_col = st.columns(2)
            with prev_col:
                if st.button("Previous", key="prev_lesson", disabled=pos == 0):
                    s.lesson_pos[course["id"]] = pos - 1
                    st.rerun()
            with next_col:
                if pos < len(lessons) - 1:
                    if st.button("Next lesson", key="next_lesson"):
                        s.lesson_pos[course["id"]] = pos + 1
                        st.rerun()
                elif st.button("Finish", key="finish_course"):
                    s.active_course = None
                    st.rerun()
            if state.is_complete(course):
                c.render('<div class="ciq-muted ciq-small" style="margin-top:12px">Course complete. '
                         'Once all four are done, take the assessment to earn your certificate.</div>')


def render():
    s = st.session_state
    if s.active_course:
        _viewer(get_course(s.active_course))
    else:
        _library()
