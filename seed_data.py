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
# Ensure tables exist
    create_tables()

    # Owner 1
    alice = Owner(name="Alice Johnson", contact="0710000001").save()
    a1_p1 = Pet(name="Buddy", species="Dog", breed="Beagle", age=4, owner_id=alice.id).save()
    a1_p2 = Pet(name="Mittens", species="Cat", breed="Domestic Shorthair", age=2, owner_id=alice.id).save()

    Appointment(pet_id=a1_p1.id, date=(date.today() + timedelta(days=7)).isoformat(),
                reason="Vaccination", vet_name="Dr. Kilonzo", notes="Rabies booster").save()
    Appointment(pet_id=a1_p1.id, date=(date.today() - timedelta(days=60)).isoformat(),
                reason="Checkup", vet_name="Dr. Kilonzo", notes="Weight OK").save()
    MedicalHistory(pet_id=a1_p1.id, record_type="vaccination", name="Rabies",
                   date=(date.today() - timedelta(days=365)).isoformat(), notes="Initial dose").save()
    MedicalHistory(pet_id=a1_p2.id, record_type="treatment", name="Flea treatment",
                   date=(date.today() - timedelta(days=30)).isoformat(), notes="Topical").save()
    Appointment(pet_id=a1_p2.id, date=(date.today() + timedelta(days=14)).isoformat(),
                reason="Spay follow-up", vet_name="Dr. Auma", notes="Stitches check").save()

    # Owner 2


