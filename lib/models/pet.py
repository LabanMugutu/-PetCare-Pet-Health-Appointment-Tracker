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