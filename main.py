"""
Entrypoint for PetCare CLI application.
Creates tables (if needed) then launches the command-based CLI loop.
"""
from lib.database import create_tables
from lib.cli import command_loop
if __name__ == "__main__":
    # Ensure DB schema exists before anything else
    create_tables()
    # Start the CLI
    command_loop()