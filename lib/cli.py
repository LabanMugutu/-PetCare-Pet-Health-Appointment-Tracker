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
        return line.split()
