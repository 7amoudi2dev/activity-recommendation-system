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


# # Get all requests
# @app.route('/api/history', methods=['GET'])
# def get_history():
#     try:
#         response = requests.get(f"{DAO_SERVICE_URL}/requests", timeout=5)
#         if response.status_code == 200:
#             return jsonify(response.json())
#         else:
#             return jsonify({"error": f"DAO Service returned {response.status_code}"}), 500
#     except requests.exceptions.ConnectionError:
#         return jsonify({"error": "Cannot connect to DAO Service. Is it running on port 5001?"}), 503
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # Get single request
# @app.route('/api/history/<int:request_id>', methods=['GET'])
# def get_request(request_id):
#     try:
#         response = requests.get(f"{DAO_SERVICE_URL}/requests/{request_id}", timeout=5)
#         if response.status_code == 200:
#             return jsonify(response.json())
#         elif response.status_code == 404:
#             return jsonify({"error": "Request not found"}), 404
#         else:
#             return jsonify({"error": f"DAO Service error"}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# Health check
# @app.route('/api/health', methods=['GET'])
# def health():
#     # Check if DAO service is healthy
#     try:
#         dao_response = requests.get(f"{DAO_SERVICE_URL}/health", timeout=2)
#         dao_healthy = dao_response.status_code == 200
#     except:
#         dao_healthy = False
#
#     return jsonify({
#         "status": "healthy",
#         "service": "Activity Service API",
#         "version": "1.0",
#         "dao_service": "connected" if dao_healthy else "disconnected"
#     })


# Root endpoint - API info
@app.route('/', methods=['GET'])
def api_info():
    return jsonify({
        "service": "Activity Recommendation API",
        "version": "1.0",
        "endpoints": {
            "POST /api/activity": "Get activity recommendation",
            "GET /api/history": "Get all activity history",
            "GET /api/history/{id}": "Get specific request",
            "GET /api/health": "Service health check"
        }
    })


if __name__ == '__main__':
    # print("Checking connection to DAO Service...")
    # try:
    #     response = requests.get(f"{DAO_SERVICE_URL}/health", timeout=2)
    #     if response.status_code == 200:
    #         print("✓ Successfully connected to DAO Service")
    #     else:
    #         print("✗ DAO Service is not healthy")
    # except:
    #     print("✗ Cannot connect to DAO Service on port 5001")
    #     print("  Make sure to start dao_service.py first!")

    print(f"Starting Activity Service API on port 5002...")
    app.run(port=5002, debug=True)