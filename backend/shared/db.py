"""SQLite 연결 헬퍼. DB 파일은 .gitignore 처리됨 (*.db) — git add 금지."""
import sqlite3

from . import config


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
