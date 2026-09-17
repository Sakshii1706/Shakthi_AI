"""
Adapter between the Shakthi AI Streamlit UI and Yogesh's verified RAG backend.

Yogesh backend:
C:\\ShakthiAI

UI project:
C:\\Shakthi_AI
"""

import os
import sys
import threading
from pathlib import Path


# ---------------------------------------------------------
# Backend location
# ---------------------------------------------------------

BACKEND_ROOT = Path(r"C:\ShakthiAI")


# ---------------------------------------------------------
# Load Yogesh's backend
# ---------------------------------------------------------

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


from pipeline.rag_pipeline import RAGPipeline


# ---------------------------------------------------------
# Thread-local pipeline storage
# ---------------------------------------------------------
#
# Streamlit may execute reruns in different threads.
# Yogesh's SQLite connection must stay in the same thread
# in which its pipeline was created.
#
# Therefore, each Streamlit thread gets its own pipeline.
#

_thread_local = threading.local()

# os.chdir() is process-wide, so protect backend operations
# that depend on relative paths such as database/knowledge.db.
_cwd_lock = threading.Lock()


def get_pipeline():
    """
    Return a RAG pipeline belonging to the current thread.

    This avoids reusing a SQLite connection created by a
    different Streamlit thread.
    """

    pipeline = getattr(_thread_local, "pipeline", None)

    if pipeline is None:

        with _cwd_lock:

            original_cwd = os.getcwd()

            try:
                # Yogesh's backend uses relative paths such as:
                # database/knowledge.db
                os.chdir(BACKEND_ROOT)

                pipeline = RAGPipeline()

                _thread_local.pipeline = pipeline

            finally:
                os.chdir(original_cwd)

    return pipeline


# ---------------------------------------------------------
# Public UI function
# ---------------------------------------------------------

def query_rag(text: str) -> dict:
    """
    Send a user query to Yogesh's real RAG backend.

    Returns the stable backend contract:

    {
        "answer": ...,
        "sources": ...,
        "scores": ...,
        "confidence": ...,
        "refused": ...
    }
    """

    pipeline = get_pipeline()

    with _cwd_lock:

        original_cwd = os.getcwd()

        try:
            # Keep backend working directory available during
            # the query because Yogesh's backend uses relative
            # paths for the SQLite database.
            os.chdir(BACKEND_ROOT)

            result = pipeline.ask(text)

        finally:
            os.chdir(original_cwd)

    return result


# ---------------------------------------------------------
# Cleanup
# ---------------------------------------------------------

def close_pipeline():
    """
    Close the RAG pipeline belonging to the current thread.
    """

    pipeline = getattr(_thread_local, "pipeline", None)

    if pipeline is not None:

        try:
            pipeline.close()
        except Exception:
            pass

        _thread_local.pipeline = None