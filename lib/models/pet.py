# lib/models/pet.py
# ----------------------------------------
# Represents the "pets" table and handles pet CRUD operations.
# ----------------------------------------

from lib.database import CURSOR, CONN

class Pet:
    def __init__(self, name, age, species, breed, owner_id, id=None):
        self.id = id
        self.name = name
        self.age = age
        self.species = species
        self.breed = breed
        self.owner_id = owner_id

    def save(self):
        """Insert a new pet into the database."""
        CURSOR.execute(
            "INSERT INTO pets (name, age, species, breed, owner_id) VALUES (?, ?, ?, ?, ?)",
            (self.name, self.age, self.species, self.breed, self.owner_id)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

    @classmethod
    def get_all(cls):
        """Retrieve all pets."""
        rows = CURSOR.execute("SELECT * FROM pets").fetchall()
        return [cls(id=row[0], name=row[1], age=row[2], species=row[3], breed=row[4], owner_id=row[5]) for row in rows]

    @classmethod
    def find_by_owner(cls, owner_id):
        """Find all pets belonging to a specific owner."""
        rows = CURSOR.execute("SELECT * FROM pets WHERE owner_id=?", (owner_id,)).fetchall()
        return [cls(id=row[0], name=row[1], age=row[2], species=row[3], breed=row[4], owner_id=row[5]) for row in rows]

    def delete(self):
        """Delete a pet record."""
        CURSOR.execute("DELETE FROM pets WHERE id=?", (self.id,))
        CONN.commit()
