"""SQLite storage for conversation history and file metadata."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional
from uuid import uuid4

from backend.app.storage import STORAGE_ROOT

DB_PATH = STORAGE_ROOT / "metadata.db"


@dataclass
class ConversationRecord:
    id: str
    created_at: str
    request_payload: List[Dict[str, Any]]


@dataclass
class MessageRecord:
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: str


@dataclass
class FileRecord:
    id: str
    conversation_id: str
    name: str
    type: str
    storage_key: str
    local_path: Optional[str]
    created_at: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                request_payload TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(conversation_id) REFERENCES conversations(id)
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                storage_key TEXT NOT NULL,
                local_path TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(conversation_id) REFERENCES conversations(id)
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_files_conversation ON files(conversation_id)"
        )


def create_conversation(request_payload: List[Dict[str, Any]]) -> ConversationRecord:
    conversation_id = uuid4().hex
    created_at = _utc_now()
    payload_json = json.dumps(request_payload)

    with get_connection() as connection:
        connection.execute(
            "INSERT INTO conversations (id, created_at, request_payload) VALUES (?, ?, ?)",
            (conversation_id, created_at, payload_json),
        )

    return ConversationRecord(id=conversation_id, created_at=created_at, request_payload=request_payload)


def add_message(conversation_id: str, role: str, content: str) -> MessageRecord:
    message_id = uuid4().hex
    created_at = _utc_now()
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO messages (id, conversation_id, role, content, created_at) VALUES (?, ?, ?, ?, ?)",
            (message_id, conversation_id, role, content, created_at),
        )
    return MessageRecord(
        id=message_id,
        conversation_id=conversation_id,
        role=role,
        content=content,
        created_at=created_at,
    )


def add_file(
    conversation_id: str,
    name: str,
    file_type: str,
    storage_key: str,
    local_path: Optional[str],
) -> FileRecord:
    file_id = uuid4().hex
    created_at = _utc_now()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO files (id, conversation_id, name, type, storage_key, local_path, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (file_id, conversation_id, name, file_type, storage_key, local_path, created_at),
        )
    return FileRecord(
        id=file_id,
        conversation_id=conversation_id,
        name=name,
        type=file_type,
        storage_key=storage_key,
        local_path=local_path,
        created_at=created_at,
    )


def list_conversations() -> List[ConversationRecord]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, created_at, request_payload FROM conversations ORDER BY created_at DESC"
        ).fetchall()

    conversations: List[ConversationRecord] = []
    for row in rows:
        payload = json.loads(row["request_payload"]) if row["request_payload"] else []
        conversations.append(
            ConversationRecord(
                id=row["id"],
                created_at=row["created_at"],
                request_payload=payload,
            )
        )
    return conversations


def get_conversation(conversation_id: str) -> Optional[ConversationRecord]:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, created_at, request_payload FROM conversations WHERE id = ?",
            (conversation_id,),
        ).fetchone()

    if not row:
        return None

    payload = json.loads(row["request_payload"]) if row["request_payload"] else []
    return ConversationRecord(
        id=row["id"],
        created_at=row["created_at"],
        request_payload=payload,
    )


def list_messages(conversation_id: str) -> List[MessageRecord]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, conversation_id, role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY created_at ASC
            """,
            (conversation_id,),
        ).fetchall()

    return [
        MessageRecord(
            id=row["id"],
            conversation_id=row["conversation_id"],
            role=row["role"],
            content=row["content"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


def list_files(conversation_id: str) -> List[FileRecord]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, conversation_id, name, type, storage_key, local_path, created_at
            FROM files
            WHERE conversation_id = ?
            ORDER BY created_at ASC
            """,
            (conversation_id,),
        ).fetchall()

    return [
        FileRecord(
            id=row["id"],
            conversation_id=row["conversation_id"],
            name=row["name"],
            type=row["type"],
            storage_key=row["storage_key"],
            local_path=row["local_path"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


def get_file(file_id: str) -> Optional[FileRecord]:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, conversation_id, name, type, storage_key, local_path, created_at
            FROM files
            WHERE id = ?
            """,
            (file_id,),
        ).fetchone()

    if not row:
        return None

    return FileRecord(
        id=row["id"],
        conversation_id=row["conversation_id"],
        name=row["name"],
        type=row["type"],
        storage_key=row["storage_key"],
        local_path=row["local_path"],
        created_at=row["created_at"],
    )
