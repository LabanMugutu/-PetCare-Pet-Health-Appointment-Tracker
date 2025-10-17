# main.py
# ----------------------------------------
# Entry point for running the PetCare CLI.
# ----------------------------------------

from lib.database import create_tables
from lib.cli import main_menu

if __name__ == "__main__":
    create_tables()
    main_menu()

