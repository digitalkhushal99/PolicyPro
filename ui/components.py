"""Small HTML building blocks shared across pages.
Markup is built on single lines: indented HTML inside st.markdown is read as a code block."""
import html

import streamlit as st


def esc(text) -> str:
    return html.escape(str(text))


def render(markup: str):
    st.markdown(markup, unsafe_allow_html=True)


def icon(name: str, size: int = 20) -> str:
    return f'<span class="ms" style="font-size:{size}px" aria-hidden="true">{name}</span>'


def page_header(title: str, subtitle: str = ""):
    sub = f"<p>{esc(subtitle)}</p>" if subtitle else ""
    render(f'<div class="ciq-page-head"><h1>{esc(title)}</h1>{sub}</div>')


def section_title(text: str):
    render(f'<div class="ciq-section">{esc(text)}</div>')


def stat_card(label: str, value: str, hint: str = "", icon_name: str = "insights", tone: str = "indigo"):
    render(
        f'<div class="ciq-stat"><div class="ic ic-{tone}">{icon(icon_name)}</div>'
        f'<div class="label">{esc(label)}</div><div class="value">{esc(value)}</div>'
        f'<div class="hint">{esc(hint)}</div></div>'
    )


def pill(text: str, tone: str = "neutral", icon_name: str | None = None) -> str:
    ic = icon(icon_name, 15) if icon_name else ""
    return f'<span class="pill pill-{tone}">{ic}{esc(text)}</span>'


def bar(pct: float) -> str:
    pct = max(0, min(100, pct))
    return (f'<div class="ciq-bar" role="progressbar" aria-valuenow="{pct:.0f}" aria-valuemin="0" '
            f'aria-valuemax="100"><span style="width:{pct:.0f}%"></span></div>')


def empty_state(icon_name: str, title: str, body: str):
    render(f'<div class="ciq-empty">{icon(icon_name, 36)}<div class="t">{esc(title)}</div><div>{esc(body)}</div></div>')
