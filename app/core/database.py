"""Database connection utilities."""

import sqlite3
from contextlib import contextmanager

from app.core.config import settings


@contextmanager
def get_db_connection():
    """Provide a database connection context."""
    conn = sqlite3.connect(settings.DATABASE_URL.replace("sqlite:///", ""))
    try:
        yield conn
    finally:
        conn.close()
