"""프로젝트 CRUD 최소 구현 (Phase 1: 이름 등록·목록 조회만). 스키마는 shared/db.py 단일 정의."""
from shared.db import get_connection


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
