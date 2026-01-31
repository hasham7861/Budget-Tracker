"""Database utilities for SQLite storage."""
import sqlite3
from pathlib import Path
from typing import Optional

# Use local .data directory in the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / ".data"
DB_FILE = DATA_DIR / "budget_tracker.db"


def init_db() -> None:
    """Initialize the database with required tables."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create notes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spending_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year TEXT NOT NULL,
            month TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(year, month)
        )
    """)

    conn.commit()
    conn.close()


def save_note(year: str, month: str, notes: str) -> None:
    """Save or update a note for a specific year/month."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO spending_notes (year, month, notes, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(year, month)
        DO UPDATE SET notes = excluded.notes, updated_at = CURRENT_TIMESTAMP
    """, (year, month, notes))

    conn.commit()
    conn.close()


def get_note(year: str, month: str) -> Optional[str]:
    """Get a note for a specific year/month."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT notes FROM spending_notes
        WHERE year = ? AND month = ?
    """, (year, month))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None
