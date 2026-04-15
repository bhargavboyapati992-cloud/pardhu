from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models as models
import crud as crud
from database import SessionLocal, engine
from ai_engine import predictor, interpret_and_decide
from notifications import send_sms
from pydantic import BaseModel
import asyncio
import httpx
import random
import datetime
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Plant Watering API")

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        users = crud.get_users(db)
        for u in users:
            send_sms(u.phone_number, "🌱 Smart Plant Watering System Simulator has started!")
        
        # Pre-seed Data so the dashboard graph isn't empty on load
        if len(crud.get_latest_sensor_data(db, limit=1)) == 0:
            base_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
            moist = 900.0
            for i in range(15):
                db_data = models.SensorData(
                    soil_moisture=moist,
                    temperature=28.0 + random.uniform(-1, 1),
                    motor_status=False,
                    timestamp=base_time + datetime.timedelta(minutes=i)
                )
                db.add(db_data)
                moist -= random.uniform(15, 30)
            db.commit()
            
    finally:
        db.close()
    
    # Start the hardware background simulator loop
    asyncio.create_task(hardware_simulator_loop())

async def hardware_simulator_loop():
    current_moisture = 750.0  # start out decently wet
    
    async with httpx.AsyncClient() as client:
        while True:
            await asyncio.sleep(60) # Run every 60 seconds
            
            # Realistic physics emulation
            if MOTOR_STATE["is_on"]:
                current_moisture += random.uniform(100.0, 180.0) # Motor is filling water
            else:
                current_moisture -= random.uniform(20.0, 40.0)   # Soil is naturally drying
            
            # keep within bounds
            current_moisture = max(0.0, min(1023.0, current_moisture))
            current_temp = round(30.0 + random.uniform(-2.0, 2.0), 2)
            
            payload = {
                "soil_moisture": round(current_moisture, 2),
                "temperature": current_temp,
                "motor_status": MOTOR_STATE["is_on"]
            }
            
            try:
                # POST to itself to trigger AI and DB logic naturally!
                # Using 8000 fallback or PORT env when hosted
                port = int(os.environ.get("PORT", 8000))
                await client.post(f"http://127.0.0.1:{port}/api/sensor-data", json=payload)
            except Exception as e:
                print(f"Simulator warning: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MotorCommand(BaseModel):
    command: str # "ON" or "OFF"
    reason: str = "Manual"

# Global state for motor to simulate IoT state
MOTOR_STATE = {"is_on": False, "mode": "Auto"} # modes: Auto, Manual

@app.post("/api/sensor-data")
def receive_sensor_data(data: crud.SensorDataCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Save data
    sensor_data = crud.add_sensor_data(db, data)
    
    # 2. Check AI and thresholds if in Auto Mode
    if MOTOR_STATE["mode"] == "Auto":
        # Fetch last 10 points for AI
        latest_data = crud.get_latest_sensor_data(db, limit=10)
        # Sort chronologically for AI
        latest_data.reverse()
        
        data_points = [{"timestamp": d.timestamp, "moisture": d.soil_moisture} for d in latest_data]
        
        predicted = predictor.train_and_predict(data_points)
        decision = interpret_and_decide(predicted, current_temp=data.temperature, moisture_threshold=600.0, temp_threshold=35.0)

        # Immediate response if AI is still gathering the first few data points
        if decision == "Not enough data":
            if data.soil_moisture < 600.0:
                decision = "TURN_ON"
            else:
                decision = "KEEP_OFF"
        
        if decision == "TURN_ON" and not MOTOR_STATE["is_on"]:
            MOTOR_STATE["is_on"] = True
            crud.add_log(db, "ON", "AI Prediction / Threshold")
            # In a real scenario, we'd send an MQTT / HTTP call to ESP8266 here.
            # We trigger SMS
            users = crud.get_users(db)
            for u in users:
                background_tasks.add_task(send_sms, u.phone_number, "⚠ Soil is predicted to be dry soon or is dry. Motor turned ON automatically.")
                
        elif decision == "KEEP_OFF" and MOTOR_STATE["is_on"]:
            # Turn off immediately when keeping off
            MOTOR_STATE["is_on"] = False
            crud.add_log(db, "OFF", "Threshold Met")
            users = crud.get_users(db)
            for u in users:
                background_tasks.add_task(send_sms, u.phone_number, "✅ Soil is wet enough. Motor turned OFF automatically.")

    return {"status": "success", "recorded_id": sensor_data.id, "motor_state": MOTOR_STATE["is_on"]}

@app.post("/api/motor-control")
def control_motor(cmd: MotorCommand, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if cmd.command not in ["ON", "OFF"]:
        raise HTTPException(status_code=400, detail="Invalid command")
    
    is_on = (cmd.command == "ON")
    MOTOR_STATE["is_on"] = is_on
    crud.add_log(db, cmd.command, cmd.reason)
    
    # Send SMS manually
    users = crud.get_users(db)
    for u in users:
        background_tasks.add_task(send_sms, u.phone_number, f"Motor was manually turned {cmd.command}.")

    return {"status": "success", "motor_state": MOTOR_STATE["is_on"]}

@app.post("/api/toggle-mode")
def toggle_mode(db: Session = Depends(get_db)):
    new_mode = "Manual" if MOTOR_STATE["mode"] == "Auto" else "Auto"
    MOTOR_STATE["mode"] = new_mode
    crud.add_log(db, "MODE_CHANGE", f"Switched to {new_mode}")
    return {"status": "success", "mode": MOTOR_STATE["mode"]}

@app.get("/api/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    latest = crud.get_latest_sensor_data(db, limit=20)
    latest.reverse() # chronological for Graph
    
    logs = crud.get_logs(db, limit=10)
    
    return {
        "motor_state": MOTOR_STATE,
        "history": [{"time": d.timestamp.strftime("%H:%M:%S"), "moisture": d.soil_moisture, "temperature": d.temperature} for d in latest],
        "logs": [{"time": l.time.strftime("%H:%M:%S"), "action": l.action, "reason": l.reason} for l in logs]
    }

@app.post("/api/users")
def create_user(user: crud.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    u = crud.create_user(db=db, user=user)
    return {"id": u.id, "name": u.name}
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.join(os.path.dirname(__file__), "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    app.mount("/vite.svg", StaticFiles(directory=frontend_dist), name="vite_svg")

    @app.get("/{full_path:path}")
    def serve_react_app(full_path: str):
        path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(path):
            return FileResponse(path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
