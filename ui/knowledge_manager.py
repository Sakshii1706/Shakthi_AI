import streamlit as st


def render_knowledge_manager():
    st.subheader("📚 Document Knowledge Manager")
    st.caption(
        "Add verified DSERT or clinical knowledge for local indexing."
    )

    uploaded_file = st.file_uploader(
        "Upload verified knowledge PDF",
        type=["pdf"],
        help="PDF files will eventually be processed and indexed locally.",
    )

    if uploaded_file:
        st.success(
            f"📄 {uploaded_file.name} received and ready for "
            "local ingestion."
        )

    st.markdown("---")

    st.markdown("### Knowledge Base Status")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Master Dataset",
            "Pending",
        )

    with col2:
        st.metric(
            "Validated Kannada QA",
            "Pending",
        )

    st.info(
        "Local PDF ingestion, chunking, embedding and indexing "
        "will be connected to the backend ingestion pipeline."
    )