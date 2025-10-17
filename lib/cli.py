# lib/cli.py
# ----------------------------------------
# The main command-line interface logic.
# Users interact here using text commands.
# ----------------------------------------

from lib.models.owner import Owner
from lib.models.pet import Pet
from lib.models.appointment import Appointment
from lib.models.medical_record import MedicalRecord

def main_menu():
    """Displays the main menu and handles user commands."""
    print("\n Welcome to PetCare — Pet Health & Appointment Tracker ")
    print("Type a command or 'help' to see options.\n")

    while True:
        command = input("Command > ").strip().lower()

        if command == "help":
            print("""
Commands:
  add_owner          → Register a new pet owner
  view_owners        → List all owners
  add_pet            → Add a new pet
  view_pets          → List all pets
  schedule_appt      → Schedule a vet appointment
  view_appts         → View appointments for a pet
  add_record         → Add medical record
  view_records       → View pet medical history
  exit               → Quit the app
""")

        elif command == "add_owner":
            name = input("Owner name: ")
            contact = input("Contact: ")
            Owner(name, contact).save()
            print(" Owner added successfully!")

        elif command == "view_owners":
            owners = Owner.get_all()
            for o in owners:
                print(f"{o.id}. {o.name} - {o.contact}")

        elif command == "add_pet":
            name = input("Pet name: ")
            age = int(input("Age: "))
            species = input("Species: ")
            breed = input("Breed: ")
            owner_id = int(input("Owner ID: "))
            Pet(name, age, species, breed, owner_id).save()
            print(" Pet added successfully!")

        elif command == "view_pets":
            pets = Pet.get_all()
            for p in pets:
                print(f"{p.id}. {p.name} ({p.species}, {p.breed}) - Owner ID {p.owner_id}")

        elif command == "schedule_appt":
            pet_id = int(input("Pet ID: "))
            date = input("Date (YYYY-MM-DD): ")
            reason = input("Reason: ")
            vet = input("Vet name: ")
            notes = input("Notes: ")
            Appointment(pet_id, date, reason, vet, notes).save()
            print(" Appointment added successfully!")

        elif command == "view_appts":
            pet_id = int(input("Pet ID: "))
            appts = Appointment.find_by_pet(pet_id)
            for a in appts:
                print(f"{a.date} - {a.reason} ({a.vet_name}) | {a.notes}")

        elif command == "add_record":
            pet_id = int(input("Pet ID: "))
            date = input("Date (YYYY-MM-DD): ")
            treatment = input("Treatment: ")
            notes = input("Notes: ")
            MedicalRecord(pet_id, date, treatment, notes).save()
            print(" Record added successfully!")

        elif command == "view_records":
            pet_id = int(input("Pet ID: "))
            records = MedicalRecord.find_by_pet(pet_id)
            for r in records:
                print(f"{r.record_date} - {r.treatment} | {r.notes}")

        elif command == "exit":
            print(" Goodbye!")
            break

        else:
            print(" Unknown command. Type 'help' for options.")

