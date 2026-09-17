import json
import os
import subprocess
import sys


ASR_PYTHON = os.getenv(
    "SHAKTHI_ASR_PYTHON",
    r"C:\ShakthiAI-ASR\ai4bharat-env\Scripts\python.exe"
)

ASR_SCRIPT = os.getenv(
    "SHAKTHI_ASR_SCRIPT",
    r"C:\ShakthiAI-ASR\kannada_asr.py"
)


def transcribe(audio_path: str) -> dict:
    """
    Transcribe Kannada audio using the working
    AI4Bharat IndicConformer environment.
    """

    if not os.path.isfile(audio_path):
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    if not os.path.isfile(ASR_PYTHON):
        raise FileNotFoundError(
            f"ASR Python executable not found: {ASR_PYTHON}"
        )

    if not os.path.isfile(ASR_SCRIPT):
        raise FileNotFoundError(
            f"ASR script not found: {ASR_SCRIPT}"
        )

    command = [
        ASR_PYTHON,
        "-c",
        (
            "import sys; "
            "sys.stdout.reconfigure(encoding='utf-8'); "
            "sys.stderr.reconfigure(encoding='utf-8'); "
            f"sys.path.insert(0, r'{os.path.dirname(ASR_SCRIPT)}'); "
            "from kannada_asr import transcribe; "
            "print(transcribe(sys.argv[1]))"
        ),
        audio_path,
    ]

    # Force the child Python process to use UTF-8.
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Kannada ASR failed:\n"
            + result.stderr
        )

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    if not lines:
        raise RuntimeError(
            "Kannada ASR returned no transcription."
        )

    text = lines[-1]

    return {
        "text": text,
        "confidence": 1.0,
    }