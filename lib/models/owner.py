"""
Owner model: represents the owners table and exposes CRUD operations.
This class behaves as a simple ORM mapping rows <-> Python objects.
"""

from typing import Optional, List
import sqlite3
from lib.database import CURSOR, CONN

class Owner:
    def __init__(self, name: str, contact: str, id: Optional[int] = None):
         """
        Initialize an Owner instance.
        Fields:
          - id: primary key (None for new objects)
          - name: full name of owner (required)
          - contact: phone or email (should be unique)
        """
        self.id = id
        self.name = name
        self.contact = contact
         def save(self) -> "Owner":
        """
        Insert a new owner record into the DB.
        Validates required fields and handles uniqueness constraint violation.
        """
        if not self.name or not self.contact:
            raise ValueError("Owner name and contact are required.")
        try:
            CURSOR.execute(
                "INSERT INTO owners (name, contact) VALUES (?, ?)",
                (self.name, self.contact)
            )
            CONN.commit()
            # set id to last inserted id for object-relational mapping
            self.id = CURSOR.lastrowid
            return self
        except sqlite3.IntegrityError as e:
            # Unique constraint violation for contact
            raise ValueError("Owner contact must be unique.") from e