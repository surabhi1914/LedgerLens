# src/ledgerlens/persistence/database.py
import sqlite3
from pathlib import Path

# Resolve project root (three levels up from src/ledgerlens/persistence/database.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "ledgerlens.db"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Ensure the data directory exists and
    return a SQLite connection configured with sqlite3.Row."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(db_path: Path = DB_PATH) -> None:
    """Create the database tables if they do not already exist."""
    schema = """
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_filename TEXT NOT NULL,
        vendor TEXT,
        invoice_number TEXT,
        invoice_date TEXT,
        subtotal TEXT,
        tax TEXT,
        discount TEXT,
        total TEXT,
        currency TEXT,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_connection(db_path) as conn:
        conn.execute(schema)
        conn.commit()
