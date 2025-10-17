"""
Pet model: represents pets table and provides CRUD + finder methods.
"""

from typing import Optional, List
from lib.database import CURSOR, CONN

class Pet:
     def __init__(self, name: str, species: str, breed: Optional[str], age: Optional[int],
                 owner_id: Optional[int], id: Optional[int] = None):
        """
        Pet fields:
          - id: primary key
          - name, species: required
          - breed, age: optional
          - owner_id: foreign key to owners.id (may be None)
        """
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.owner_id = owner_id
    def save(self) -> "Pet":
        """Insert a new pet record and set self.id."""
        if not self.name or not self.species:
            raise ValueError("Pet name and species are required.")
        CURSOR.execute(
            "INSERT INTO pets (name, species, breed, age, owner_id) VALUES (?, ?, ?, ?, ?)",
            (self.name, self.species, self.breed, self.age, self.owner_id)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self
    def update(self, name: Optional[str] = None, species: Optional[str] = None,
               breed: Optional[str] = None, age: Optional[int] = None, owner_id: Optional[int] = None) -> "Pet":
        """Update pet fields; only non-None args are applied."""
        if name: self.name = name
        if species: self.species = species
        if breed is not None: self.breed = breed
        if age is not None: self.age = age
        if owner_id is not None: self.owner_id = owner_id
        if not self.id:
            raise ValueError("Pet must have an id to update.")
        CURSOR.execute(
            "UPDATE pets SET name = ?, species = ?, breed = ?, age = ?, owner_id = ? WHERE id = ?",
            (self.name, self.species, self.breed, self.age, self.owner_id, self.id)
        )
        CONN.commit()
        return self
    def delete(self) -> None:
        """Delete this pet. Application logic should handle related records first."""
        if not self.id:
            raise ValueError("Pet must have an id to delete.")
        CURSOR.execute("DELETE FROM pets WHERE id = ?", (self.id,))
        CONN.commit()
    @classmethod
    def find_by_id(cls, pet_id: int) -> Optional["Pet"]:
        """Return a Pet by its id or None."""
        row = CURSOR.execute("SELECT id, name, species, breed, age, owner_id FROM pets WHERE id = ?", (pet_id,)).fetchone()
        if row:
            return cls(id=row["id"], name=row["name"], species=row["species"], breed=row["breed"], age=row["age"], owner_id=row["owner_id"])
        return None

    @classmethod
    def all(cls) -> List["Pet"]:
        """Return all pets as Pet instances."""
        rows = CURSOR.execute("SELECT id, name, species, breed, age, owner_id FROM pets").fetchall()
        return [cls(id=r["id"], name=r["name"], species=r["species"], breed=r["breed"], age=r["age"], owner_id=r["owner_id"]) for r in rows]

    @classmethod
    def find_by_owner(cls, owner_id: int) -> List["Pet"]:
        """Return pets associated with a specific owner_id."""
        rows = CURSOR.execute("SELECT id, name, species, breed, age, owner_id FROM pets WHERE owner_id = ?", (owner_id,)).fetchall()
        return [cls(id=r["id"], name=r["name"], species=r["species"], breed=r["breed"], age=r["age"], owner_id=r["owner_id"]) for r in rows]

    @classmethod
    def search_by_name(cls, q: str) -> List["Pet"]:
        """Search pets by partial name match."""
        like = f"%{q}%"
        rows = CURSOR.execute("SELECT id, name, species, breed, age, owner_id FROM pets WHERE name LIKE ?", (like,)).fetchall()
        return [cls(id=r["id"], name=r["name"], species=r["species"], breed=r["breed"], age=r["age"], owner_id=r["owner_id"]) for r in rows]
