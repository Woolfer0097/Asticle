import streamlit as st


PAGE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,600;7..72,700&family=Nunito+Sans:wght@400;600;700;800&display=swap');

    :root {
        --paper: #f7f2e8;
        --ink: #1d1c18;
        --muted: #746f64;
        --line: #d8cbb8;
        --accent: #a43f2d;
        --accent-dark: #7d2c20;
        --sage: #3d6357;
        --field: #fffaf0;
    }

    .stApp {
        background:
            linear-gradient(90deg, rgba(29,28,24,.035) 1px, transparent 1px),
            linear-gradient(rgba(29,28,24,.035) 1px, transparent 1px),
            radial-gradient(circle at top left, rgba(164,63,45,.18), transparent 28rem),
            var(--paper);
        background-size: 28px 28px, 28px 28px, auto, auto;
        color: var(--ink);
    }

    .main .block-container {
        max-width: 1240px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--ink);
        font-family: "Literata", Georgia, serif;
        letter-spacing: 0;
    }

    p, label, span, div, button, input, textarea {
        font-family: "Nunito Sans", sans-serif;
    }

    .brand {
        border-bottom: 1px solid var(--line);
        margin-bottom: 1.4rem;
        padding: .35rem 0 1.15rem 0;
    }

    .brand h1 {
        font-size: clamp(2.4rem, 6vw, 5.5rem);
        line-height: .92;
        margin: 0;
    }

    .brand p {
        color: var(--muted);
        font-size: 1.05rem;
        max-width: 820px;
        margin: .85rem 0 0 0;
    }

    .article-cover {
        align-items: center;
        background:
            linear-gradient(135deg, rgba(61,99,87,.18), transparent),
            repeating-linear-gradient(-45deg, rgba(29,28,24,.08) 0 1px, transparent 1px 9px);
        border: 1px dashed rgba(29,28,24,.26);
        border-radius: 6px;
        color: var(--muted);
        display: flex;
        font-weight: 800;
        justify-content: center;
        min-height: 190px;
        text-transform: uppercase;
    }

    .metric-strip {
        display: grid;
        gap: .75rem;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        margin: 1rem 0 1.4rem;
    }

    .metric-strip div {
        background: rgba(255,250,240,.82);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: .8rem .9rem;
    }

    .metric-strip strong {
        color: var(--accent);
        display: block;
        font-size: 1.35rem;
        line-height: 1;
    }

    .metric-strip span {
        color: var(--muted);
        font-size: .83rem;
        text-transform: uppercase;
    }

    .note {
        background: rgba(61,99,87,.1);
        border-left: 4px solid var(--sage);
        border-radius: 0 8px 8px 0;
        color: var(--ink);
        padding: .85rem 1rem;
    }

    .small-muted {
        color: var(--muted);
        font-size: .9rem;
    }

    .stButton > button,
    .stDownloadButton > button,
    div[data-testid="stFormSubmitButton"] button {
        border-radius: 6px;
        font-weight: 800;
    }

    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button[kind="primary"] {
        background: var(--accent);
        border-color: var(--accent);
    }

    .stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover {
        background: var(--accent-dark);
        border-color: var(--accent-dark);
    }

    textarea, input {
        background: var(--field) !important;
    }

    @media (max-width: 760px) {
        .metric-strip {
            grid-template-columns: 1fr;
        }
    }
</style>
"""


def configure_page() -> None:
    st.set_page_config(
        page_title="Asticle",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)
