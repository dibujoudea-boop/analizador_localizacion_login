from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, List


DB_PATH = Path("outputs/login_analyzer_events.db")


def init_db(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS login_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                ip TEXT NOT NULL,
                declared_city TEXT,
                declared_country TEXT,
                network_type TEXT,
                risk_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                recommended_action TEXT NOT NULL,
                risk_reasons TEXT NOT NULL,
                raw_event TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_event_result(
    event: Dict[str, Any],
    risk_score: int,
    risk_level: str,
    recommended_action: str,
    risk_reasons: List[str],
    db_path: Path = DB_PATH,
) -> None:
    init_db(db_path)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO login_events (
                user_id,
                timestamp,
                ip,
                declared_city,
                declared_country,
                network_type,
                risk_score,
                risk_level,
                recommended_action,
                risk_reasons,
                raw_event
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.get("user_id"),
                event.get("timestamp"),
                event.get("ip"),
                event.get("declared_city"),
                event.get("declared_country"),
                event.get("network_type"),
                risk_score,
                risk_level,
                recommended_action,
                json.dumps(risk_reasons, ensure_ascii=False),
                json.dumps(event, ensure_ascii=False),
            ),
        )
        conn.commit()


def read_recent_events(limit: int = 20, db_path: Path = DB_PATH) -> list[dict]:
    init_db(db_path)

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT *
            FROM login_events
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]
