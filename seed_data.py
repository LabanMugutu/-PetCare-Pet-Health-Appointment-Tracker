# seed_data.py
# ----------------------------------------
# Populates the database with sample data for testing.
# ----------------------------------------

from lib.database import create_tables
from lib.models.owner import Owner
from lib.models.pet import Pet
from lib.models.appointment import Appointment
from lib.models.medical_record import MedicalRecord

def seed():
    create_tables()

    # Create sample owners
    alice = Owner("Alice Johnson", "0710000001").save()
    brian = Owner("Brian Kim", "0722000002").save()
    cathy = Owner("Cathy Wanjiku", "0733000003").save()

    # Pets for Alice
    p1 = Pet("Bella", 3, "Dog", "Beagle", alice.id).save()
    p2 = Pet("Milo", 1, "Cat", "Siamese", alice.id).save()

    # Pets for Brian
    p3 = Pet("Rocky", 5, "Dog", "German Shepherd", brian.id).save()
    p4 = Pet("Coco", 2, "Parrot", "African Grey", brian.id).save()

    # Pets for Cathy
    p5 = Pet("Simba", 4, "Cat", "Maine Coon", cathy.id).save()
    p6 = Pet("Luna", 2, "Dog", "Poodle", cathy.id).save()

    # Appointments and records
    Appointment(p1.id, "2025-10-20", "Checkup", "Dr. Muli", "Healthy").save()
    Appointment(p3.id, "2025-10-25", "Vaccination", "Dr. Amina", "Next in 1 year").save()
    Appointment(p5.id, "2025-11-05", "Dental Cleaning", "Dr. Otieno", "Minor tartar").save()

    MedicalRecord(p1.id, "2025-01-10", "Rabies Vaccine", "No issues").save()
    MedicalRecord(p3.id, "2025-03-12", "Deworming", "Good recovery").save()
    MedicalRecord(p6.id, "2025-04-22", "Ear Infection Treatment", "Cleared").save()

    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed()
