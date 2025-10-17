# lib/models/owner.py
# ----------------------------------------
# Represents the "owners" table and manages owner CRUD operations.
# ----------------------------------------

from lib.database import CURSOR, CONN

class Owner:
    def __init__(self, name, contact, id=None):
        self.id = id
        self.name = name
        self.contact = contact

    def save(self):
        """Insert a new owner record into the database."""
        CURSOR.execute("INSERT INTO owners (name, contact) VALUES (?, ?)", (self.name, self.contact))
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

    def update(self, name=None, contact=None):
        """Update owner details."""
        if name:
            self.name = name
        if contact:
            self.contact = contact
        CURSOR.execute("UPDATE owners SET name=?, contact=? WHERE id=?", (self.name, self.contact, self.id))
        CONN.commit()

    def delete(self):
        """Delete an owner from the database."""
        CURSOR.execute("DELETE FROM owners WHERE id=?", (self.id,))
        CONN.commit()

    @classmethod
    def get_all(cls):
        """Fetch all owners."""
        rows = CURSOR.execute("SELECT * FROM owners").fetchall()
        return [cls(id=row[0], name=row[1], contact=row[2]) for row in rows]

    @classmethod
    def find_by_id(cls, owner_id):
        """Find an owner by their ID."""
        row = CURSOR.execute("SELECT * FROM owners WHERE id=?", (owner_id,)).fetchone()
        return cls(id=row[0], name=row[1], contact=row[2]) if row else None

