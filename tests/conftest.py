import os
import pytest

@pytest.fixture(autouse=True)
def use_test_db(monkeypatch, tmp_path):
    """
    Configure tests to use an isolated temporary database.
    Sets PETCARE_DB env var before modules import the DB connection.
    """
    test_db = str(tmp_path / "test_database.db")
    monkeypatch.setenv("PETCARE_DB", test_db)
    yield
    # tmp_path cleanup handled by pytest