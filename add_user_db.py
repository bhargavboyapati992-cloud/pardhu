import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
import models

db = SessionLocal()

# Add user directly to SQLAlchemy to avoid pydantic issues if any
new_user = models.User(
    name="pardhu",
    email="peddinenipardhuavinash@gmail.com",
    phone_number="+917793929357"
)

try:
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"User created successfully: {new_user.name} ({new_user.phone_number})")
except Exception as e:
    print(f"Failed to create user. Error: {e}")
    db.rollback()

db.close()
