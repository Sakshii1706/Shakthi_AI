import json
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------
# DEMO TELEMETRY DATA
# ---------------------------------------------------------

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "demo_telemetry.json"
)


def load_telemetry():
    """
    Load local demo telemetry.

    This is placeholder/demo data only.
    Real telemetry will be connected during backend integration.
    """

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------
# TELEMETRY UI
# ---------------------------------------------------------

def render_telemetry():

    st.subheader("📊 ICDS Frontline Telemetry")

    st.caption(
        "Anonymized local telemetry and compliance pulse."
    )

    # Load local telemetry JSON
    data = load_telemetry()

    # -----------------------------------------------------
    # DATA STATUS
    # -----------------------------------------------------

    if data is None:

        st.warning(
            "⚠️ Local telemetry data is currently unavailable."
        )

        adherence = "Awaiting Data"
        top_query = "Awaiting Data"
        dropout_risk = "Awaiting Data"
        sync_status = "Unknown"

    else:

        adherence = f"{data.get('pilot_school_adherence', 0)}%"
        top_query = data.get(
            "top_student_query",
            "Awaiting Data"
        )
        dropout_risk = data.get(
            "dropout_risk_index",
            "Awaiting Data"
        )
        sync_status = data.get(
            "sync_status",
            "Local Only"
        )

        # Clearly identify placeholder telemetry
        if data.get("demo_data", False):
            st.info(
                "🧪 DEMO DATA — These telemetry values are "
                "placeholders for interface testing."
            )

    # -----------------------------------------------------
    # PRIMARY METRICS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Pilot School Adherence",
            adherence,
        )

    with col2:
        st.metric(
            "Top Student Query",
            top_query,
        )

    with col3:
        st.metric(
            "Dropout Risk Index",
            dropout_risk,
        )

    st.markdown("---")

    # -----------------------------------------------------
    # OFFLINE TELEMETRY STATUS
    # -----------------------------------------------------

    st.success(
        "🟢 Store-and-forward telemetry is available for "
        "local offline operation."
    )

    st.info(
        "Telemetry will use anonymized local data. "
        "No live cloud synchronization is required "
        "for normal operation."
    )

    # -----------------------------------------------------
    # SYSTEM STATUS
    # -----------------------------------------------------

    st.markdown("### System Status")

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        st.write("🔒 **Air-gapped:** Ready")

    with status_col2:
        st.write("💾 **Local Storage:** Ready")

    with status_col3:
        st.write(f"📡 **Sync:** {sync_status}")