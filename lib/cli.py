"""
Command-based CLI loop.
Users type commands like:
  add_owner "Alice Johnson" "0710000001"
  list_owners
  add_pet "Buddy" "Dog" "Beagle" 4 1
  schedule_appointment 1 2025-11-10 "Vaccination" "Dr. Kilonzo" "Notes"
Type `help` to view commands, `exit` to quit.
"""

import shlex  # helps parse quoted arguments
from datetime import date
from lib.models.owner import Owner
from lib.models.pet import Pet
from lib.models.appointment import Appointment
from lib.models.medical_history import MedicalHistory
def print_help():
    """Print available commands and usage examples."""
    print("""
Available commands (examples):
  help
  exit
  add_owner "Name" "Contact"
  list_owners
  find_owner_by_name "query"

  add_pet "Name" "Species" "Breed" Age OwnerID
  list_pets
  view_pet PetID
  find_pet_by_name "query"
  list_pets_by_owner OwnerID
  update_pet PetID "Name" "Species" "Breed" Age OwnerID
  delete_pet PetID

  schedule_appointment PetID YYYY-MM-DD "Reason" "Vet Name" "Notes"
  list_appointments
  list_appointments_for_pet PetID
  update_appointment ApptID YYYY-MM-DD "Reason" "Vet" "Notes"
  delete_appointment ApptID

  log_medical PetID "vaccination|treatment" "Name" YYYY-MM-DD "Notes"
  list_medical_for_pet PetID
  delete_medical RecordID

  report_next_appointments
  report_pets_per_owner
  report_owner_appointments OwnerID
""")


