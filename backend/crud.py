from sqlalchemy.orm import Session
from datetime import datetime
import models as models
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone_number: str
    email: str
    password: str

class SensorDataCreate(BaseModel):
    soil_moisture: float
    temperature: float
    motor_status: bool

def create_user(db: Session, user: UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session):
    return db.query(models.User).all()

def add_sensor_data(db: Session, data: SensorDataCreate):
    db_data = models.SensorData(**data.dict(), timestamp=datetime.utcnow())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_latest_sensor_data(db: Session, limit: int = 100):
    return db.query(models.SensorData).order_by(models.SensorData.timestamp.desc()).limit(limit).all()

def add_log(db: Session, action: str, reason: str):
    db_log = models.Log(action=action, reason=reason, time=datetime.utcnow())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session, limit: int = 20):
    return db.query(models.Log).order_by(models.Log.time.desc()).limit(limit).all()
