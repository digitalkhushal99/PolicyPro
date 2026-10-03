"""Page registry so any page can send the user to another one."""
import streamlit as st

PAGES: dict = {}


def go(key: str):
    st.switch_page(PAGES[key])
