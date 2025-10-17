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

    @classmethod
    def find_by_pet(cls, pet_id: int) -> List["Appointment"]:
        """Return all appointments for a pet (ordered DESC by date)."""
        rows = CURSOR.execute("SELECT id, pet_id, date, reason, vet_name, notes FROM appointments WHERE pet_id = ? ORDER BY date DESC", (pet_id,)).fetchall()
        return [cls(id=r["id"], pet_id=r["pet_id"], date=r["date"], reason=r["reason"], vet_name=r["vet_name"], notes=r["notes"]) for r in rows]

     @classmethod
    def upcoming_for_pet(cls, pet_id: int, current_date: str) -> List["Appointment"]:
        """Return appointments for a pet with date >= current_date ordered asc."""
        rows = CURSOR.execute("SELECT id, pet_id, date, reason, vet_name, notes FROM appointments WHERE pet_id = ? AND date >= ? ORDER BY date ASC", (pet_id, current_date)).fetchall()
        return [cls(id=r["id"], pet_id=r["pet_id"], date=r["date"], reason=r["reason"], vet_name=r["vet_name"], notes=r["notes"]) for r in rows]

    @classmethod
    def past_for_pet(cls, pet_id: int, current_date: str) -> List["Appointment"]:
        """Return appointments for a pet with date < current_date ordered desc."""
        rows = CURSOR.execute("SELECT id, pet_id, date, reason, vet_name, notes FROM appointments WHERE pet_id = ? AND date < ? ORDER BY date DESC", (pet_id, current_date)).fetchall()
        return [cls(id=r["id"], pet_id=r["pet_id"], date=r["date"], reason=r["reason"], vet_name=r["vet_name"], notes=r["notes"]) for r in rows]

    @classmethod
    def next_appointment_for_pet(cls, pet_id: int, current_date: str) -> Optional[Tuple[int, str]]:
        """Return tuple (id, date) for the next appointment for the pet, or None."""
        row = CURSOR.execute("SELECT id, date FROM appointments WHERE pet_id = ? AND date >= ? ORDER BY date ASC LIMIT 1", (pet_id, current_date)).fetchone()
        if row:
            return (row["id"], row["date"])
        return None
    
    @classmethod
    def upcoming_for_owner(cls, owner_id: int) -> List[Tuple[int, str, str]]:
        """
        Return list of tuples (appointment_id, pet_name, date) for an owner's appointments.
        Demonstrates JOINs across appointments and pets.
        """
        rows = CURSOR.execute("""
            SELECT a.id as appt_id, p.name as pet_name, a.date as date
            FROM appointments a
            JOIN pets p ON a.pet_id = p.id
            WHERE p.owner_id = ?
            ORDER BY a.date ASC
        """, (owner_id,)).fetchall()
        return [(r["appt_id"], r["pet_name"], r["date"]) for r in rows]