def parse_args(line: str):
    """
    Use shlex.split to support quoted strings.
    Returns list of tokens.
    """
    try:
        return shlex.split(line)
    except ValueError:
        # fallback: naive split
        return line.split()def command_loop():
    """
    Main loop that reads user input and executes commands.
    It's intentionally simple and synchronous for clarity and grading.
    """
    print("Welcome to PetCare (command-based). Type `help` for commands.")
    while True:
        try:
            line = input("petcare> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting PetCare.")
            break

        if not line:
            continue

        parts = parse_args(line)
        cmd = parts[0].lower()
        args = parts[1:]

        # Exit & help
        if cmd in ("exit", "quit"):
            print("Goodbye!")
            break
        if cmd == "help":
            print_help()
            continue

        # ------- Owner commands -------
        if cmd == "add_owner":
            if len(args) < 2:
                print("Usage: add_owner \"Name\" \"Contact\"")
                continue
            name, contact = args[0], args[1]
            try:
                o = Owner(name, contact).save()
                print(f"Added owner id={o.id}")
            except Exception as e:
                print("Error:", e)
            continue

        if cmd == "list_owners":
            owners = Owner.all()
            for o in owners:
                print(f"{o.id}: {o.name} ({o.contact})")
            continue

        if cmd == "find_owner_by_name":
            if not args:
                print("Usage: find_owner_by_name \"query\"")
                continue
            results = Owner.find_by_name(args[0])
            for r in results:
                print(f"{r.id}: {r.name} ({r.contact})")
            continue

        # ------- Pet commands -------
        if cmd == "add_pet":
            # expects: "Name" "Species" "Breed" Age OwnerID
            if len(args) < 5:
                print('Usage: add_pet "Name" "Species" "Breed" Age OwnerID')
                continue
            name, species, breed = args[0], args[1], args[2]
            age = int(args[3]) if args[3].isdigit() else None
            owner_id = int(args[4]) if args[4].isdigit() else None
            try:
                p = Pet(name, species, breed, age, owner_id).save()
                print(f"Added pet id={p.id}")
            except Exception as e:
                print("Error:", e)
            continue

        if cmd == "list_pets":
            pets = Pet.all()
            for p in pets:
                print(f"{p.id}: {p.name} ({p.species}) Breed:{p.breed} Age:{p.age} OwnerID:{p.owner_id}")
            continue

        if cmd == "view_pet":
            if not args or not args[0].isdigit():
                print("Usage: view_pet PetID")
                continue
            pet = Pet.find_by_id(int(args[0]))
            if not pet:
                print("Pet not found.")
                continue
            print(f"{pet.id}: {pet.name} ({pet.species}) Breed:{pet.breed} Age:{pet.age} OwnerID:{pet.owner_id}")
            today = date.today().isoformat()
            print("Upcoming appointments:")
            for a in Appointment.upcoming_for_pet(pet.id, today):
                print(f"  {a.id}: {a.date} - {a.reason} (Vet: {a.vet_name}) Notes: {a.notes}")
            print("Past appointments:")
            for a in Appointment.past_for_pet(pet.id, today):
                print(f"  {a.id}: {a.date} - {a.reason} (Vet: {a.vet_name}) Notes: {a.notes}")
            print("Medical history:")
            for r in MedicalHistory.find_by_pet(pet.id):
                print(f"  {r.id}: [{r.record_type}] {r.name} on {r.date} Notes: {r.notes}")
            continue

        if cmd == "find_pet_by_name":
            if not args:
                print('Usage: find_pet_by_name "query"')
                continue
            results = Pet.search_by_name(args[0])
            for p in results:
                print(f"{p.id}: {p.name} ({p.species}) OwnerID:{p.owner_id}")
            continue

        if cmd == "list_pets_by_owner":
            if not args or not args[0].isdigit():
                print("Usage: list_pets_by_owner OwnerID")
                continue
            pets = Pet.find_by_owner(int(args[0]))
            for p in pets:
                print(f"{p.id}: {p.name} ({p.species})")
            continue

        if cmd == "update_pet":
            # update_pet PetID "Name" "Species" "Breed" Age OwnerID
            if len(args) < 6 or not args[0].isdigit():
                print('Usage: update_pet PetID "Name" "Species" "Breed" Age OwnerID')
                continue
            pet_id = int(args[0])
            pet = Pet.find_by_id(pet_id)
            if not pet:
                print("Pet not found.")
                continue
            name, species, breed = args[1], args[2], args[3]
            age = int(args[4]) if args[4].isdigit() else None
            owner_id = int(args[5]) if args[5].isdigit() else None
            pet.update(name=name, species=species, breed=breed, age=age, owner_id=owner_id)
            print("Pet updated.")
            continue

        if cmd == "delete_pet":
            if not args or not args[0].isdigit():
                print("Usage: delete_pet PetID")
                continue
            pet = Pet.find_by_id(int(args[0]))
            if not pet:
                print("Not found.")
                continue
            # check appointments/medical history first
            if Appointment.find_by_pet(pet.id) or MedicalHistory.find_by_pet(pet.id):
                print("Cannot delete pet with appointments or medical records. Remove those first.")
                continue
            pet.delete()
            print("Pet deleted.")
            continue

        # ------- Appointment commands -------
        if cmd == "schedule_appointment":
            # schedule_appointment PetID YYYY-MM-DD "Reason" "Vet" "Notes"
            if len(args) < 5 or not args[0].isdigit():
                print('Usage: schedule_appointment PetID YYYY-MM-DD "Reason" "Vet Name" "Notes"')
                continue
            pet_id = int(args[0])
            date_str = args[1]
            reason = args[2]
            vet = args[3]
            notes = args[4]
            try:
                a = Appointment(pet_id, date_str, reason, vet, notes).save()
                print(f"Scheduled appointment id={a.id}")
            except Exception as e:
                print("Error:", e)
            continue

        if cmd == "list_appointments":
            appts = Appointment.find_by_pet  # not used directly; show all by querying DB rows
            rows = Appointment.find_by_pet  # placeholder
            # show all appointments by reading Appointment.all via raw SQL pattern
            rows = []
            # use CURSOR to fetch all appointments if needed
            from lib.database import CURSOR
            raw = CURSOR.execute("SELECT id, pet_id, date, reason, vet_name, notes FROM appointments ORDER BY date DESC").fetchall()
            for r in raw:
                print(f"{r['id']}: Pet {r['pet_id']} on {r['date']} - {r['reason']} (Vet: {r['vet_name']}) Notes:{r['notes']}")
            continue

        if cmd == "list_appointments_for_pet":
            if not args or not args[0].isdigit():
                print("Usage: list_appointments_for_pet PetID")
                continue
            for a in Appointment.find_by_pet(int(args[0])):
                print(f"{a.id}: {a.date} - {a.reason} (Vet: {a.vet_name}) Notes: {a.notes}")
            continue

        if cmd == "update_appointment":
            # update_appointment ApptID YYYY-MM-DD "Reason" "Vet" "Notes"
            if len(args) < 5 or not args[0].isdigit():
                print('Usage: update_appointment ApptID YYYY-MM-DD "Reason" "Vet" "Notes"')
                continue
            appt = Appointment.find_by_id(int(args[0]))
            if not appt:
                print("Appointment not found.")
                continue
            date_str = args[1]
            reason = args[2]
            vet = args[3]
            notes = args[4]
            appt.update(date=date_str, reason=reason, vet_name=vet, notes=notes)
            print("Appointment updated.")
            continue

        if cmd == "delete_appointment":
            if not args or not args[0].isdigit():
                print("Usage: delete_appointment ApptID")
                continue
            appt = Appointment.find_by_id(int(args[0]))
            if not appt:
                print("Not found.")
                continue
            appt.delete()
            print("Appointment deleted.")
            continue

        # ------- Medical history commands -------
        if cmd == "log_medical":
            # log_medical PetID "vaccination|treatment" "Name" YYYY-MM-DD "Notes"
            if len(args) < 5 or not args[0].isdigit():
                print('Usage: log_medical PetID "vaccination|treatment" "Name" YYYY-MM-DD "Notes"')
                continue
            pet_id = int(args[0])
            rtype = args[1]
            name = args[2]
            date_str = args[3]
            notes = args[4]
            try:
                mh = MedicalHistory(pet_id, rtype, name, date_str, notes).save()
                print(f"Medical record added id={mh.id}")
            except Exception as e:
                print("Error:", e)
            continue

        if cmd == "list_medical_for_pet":
            if not args or not args[0].isdigit():
                print("Usage: list_medical_for_pet PetID")
                continue
            for r in MedicalHistory.find_by_pet(int(args[0])):
                print(f"{r.id}: [{r.record_type}] {r.name} on {r.date} Notes: {r.notes}")
            continue

        if cmd == "delete_medical":
            if not args or not args[0].isdigit():
                print("Usage: delete_medical RecordID")
                continue
            from lib.database import CURSOR
            row = CURSOR.execute("SELECT id, pet_id, record_type, name, date, notes FROM medical_history WHERE id = ?", (int(args[0]),)).fetchone()
            if not row:
                print("Not found.")
                continue
            mh = MedicalHistory(pet_id=row["pet_id"], record_type=row["record_type"], name=row["name"], date=row["date"], notes=row["notes"], id=row["id"])
            mh.delete()
            print("Deleted.")
            continue

        # ------- Reports -------
        if cmd == "report_next_appointments":
            pets = Pet.all()
            today = date.today().isoformat()
            for p in pets:
                nxt = Appointment.next_appointment_for_pet(p.id, today)
                if nxt:
                    print(f"Pet {p.id} - {p.name}: next appointment {nxt[1]} (id: {nxt[0]})")
                else:
                    print(f"Pet {p.id} - {p.name}: no upcoming appointments")
            continue

        if cmd == "report_pets_per_owner":
            owners = Owner.all()
            for o in owners:
                pets = Pet.find_by_owner(o.id)
                print(f"Owner {o.id} - {o.name}: {len(pets)} pets")
            continue

        if cmd == "report_owner_appointments":
            if not args or not args[0].isdigit():
                print("Usage: report_owner_appointments OwnerID")
                continue
            rows = Appointment.upcoming_for_owner(int(args[0]))
            if not rows:
                print("No upcoming appointments for that owner.")
            for appt_id, pet_name, dt in rows:
                print(f"{appt_id}: {pet_name} on {dt}")
            continue

        # Unknown command
        print("Unknown command. Type `help` for a list of commands.")
