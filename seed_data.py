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
    brian = Owner(name="Brian Kim", contact="0710000002").save()
    b1_p1 = Pet(name="Shadow", species="Dog", breed="German Shepherd", age=5, owner_id=brian.id).save()
    b1_p2 = Pet(name="Goldie", species="Fish", breed="Goldfish", age=1, owner_id=brian.id).save()
    b1_p3 = Pet(name="Coco", species="Bird", breed="Parrot", age=3, owner_id=brian.id).save()
    Appointment(pet_id=b1_p1.id, date=(date.today() + timedelta(days=3)).isoformat(),
                reason="Dental cleaning", vet_name="Dr. Mwende", notes="Anesthesia planned").save()
    MedicalHistory(pet_id=b1_p1.id, record_type="treatment", name="Dental cleaning",
                   date=(date.today() - timedelta(days=400)).isoformat(), notes="Routine").save()
    Appointment(pet_id=b1_p3.id, date=(date.today() + timedelta(days=21)).isoformat(),
                reason="Wing trim", vet_name="Dr. Auma", notes="Check behavior").save()
    MedicalHistory(pet_id=b1_p3.id, record_type="vaccination", name="Polyomavirus",
                   date=(date.today() - timedelta(days=200)).isoformat(), notes="Administered at clinic").save()

    # Owner 3
    clara = Owner(name="Clara Otieno", contact="0710000003").save()
    c1_p1 = Pet(name="Rex", species="Dog", breed="Mixed", age=6, owner_id=clara.id).save()
    c1_p2 = Pet(name="Whisk", species="Cat", breed="Siamese", age=1, owner_id=clara.id).save()
    Appointment(pet_id=c1_p1.id, date=(date.today() + timedelta(days=10)).isoformat(),
                reason="Annual checkup", vet_name="Dr. Kilonzo", notes="Bring previous records").save()
    MedicalHistory(pet_id=c1_p1.id, record_type="vaccination", name="Distemper",
                   date=(date.today() - timedelta(days=500)).isoformat(), notes="Full course").save()
    Appointment(pet_id=c1_p2.id, date=(date.today() - timedelta(days=2)).isoformat(),
                reason="Injury check", vet_name="Dr. Mwende", notes="Front paw scratch").save()
    MedicalHistory(pet_id=c1_p2.id, record_type="treatment", name="Stitch",
                   date=(date.today() - timedelta(days=2)).isoformat(), notes="Local anesthetic").save()

    # Print summary
    print("=== Seed Complete ===")
    print(f"Owners: {', '.join([alice.name, brian.name, clara.name])}")
    print("Pets per owner:")
    for owner in (alice, brian, clara):
        pets = Pet.find_by_owner(owner.id)
        pet_list = ", ".join([f"{p.name}({p.species})" for p in pets])
        print(f" - {owner.name}: {pet_list}")

if __name__ == "__main__":
    seed()


