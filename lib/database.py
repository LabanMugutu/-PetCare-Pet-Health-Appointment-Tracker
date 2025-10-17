# lib/database.py
# ----------------------------------------
# Handles database connection and table creation using sqlite3.
# This file defines CURSOR and CONN used by all model classes.
# ----------------------------------------

import sqlite3

# Connect to SQLite database (creates one if it doesn't exist)
CONN = sqlite3.connect('db/database.db')
CURSOR = CONN.cursor()

def create_tables():
    """Creates all necessary tables if they don't exist."""
    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS owners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    ''')

    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            species TEXT,
            breed TEXT,
            owner_id INTEGER,
            FOREIGN KEY (owner_id) REFERENCES owners(id)
        )
    ''')

    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            date TEXT,
            reason TEXT,
            vet_name TEXT,
            notes TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        )
    ''')

    CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER,
            record_date TEXT,
            treatment TEXT,
            notes TEXT,
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        )
    ''')

    CONN.commit()
