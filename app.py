import streamlit as st

from ui.student_assistant import render_student_assistant
from ui.telemetry import render_telemetry


st.set_page_config(
    page_title="Shakthi AI | Sovereign Edge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# GLOBAL UI STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .shakthi-brand {
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 0.15rem;
    }

    .shakthi-subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }

    .shakthi-hero {
        padding: 1.35rem 1.5rem;
        border: 1px solid rgba(100, 116, 139, 0.18);
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            rgba(14, 165, 233, 0.08),
            rgba(99, 102, 241, 0.05)
        );
        margin-bottom: 1.4rem;
    }

    .hero-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }

    .hero-text {
        color: #64748b;
        line-height: 1.55;
        margin-bottom: 0.8rem;
    }

    .hero-pill {
        display: inline-block;
        padding: 0.3rem 0.65rem;
        margin-right: 0.35rem;
        margin-bottom: 0.25rem;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.06);
        font-size: 0.82rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(100, 116, 139, 0.12);
    }

    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 750;
        margin-bottom: 0.4rem;
    }

    .status-card {
        padding: 0.9rem;
        border-radius: 12px;
        border: 1px solid rgba(34, 197, 94, 0.22);
        background: rgba(34, 197, 94, 0.06);
        margin-bottom: 1rem;
    }

    .status-card strong {
        display: block;
        margin-bottom: 0.2rem;
    }

    .footer-note {
        color: #64748b;
        font-size: 0.82rem;
        text-align: center;
        padding-top: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="shakthi-brand">⚡ SHAKTHI AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="shakthi-subtitle">'
    "Sovereign Edge Intelligence Platform • Powered by Namma Web"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="shakthi-hero">
        <div class="hero-title">
            Kannada-first intelligence that stays on the edge.
        </div>
        <div class="hero-text">
            Ask questions using Kannada text or voice. Shakthi AI uses
            verified local knowledge and local AI models without requiring
            a cloud service during normal operation.
        </div>
        <span class="hero-pill">🔒 Local / Air-gapped</span>
        <span class="hero-pill">🧠 Gemma 3 4B</span>
        <span class="hero-pill">📚 Verified knowledge</span>
        <span class="hero-pill">🎙️ Kannada voice</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🖥️ Edge Appliance</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="status-card">
            <strong>🟢 Local system ready</strong>
            Designed for air-gapped operation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Compute**")
    st.caption("Quad-Core CPU • Target 8GB RAM")

    st.markdown("**Inference**")
    st.caption("Gemma 3 4B via local Ollama")

    st.markdown("**Embeddings**")
    st.caption("Multilingual MiniLM • 384D")

    st.markdown("**Retrieval**")
    st.caption("SQLite • Top-k = 2")

    st.markdown("**Knowledge**")
    st.caption("Verified local manuals")

    st.divider()

    st.markdown("**Privacy**")
    st.caption("Queries and operational telemetry remain local.")

    st.divider()

    st.caption("SHAKTHI AI • Engineering Directive 2026")


# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

tab1, tab2 = st.tabs(
    [
        "🗣️ Vernacular Student Assistant",
        "📊 ICDS Frontline Telemetry",
    ]
)


# ---------------------------------------------------------
# TAB 1
# ---------------------------------------------------------

with tab1:
    render_student_assistant()


# ---------------------------------------------------------
# TAB 2
# ---------------------------------------------------------

with tab2:
    render_telemetry()


# ---------------------------------------------------------

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.markdown(
    '<div class="footer-note">'
    "🔒 Shakthi AI is designed for local, air-gapped operation "
    "with verified knowledge and bounded responses."
    "</div>",
    unsafe_allow_html=True,
)