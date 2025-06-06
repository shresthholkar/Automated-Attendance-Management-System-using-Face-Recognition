from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from database import add_user, add_face_encoding, get_face_encodings, get_all_users, mark_attendance, get_attendance_records
from face_recognition_module import deserialize_encoding, serialize_encoding, compare_faces

app = Flask(__name__)
CORS(app)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    encoding_list = data.get('face_encoding')  # Expecting list of floats

    if not name or not encoding_list:
        return jsonify({'error': 'Name and face_encoding are required'}), 400

    encoding = np.array(encoding_list)

    # Check for duplicate face encodings
    existing_encodings_data = get_face_encodings()
    existing_encodings = []
    for _, encoding_blob in existing_encodings_data:
        existing_encodings.append(deserialize_encoding(encoding_blob))
    if existing_encodings:
        match, _, _ = compare_faces(np.array(existing_encodings), encoding)
        if match:
            return jsonify({'error': 'User already registered'}), 400

    user_id = add_user(name)
    if user_id is None:
        return jsonify({'error': 'User name already exists or database error'}), 400

    serialized = serialize_encoding(encoding)
    add_face_encoding(user_id, serialized)

    return jsonify({'message': f"User '{name}' registered successfully."}), 201

@app.route('/attendance', methods=['POST'])
def mark_attendance_api():
    data = request.json
    encoding_list = data.get('face_encoding')  # Expecting list of floats

    if not encoding_list:
        return jsonify({'error': 'face_encoding is required'}), 400

    encoding = np.array(encoding_list)

    known_encodings_data = get_face_encodings()
    if not known_encodings_data:
        return jsonify({'error': 'No registered users found'}), 400

    known_encodings = []
    known_user_ids = []
    for user_id, encoding_blob in known_encodings_data:
        known_encodings.append(deserialize_encoding(encoding_blob))
        known_user_ids.append(user_id)

    match, index, _ = compare_faces(np.array(known_encodings), encoding)
    if match:
        user_id = known_user_ids[index]
        mark_attendance(user_id)
        return jsonify({'message': 'Attendance marked', 'user_id': user_id}), 200
    else:
        return jsonify({'error': 'No matching user found'}), 404

@app.route('/reports', methods=['GET'])
def get_reports():
    records = get_attendance_records()
    # records is list of tuples (name, timestamp)
    result = [{'name': name, 'timestamp': timestamp} for name, timestamp in records]
    return jsonify(result), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Attendance API. Available endpoints: /register, /attendance, /reports'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
