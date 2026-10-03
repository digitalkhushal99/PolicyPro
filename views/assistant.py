"""AI compliance assistant: chat grounded in the policy documents."""
import streamlit as st

import rag
from ui import components as c
from ui import state

MAX_QUESTION_CHARS = 500
SUGGESTIONS = [
    "Can I accept a gift from a vendor?",
    "How do I report harassment?",
    "What counts as a bribe?",
    "What personal data does the company collect?",
]


# ======================================================================
# AI RESPONSE FUNCTION: the single place where the app talks to the AI.
# It runs the RAG pipeline in rag.py: search the policy index, then ask
# Gemini to answer only from the matching excerpts, with citations.
# Returns {"status", "answer", "sources", ...}.
# ======================================================================
def get_ai_response(prompt: str, history: list[dict]) -> dict:
    return rag.answer(prompt, history)


def _render_message(m: dict):
    if m["role"] == "user":
        with st.chat_message("user"):
            st.markdown(m["content"].replace("$", "\\$"))
        return
    with st.chat_message("assistant", avatar=":material/shield:"):
        st.markdown(m["content"].replace("$", "\\$"))  # stop $ signs being read as maths
        status = m.get("status")
        if status == "error":
            st.warning("The AI service is busy right now, so here are the policy pages that match your question.")
        elif status in ("out_of_scope", "not_covered"):
            st.caption("This is outside what the loaded policies cover. For help, contact the Office of Integrity & Compliance.")
        sources = m.get("sources") or []
        is_question = m["content"].strip().endswith("?") and len(m["content"]) < 250
        if sources and not is_question:
            with st.expander(f"Sources ({len(sources)})", icon=":material/description:"):
                for s in sources:
                    st.markdown(f"**{s['source']}**, page {s['page']} (match {s['score']})")


def render():
    s = st.session_state
    head, action = st.columns([5, 1], vertical_alignment="bottom")
    with head:
        c.page_header("AI compliance assistant",
                      "Ask in plain language. Answers come only from the company's policies, with the page they're based on.")
    with action:
        if s.messages and st.button("Clear chat", icon=":material/restart_alt:", key="clear_chat"):
            s.messages = []
            st.rerun()

    if not s.messages:
        name = state.first_name()
        with st.chat_message("assistant", avatar=":material/shield:"):
            st.markdown(
                f"Hi{', ' + name if name else ''}. I can answer questions about the Code of Conduct, "
                "the Anti-Bribery Policy, the POSH Policy and the Data Privacy Policy. "
                "Pick a question below or type your own."
            )

    for m in s.messages:
        _render_message(m)

    chip = st.pills("Suggested questions", SUGGESTIONS, key=f"chips_{s.chip_round}",
                    label_visibility="collapsed")
    typed = st.chat_input("Ask about gifts, bribery, harassment or data privacy",
                          max_chars=MAX_QUESTION_CHARS)
    question = typed or chip
    if not question:
        return
    if chip and not typed:
        s.chip_round += 1  # clear the chip selection on the next run

    history = [{"role": m["role"], "content": m["content"]} for m in s.messages]
    _render_message({"role": "user", "content": question})
    with st.chat_message("assistant", avatar=":material/shield:"):
        with st.spinner("Checking the policies..."):
            result = get_ai_response(question, history)

    s.messages.append({"role": "user", "content": question})
    s.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result.get("sources", []),
        "status": result["status"],
    })
    short = question if len(question) <= 60 else question[:57] + "..."
    state.log("forum", f"Asked: {short}", "violet")
    st.rerun()
