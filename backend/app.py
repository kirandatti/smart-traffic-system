from flask import Flask, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import random

app = Flask(__name__)
CORS(app)

# Load trained model and encoders
model = joblib.load('traffic_model.pkl')
target_encoder = joblib.load('target_encoder.pkl')

# Traffic situation labels (Heavy, High, Low, Normal - alphabetical order from encoder)
labels = target_encoder.classes_

def predict_traffic():
    # Simulate live traffic input (in real system, this comes from sensors/cameras)
    car_count = random.randint(10, 80)
    bike_count = random.randint(5, 40)
    bus_count = random.randint(0, 15)
    truck_count = random.randint(0, 20)
    total = car_count + bike_count + bus_count + truck_count
    day_of_week = random.randint(0, 6)  # 0=Monday ... 6=Sunday (encoded)

    features = np.array([[car_count, bike_count, bus_count, truck_count, total, day_of_week]])
    prediction = model.predict(features)[0]
    situation = target_encoder.inverse_transform([prediction])[0]

    return {
        "car_count": car_count,
        "bike_count": bike_count,
        "bus_count": bus_count,
        "truck_count": truck_count,
        "total_vehicles": total,
        "situation": situation
    }

# Signal timing logic based on congestion level
def get_signal_timing(situation):
    timing_map = {
        "heavy": 55,
        "high": 45,
        "normal": 30,
        "low": 20
    }
    return timing_map.get(situation.lower(), 30)

@app.route('/predict', methods=['GET'])
def predict():
    result_a = predict_traffic()
    result_b = predict_traffic()

    data = {
        "intersection_a": {
            "congestion_percent": min(int((result_a["total_vehicles"] / 155) * 100), 100),
            "status": result_a["situation"].capitalize(),
            "vehicles": result_a["total_vehicles"]
        },
        "intersection_b": {
            "congestion_percent": min(int((result_b["total_vehicles"] / 155) * 100), 100),
            "status": result_b["situation"].capitalize(),
            "vehicles": result_b["total_vehicles"]
        },
        "recommended_signal_timing": {
            "green_seconds": get_signal_timing(result_a["situation"])
        }
    }
    return jsonify(data)

@app.route('/', methods=['GET'])
def home():
    return "Smart Traffic Backend is Running (Real AI Model) ✅"

if __name__ == '__main__':
    app.run(debug=True, port=5000)