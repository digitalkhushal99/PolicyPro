"""Progress and certificates."""
import plotly.graph_objects as go
import streamlit as st

import certificate
from ui import components as c
from ui import state, styles
from ui.courses import COURSES


def _trend_chart():
    attempts = st.session_state.quiz_attempts
    x = [f"Attempt {a['n']}" for a in attempts]
    y = [a["pct"] for a in attempts]
    colors = [styles.TEAL if a["passed"] else styles.WARNING for a in attempts]
    fig = go.Figure(go.Scatter(
        x=x, y=y, mode="lines+markers",
        line=dict(color=styles.INDIGO, width=3, shape="spline"),
        marker=dict(size=11, color=colors, line=dict(color="#FFFFFF", width=2)),
        fill="tozeroy", fillcolor="rgba(31,77,63,0.08)",
        hovertemplate="%{x}: %{y}%<extra></extra>",
    ))
    fig.add_hline(y=80, line_dash="dot", line_color=styles.MUTED,
                  annotation_text="Pass mark", annotation_position="top left",
                  annotation_font=dict(color=styles.MUTED, size=12))
    fig.update_yaxes(range=[0, 105], ticksuffix="%", gridcolor=styles.TRACK, zeroline=False)
    fig.update_xaxes(showgrid=False)
    return styles.plotly_layout(fig, 260)


def _timeline():
    s = st.session_state
    events = [(t, f"Finished {c.esc(next(x['title'] for x in COURSES if x['id'] == cid))}", "")
              for cid, t in s.course_completed_at.items()]
    events += [(a["time"], f"Passed the assessment with {a['pct']}%", "gold")
               for a in s.quiz_attempts if a["passed"]]
    if not events:
        c.empty_state("timeline", "No completed training yet",
                      "Finished courses and passed assessments will be listed here.")
        return
    items = [f'<div class="ciq-tl-item {cls}"><div class="t">{text}</div>'
             f'<div class="d">{t:%d %b %Y, %I:%M %p}</div></div>'
             for t, text, cls in sorted(events, key=lambda e: e[0], reverse=True)]
    c.render(f'<div class="ciq-timeline">{"".join(items)}</div>')


def render():
    s = st.session_state
    c.page_header("Progress and certificates", "What you've completed this session, and the certificates you've earned.")

    col1, col2, col3 = st.columns(3)
    with col1:
        c.stat_card("Compliance score", f"{state.compliance_score()}%",
                    "Courses 60%, best assessment 40%.", "verified_user", "indigo")
    with col2:
        c.stat_card("Lessons completed", f"{state.total_lessons_done()} of {state.total_lessons()}",
                    f"Across {len(COURSES)} courses.", "task_alt", "teal")
    with col3:
        best = state.best_quiz_pct()
        c.stat_card("Best assessment score", f"{best}%" if s.quiz_attempts else "None yet",
                    "80% or more earns a certificate.", "quiz", "amber")
    st.write("")

    left, right = st.columns([1.3, 1], gap="medium")
    with left:
        with st.container(key="card-trend"):
            c.section_title("Assessment scores")
            if s.quiz_attempts:
                st.plotly_chart(_trend_chart(), config=styles.PLOTLY_CONFIG, key="trend_chart")
            else:
                c.empty_state("show_chart", "No attempts yet",
                              "Take the assessment to start tracking your scores.")
    with right:
        with st.container(key="card-timeline"):
            c.section_title("Completed training")
            _timeline()

    st.write("")
    c.section_title("Certificates")
    if not s.certificates:
        c.render('<p class="ciq-muted">Pass the assessment with 80% or more to earn your first certificate.</p>')
        return
    name = s.user_name.strip()
    if not name:
        st.info("Add your name on the dashboard to download certificates.")
    cols = st.columns(2, gap="medium")
    for i, cert in enumerate(reversed(s.certificates)):
        with cols[i % 2]:
            with st.container(key=f"card-cert-{cert['id']}"):
                c.render(f'<div class="ciq-cert"><div class="ic ic-teal">{c.icon("workspace_premium", 24)}</div>'
                         f'<div><div class="t">Compliance Policy Training</div>'
                         f'<div class="d">Issued {cert["date"]:%d %B %Y}. Score {cert["score"]}/{cert["total"]}.'
                         f'<br>Certificate ID {cert["id"]}</div></div></div>')
                if name:
                    st.download_button(
                        "Download PDF", icon=":material/download:", key=f"dl_{cert['id']}",
                        data=certificate.make_certificate(name, cert["score"], cert["total"], cert["id"], cert["date"].date()),
                        file_name=f"complianceiq_certificate_{cert['id']}.pdf", mime="application/pdf",
                    )
