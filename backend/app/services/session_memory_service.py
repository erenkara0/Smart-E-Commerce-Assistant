import sqlite3
from pathlib import Path
from typing import Literal

from app.core.config import ROOT_DIR, settings


MessageRole = Literal["user", "assistant"]


class SessionMemoryService:
    def __init__(self, db_path: str | Path | None = None) -> None:
        configured_path = Path(db_path or settings.sqlite_db_path)

        if configured_path.is_absolute():
            self.db_path = configured_path
        else:
            self.db_path = ROOT_DIR / configured_path

    def initialize_database(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS
                idx_chat_messages_session_id_id
                ON chat_messages (session_id, id)
                """
            )

            connection.commit()

    def save_message(
        self,
        session_id: str,
        role: MessageRole,
        content: str,
    ) -> int:
        normalized_session_id = session_id.strip()
        normalized_content = content.strip()

        if not normalized_session_id:
            raise ValueError("Session ID cannot be empty.")

        if not normalized_content:
            raise ValueError("Message content cannot be empty.")

        self.initialize_database()

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO chat_messages (session_id, role, content)
                VALUES (?, ?, ?)
                """,
                (normalized_session_id, role, normalized_content),
            )
            connection.commit()

            if cursor.lastrowid is None:
                raise RuntimeError("Message could not be saved.")

            return int(cursor.lastrowid)

    def get_recent_messages(
        self,
        session_id: str,
        limit: int | None = None,
    ) -> list[dict[str, str | int]]:
        normalized_session_id = session_id.strip()
        message_limit = limit or settings.session_memory_limit

        if not normalized_session_id:
            raise ValueError("Session ID cannot be empty.")

        if message_limit < 1:
            raise ValueError("Message limit must be greater than zero.")

        self.initialize_database()

        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row

            rows = connection.execute(
                """
                SELECT id, session_id, role, content, created_at
                FROM chat_messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (normalized_session_id, message_limit),
            ).fetchall()

        return [dict(row) for row in reversed(rows)]


session_memory_service = SessionMemoryService()