import os
import sys
import threading
from pathlib import Path


# ------------------------------------------------------------
# Portable backend location
# ------------------------------------------------------------
# The launcher sets SHAKTHI_BACKEND_ROOT.
# C:\ShakthiAI remains the fallback for the current machine.
# ------------------------------------------------------------

BACKEND_ROOT = Path(
    os.environ.get(
        "SHAKTHI_BACKEND_ROOT",
        r"C:\ShakthiAI",
    )
).resolve()


if not BACKEND_ROOT.exists():
    raise FileNotFoundError(
        f"Shakthi AI backend not found: {BACKEND_ROOT}"
    )


if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


from pipeline.rag_pipeline import RAGPipeline


_thread_local = threading.local()
_cwd_lock = threading.Lock()


def get_pipeline():
    pipeline = getattr(_thread_local, "pipeline", None)

    if pipeline is None:
        with _cwd_lock:
            original_cwd = os.getcwd()

            try:
                os.chdir(BACKEND_ROOT)
                pipeline = RAGPipeline()
                _thread_local.pipeline = pipeline

            finally:
                os.chdir(original_cwd)

    return pipeline


def query_rag(text: str) -> dict:
    pipeline = get_pipeline()

    with _cwd_lock:
        original_cwd = os.getcwd()

        try:
            result = pipeline.ask(text)

        finally:
            os.chdir(original_cwd)

    return result


def close_pipeline():
    pipeline = getattr(_thread_local, "pipeline", None)

    if pipeline is not None:
        try:
            pipeline.close()
        except Exception:
            pass

        _thread_local.pipeline = None
