import cv2
import dlib
import numpy as np
import pickle
import os

# Load Dlib's face detector and models
detector = dlib.get_frontal_face_detector()
shape_predictor_path = os.path.join(os.path.dirname(__file__), "shape_predictor_68_face_landmarks.dat")
face_rec_model_path = os.path.join(os.path.dirname(__file__), "dlib_face_recognition_resnet_model_v1.dat")

# Check if model files exist
if not os.path.exists(shape_predictor_path) or not os.path.exists(face_rec_model_path):
    raise FileNotFoundError("Required Dlib model files are missing.")

predictor = dlib.shape_predictor(shape_predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

def detect_faces(image):
    """Detect faces in an image and return bounding boxes"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    print(f"DEBUG: detect_faces found {len(faces)} faces")  # Added debug print
    return faces

def get_face_encodings(image, faces):
    """Get 128D face encodings for each detected face"""
    encodings = []
    for face in faces:
        shape = predictor(image, face)
        face_descriptor = face_rec_model.compute_face_descriptor(image, shape)
        encodings.append(np.array(face_descriptor))
    return encodings

def compare_faces(known_encodings, face_encoding, tolerance=0.6):
    """Compare a face encoding against known encodings"""
    distances = np.linalg.norm(known_encodings - face_encoding, axis=1)
    min_distance = np.min(distances)
    if min_distance <= tolerance:
        index = np.argmin(distances)
        return True, index, min_distance
    else:
        return False, None, None

def serialize_encoding(encoding):
    """Serialize numpy array encoding to bytes for database storage"""
    return pickle.dumps(encoding)

def deserialize_encoding(blob):
    """Deserialize bytes from database to numpy array encoding"""
    return pickle.loads(blob)
