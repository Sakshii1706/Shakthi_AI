import os
import tempfile
import time

import streamlit as st

from core.backend.rag_backend import query_rag
from core.telemetry import record_event
from voice.indicconformer.asr_bridge import transcribe


# Conservative corrections for verified IndicConformer Kannada ASR errors.
# These are applied only to the query sent to RAG, not to the displayed
# transcription.
ASR_CORRECTIONS = {
    "ಕಬ್ಬಿನದ": "ಕಬ್ಬಿಣದ",
    "ಮಾತ್ರೆಗಳಗಳನ್ನು": "ಮಾತ್ರೆಗಳನ್ನು",
}


def normalize_asr_query(text: str) -> str:
    """Apply only verified, conservative Kannada ASR corrections."""
    normalized = text

    for wrong, correct in ASR_CORRECTIONS.items():
        normalized = normalized.replace(wrong, correct)

    return normalized


def _record_query_telemetry(
    *,
    user_query: str,
    input_mode: str,
    result: dict,
    response_time_ms: float,
) -> None:
    """
    Record anonymized operational telemetry.

    Telemetry failures must never break the RAG response.
    The actual query text is intentionally not stored.
    """

    try:
        confidence = result.get("confidence")
        sources = result.get("sources", [])

        record_event(
            input_mode=input_mode,
            language="kn",
            query_length=len(user_query),
            refused=bool(result.get("refused", False)),
            confidence=confidence,
            response_time_ms=response_time_ms,
            source_count=len(sources) if sources else 0,
        )

    except Exception:
        # Telemetry is non-critical. Never interrupt the assistant.
        pass


def _process_rag_query(
    user_query: str,
    input_mode: str = "text",
):
    """
    Send a Kannada text query to the existing Shakthi AI RAG backend
    and render the response.

    input_mode:
        "text" for typed queries
        "voice" for ASR-generated queries
    """

    if not user_query or not user_query.strip():
        return

    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):

        with st.spinner("ಉತ್ತರವನ್ನು ಹುಡುಕಲಾಗುತ್ತಿದೆ..."):

            start_time = time.perf_counter()

            try:
                result = query_rag(user_query)

            except Exception as e:
                response_time_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                # Do not let a backend failure disappear from
                # operational telemetry.
                try:
                    record_event(
                        input_mode=input_mode,
                        language="kn",
                        query_length=len(user_query),
                        refused=True,
                        confidence=None,
                        response_time_ms=response_time_ms,
                        source_count=0,
                    )
                except Exception:
                    pass

                st.error(
                    "RAG backend error. Please check the local "
                    "backend configuration."
                )
                st.exception(e)
                return

            response_time_ms = (
                time.perf_counter() - start_time
            ) * 1000

        _record_query_telemetry(
            user_query=user_query,
            input_mode=input_mode,
            result=result,
            response_time_ms=response_time_ms,
        )

        # -------------------------------------------------
        # Refusal / Guardrail
        # -------------------------------------------------

        if result.get("refused", False):

            st.markdown("### 🛡️ Outside verified knowledge")

            st.warning(
                result.get(
                    "answer",
                    "ಈ ಪ್ರಶ್ನೆಗೆ ಮಾಹಿತಿಯಲ್ಲಿ ಉತ್ತರ ಸಿಗಲಿಲ್ಲ.",
                )
            )

            st.caption(
                "ಈ ಪ್ರಶ್ನೆಗೆ ಪರಿಶೀಲಿಸಿದ ಸ್ಥಳೀಯ ಜ್ಞಾನ ಮೂಲಗಳಲ್ಲಿ "
                "ಸೂಕ್ತ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ."
            )

            return

        # -------------------------------------------------
        # Normal Answer
        # -------------------------------------------------

        st.markdown("### 🤖 Shakthi's answer")

        st.write(
            result.get(
                "answer",
                "ಉತ್ತರ ಲಭ್ಯವಿಲ್ಲ.",
            )
        )

        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        sources = result.get("sources", [])

        if sources:

            st.markdown("### 📚 Verified local sources")

            for source in sources:

                if isinstance(source, dict):

                    source_name = source.get(
                        "source",
                        "Local Knowledge Base",
                    )

                    page = source.get("page")
                    chunk_id = source.get("chunk_id")

                    source_parts = [str(source_name)]

                    if page is not None:
                        source_parts.append(f"Page {page}")

                    if chunk_id is not None:
                        source_parts.append(str(chunk_id))

                    st.caption(
                        "• " + " — ".join(source_parts)
                    )

                else:
                    st.caption(f"• {source}")

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        confidence = result.get("confidence")

        if confidence is not None:

            confidence = min(
                max(float(confidence), 0.0),
                1.0,
            )

            st.progress(
                confidence,
                text=f"Retrieval confidence: {confidence:.0%}",
            )


