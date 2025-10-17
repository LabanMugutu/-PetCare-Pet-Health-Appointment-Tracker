"""
Appointment model: maps to appointments table and provides queries
for upcoming/past appointments per pet and for owners.
"""

from typing import Optional, List, Tuple
from lib.database import CURSOR, CONN
class Appointment:
    def __init__(self, pet_id: int, date: str, reason: str, vet_name: Optional[str] = None, notes: Optional[str] = None, id: Optional[int] = None):
        """
        Appointment fields:
          - pet_id: foreign key to pets.id
          - date: ISO date string 'YYYY-MM-DD'
          - reason, vet_name, notes: additional details
        """
        self.id = id
        self.pet_id = pet_id
        self.date = date
        self.reason = reason
        self.vet_name = vet_name
        self.notes = notes
     def save(self) -> "Appointment":
        """Insert appointment into DB and set id."""
        if not self.pet_id or not self.date:
            raise ValueError("Appointment requires pet_id and date.")
        CURSOR.execute(
            "INSERT INTO appointments (pet_id, date, reason, vet_name, notes) VALUES (?, ?, ?, ?, ?)",
            (self.pet_id, self.date, self.reason, self.vet_name, self.notes)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self
    def update(self, date: Optional[str] = None, reason: Optional[str] = None,
               vet_name: Optional[str] = None, notes: Optional[str] = None) -> "Appointment":
        """Update appointment fields."""
        if date: self.date = date
        if reason: self.reason = reason
        if vet_name is not None: self.vet_name = vet_name
        if notes is not None: self.notes = notes
        if not self.id:
            raise ValueError("Appointment must have an id to update.")
        CURSOR.execute(
            "UPDATE appointments SET pet_id = ?, date = ?, reason = ?, vet_name = ?, notes = ? WHERE id = ?",
            (self.pet_id, self.date, self.reason, self.vet_name, self.notes, self.id)
        )
        CONN.commit()
        return self
    def delete(self) -> None:
        """Delete this appointment."""
        if not self.id:
            raise ValueError("Appointment must have an id to delete.")
        CURSOR.execute("DELETE FROM appointments WHERE id = ?", (self.id,))
        CONN.commit()
    @classmethod
    def find_by_id(cls, appt_id: int) -> Optional["Appointment"]:
        """Return Appointment by id."""
        row = CURSOR.execute("SELECT id, pet_id, date, reason, vet_name, notes FROM appointments WHERE id = ?", (appt_id,)).fetchone()
        if row:
            return cls(id=row["id"], pet_id=row["pet_id"], date=row["date"], reason=row["reason"], vet_name=row["vet_name"], notes=row["notes"])
        return None