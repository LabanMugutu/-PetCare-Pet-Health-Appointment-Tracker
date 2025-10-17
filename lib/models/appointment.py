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