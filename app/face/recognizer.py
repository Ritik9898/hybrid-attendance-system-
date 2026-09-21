import cv2
import os
import numpy as np


# -----------------------------
# Project paths
# -----------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "face_recognition_sface_2021dec.onnx"
)

FACE_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data",
    "faces",
    "ritik"
)


# -----------------------------
# Create SFace recognizer
# -----------------------------

recognizer = cv2.FaceRecognizerSF.create(
    MODEL_PATH,
    ""
)


# -----------------------------
# Store registered face features
# -----------------------------

registered_features = []


# -----------------------------
# Load registered face images
# -----------------------------

def load_registered_faces():

    for filename in os.listdir(FACE_FOLDER):

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue

        image_path = os.path.join(
            FACE_FOLDER,
            filename
        )

        image = cv2.imread(image_path)

        if image is None:
            continue

        # Detect face using the same YuNet detector
        from app.face.detector import detect_faces
        faces = detect_faces(image)

        if faces is None or len(faces) == 0:
            continue

        # Take first detected face
        face = faces[0]

        # Align and crop face for SFace
        aligned_face = recognizer.alignCrop(
            image,
            face
        )

        # Extract face feature
        feature = recognizer.feature(
            aligned_face
        )

        registered_features.append(
            feature
        )

    print(
        f"Loaded {len(registered_features)} registered face features."
    )


# -----------------------------
# Recognize a face
# -----------------------------

def recognize_face(image, face):

    aligned_face = recognizer.alignCrop(
        image,
        face
    )

    feature = recognizer.feature(
        aligned_face
    )

    best_score = -1

    for registered_feature in registered_features:

        score = recognizer.match(
            feature,
            registered_feature,
            cv2.FaceRecognizerSF_FR_COSINE
        )

        if score > best_score:
            best_score = score

    # Recognition threshold
    threshold = 0.363

    if best_score >= threshold:
        name = "Ritik"
    else:
        name = "Unknown"

    return name, best_score