# lib/models/medical_record.py
# ----------------------------------------
# Represents the "medical_records" table for pet health logs.
# ----------------------------------------

from lib.database import CURSOR, CONN

class MedicalRecord:
    def __init__(self, pet_id, record_date, treatment, notes, id=None):
        self.id = id
        self.pet_id = pet_id
        self.record_date = record_date
        self.treatment = treatment
        self.notes = notes

    def save(self):
        """Insert a new medical record."""
        CURSOR.execute(
            "INSERT INTO medical_records (pet_id, record_date, treatment, notes) VALUES (?, ?, ?, ?)",
            (self.pet_id, self.record_date, self.treatment, self.notes)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

    @classmethod
    def find_by_pet(cls, pet_id):
        """Get all medical records for a pet."""
        rows = CURSOR.execute("SELECT * FROM medical_records WHERE pet_id=?", (pet_id,)).fetchall()
        return [cls(id=row[0], pet_id=row[1], record_date=row[2], treatment=row[3], notes=row[4]) for row in rows]
# lib/models/medical_record.py
# ----------------------------------------
# Represents the "medical_records" table for pet health logs.
# ----------------------------------------

from lib.database import CURSOR, CONN

class MedicalRecord:
    def __init__(self, pet_id, record_date, treatment, notes, id=None):
        self.id = id
        self.pet_id = pet_id
        self.record_date = record_date
        self.treatment = treatment
        self.notes = notes

    def save(self):
        """Insert a new medical record."""
        CURSOR.execute(
            "INSERT INTO medical_records (pet_id, record_date, treatment, notes) VALUES (?, ?, ?, ?)",
            (self.pet_id, self.record_date, self.treatment, self.notes)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

    @classmethod
    def find_by_pet(cls, pet_id):
        """Get all medical records for a pet."""
        rows = CURSOR.execute("SELECT * FROM medical_records WHERE pet_id=?", (pet_id,)).fetchall()
        return [cls(id=row[0], pet_id=row[1], record_date=row[2], treatment=row[3], notes=row[4]) for row in rows]
