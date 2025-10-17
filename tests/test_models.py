"""
Basic pytest tests for Owner, Pet, Appointment, MedicalHistory models.
These tests validate core CRUD and relation behaviors.
"""
from lib.database import create_tables
from lib.models.owner import Owner
from lib.models.pet import Pet
from lib.models.appointment import Appointment
from lib.models.medical_history import MedicalHistory
from datetime import date, timedelta

def setup_module(module):
    # create tables on the test DB
    create_tables()

def test_owner_pet_crud_and_search():
    # create owner and pets
    o = Owner(name="Alice Example", contact="0700000001").save()
    assert o.id is not None

    p1 = Pet(name="Buddy", species="Dog", breed="Beagle", age=3, owner_id=o.id).save()
    p2 = Pet(name="Buddy Jr", species="Dog", breed="Beagle", age=1, owner_id=o.id).save()

    # search pet by name
    found = Pet.search_by_name("Buddy")
    assert any(p.id == p1.id for p in found)

    # search owner by name
    owners_found = Owner.find_by_name("Alice")
    assert any(x.id == o.id for x in owners_found)

    # cleanup
    p1.delete()
    p2.delete()
    o.delete()

def test_appointments_and_reports():
    o = Owner(name="Report Owner", contact="0700000002").save()
    p = Pet(name="Spot", species="Cat", breed="Siamese", age=2, owner_id=o.id).save()

    today = date.today()
    ap1 = Appointment(pet_id=p.id, date=(today + timedelta(days=2)).isoformat(), reason="Vaccine", vet_name="Dr X").save()
    ap2 = Appointment(pet_id=p.id, date=(today - timedelta(days=3)).isoformat(), reason="Check", vet_name="Dr Y").save()

    upcoming = Appointment.upcoming_for_pet(p.id, today.isoformat())
    past = Appointment.past_for_pet(p.id, today.isoformat())

    assert any(a.id == ap1.id for a in upcoming)
    assert any(a.id == ap2.id for a in past)

    nxt = Appointment.next_appointment_for_pet(p.id, today.isoformat())
    assert nxt is not None and nxt[0] == ap1.id

    rows = Appointment.upcoming_for_owner(o.id)
    assert any(r[0] == ap1.id for r in rows)

    # cleanup
    ap1.delete()
    ap2.delete()
    p.delete()
    o.delete()

def test_medical_history():
    o = Owner(name="Health Owner", contact="0700000003").save()
    p = Pet(name="Rex", species="Dog", breed="Mixed", age=4, owner_id=o.id).save()
    mh1 = MedicalHistory(pet_id=p.id, record_type="vaccination", name="Rabies", date=date.today().isoformat(), notes="First dose").save()
    mh2 = MedicalHistory(pet_id=p.id, record_type="treatment", name="Deworming", date=date.today().isoformat(), notes="Oral").save()

    recs = MedicalHistory.find_by_pet(p.id)
    assert any(r.id == mh1.id for r in recs)
    assert any(r.id == mh2.id for r in recs)

    # cleanup
    mh1.delete()
    mh2.delete()
    p.delete()
    o.delete()