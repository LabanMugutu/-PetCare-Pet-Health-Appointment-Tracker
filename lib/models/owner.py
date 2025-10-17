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
    def update(self, name: Optional[str] = None, contact: Optional[str] = None) -> "Owner":
        """
        Update this owner's fields in the DB.
        Only non-None arguments are applied.
        """
        if name:
            self.name = name
        if contact:
            self.contact = contact
        if not self.id:
            raise ValueError("Owner must have an id to update.")
        CURSOR.execute(
            "UPDATE owners SET name = ?, contact = ? WHERE id = ?",
            (self.name, self.contact, self.id)
        )
        CONN.commit()
        return self
    def delete(self) -> None:
        """
        Delete the owner record from the DB.
        Note: application logic should ensure pets are reassigned/deleted first.
        """
        if not self.id:
            raise ValueError("Owner must have an id to delete.")
        CURSOR.execute("DELETE FROM owners WHERE id = ?", (self.id,))
        CONN.commit()

    @classmethod
    def find_by_id(cls, owner_id: int) -> Optional["Owner"]:
        """Return Owner instance or None for given id."""
        row = CURSOR.execute("SELECT id, name, contact FROM owners WHERE id = ?", (owner_id,)).fetchone()
        if row:
            return cls(id=row["id"], name=row["name"], contact=row["contact"])
        return None

    @classmethod
    def all(cls) -> List["Owner"]:
        """Return all owners as a list of Owner instances."""
        rows = CURSOR.execute("SELECT id, name, contact FROM owners").fetchall()
        return [cls(id=r["id"], name=r["name"], contact=r["contact"]) for r in rows]

    @classmethod
    def find_by_name(cls, name_query: str) -> List["Owner"]:
        """
        Search owners by partial name match using LIKE.2
        Demonstrates parameterized queries to avoid SQL injection.
        """
        like = f"%{name_query}%"
        rows = CURSOR.execute("SELECT id, name, contact FROM owners WHERE name LIKE ?", (like,)).fetchall()
        return [cls(id=r["id"], name=r["name"], contact=r["contact"]) for r in rows]5