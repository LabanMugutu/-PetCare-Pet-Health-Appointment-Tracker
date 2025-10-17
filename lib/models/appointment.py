"""
Appointment model: maps to appointments table and provides queries
for upcoming/past appointments per pet and for owners.
"""

from typing import Optional, List, Tuple
from lib.database import CURSOR, CONN