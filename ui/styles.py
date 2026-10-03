"""Design tokens and global CSS: the 'Meadow' theme.

Everything visual hangs off the tokens in :root, so a new look is mostly a new token block:
colours, two typefaces, and a shape language (flat bordered cards, small radii, pill buttons)."""
import streamlit as st

# Python-side constants, used by the Plotly charts
INK = "#17261F"
INDIGO = "#1F4D3F"        # primary (forest). Name kept so the chart code needs no changes.
TEAL = "#2E7D4F"          # "passed" green on charts
TEAL_BRIGHT = "#E9A23B"   # marigold: the gauge fill
BG = "#F4F6F1"
TRACK = "#E3E9E2"
MUTED = "#5E6F66"
SUCCESS = "#2E7D4F"
WARNING = "#C9861C"
DANGER = "#B3382C"
FONT = "DM Sans, system-ui, -apple-system, Segoe UI, sans-serif"

PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400..600,0..1,0&display=block');

/* ============ 1. TOKENS ============ */
:root {
  --bg: #F4F6F1; --surface: #FFFFFF; --text: #17261F; --muted: #5E6F66; --line: #DCE3DB; --track: #E3E9E2;
  --forest: #1F4D3F; --forest-dark: #153A2F; --forest-soft: #E3EDE6; --cream: #F4F6F1;
  --marigold: #E9A23B; --marigold-deep: #B8741A; --marigold-soft: #FCF1DC;
  --sky: #2F6F8F; --sky-soft: #E4EFF5;
  --plum: #7A4E6D; --plum-soft: #F3E9F0;
  --success: #2E7D4F; --success-soft: #E4F3EA;
  --warning: #B7791F; --warning-soft: #FCF1DC;
  --danger: #B3382C; --danger-soft: #FBE9E6;
  --r-lg: 8px; --r-md: 6px; --r-pill: 999px;
  --ease: 160ms ease;
  --body: 'DM Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --display: 'Fraunces', Georgia, 'Times New Roman', serif;
}

/* ============ 2. BASE TYPE ============ */
.stApp { background: var(--bg); color: var(--text); font-family: var(--body); }
.stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp button { font-family: var(--body); }
.stApp h1, .stApp h2, .stApp h3 { font-family: var(--display); color: var(--text); font-weight: 600; letter-spacing: -0.01em; }
[data-testid="stHeaderActionElements"] { display: none; }

/* ============ 3. CHROME: top bar instead of sidebar ============ */
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton { display: none !important; }
header[data-testid="stHeader"] { background: var(--surface); border-bottom: 1px solid var(--line); height: 3.75rem; }
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none !important; }
.block-container, [data-testid="stMainBlockContainer"] { max-width: 1100px; padding-top: 5.5rem; padding-bottom: 4rem; }
[data-testid="stBottom"] > div { background: var(--bg); }
[data-testid="stHeader"] a, [data-testid="stHeader"] button { font-family: var(--body); font-weight: 500; }

