"""SQLite database configuration and schema initialization."""

import os
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
_configured_path = os.environ.get("DATABASE_PATH")
_legacy_path = BASE_DIR / "attendance_expense.db"
DATABASE_PATH = (Path(_configured_path).expanduser() if _configured_path else
                 _legacy_path if _legacy_path.exists() else BASE_DIR / "instance" / "attendance_expense.db")


def get_connection():
    """Open a configured SQLite connection with foreign key checks enabled."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DATABASE_PATH), timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 15000")
    return conn


def init_db():
    """Create the application tables and migrate older local databases."""
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                branch TEXT NOT NULL,
                year INTEGER NOT NULL,
                semester INTEGER NOT NULL,
                email TEXT,
                phone TEXT,
                password TEXT
            );
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                attendance_date TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
                FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                UNIQUE(student_id, attendance_date)
            );
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                expense_date TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE CASCADE
            );
            """
        )
        # Databases created before password support need this additive migration.
        student_columns = {row["name"] for row in conn.execute("PRAGMA table_info(students)")}
        if "password" not in student_columns:
            conn.execute("ALTER TABLE students ADD COLUMN password TEXT")


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DATABASE_PATH}")
