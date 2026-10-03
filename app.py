"""PolicyCompass: AI policy training assistant (alternate visual design of the same app).
Run with:  streamlit run app.py"""
import streamlit as st

st.set_page_config(page_title="PolicyCompass", page_icon="assets/icon.svg", layout="wide",
                   initial_sidebar_state="collapsed")

import rag  # noqa: E402  (imports after set_page_config on purpose)
from ui import components as c  # noqa: E402
from ui import nav, state, styles  # noqa: E402
from views import assessment, assistant, dashboard, library, progress, team  # noqa: E402

styles.inject()
state.init()


@st.cache_resource(show_spinner="Loading the policy library...")
def warm_up():
    rag._resources()  # FAISS index, chunks and embedding model, loaded once per server
    return True


warm_up()

pages = {
    "dashboard": st.Page(dashboard.render, title="Home", icon=":material/home:",
                         url_path="dashboard", default=True),
    "assistant": st.Page(assistant.render, title="Ask", icon=":material/chat_bubble:", url_path="assistant"),
    "library": st.Page(library.render, title="Learn", icon=":material/menu_book:", url_path="library"),
    "assessment": st.Page(assessment.render, title="Quiz", icon=":material/edit_note:", url_path="assessment"),
    "progress": st.Page(progress.render, title="Progress", icon=":material/trending_up:", url_path="progress"),
    "team": st.Page(team.render, title="Team", icon=":material/groups:", url_path="team"),
}
nav.PAGES.update(pages)

# Design change 1: navigation moves from a left sidebar to a top bar (position="top").
current = st.navigation(list(pages.values()), position="top")
st.logo("assets/logo.svg", size="large", icon_image="assets/icon.svg")

current.run()

# Design change 2: the sidebar's notices become a quiet footer on every page.
name = st.session_state.user_name.strip()
who = f"Signed in as {c.esc(name)}. " if name else ""
c.render(
    f'<div class="ciq-footer"><strong>{who}</strong>The assistant is an AI, not a person. Your questions are sent to '
    'Google Gemini to write answers, and nothing is saved once you close or refresh this tab. '
    'Student demo built on public Infosys policy documents; not affiliated with or endorsed by Infosys. '
    'General guidance, not legal advice.</div>'
)
