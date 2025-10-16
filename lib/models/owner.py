"""
Owner model: represents the owners table and exposes CRUD operations.
This class behaves as a simple ORM mapping rows <-> Python objects.
"""

from typing import Optional, List
import sqlite3
from lib.database import CURSOR, CONN
