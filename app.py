import streamlit as st

from ui.student_assistant import render_student_assistant
from ui.telemetry import render_telemetry
from ui.knowledge_manager import render_knowledge_manager


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Shakthi AI • Sovereign Edge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1.05rem;
        color: #64748b;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }

    .status-box {
        padding: 0.8rem 1rem;
        border-radius: 0.6rem;
        background: rgba(14, 165, 233, 0.08);
        border: 1px solid rgba(14, 165, 233, 0.25);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">⚡ SHAKTHI AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Sovereign Edge Intelligence Platform • Powered by Namma Web"
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## 💻 Edge Appliance Status")

    st.success("🟢 100% AIR-GAPPED OFFLINE")

    st.markdown("**Compute Engine:** Quad-Core CPU")

    st.markdown("**Target RAM:** 8GB")

    st.markdown("**Vector Store:** Local Persistent")

    st.markdown("**Inference:** Gemma 3 4B")


    st.markdown("**Embeddings:** Multilingual MiniLM 384D")

    st.markdown("**Retrieval:** Top-k = 2")

    st.markdown("**Knowledge:** Verified Local Manuals")

    st.divider()

    st.caption("SHAKTHI AI • Engineering Directive 2026")


# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "🗣 Vernacular Student Assistant",
        "📊 ICDS Frontline Telemetry",
        "📚 Document Knowledge Manager",
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
# TAB 3
# ---------------------------------------------------------

with tab3:
    render_knowledge_manager()


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "🔒 Shakthi AI is designed for local, air-gapped operation "
    "with verified knowledge and bounded responses."
)