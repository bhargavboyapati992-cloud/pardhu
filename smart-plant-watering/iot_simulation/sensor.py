import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import random
import urllib.request
import json

moisture = 650.0
temperature = 40.0
motor_is_on = False

print("Simulator Started. Emitting data to Backend...")


while True:
    if motor_is_on:
        moisture = min(1023.0, moisture + random.uniform(20, 50))
    else:
        moisture = max(0.0, moisture - random.uniform(5, 15))

    temperature += random.uniform(-0.5, 0.5)

    motor_is_on = moisture < 600

    data = {
        "soil_moisture": round(moisture, 2),
        "temperature": round(temperature, 2),
        "motor_status": motor_is_on
    }

    print(data, flush=True)
    
    # Post data to the backend API so it appears on the dashboard
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/sensor-data", method="POST")
        req.add_header('Content-Type', 'application/json')
        payload = json.dumps({
            "soil_moisture": data["soil_moisture"],
            "temperature": data["temperature"],
            "motor_status": data["motor_status"]
        }).encode('utf-8')
        
        with urllib.request.urlopen(req, data=payload) as response:
            pass
    except Exception as e:
        print(f"Waiting for backend... ({e})")

    time.sleep(2)