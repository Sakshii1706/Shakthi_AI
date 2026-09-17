"""
Temporary mock backend for Shakthi AI UI development.

This is NOT the real AI backend.
It will be replaced by Yogesh's implementation later.
"""


def mock_query_rag(text: str) -> dict:
    """
    Simulates Yogesh's RAG response.
    """

    text_lower = text.lower()

    # Test 4: Out-of-scope query
    if "ಕ್ರಿಕೆಟ್" in text or "cricket" in text_lower:
        return {
            "answer": (
                "ಕ್ಷಮಿಸಿ. ಈ ಪ್ರಶ್ನೆ ಶಕ್ತಿ AI ಪರಿಶೀಲಿಸಿದ "
                "ಆರೋಗ್ಯ ಮತ್ತು ಶಿಕ್ಷಣ ಮಾಹಿತಿಯ ವ್ಯಾಪ್ತಿಗೆ ಹೊರಗಾಗಿದೆ."
            ),
            "sources": [],
            "confidence": 0.0,
            "refused": True
        }

    # Test 1: Anemia
    if "ಸುಸ್ತು" in text or "ತಲೆ ಸುತ್ತು" in text:
        return {
            "answer": (
                "ನಿಮಗೆ ಸುಸ್ತು ಮತ್ತು ತಲೆ ಸುತ್ತುವ ಅನುಭವವಾಗುತ್ತಿರುವುದಕ್ಕೆ "
                "ಹಲವು ಕಾರಣಗಳಿರಬಹುದು. ರಕ್ತಹೀನತೆ ಕೂಡ ಒಂದು ಸಾಧ್ಯ ಕಾರಣವಾಗಿರಬಹುದು. "
                "ಕಬ್ಬಿಣಾಂಶ ಹೊಂದಿರುವ ಆಹಾರವನ್ನು ಸೇವಿಸುವುದು ಮತ್ತು ಆರೋಗ್ಯ "
                "ಸಿಬ್ಬಂದಿಯ ಸಲಹೆಯಂತೆ IFA ಮಾತ್ರೆಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುವುದು ಮುಖ್ಯ."
            ),
            "sources": [
                "Demo: Verified Kannada Health Knowledge"
            ],
            "confidence": 0.91,
            "refused": False
        }

    # Test 2: IFA side effect
    if "ಕಪ್ಪು ಮಲ" in text:
        return {
            "answer": (
                "ಐರನ್ ಮಾತ್ರೆಗಳನ್ನು ತೆಗೆದುಕೊಂಡ ನಂತರ ಮಲ ಕಪ್ಪಾಗುವುದು "
                "ಸಾಮಾನ್ಯ ಅಡ್ಡ ಪರಿಣಾಮವಾಗಿರಬಹುದು. ಈ ಕಾರಣಕ್ಕೆ ಮಾತ್ರೆಗಳನ್ನು "
                "ಸ್ವತಃ ನಿಲ್ಲಿಸಬೇಡಿ. ಯಾವುದೇ ಅಸಾಮಾನ್ಯ ಲಕ್ಷಣಗಳಿದ್ದರೆ "
                "ಆರೋಗ್ಯ ಸಿಬ್ಬಂದಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ."
            ),
            "sources": [
                "Demo: Verified IFA Guidance"
            ],
            "confidence": 0.94,
            "refused": False
        }

    # Test 3: DSERT science
    if "ರಕ್ತ" in text or "ಹಿಮೋಗ್ಲೋಬಿನ್" in text:
        return {
            "answer": (
                "ರಕ್ತದಲ್ಲಿರುವ ಮುಖ್ಯ ಘಟಕಗಳಲ್ಲಿ ಕೆಂಪು ರಕ್ತಕಣಗಳು (RBC), "
                "ಬಿಳಿ ರಕ್ತಕಣಗಳು (WBC), ಪ್ಲೇಟ್‌ಲೆಟ್‌ಗಳು ಮತ್ತು ಪ್ಲಾಸ್ಮಾ "
                "ಮುಖ್ಯವಾದವು. ಹಿಮೋಗ್ಲೋಬಿನ್ ಆಮ್ಲಜನಕವನ್ನು ಸಾಗಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ."
            ),
            "sources": [
                "Demo: DSERT Class 10 Science"
            ],
            "confidence": 0.96,
            "refused": False
        }

    # Generic demo response
    return {
        "answer": (
            "ಇದು Shakthi AI UI ಪರೀಕ್ಷೆಗಾಗಿ ಬಳಸುತ್ತಿರುವ "
            "ತಾತ್ಕಾಲಿಕ demo response. ನಿಜವಾದ RAG backend ಇನ್ನೂ ಸಂಪರ್ಕಗೊಂಡಿಲ್ಲ."
        ),
        "sources": [
            "Demo Backend"
        ],
        "confidence": 0.50,
        "refused": False
    }


def mock_transcribe(audio=None) -> dict:
    """
    Temporary Whisper mock.
    """

    return {
        "text": "ನನಗೆ ತುಂಬಾ ಸುಸ್ತು ಅನಿಸುತ್ತೆ ಮತ್ತು ತಲೆ ಸುತ್ತುತ್ತೆ.",
        "confidence": 0.95
    }


def mock_synthesize(text: str):
    """
    Temporary Piper mock.

    No real audio is generated yet.
    """

    return None