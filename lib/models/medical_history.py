class MedicalHistory:
    def __init__(self, pet_id: int, record_type: str, name: str, date: str, notes: Optional[str] = None, id: Optional[int] = None):
        """
        Fields:
          - pet_id: foreign key to pets.id
          - record_type: 'vaccination' or 'treatment'
          - name: vaccine or treatment name
          - date: ISO date string
          - notes: optional details
        """
        self.id = id
        self.pet_id = pet_id
        self.record_type = record_type
        self.name = name
        self.date = date
        self.notes = notes

    def save(self) -> "MedicalHistory":
        """Insert a new medical record."""
        if not self.pet_id or not self.record_type or not self.date:
            raise ValueError("pet_id, record_type and date are required.")
        CURSOR.execute(
            "INSERT INTO medical_history (pet_id, record_type, name, date, notes) VALUES (?, ?, ?, ?, ?)",
            (self.pet_id, self.record_type, self.name, self.date, self.notes)
        )
        CONN.commit()
        self.id = CURSOR.lastrowid
        return self

    def delete(self) -> None:
        """Delete a medical history record."""
        if not self.id:
            raise ValueError("Record must have an id to delete.")
        CURSOR.execute("DELETE FROM medical_history WHERE id = ?", (self.id,))
        CONN.commit()
        
    @classmethod
    def find_by_pet(cls, pet_id: int) -> List["MedicalHistory"]:
        """Return medical records for a pet ordered by date desc."""
        rows = CURSOR.execute("SELECT id, pet_id, record_type, name, date, notes FROM medical_history WHERE pet_id = ? ORDER BY date DESC", (pet_id,)).fetchall()
        return [cls(id=r["id"], pet_id=r["pet_id"], record_type=r["record_type"], name=r["name"], date=r["date"], notes=r["notes"]) for r in rows]

    @classmethod
    def all_for_owner(cls, owner_id: int) -> List["MedicalHistory"]:
        """
        Return medical history across all pets for a specific owner (JOIN).
        """
        rows = CURSOR.execute("""
            SELECT mh.id, mh.pet_id, mh.record_type, mh.name, mh.date, mh.notes
            FROM medical_history mh
            JOIN pets p ON mh.pet_id = p.id
            WHERE p.owner_id = ?
            ORDER BY mh.date DESC
        """, (owner_id,)).fetchall()
        return [cls(id=r["id"], pet_id=r["pet_id"], record_type=r["record_type"], name=r["name"], date=r["date"], notes=r["notes"]) for r in rows]