def render_student_assistant():
    """
    Shakthi AI Student Assistant UI.

    Text:
        Kannada query -> existing RAG backend

    Voice:
        Kannada audio -> AI4Bharat IndicConformer ASR
        -> Kannada transcription -> conservative ASR normalization
        -> existing RAG backend
    """

    st.markdown("## 🎓 Vernacular Student Assistant")

    st.markdown(
        """
        <div style="
            padding: 0.9rem 1rem;
            border: 1px solid rgba(99,132,255,0.28);
            border-radius: 14px;
            background: rgba(27,42,74,0.45);
            margin-bottom: 1rem;
        ">
            <div style="font-weight:700; margin-bottom:0.25rem; color:#E7ECFF;">
                Ask Shakthi in Kannada
            </div>
            <div style="color:rgba(231,236,255,0.75); font-size:0.92rem; line-height:1.5;">
                Type your question or use your voice. Answers are grounded
                in verified local knowledge and processed on the edge.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # TEXT QUERY
    # =====================================================

    user_query = st.chat_input(
        "ಕನ್ನಡದಲ್ಲಿ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ..."
    )

    if user_query:
        _process_rag_query(
            user_query,
            input_mode="text",
        )

    # =====================================================
    # VOICE INPUT
    # =====================================================

    st.divider()

    st.markdown("### 🎤 Kannada Voice Assistant")

    st.caption(
        "Record a Kannada voice query. The audio is processed locally "
        "using AI4Bharat IndicConformer."
    )

    audio_value = st.audio_input(
        "🎙️ Record Kannada query"
    )

    if audio_value is not None:

        st.audio(
            audio_value,
            format="audio/wav",
        )

        if st.button(
            "▶️ Transcribe & Ask",
            key="transcribe_and_ask",
        ):

            temp_audio_path = None

            try:

                # -----------------------------------------
                # Save Streamlit audio to temporary WAV
                # -----------------------------------------

                with tempfile.NamedTemporaryFile(
                    suffix=".wav",
                    delete=False,
                ) as temp_audio:

                    temp_audio.write(
                        audio_value.getvalue()
                    )

                    temp_audio_path = temp_audio.name

                # -----------------------------------------
                # IndicConformer ASR
                # -----------------------------------------

                with st.spinner(
                    "ಕನ್ನಡ ಧ್ವನಿಯನ್ನು ಪಠ್ಯಕ್ಕೆ ಪರಿವರ್ತಿಸಲಾಗುತ್ತಿದೆ..."
                ):

                    voice_result = transcribe(
                        temp_audio_path
                    )

                transcribed_text = voice_result.get(
                    "text",
                    "",
                ).strip()

                asr_confidence = voice_result.get(
                    "confidence"
                )

                if not transcribed_text:

                    st.error(
                        "ಧ್ವನಿಯಿಂದ ಯಾವುದೇ ಪಠ್ಯವನ್ನು ಗುರುತಿಸಲಾಗಲಿಲ್ಲ."
                    )

                    return

                # -----------------------------------------
                # Display raw transcription
                # -----------------------------------------

                st.markdown("### 🎙️ You said")

                st.success(
                    transcribed_text
                )

                if asr_confidence is not None:

                    st.caption(
                        f"ASR confidence: "
                        f"{float(asr_confidence):.0%}"
                    )

                # -----------------------------------------
                # Send normalized transcription to RAG
                # -----------------------------------------

                rag_query = normalize_asr_query(
                    transcribed_text
                )

                _process_rag_query(
                    rag_query,
                    input_mode="voice",
                )

            except Exception as e:

                st.error(
                    "Kannada ASR failed. "
                    "Please check the IndicConformer configuration."
                )

                st.exception(e)

            finally:

                # -----------------------------------------
                # Clean temporary audio
                # -----------------------------------------

                if (
                    temp_audio_path
                    and os.path.exists(temp_audio_path)
                ):

                    try:
                        os.remove(temp_audio_path)

                    except OSError:
                        pass
