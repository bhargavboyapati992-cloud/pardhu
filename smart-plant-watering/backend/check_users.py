import sys
import os

# Add the backend dir to sys.path so we can import from the database
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
import crud

db = SessionLocal()
users = crud.get_users(db)
for u in users:
    print(f"User: {u.name}, Email: {u.email}, Phone: {u.phone_number}")

db.close()
