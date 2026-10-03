"""Assessment: one question at a time with instant feedback, then results and certificate."""
import math
import uuid

import streamlit as st

import certificate
import quiz
from ui import components as c
from ui import state


def _start():
    s = st.session_state
    with st.spinner("Writing your questions from the policies..."):
        s.quiz = quiz.generate_quiz()
    s.quiz_idx = 0
    s.quiz_results = []
    s.quiz_checked = False
    state.log("quiz", "Started an assessment", "amber")


def _intro():
    s = st.session_state
    with st.container(key="card-quizintro"):
        left, right = st.columns([2.2, 1], vertical_alignment="center")
        with left:
            c.render('<h3 style="margin:0 0 6px">Ready when you are</h3>'
                     '<p class="ciq-muted" style="margin:0">Each assessment is written fresh from the policy '
                     'documents, so no two are the same. You\'ll see whether you\'re right after every question.</p>')
            if state.courses_completed() < 4:
                st.write("")
                c.render(c.pill("Tip: finishing the courses first makes this easier", "warning", "lightbulb"))
        with right:
            if st.button("Start assessment", type="primary", icon=":material/play_arrow:", key="start_quiz"):
                _start()
                st.rerun()
    if s.quiz_attempts:
        st.write("")
        c.render(f'<div class="ciq-muted ciq-small">You have taken {len(s.quiz_attempts)} '
                 f'assessment{"s" if len(s.quiz_attempts) > 1 else ""} this session. '
                 f'Best score: {state.best_quiz_pct()}%.</div>')


def _question():
    s = st.session_state
    questions = s.quiz["questions"]
    n, idx = len(questions), s.quiz_idx
    q = questions[idx]
    correct_so_far = sum(r["correct"] for r in s.quiz_results)

    c.render(f'<div class="ciq-qhead"><span>Question {idx + 1} of {n}</span>'
             f'<span>{correct_so_far} correct so far</span></div>{c.bar(100 * idx / n)}')
    if s.quiz["origin"] == "fallback":
        st.caption("The AI service is busy, so this is the standard question set.")
    st.write("")

    with st.container(key="card-question"):
        c.render(f'<p class="ciq-scenario">{c.esc(q["scenario"])}</p>'
                 f'<h3 class="ciq-question">{c.esc(q["question"])}</h3>')
        choice = st.radio("Choose an answer", q["options"], index=None, key=f"{s.quiz['id']}_{idx}",
                          disabled=s.quiz_checked, label_visibility="collapsed")

        if not s.quiz_checked:
            st.write("")
            if st.button("Check answer", type="primary", disabled=choice is None, key=f"check_{idx}"):
                correct = choice == q["options"][q["correct_index"]]
                s.quiz_results.append({"chosen": choice, "correct": correct})
                s.quiz_checked = True
                st.rerun()
            return

        result = s.quiz_results[idx]
        answer = q["options"][q["correct_index"]]
        src = f'<div class="src">{c.esc(q["source"])}, page {q["page"]}</div>'
        if result["correct"]:
            c.render(f'<div class="ciq-feedback ok"><div class="title">{c.icon("check_circle")} Correct</div>'
                     f'<div>{c.esc(q["explanation"])}</div>{src}</div>')
        else:
            c.render(f'<div class="ciq-feedback bad"><div class="title">{c.icon("cancel")} Not quite</div>'
                     f'<div>The answer is: <strong>{c.esc(answer)}</strong>. {c.esc(q["explanation"])}</div>{src}</div>')
        last = idx == n - 1
        if st.button("See my results" if last else "Next question", type="primary", key=f"next_{idx}",
                     icon=":material/flag:" if last else ":material/arrow_forward:"):
            s.quiz_idx += 1
            s.quiz_checked = False
            st.rerun()


def _record(score: int, n: int, pct: int, passed: bool):
    """Save the attempt once, even though Streamlit reruns this page many times."""
    s = st.session_state
    if s.quiz.get("recorded"):
        return
    s.quiz["recorded"] = True
    s.quiz_attempts.append({"n": len(s.quiz_attempts) + 1, "score": score, "total": n,
                            "pct": pct, "passed": passed, "time": state.now()})
    state.log("quiz", f"Scored {score}/{n} on the assessment", "amber")
    if passed:
        s.certificates.append({"id": uuid.uuid4().hex[:10].upper(), "score": score, "total": n,
                               "date": state.now()})
        state.log("workspace_premium", "Earned a compliance certificate", "teal")


def _results():
    s = st.session_state
    questions = s.quiz["questions"]
    n = len(questions)
    score = sum(r["correct"] for r in s.quiz_results)
    pct = round(100 * score / n)
    needed = math.ceil(state.PASS_MARK * n)
    passed = score >= needed
    _record(score, n, pct, passed)

    if passed:
        title, body = "You passed", f"You scored {pct}%. Your certificate is ready below."
    else:
        title = "Not quite there yet"
        body = (f"You scored {pct}%. You need {needed} of {n} to pass. "
                "Review the answers, then try a fresh set of questions.")
    c.render(f'<div class="ciq-result {"pass" if passed else "fail"}"><div class="big">{score}/{n}</div>'
             f'<div><div class="t">{title}</div><div class="d">{c.esc(body)}</div></div></div>')

    with st.expander("Review your answers", icon=":material/fact_check:"):
        for i, (q, r) in enumerate(zip(questions, s.quiz_results), start=1):
            mark = "✅" if r["correct"] else "❌"
            st.markdown(f"{mark} **Q{i}. {q['question']}**  \nYour answer: {r['chosen']}  \n"
                        f"Correct answer: {q['options'][q['correct_index']]}  \n"
                        f"*{q['explanation']}* ({q['source']}, page {q['page']})")

    if passed:
        cert = s.certificates[-1]
        with st.container(key="card-certificate"):
            c.render(f'<div class="ciq-cert"><div class="ic ic-teal">{c.icon("workspace_premium", 24)}</div>'
                     f'<div><div class="t">Compliance Policy Training certificate</div>'
                     f'<div class="d">Certificate ID {cert["id"]}, issued {cert["date"]:%d %B %Y}</div></div></div>')
            name = st.text_input("Name on the certificate", value=s.user_name, max_chars=50,
                                 help="Used only to create the PDF. Never sent to the AI.").strip()
            if name and state.NAME_PATTERN.fullmatch(name):
                if not s.user_name:
                    s.user_name = name
                st.download_button(
                    "Download certificate (PDF)", type="primary", icon=":material/download:",
                    data=certificate.make_certificate(name, cert["score"], cert["total"], cert["id"], cert["date"].date()),
                    file_name="complianceiq_certificate.pdf", mime="application/pdf",
                )
            elif name:
                st.warning("Use English letters, spaces, dots, hyphens or apostrophes.")

    st.write("")
    if st.button("Take a new assessment", type="secondary" if passed else "primary",
                 icon=":material/refresh:", key="retake"):
        _start()
        st.rerun()


def render():
    s = st.session_state
    c.page_header("Assessment",
                  f"Five scenario questions drawn from all four policies. "
                  f"Score {int(state.PASS_MARK * 100)}% or more to earn your certificate.")
    if not s.quiz:
        _intro()
    elif s.quiz_idx < len(s.quiz["questions"]):
        _question()
    else:
        _results()
