from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

#DB Conn
def get_db():
    return psycopg2.connect(
        host="localhost",
        database="activity",
        user="admin",
        password="password"
    )

# CREATE
@app.route('/requests', methods=['POST'])
def create_request():
    data = request.json

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO requests (client_name, birth_date, machine_name, username, temperature, activity)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                """, (data['client_name'], data['birth_date'], data['machine_name'],
                      data['username'], data['temperature'], data['activity']))

    request_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": request_id, "message": "Request created successfully"}), 201

# READ - GET ALL
@app.route('/requests', methods=['GET'])
def get_all_requests():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests ORDER BY created_at DESC")

    rows = cur.fetchall()
    requests = []
    for row in rows:
        requests.append({
            'id': row[0],
            'client_name': row[1],
            'birth_date': str(row[2]),
            'machine_name': row[3],
            'username': row[4],
            'temperature': row[5],
            'activity': row[6],
            'created_at': str(row[7])
        })

    cur.close()
    conn.close()

    return jsonify(requests)


# READ - Get single
@app.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests WHERE id = %s", (request_id,))

    row = cur.fetchone()
    if row:
        request_data = {
            'id': row[0],
            'client_name': row[1],
            'birth_date': str(row[2]),
            'machine_name': row[3],
            'username': row[4],
            'temperature': row[5],
            'activity': row[6],
            'created_at': str(row[7])
        }
        cur.close()
        conn.close()
        return jsonify(request_data)

    cur.close()
    conn.close()
    return jsonify({"error": "Request not found"}), 404


# UPDATE
@app.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    data = request.json

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
                UPDATE requests
                SET client_name  = %s,
                    birth_date   = %s,
                    machine_name = %s,
                    username     = %s,
                    temperature  = %s,
                    activity     = %s
                WHERE id = %s
                """, (data['client_name'], data['birth_date'], data['machine_name'],
                      data['username'], data['temperature'], data['activity'], request_id))

    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if affected:
        return jsonify({"message": "Request updated successfully"})
    return jsonify({"error": "Request not found"}), 404


# DELETE
@app.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM requests WHERE id = %s", (request_id,))

    affected = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if affected:
        return jsonify({"message": "Request deleted successfully"})
    return jsonify({"error": "Request not found"}), 404

if __name__ == '__main__':
    app.run(port=5001, debug=True)