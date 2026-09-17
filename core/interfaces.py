"""
Shakthi AI Integration Contracts

This file defines the interfaces between:
- Sakshi's UI
- Yogesh's RAG backend
- Sinchana's voice pipeline

The actual implementations will be connected later.
"""


def query_rag(text: str) -> dict:
    """
    Query the local Shakthi AI RAG pipeline.

    Expected return format:

    {
        "answer": str,
        "sources": list[str],
        "confidence": float,
        "refused": bool
    }
    """
    raise NotImplementedError("RAG backend not connected yet.")


def transcribe(audio) -> dict:
    """
    Convert Kannada speech to text using local Whisper.cpp.

    Expected return format:

    {
        "text": str,
        "confidence": float
    }
    """
    raise NotImplementedError("Whisper backend not connected yet.")


def synthesize(text: str):
    """
    Convert Kannada text to speech using local Piper.

    Expected return:
        WAV file path or audio bytes.

    Final implementation will be provided by Sinchana.
    """
    raise NotImplementedError("Piper backend not connected yet.")