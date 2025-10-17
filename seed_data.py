# seed_data.py
"""
Seed Data Script for PetCare — Pet Health & Appointment Tracker
Populates DB with:
- 3 owners
- each owner has 2–3 pets
- each pet has appointments and medical records
Run: python seed_data.py
"""

from datetime import date, timedelta
from lib.database import create_tables
from lib.models.owner import Owner
from lib.models.pet import Pet
from lib.models.appointment import Appointment
from lib.models.medical_history import MedicalHistory
def seed():
    # Ensure tables exist
    create_tables()

