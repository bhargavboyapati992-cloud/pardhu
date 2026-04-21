from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    soil_moisture = Column(Float)
    temperature = Column(Float)
    motor_status = Column(Boolean)

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String) # 'ON', 'OFF'
    time = Column(DateTime, default=datetime.utcnow)
    reason = Column(String) # 'AI', 'Manual', 'Threshold'
