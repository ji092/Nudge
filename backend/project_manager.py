"""프로젝트 CRUD 최소 구현 (Phase 1: 이름 등록·목록 조회만)."""
from shared.db import get_connection

SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
"""


def init_db() -> None:
    conn = get_connection()
    try:
        conn.execute(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def add_project(name: str) -> None:
    conn = get_connection()
    try:
        conn.execute("INSERT INTO projects (name) VALUES (?)", (name,))
        conn.commit()
    finally:
        conn.close()


def list_projects() -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT id, name, created_at FROM projects").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
