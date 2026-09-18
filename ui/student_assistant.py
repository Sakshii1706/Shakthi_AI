import os
import tempfile

import streamlit as st

from core.backend.rag_backend import query_rag
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


def _process_rag_query(user_query: str):
    """
    Send a Kannada text query to the existing Shakthi AI RAG backend
    and render the response.
    """

    if not user_query or not user_query.strip():
        return

    with st.chat_message("user"):
        st.write(user_query)

    with st.chat_message("assistant"):

        with st.spinner("ಉತ್ತರವನ್ನು ಹುಡುಕಲಾಗುತ್ತಿದೆ..."):

            try:
                result = query_rag(user_query)

            except Exception as e:
                st.error(
                    "RAG backend error. Please check the local "
                    "backend configuration."
                )
                st.exception(e)
                return

        # -------------------------------------------------
        # Refusal / Guardrail
        # -------------------------------------------------

        if result.get("refused", False):

            st.warning(
                result.get(
                    "answer",
                    "ಈ ಪ್ರಶ್ನೆಗೆ ಮಾಹಿತಿಯಲ್ಲಿ ಉತ್ತರ ಸಿಗಲಿಲ್ಲ."
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

        st.write(
            result.get(
                "answer",
                "ಉತ್ತರ ಲಭ್ಯವಿಲ್ಲ."
            )
        )

        # -------------------------------------------------
        # Sources
        # -------------------------------------------------

        sources = result.get("sources", [])

        if sources:

            st.markdown("**📚 Sources**")

            for source in sources:

                if isinstance(source, dict):

                    source_name = source.get(
                        "source",
                        "Local Knowledge Base"
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
                1.0
            )

            st.progress(
                confidence,
                text=f"Retrieval confidence: {confidence:.0%}"
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

    st.subheader("🎓 Vernacular Student Assistant")

    st.caption(
        "Ask questions in Kannada about verified health, education, "
        "or safety information."
    )

    # =====================================================
    # TEXT QUERY
    # =====================================================

    user_query = st.chat_input(
        "ಕನ್ನಡದಲ್ಲಿ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ..."
    )

    if user_query:
        _process_rag_query(user_query)

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
            format="audio/wav"
        )

        if st.button(
            "▶️ Transcribe & Ask",
            key="transcribe_and_ask"
        ):

            temp_audio_path = None

            try:

                # -----------------------------------------
                # Save Streamlit audio to temporary WAV
                # -----------------------------------------

                with tempfile.NamedTemporaryFile(
                    suffix=".wav",
                    delete=False
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
                    ""
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

                st.markdown("### 📝 Transcription")

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
                    rag_query
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