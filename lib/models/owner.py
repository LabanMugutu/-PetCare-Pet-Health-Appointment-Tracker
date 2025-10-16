"""
Owner model: represents the owners table and exposes CRUD operations.
This class behaves as a simple ORM mapping rows <-> Python objects.
"""

from typing import Optional, List
import sqlite3
from lib.database import CURSOR, CONN

class Owner:
    def __init__(self, name: str, contact: str, id: Optional[int] = None):