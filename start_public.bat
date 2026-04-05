@echo off
echo Starting Smart Plant Watering System (Unified Service)...

echo 1. Starting Backend & UI Server...
start cmd /k "cd smart-plant-watering\backend && .\venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000"

echo 2. Starting IoT Simulator...
start cmd /k "cd smart-plant-watering\iot_simulation && ..\backend\venv\Scripts\python sensor.py"

echo 3. Starting Public Internet Tunnel...
echo.
echo =======================================================
echo YOUR APP WILL BE AVAILABLE AT THE LINK GENERATED BELOW:
echo =======================================================
cd smart-plant-watering && npx localtunnel --port 8000 --subdomain pardhu-plant-system
