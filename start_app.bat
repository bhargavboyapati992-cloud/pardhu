@echo off
echo Starting Smart Plant Watering App...

echo Starting Backend API...
start cmd /k "cd smart-plant-watering\backend && .\venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000"

echo Starting Frontend Dashboard...
start cmd /k "cd smart-plant-watering\frontend && npm run dev"

echo Starting IoT Simulator...
start cmd /k "cd smart-plant-watering\iot_simulation && ..\backend\venv\Scripts\python sensor.py"

echo All services started! Check the opened terminal windows.
pause
