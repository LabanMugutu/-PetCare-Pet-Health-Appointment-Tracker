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
