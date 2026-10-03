"""Manager view with SAMPLE data, to show how the tool would report across a company."""
import plotly.graph_objects as go
import streamlit as st

from ui import components as c
from ui import styles

COURSE_NAMES = ["Anti-bribery", "Gifts", "Harassment", "Data privacy"]
# Sample data: % of each department's staff who finished each course
COMPLETION = {
    "Engineering": [92, 88, 95, 81],
    "Sales": [74, 69, 90, 62],
    "Marketing": [85, 80, 93, 77],
    "Finance": [97, 95, 98, 94],
    "Human resources": [100, 98, 100, 96],
    "Operations": [68, 61, 84, 58],
}
TARGET = 75


def _bar_chart():
    avg = {d: sum(v) / len(v) for d, v in COMPLETION.items()}
    depts = sorted(avg, key=avg.get)
    vals = [round(avg[d]) for d in depts]
    colors = [styles.WARNING if v < TARGET else styles.INDIGO for v in vals]
    fig = go.Figure(go.Bar(x=vals, y=depts, orientation="h", marker=dict(color=colors, cornerradius=6),
                           text=[f"{v}%" for v in vals], textposition="outside",
                           hovertemplate="%{y}: %{x}%<extra></extra>"))
    fig.add_vline(x=TARGET, line_dash="dot", line_color=styles.MUTED,
                  annotation_text=f"Target {TARGET}%", annotation_position="top",
                  annotation_font=dict(color=styles.MUTED, size=12))
    fig.update_xaxes(range=[0, 110], showgrid=False, visible=False)
    fig.update_yaxes(showgrid=False)
    return styles.plotly_layout(fig, 300)


def _heatmap():
    depts = list(COMPLETION)
    z = [COMPLETION[d] for d in depts]
    fig = go.Figure(go.Heatmap(
        z=z, x=COURSE_NAMES, y=depts, zmin=50, zmax=100,
        colorscale=[[0, "#FCF1DC"], [0.5, "#BFD3C8"], [1, styles.INDIGO]],
        text=[[f"{v}%" for v in row] for row in z], texttemplate="%{text}",
        textfont=dict(family=styles.FONT, size=13), xgap=4, ygap=4, showscale=False,
        hovertemplate="%{y}, %{x}: %{z}%<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(tickangle=0, side="top")
    return styles.plotly_layout(fig, 300)


def render():
    head, badge = st.columns([5, 1], vertical_alignment="center")
    with head:
        c.page_header("Team overview", "How a compliance manager would track completion across departments.")
    with badge:
        c.render(c.pill("Sample data", "warning", "info"))

    all_vals = [v for row in COMPLETION.values() for v in row]
    below = sum(1 for v in COMPLETION.values() if sum(v) / len(v) < TARGET)
    col1, col2, col3 = st.columns(3)
    with col1:
        c.stat_card("Average completion", f"{round(sum(all_vals) / len(all_vals))}%",
                    "Across six departments and four courses.", "groups", "indigo")
    with col2:
        c.stat_card("Departments below target", str(below), f"Target is {TARGET}% completion.", "warning", "amber")
    with col3:
        c.stat_card("Lowest course", "Data privacy", "Weakest completion in most departments.", "shield_lock", "teal")
    st.write("")

    left, right = st.columns(2, gap="medium")
    with left:
        with st.container(key="card-teambar"):
            c.section_title("Completion by department")
            st.plotly_chart(_bar_chart(), config=styles.PLOTLY_CONFIG, key="team_bar")
    with right:
        with st.container(key="card-teamheat"):
            c.section_title("Completion by course")
            st.plotly_chart(_heatmap(), config=styles.PLOTLY_CONFIG, key="team_heat")

    c.render('<div class="ciq-footnote">This page uses made-up numbers for illustration. In a real rollout '
             'it would read completion records from the company\'s learning system.</div>')
