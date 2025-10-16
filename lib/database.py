"""
Database module.
Provides a shared sqlite3 connection and a create_tables() function
that creates the schema used by the models.
"""

import os
import sqlite3
# Allow overriding DB path with env var (useful in tests)
DB_PATH = os.environ.get("PETCARE_DB", "db/database.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
# Create a connection and cursor shared across modules
CONN = sqlite3.connect(DB_PATH, check_same_thread=False)
# Row factory allows access by column name, e.g., row["id"]
CONN.row_factory = sqlite3.Row
CURSOR = CONN.cursor()
def create_tables() -> None:
    """
    Create the four tables used by PetCare:
    - owners
    - pets
    - appointments
    - medical_history
    """
    # Owners table
    CURSOR.execute("""
    CREATE TABLE IF NOT EXISTS owners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact TEXT UNIQUE
    );
    """)
