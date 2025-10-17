# lib/models/appointment.py
# ----------------------------------------
# Represents the "appointments" table for pet vet visits.
# ----------------------------------------

from lib.database import CURSOR, CONN

class Appointment:
    def __init__(self, pet_id, date, reason, vet_name, notes, id=None):
        self.id = id
        self.pet_id = pet_id
        self.date = date
        self.reason = reason
        self.vet_name = vet_name
        self.notes = notes

    def save(self):
        """Insert a new appointment record."""
        CURSOR.execute(
            "INSERT INTO appointments (pet_id, date, reason, vet_name, notes) VALUES (?, ?, ?, ?, ?)",
            (self.pet_id, self.date, self.reason, self.vet_name, self.notes)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

    @classmethod
    def find_by_pet(cls, pet_id):
        """Return all appointments for a given pet."""
        rows = CURSOR.execute("SELECT * FROM appointments WHERE pet_id=?", (pet_id,)).fetchall()
        return [cls(id=row[0], pet_id=row[1], date=row[2], reason=row[3], vet_name=row[4], notes=row[5]) for row in rows]