/* top navigation links: quiet pills, the active page is filled */
[data-testid="stTopNavLink"] { border-radius: var(--r-pill); padding: 6px 14px; color: var(--muted); transition: background var(--ease), color var(--ease); }
[data-testid="stTopNavLink"] * { color: inherit !important; }
[data-testid="stTopNavLink"]:hover { background: var(--forest-soft); color: var(--forest); }
[data-testid="stTopNavLink"][aria-current="page"] { background: var(--forest); color: #FFFFFF; }
[data-testid="stTopNavLink"][aria-current="page"]:hover { background: var(--forest-dark); color: #FFFFFF; }

/* ============ 4. ICON CHIPS ============ */
.ms { font-family: 'Material Symbols Rounded'; font-weight: 500; font-style: normal; font-size: 20px;
  line-height: 1; display: inline-block; letter-spacing: normal; text-transform: none; white-space: nowrap;
  direction: ltr; font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased; vertical-align: middle; }
.ic-indigo { background: var(--forest-soft); color: var(--forest); }
.ic-teal { background: var(--sky-soft); color: var(--sky); }
.ic-violet { background: var(--plum-soft); color: var(--plum); }
.ic-amber { background: var(--marigold-soft); color: var(--marigold-deep); }
.ic-neutral { background: #EDF0EC; color: var(--muted); }

/* ============ 5. PAGE HEADER & TEXT ============ */
.ciq-page-head { margin: 0 0 28px; padding-bottom: 18px; border-bottom: 1px solid var(--line); }
.ciq-page-head h1 { font-size: 2.3rem; margin: 0 0 8px; padding: 0; line-height: 1.15; }
.ciq-page-head p { color: var(--muted); margin: 0; font-size: 1.02rem; line-height: 1.6; max-width: 66ch; }
.ciq-section { font-family: var(--display); font-weight: 600; font-size: 1.2rem; margin: 0 0 12px; color: var(--text); }
.ciq-muted { color: var(--muted); }
.ciq-small { font-size: .85rem; }
.ciq-footnote { color: var(--muted); font-size: .8rem; margin-top: 16px; }
.ciq-footer { margin-top: 56px; padding-top: 18px; border-top: 1px solid var(--line); color: var(--muted);
  font-size: .8rem; line-height: 1.6; max-width: 90ch; }

/* ============ 6. CARDS: flat, bordered, no shadow ============ */
div[class*="st-key-card"] { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-lg); padding: 22px 24px; }
div[class*="st-key-card-course"] { border-top: 4px solid var(--forest); transition: border-color var(--ease), transform var(--ease); }
div[class*="st-key-card-course"]:hover { border-color: var(--marigold); transform: translateY(-2px); }
div[class*="st-key-card-course"] .stButton > button { width: 100%; }

/* ============ 7. HERO: the one bold moment ============ */
.st-key-hero { background: var(--forest-dark); border-radius: var(--r-lg); padding: 38px 42px 28px; }
.stApp .st-key-hero h1 { color: var(--cream); font-size: 2.7rem; line-height: 1.1; margin: 0 0 12px; padding: 0; }
.stApp .st-key-hero p { color: #BFD3C8; font-size: 1.05rem; line-height: 1.6; max-width: 46ch; margin: 0 0 20px; }
.ciq-hero-meta { color: #9DB8AA; font-size: .82rem; text-align: center; margin-top: -8px; }
.st-key-hero .stButton > button[kind="primary"], .st-key-hero [data-testid="stBaseButton-primary"] {
  background: var(--marigold); border-color: var(--marigold); color: #1B1405; }
.st-key-hero .stButton > button[kind="primary"]:hover { background: #F2B357; border-color: #F2B357; color: #1B1405; }
.st-key-hero .stButton > button[kind="secondary"], .st-key-hero [data-testid="stBaseButton-secondary"] {
  background: transparent; color: var(--cream); border-color: rgba(244,246,241,.45); }
.st-key-hero .stButton > button[kind="secondary"]:hover { background: rgba(244,246,241,.1); color: #FFFFFF; border-color: var(--cream); }

.st-key-hero [data-testid="stBaseButton-primary"] p, .st-key-hero [data-testid="stBaseButton-primary"] span { color: #1B1405 !important; }
.st-key-hero [data-testid="stBaseButton-secondary"] p, .st-key-hero [data-testid="stBaseButton-secondary"] span { color: var(--cream) !important; }
[data-testid="stBaseButton-primary"] p, [data-testid="stBaseButton-primary"] span { color: inherit; }

/* ============ 8. STAT CARDS ============ */
.ciq-stat { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-lg); padding: 20px 22px; height: 100%; }
.ciq-stat .ic { width: 38px; height: 38px; border-radius: 50%; display: grid; place-items: center; margin-bottom: 14px; }
.ciq-stat .label { color: var(--muted); font-size: .88rem; font-weight: 500; }
.ciq-stat .value { font-family: var(--display); font-size: 2.1rem; font-weight: 600; margin: 2px 0 4px; color: var(--text); }
.ciq-stat .hint { color: var(--muted); font-size: .84rem; line-height: 1.45; }

/* ============ 9. PILLS & PROGRESS ============ */
.pill { display: inline-flex; align-items: center; gap: 4px; padding: 3px 11px; border-radius: var(--r-pill);
  font-size: .78rem; font-weight: 600; white-space: nowrap; }
.pill-success { background: var(--success-soft); color: #1F6B3E; }
.pill-warning { background: var(--warning-soft); color: #8A5A10; }
.pill-danger { background: var(--danger-soft); color: #9A2C21; }
.pill-indigo { background: var(--forest-soft); color: var(--forest); }
.pill-neutral { background: #EDF0EC; color: var(--muted); }
.ciq-bar { height: 8px; background: var(--track); border-radius: var(--r-pill); overflow: hidden; }
.ciq-bar > span { display: block; height: 100%; border-radius: var(--r-pill);
  background: linear-gradient(90deg, var(--forest), var(--marigold)); transition: width 400ms ease; }

/* ============ 10. LISTS ============ */
.ciq-row { padding: 12px 0; border-bottom: 1px solid var(--line); }
.ciq-row:last-child { border-bottom: none; }
.ciq-row-top { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 8px; }
.ciq-row .name { display: flex; gap: 10px; align-items: center; font-weight: 600; }
.ciq-row .name .ms { width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; font-size: 18px; }
.ciq-feed-item { display: flex; gap: 12px; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid var(--line); }
.ciq-feed-item:last-child { border-bottom: none; }
.ciq-feed-item .ic { width: 32px; height: 32px; border-radius: 50%; display: grid; place-items: center; flex: none; }
.ciq-feed-item .txt { font-size: .92rem; line-height: 1.4; }
.ciq-feed-item .when { color: var(--muted); font-size: .78rem; margin-top: 2px; }
.ciq-timeline { position: relative; padding-left: 24px; }
.ciq-timeline::before { content: ""; position: absolute; left: 6px; top: 6px; bottom: 10px; width: 2px; background: var(--line); }
.ciq-tl-item { position: relative; padding: 0 0 18px; }
.ciq-tl-item::before { content: ""; position: absolute; left: -23px; top: 5px; width: 12px; height: 12px;
  border-radius: 50%; background: var(--forest); box-shadow: 0 0 0 3px var(--forest-soft); }
.ciq-tl-item.gold::before { background: var(--marigold); box-shadow: 0 0 0 3px var(--marigold-soft); }
.ciq-tl-item .t { font-weight: 600; }
.ciq-tl-item .d { color: var(--muted); font-size: .84rem; }
.ciq-empty { text-align: center; padding: 26px 12px; color: var(--muted); }
.ciq-empty .ms { font-size: 36px; color: #A9BDB1; margin-bottom: 8px; }
.ciq-empty .t { font-weight: 600; color: var(--text); margin-bottom: 4px; }

/* ============ 11. COURSE CARDS ============ */
.ciq-course-ic { width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; margin-bottom: 14px; }
.ciq-course h3 { margin: 0 0 6px; padding: 0; font-size: 1.3rem; }
.ciq-course p { color: var(--muted); font-size: .92rem; line-height: 1.5; margin: 0 0 16px; min-height: 2.9em; }
.ciq-course .meta { display: flex; justify-content: space-between; align-items: center; font-size: .84rem; color: var(--muted); margin-bottom: 10px; gap: 8px; }
.ciq-course .due { color: var(--muted); font-size: .8rem; margin: 8px 0 12px; }
.ciq-soon { background: transparent; border: 1px dashed #BCC9BF; border-radius: var(--r-lg); padding: 20px 24px;
  display: flex; gap: 14px; align-items: center; color: var(--muted); }
.ciq-soon .t { font-weight: 600; color: var(--text); }

/* ============ 12. LESSON VIEWER ============ */
.ciq-stepper { display: flex; gap: 6px; margin: 0 0 24px; }
.ciq-step { flex: 1; display: flex; align-items: center; gap: 10px; padding: 10px 4px; border-bottom: 3px solid var(--line);
  font-size: .88rem; color: var(--muted); min-width: 0; }
.ciq-step .label { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ciq-step .num { width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center; font-weight: 700;
  font-size: .8rem; background: var(--track); color: var(--muted); flex: none; }
.ciq-step.done { border-bottom-color: var(--success); }
.ciq-step.done .num { background: var(--success); color: #fff; }
.ciq-step.current { border-bottom-color: var(--marigold); color: var(--text); font-weight: 600; }
.ciq-step.current .num { background: var(--forest); color: #fff; }
.ciq-lesson-kicker { color: var(--marigold-deep); font-weight: 600; font-size: .9rem; margin-bottom: 4px; }
.stApp .ciq-lesson-title { font-size: 1.8rem; margin: 0 0 14px; padding: 0; }
.ciq-quote { border-left: 3px solid var(--marigold); background: #FAFBF8; padding: 12px 16px; border-radius: 0 var(--r-md) var(--r-md) 0;
  color: #34463D; font-size: .92rem; line-height: 1.65; margin-bottom: 12px; }
.ciq-quote .src { font-size: .78rem; color: var(--muted); margin-top: 6px; font-weight: 600; }

/* ============ 13. ASSESSMENT ============ */
.ciq-qhead { display: flex; justify-content: space-between; color: var(--muted); font-size: .88rem; margin-bottom: 8px; }
.ciq-scenario { color: #34463D; font-size: 1.02rem; line-height: 1.6; margin: 0 0 8px; }
.stApp .ciq-question { font-size: 1.35rem; margin: 0 0 16px; padding: 0; }
div[role="radiogroup"] { gap: 10px; width: 100%; }
[data-testid="stElementContainer"]:has([data-testid="stRadio"]), [data-testid="stRadio"],
[data-testid="stRadio"] > div, [data-testid="stRadioGroup"], [data-testid="stRadioGroup"] > div { width: 100% !important; }
div[role="radiogroup"] > label, [data-testid="stRadioOption"] { background: var(--surface); border: 1.5px solid var(--line);
  border-radius: var(--r-lg); padding: 12px 16px; width: 100%; box-sizing: border-box; margin: 0;
  transition: border-color var(--ease), background var(--ease); }
div[role="radiogroup"] > label:hover, [data-testid="stRadioOption"]:hover { border-color: #9DB8AA; }
div[role="radiogroup"] > label:has(input:checked), [data-testid="stRadioOption"]:has(input:checked) {
  border-color: var(--forest); background: var(--forest-soft); }
.ciq-feedback { border-radius: var(--r-lg); padding: 16px 18px; margin: 14px 0 12px; border: 1px solid;
  animation: ciq-rise 220ms ease-out; line-height: 1.55; }
.ciq-feedback.ok { background: var(--success-soft); border-color: #B5DCC3; }
.ciq-feedback.bad { background: var(--danger-soft); border-color: #EFC0BA; }
.ciq-feedback .title { font-weight: 700; display: flex; gap: 8px; align-items: center; margin-bottom: 4px; }
.ciq-feedback.ok .title { color: #1F6B3E; }
.ciq-feedback.bad .title { color: #9A2C21; }
.ciq-feedback .src { color: var(--muted); font-size: .8rem; margin-top: 6px; }
.ciq-result { display: flex; gap: 24px; align-items: center; border-radius: var(--r-lg); padding: 26px 30px; margin-bottom: 18px;
  animation: ciq-rise 260ms ease-out; }
.ciq-result.pass { background: var(--success-soft); border: 1px solid #B5DCC3; }
.ciq-result.fail { background: var(--warning-soft); border: 1px solid #F0D4A2; }
.ciq-result .big { font-family: var(--display); font-size: 3.2rem; font-weight: 700; line-height: 1; }
.ciq-result.pass .big { color: #1F6B3E; }
.ciq-result.fail .big { color: #8A5A10; }
.ciq-result .t { font-family: var(--display); font-weight: 600; font-size: 1.3rem; margin-bottom: 4px; }
.ciq-result .d { color: #34463D; line-height: 1.55; }
@keyframes ciq-rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

/* ============ 14. CERTIFICATES ============ */
.ciq-cert { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 12px; }
.ciq-cert .ic { width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center; flex: none; }
.ciq-cert .t { font-weight: 700; }
.ciq-cert .d { color: var(--muted); font-size: .85rem; line-height: 1.5; }

/* ============ 15. BUTTONS: pills, outlined by default ============ */
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  border-radius: var(--r-pill); border: 1.5px solid var(--forest); background: transparent; color: var(--forest);
  font-weight: 600; padding: .4rem 1.2rem; box-shadow: none;
  transition: background var(--ease), color var(--ease), border-color var(--ease), transform var(--ease); }
.stButton > button p, .stDownloadButton > button p { color: inherit; font-weight: 600; }
.stButton > button:hover, .stDownloadButton > button:hover { background: var(--forest-soft); border-color: var(--forest); color: var(--forest-dark); }
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"], [data-testid="stBaseButton-primary"] {
  background: var(--forest); border-color: var(--forest); color: #FFFFFF; }
.stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {
  background: var(--forest-dark); border-color: var(--forest-dark); color: #FFFFFF; }
.stButton > button:disabled { opacity: .45; }
.stApp button:focus-visible { outline: 3px solid rgba(233,162,59,.55); outline-offset: 2px; }
[data-baseweb="input"], [data-baseweb="base-input"] { border-radius: var(--r-md); }
[data-testid="stExpander"] details { border-radius: var(--r-lg); border-color: var(--line); background: var(--surface); }

/* ============ 16. CHAT: editorial bubbles ============ */
[data-testid="stChatMessage"] { background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--forest);
  border-radius: 4px 16px 16px 16px; padding: 16px 20px; margin-bottom: 14px; width: 88%; box-sizing: border-box; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  background: var(--forest); border: none; border-radius: 16px 4px 16px 16px; width: 76%; margin-left: auto; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li { color: var(--cream); }
[data-testid="stChatMessageAvatarUser"] { background: var(--marigold) !important; color: #1B1405 !important; }
[data-testid="stChatInput"] { border-radius: var(--r-pill); }
[data-testid="stChatInput"] > div { border-radius: var(--r-pill); border-color: var(--line); }

@media (max-width: 720px) {
  .ciq-step .label { display: none; }
  .st-key-hero { padding: 24px 22px; }
  .stApp .st-key-hero h1 { font-size: 2rem; }
  [data-testid="stChatMessage"], [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { width: 100%; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
"""


def inject():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def plotly_layout(fig, height: int):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=16, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=INK, size=13),
        showlegend=False,
    )
    return fig
