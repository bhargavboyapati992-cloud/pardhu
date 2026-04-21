import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

class MoisturePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def train_and_predict(self, data_points):
        """
        data_points: list of dicts [{'timestamp': datetime, 'moisture': float}]
        Predicts if moisture will drop below 30 in the next hour.
        """
        if len(data_points) < 5:
            # Not enough data, return None to fallback to threshold
            return None

        # Convert timestamps to relative seconds
        base_time = data_points[0]['timestamp']
        X = np.array([(d['timestamp'] - base_time).total_seconds() for d in data_points]).reshape(-1, 1)
        y = np.array([d['moisture'] for d in data_points])

        self.model.fit(X, y)

        # Predict 5 minutes into the future (300 seconds) from the latest data point
        latest_time = data_points[-1]['timestamp']
        future_time = (latest_time - base_time).total_seconds() + 300
        
        predicted_moisture = self.model.predict([[future_time]])[0]
        
        return predicted_moisture

predictor = MoisturePredictor()

def interpret_and_decide(predicted_moisture, current_moisture=0.0, current_temp=0.0, moisture_threshold=600.0, temp_threshold=35.0):
    if current_moisture >= moisture_threshold:
        return "KEEP_OFF"
    
    if predicted_moisture is None:
        return "TURN_ON" if current_moisture < moisture_threshold else "KEEP_OFF"
        
    if predicted_moisture < moisture_threshold:
        return "TURN_ON"
        
    return "KEEP_OFF"
