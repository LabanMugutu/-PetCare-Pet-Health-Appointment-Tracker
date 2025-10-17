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
