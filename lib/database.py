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