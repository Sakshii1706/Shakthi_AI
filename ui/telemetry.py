from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from core.telemetry import get_summary


# ---------------------------------------------------------
# TELEMETRY HELPERS
# ---------------------------------------------------------

def _format_response_time(milliseconds):
    if milliseconds is None:
        return "—"

    milliseconds = float(milliseconds)

    if milliseconds < 1000:
        return f"{milliseconds:.0f} ms"

    return f"{milliseconds / 1000:.1f} s"


def _format_confidence(confidence):
    if confidence is None:
        return "—"

    return f"{float(confidence) * 100:.1f}%"


def _format_last_activity(timestamp):
    if not timestamp:
        return "No activity yet"

    try:
        parsed = datetime.fromisoformat(timestamp)

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone().strftime("%d %b %Y, %I:%M %p")

    except ValueError:
        return str(timestamp)


# ---------------------------------------------------------
# TELEMETRY UI
# ---------------------------------------------------------

def render_telemetry():

    st.subheader("📊 ICDS Frontline Telemetry")

    st.caption(
        "Anonymized local operational telemetry from the Shakthi AI edge appliance."
    )

    # -----------------------------------------------------
    # LOAD REAL LOCAL TELEMETRY
    # -----------------------------------------------------

    try:
        data = get_summary()

    except Exception as exc:
        st.error(
            "Local telemetry is currently unavailable."
        )
        st.caption(f"Telemetry error: {exc}")
        return

    total = data.get("total", 0)
    answered = data.get("answered", 0)
    refused = data.get("refused", 0)
    voice = data.get("voice", 0)
    text = data.get("text", 0)

    avg_response_time = data.get("avg_response_time_ms")
    avg_confidence = data.get("avg_confidence")
    last_event = data.get("last_event_utc")

    # -----------------------------------------------------
    # DATA STATUS
    # -----------------------------------------------------

    if total == 0:
        st.info(
            "No telemetry events have been recorded yet. "
            "Use the Vernacular Student Assistant to generate local activity."
        )
    else:
        st.success(
            f"Local telemetry active — {total} interaction"
            f"{'' if total == 1 else 's'} recorded."
        )

    # -----------------------------------------------------
    # PRIMARY METRICS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Interactions",
            total,
        )

    with col2:
        st.metric(
            "Answered",
            answered,
        )

    with col3:
        st.metric(
            "Refused",
            refused,
        )

    # -----------------------------------------------------
    # INPUT / PERFORMANCE METRICS
    # -----------------------------------------------------

    st.markdown("### Interaction Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Voice",
            voice,
        )

    with col2:
        st.metric(
            "Text",
            text,
        )

    with col3:
        st.metric(
            "Avg. Response Time",
            _format_response_time(avg_response_time),
        )

    # -----------------------------------------------------
    # RAG METRICS
    # -----------------------------------------------------

    st.markdown("### RAG Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Avg. Confidence",
            _format_confidence(avg_confidence),
        )

    with col2:
        st.metric(
            "Answered Rate",
            (
                f"{(answered / total) * 100:.1f}%"
                if total
                else "—"
            ),
        )

    with col3:
        st.metric(
            "Refusal Rate",
            (
                f"{(refused / total) * 100:.1f}%"
                if total
                else "—"
            ),
        )

    # -----------------------------------------------------
    # LAST ACTIVITY
    # -----------------------------------------------------

    st.markdown("### Activity")

    st.info(
        f"Last local interaction: **{_format_last_activity(last_event)}**"
    )

    # -----------------------------------------------------
    # OFFLINE / STORE-AND-FORWARD STATUS
    # -----------------------------------------------------

    st.markdown("### Edge Telemetry Status")

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        st.success("🔒 Air-gapped: Ready")

    with status_col2:
        st.success("💾 Local Storage: Ready")

    with status_col3:
        st.success("📡 Sync: Local Only")

    st.caption(
        "Telemetry is persisted locally in SQLite. "
        "The operational telemetry store does not save the user's query text."
    )
