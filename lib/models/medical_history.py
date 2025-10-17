"""
MedicalHistory model: stores vaccinations and treatments for pets.
"""

from typing import Optional, List
from lib.database import CURSOR, CONN
class MedicalHistory:
    def __init__(self, pet_id: int, record_type: str, name: str, date: str, notes: Optional[str] = None, id: Optional[int] = None):
        """
        Fields:
          - pet_id: foreign key to pets.id
          - record_type: 'vaccination' or 'treatment'
          - name: vaccine or treatment name
          - date: ISO date string
          - notes: optional details
        """
        self.id = id
        self.pet_id = pet_id
        self.record_type = record_type
        self.name = name
        self.date = date
        self.notes = notes

    def save(self) -> "MedicalHistory":
        """Insert a new medical record."""
        if not self.pet_id or not self.record_type or not self.date:
            raise ValueError("pet_id, record_type and date are required.")
        CURSOR.execute(
            "INSERT INTO medical_history (pet_id, record_type, name, date, notes) VALUES (?, ?, ?, ?, ?)",
            (self.pet_id, self.record_type, self.name, self.date, self.notes)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

