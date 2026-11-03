"""Colours, CSS and Plotly styling shared by every tab."""
from __future__ import annotations
import streamlit as st

# One colour per algorithm, used identically in every chart / network view.
ALGO_ORDER = ["Greedy", "Betweenness", "SA", "Exhaustive"]
ALGO_COLORS = {
    "Greedy": "#38bdf8",       # sky
    "Betweenness": "#fb923c",  # orange
    "SA": "#c084fc",           # violet
    "Exhaustive": "#2dd4bf",   # teal
}
ALGO_LONG = {
    "Greedy": "Greedy",
    "Betweenness": "Betweenness (top-k)",
    "SA": "Simulated Annealing",
    "Exhaustive": "Exhaustive",
}

ROLE_COLORS = {
    "Source": "#a3e635",
    "Target": "#f43f5e",
    "Eligible": "#3b82f6",
    "Ineligible": "#64748b",
}
HONEYPOT = "#facc15"
PATH_HILITE = "#fb7185"
SYNTH_EDGE = "#f472b6"
EDGE_BASE = "#475569"
GOOD = "#34d399"
BAD = "#f87171"
MUTED = "#94a3b8"

CSS = """
<style>
:root { --accent:#22d3ee; --violet:#a78bfa; --pink:#f472b6; --amber:#fbbf24; --green:#34d399;
        --panel:#111a2e; --line:#1e293b; }
.stApp {
  background:
    radial-gradient(1100px 600px at 8% -10%, rgba(34,211,238,.13), transparent 60%),
    radial-gradient(900px 520px at 100% 0%, rgba(168,85,247,.16), transparent 55%),
    radial-gradient(900px 600px at 50% 115%, rgba(244,114,182,.11), transparent 60%),
    #0b1220;
}
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1500px; }
/* ---------- headings with neon glow ---------- */
h1 { font-weight: 800; letter-spacing: -0.01em;
  background: linear-gradient(90deg,#22d3ee 0%,#a78bfa 50%,#f472b6 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent !important;
  filter: drop-shadow(0 0 12px rgba(34,211,238,.55)) drop-shadow(0 0 28px rgba(168,85,247,.35)); }
h2 { color:#e0f2fe !important; text-shadow: 0 0 12px rgba(34,211,238,.6), 0 0 30px rgba(34,211,238,.25); }
h3 { color:#f5e9ff !important; text-shadow: 0 0 10px rgba(168,85,247,.6), 0 0 24px rgba(168,85,247,.25); }
/* ---------- metric cards: rotating neon colours ---------- */
div[data-testid="stMetric"] {
  --c: #22d3ee;
  background: linear-gradient(160deg, rgba(17,26,46,.95) 0%, rgba(12,19,36,.95) 100%);
  border: 1px solid color-mix(in srgb, var(--c) 45%, #1e293b); border-left: 4px solid var(--c);
  border-radius: 12px; padding: .8rem 1rem;
  box-shadow: 0 0 18px -5px var(--c), inset 0 0 26px -16px var(--c);
}
[data-testid="stHorizontalBlock"] > div:nth-child(5n+2) div[data-testid="stMetric"] { --c:#a78bfa; }
[data-testid="stHorizontalBlock"] > div:nth-child(5n+3) div[data-testid="stMetric"] { --c:#f472b6; }
[data-testid="stHorizontalBlock"] > div:nth-child(5n+4) div[data-testid="stMetric"] { --c:#fbbf24; }
[data-testid="stHorizontalBlock"] > div:nth-child(5n+5) div[data-testid="stMetric"] { --c:#34d399; }
div[data-testid="stMetricLabel"] p { color:#9fb3cc; font-size:.78rem; text-transform:uppercase; letter-spacing:.06em; }
div[data-testid="stMetricValue"] { font-size:1.55rem; font-weight:700; color:#fff;
  text-shadow: 0 0 14px var(--c); }
/* ---------- images, charts, tables glow ---------- */
div[data-testid="stImage"] img, div[data-testid="stImageContainer"] img {
  border-radius: 14px; border: 1px solid rgba(34,211,238,.45);
  box-shadow: 0 0 22px rgba(34,211,238,.38), 0 0 60px rgba(168,85,247,.28), 0 0 90px rgba(244,114,182,.12); }
div[data-testid="stPlotlyChart"], iframe {
  border-radius: 14px; border: 1px solid rgba(99,102,241,.35);
  box-shadow: 0 0 22px -6px rgba(34,211,238,.45), 0 0 50px -18px rgba(168,85,247,.5); }
div[data-testid="stDataFrame"] { border-radius: 10px; box-shadow: 0 0 18px -8px rgba(34,211,238,.5); }
/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] > div:first-child {
  background: linear-gradient(185deg, #10204a 0%, #1a1240 45%, #0d1426 100%); }
section[data-testid="stSidebar"] { border-right: 1px solid rgba(34,211,238,.35);
  box-shadow: 6px 0 30px -10px rgba(34,211,238,.35); }
.brand { font-weight:800; font-size:1.2rem; letter-spacing:.1em; color:#fff;
  text-shadow: 0 0 14px rgba(34,211,238,.8); }
.brand span { color: var(--accent); text-shadow: 0 0 16px var(--accent), 0 0 34px var(--accent); }
.brand-sub { color:#8fa6c8; font-size:.72rem; letter-spacing:.12em; text-transform:uppercase; margin-bottom:.8rem; }
.runcard { background: rgba(10,18,38,.75); border:1px solid rgba(167,139,250,.5); border-radius:12px;
  padding:.7rem .85rem; font-size:.82rem; line-height:1.55; box-shadow: 0 0 20px -6px #a78bfa; }
.runcard b { color:#fff; } .runcard .k { color:#9fb3cc; }
/* ---------- buttons ---------- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
  border: 1px solid rgba(34,211,238,.55); box-shadow: 0 0 14px -3px rgba(34,211,238,.6); transition: all .2s; }
.stButton > button:hover, .stDownloadButton > button:hover { box-shadow: 0 0 22px rgba(34,211,238,.9); transform: translateY(-1px); }
button[kind="primary"], button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"] {
  background: linear-gradient(90deg,#06b6d4,#8b5cf6 55%,#ec4899) !important; border: 0 !important; color:#fff !important;
  box-shadow: 0 0 22px rgba(139,92,246,.7), 0 0 44px rgba(236,72,153,.35) !important; }
/* ---------- tags, callouts, chips ---------- */
.tag { display:inline-block; padding:.12rem .55rem; border-radius:999px; font-size:.74rem; font-weight:600;
  border:1px solid; margin-right:.3rem; box-shadow: 0 0 10px -2px currentColor; }
.callout { background: linear-gradient(90deg, rgba(34,211,238,.12), rgba(15,28,51,.9)); border:1px solid rgba(34,211,238,.45);
  border-left:4px solid var(--accent); border-radius:10px; padding:.7rem .95rem; margin:.4rem 0 .8rem 0; font-size:.92rem;
  box-shadow: 0 0 20px -8px var(--accent); }
.callout.warn { border-left-color:#fbbf24; background: linear-gradient(90deg, rgba(251,191,36,.14), rgba(33,26,11,.92));
  border-color: rgba(251,191,36,.5); box-shadow: 0 0 20px -8px #fbbf24; }
.callout.good { border-left-color:#34d399; background: linear-gradient(90deg, rgba(52,211,153,.14), rgba(11,33,25,.92));
  border-color: rgba(52,211,153,.5); box-shadow: 0 0 20px -8px #34d399; }
.sub { color:#9fb3cc; margin-top:-.6rem; margin-bottom:1rem; }
.nodechip { display:inline-block; background:rgba(15,23,42,.9); border:1px solid #38bdf8; color:#e0f2fe;
  border-radius:6px; padding:.05rem .5rem; margin:.1rem .2rem .1rem 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size:.82rem; box-shadow: 0 0 10px -2px #38bdf8; }
.stTabs [data-baseweb="tab"] { height: 2.4rem; }
.stTabs [aria-selected="true"] { text-shadow: 0 0 10px var(--accent); }
div[data-testid="stExpander"] { border:1px solid rgba(167,139,250,.35); border-radius:12px;
  box-shadow: 0 0 16px -8px #a78bfa; }
/* ---------- sidebar nav: whole-row block buttons instead of radio dots ---------- */
section[data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stRadio"]),
section[data-testid="stSidebar"] [data-testid="stRadio"] { width: 100% !important; }
section[data-testid="stSidebar"] [role="radiogroup"] { gap: .1rem; width: 100%; }
section[data-testid="stSidebar"] [role="radiogroup"] > div { width: 100%; }
section[data-testid="stSidebar"] label[data-testid="stRadioOption"],
section[data-testid="stSidebar"] [role="radiogroup"] > label {
  display: flex !important; width: 100% !important; box-sizing: border-box; padding: .38rem .8rem; margin: 0; border-radius: 8px; cursor: pointer;
  border: 1px solid transparent; background: transparent; transition: background .15s, border-color .15s; }
/* hide the round radio indicator (new + older Streamlit markup) */
section[data-testid="stSidebar"] label[data-testid="stRadioOption"] > div > div:first-child,
section[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child { display: none !important; }
section[data-testid="stSidebar"] label[data-testid="stRadioOption"] p { color:#a9bbd6; font-size:.92rem; }
section[data-testid="stSidebar"] label[data-testid="stRadioOption"]:hover,
section[data-testid="stSidebar"] [role="radiogroup"] > label:hover { background: rgba(148,163,184,.10); }
section[data-testid="stSidebar"] label[data-testid="stRadioOption"]:has(input:checked),
section[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {
  background: rgba(34,211,238,.10); border-color: rgba(34,211,238,.28); }
section[data-testid="stSidebar"] label[data-testid="stRadioOption"]:has(input:checked) p { color:#e0f2fe; font-weight:600; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def header(title: str, subtitle: str | None = None):
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f'<div class="sub">{subtitle}</div>', unsafe_allow_html=True)


def callout(text: str, kind: str = "info"):
    cls = {"info": "", "warn": " warn", "good": " good"}[kind]
    st.markdown(f'<div class="callout{cls}">{text}</div>', unsafe_allow_html=True)


def tag(text: str, color: str) -> str:
    return (f'<span class="tag" style="color:{color};border-color:{color};'
            f'background:{color}1a">{text}</span>')


def chips(nodes) -> str:
    items = sorted(nodes, key=str)
    if not items:
        return '<span class="sub">(none)</span>'
    return "".join(f'<span class="nodechip">{n}</span>' for n in items)


def style(fig, height: int | None = None, legend: bool = True, title: str | None = None):
    """Apply the dark cyber look to any Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, -apple-system, Segoe UI, sans-serif",
                  color="#cbd5e1", size=12),
        margin=dict(l=10, r=10, t=48 if title else 30, b=56 if legend else 10),
        showlegend=legend,
        legend=dict(bgcolor="rgba(15,23,42,0.7)", bordercolor="#1e293b", borderwidth=1,
                    orientation="h", yanchor="top", y=-0.14, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="#0f172a", bordercolor="#334155", font_size=12),
    )
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=14, color="#e2e8f0"),
                                     x=0, xanchor="left"))
    if height:
        fig.update_layout(height=height)
    fig.update_xaxes(gridcolor="#1e293b", zerolinecolor="#1e293b", linecolor="#334155")
    fig.update_yaxes(gridcolor="#1e293b", zerolinecolor="#1e293b", linecolor="#334155")
    return fig