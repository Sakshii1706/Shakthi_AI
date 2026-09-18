import sqlite3
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TELEMETRY_DB = PROJECT_ROOT / "data" / "telemetry.db"


def _connect():
    TELEMETRY_DB.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        TELEMETRY_DB,
        timeout=5,
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS telemetry_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_utc TEXT NOT NULL,
            input_mode TEXT NOT NULL,
            language TEXT NOT NULL,
            query_length INTEGER NOT NULL,
            refused INTEGER NOT NULL,
            confidence REAL,
            response_time_ms REAL,
            source_count INTEGER NOT NULL
        )
        """
    )

    connection.commit()
    return connection


def record_event(
    *,
    input_mode: str,
    language: str = "kn",
    query_length: int = 0,
    refused: bool = False,
    confidence: float | None = None,
    response_time_ms: float | None = None,
    source_count: int = 0,
) -> None:
    """
    Persist one anonymized local operational telemetry event.

    The user's actual query text is intentionally NOT stored.
    """

    connection = _connect()

    try:
        connection.execute(
            """
            INSERT INTO telemetry_events (
                timestamp_utc,
                input_mode,
                language,
                query_length,
                refused,
                confidence,
                response_time_ms,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                input_mode,
                language,
                int(query_length),
                int(bool(refused)),
                (
                    float(confidence)
                    if confidence is not None
                    else None
                ),
                (
                    float(response_time_ms)
                    if response_time_ms is not None
                    else None
                ),
                int(source_count),
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_summary() -> dict:
    """
    Return aggregate telemetry from the local database.
    """

    connection = _connect()

    try:
        total = connection.execute(
            "SELECT COUNT(*) FROM telemetry_events"
        ).fetchone()[0]

        answered = connection.execute(
            """
            SELECT COUNT(*)
            FROM telemetry_events
            WHERE refused = 0
            """
        ).fetchone()[0]

        refused = connection.execute(
            """
            SELECT COUNT(*)
            FROM telemetry_events
            WHERE refused = 1
            """
        ).fetchone()[0]

        voice = connection.execute(
            """
            SELECT COUNT(*)
            FROM telemetry_events
            WHERE input_mode = 'voice'
            """
        ).fetchone()[0]

        text = connection.execute(
            """
            SELECT COUNT(*)
            FROM telemetry_events
            WHERE input_mode = 'text'
            """
        ).fetchone()[0]

        avg_response = connection.execute(
            """
            SELECT AVG(response_time_ms)
            FROM telemetry_events
            WHERE response_time_ms IS NOT NULL
            """
        ).fetchone()[0]

        avg_confidence = connection.execute(
            """
            SELECT AVG(confidence)
            FROM telemetry_events
            WHERE confidence IS NOT NULL
            """
        ).fetchone()[0]

        last_event = connection.execute(
            """
            SELECT timestamp_utc
            FROM telemetry_events
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

        return {
            "total": total,
            "answered": answered,
            "refused": refused,
            "voice": voice,
            "text": text,
            "avg_response_time_ms": avg_response,
            "avg_confidence": avg_confidence,
            "last_event_utc": (
                last_event[0]
                if last_event
                else None
            ),
        }

    finally:
        connection.close()
