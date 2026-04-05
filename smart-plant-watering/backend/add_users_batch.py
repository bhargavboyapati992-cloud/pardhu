import sys
import os

from database import SessionLocal
import models

db = SessionLocal()
numbers = ["+917075022609", "+919949805658", "+919110573199"]

added = 0
for i, ph in enumerate(numbers):
    try:
        new_user = models.User(
            name=f"Friend_{i+1}",
            email=f"friend{i+1}_{ph}@example.com",
            phone_number=ph
        )
        db.add(new_user)
        db.commit()
        print(f"Added: Friend_{i+1} ({ph})")
        added += 1
    except Exception as e:
        db.rollback()
        print(f"Error adding {ph}: {e}")

db.close()
print(f"Successfully added {added} numbers to the database.")
