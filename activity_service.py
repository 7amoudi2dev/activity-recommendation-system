from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# DAO Service URL
DAO_SERVICE_URL = "http://localhost:5001"

# Logic
def get_activity_recommendation(temperature):
    if temperature >= 25:
        return "Swimming"
    elif temperature >= 18:
        return "Tennis"
    elif temperature >= 2:
        return "Hiking"
    else:
        return "Skiing"


# Activity endpoint
@app.route('/api/activity', methods=['POST'])
def process_activity_request():
    data = request.json

    # Validate input
    required_fields = ['client_name', 'birth_date', 'machine_name', 'username', 'temperature']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Apply business logic
    temperature = float(data['temperature'])
    activity = get_activity_recommendation(temperature)

    # Prepare data for DAO
    dao_data = {
        'client_name': data['client_name'],
        'birth_date': data['birth_date'],
        'machine_name': data['machine_name'],
        'username': data['username'],
        'temperature': temperature,
        'activity': activity
    }

    # Send to DAO Service
    try:
        response = requests.post(f"{DAO_SERVICE_URL}/requests", json=dao_data, timeout=5)
        if response.status_code == 201:
            return jsonify({
                "activity": activity,
                "message": "Activity recommendation saved",
                "temperature": temperature
            }), 201
        else:
            return jsonify({"error": f"DAO Service error: {response.text}"}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to DAO Service. Is it running on port 5001?"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"Starting Activity Service API on port 5002...")
    app.run(port=5002, debug=True)