@echo off
echo Starting Smart Plant Watering System (Unified Service)...

echo 1. Starting Backend ^& UI Server...
start cmd /k "cd /d %~dp0smart-plant-watering\backend && .\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo 2. Starting IoT Simulator...
start cmd /k "cd /d %~dp0smart-plant-watering\iot_simulation && %~dp0smart-plant-watering\backend\venv\Scripts\python.exe sensor.py"

echo 3. Starting Public Internet Tunnel...
echo.
echo =======================================================
echo YOUR APP WILL BE AVAILABLE AT THE LINK GENERATED BELOW:
echo =======================================================
cd /d %~dp0smart-plant-watering && npx localtunnel --port 8000 --subdomain pardhu-plant-system
