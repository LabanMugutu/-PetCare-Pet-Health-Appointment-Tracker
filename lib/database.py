"""
Database module.
Provides a shared sqlite3 connection and a create_tables() function
that creates the schema used by the models.
"""

import os
import sqlite3