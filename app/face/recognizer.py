import cv2
import os

from app.face.detector import detect_faces


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "face_recognition_sface_2021dec.onnx"
)

FACE_ROOT_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data",
    "faces"
)


# --------------------------------------------------
# Create SFace recognizer
# --------------------------------------------------

recognizer = cv2.FaceRecognizerSF.create(
    MODEL_PATH,
    ""
)


# --------------------------------------------------
# Store registered face features
#
# Each item:
# {
#     "name": "Ritik",
#     "feature": feature
# }
# --------------------------------------------------

registered_features = []


# --------------------------------------------------
# Convert folder name back to display name
# --------------------------------------------------

def display_name(folder_name):
    return folder_name.replace("_", " ").title()


# --------------------------------------------------
# Load ALL registered student faces
# --------------------------------------------------

def load_registered_faces():

    registered_features.clear()

    if not os.path.exists(FACE_ROOT_FOLDER):
        print("Face registration folder does not exist.")
        return

    # Loop through every student folder
    for student_folder in os.listdir(FACE_ROOT_FOLDER):

        student_path = os.path.join(
            FACE_ROOT_FOLDER,
            student_folder
        )

        # Ignore files
        if not os.path.isdir(student_path):
            continue

        student_name = display_name(student_folder)

        # Loop through student's face images
        for filename in os.listdir(student_path):

            if not filename.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):
                continue

            image_path = os.path.join(
                student_path,
                filename
            )

            image = cv2.imread(image_path)

            if image is None:
                continue

            # Detect face
            faces = detect_faces(image)

            if faces is None or len(faces) == 0:
                continue

            # Take first detected face
            face = faces[0]

            # Align face for SFace
            aligned_face = recognizer.alignCrop(
                image,
                face
            )

            # Extract face feature
            feature = recognizer.feature(
                aligned_face
            )

            registered_features.append({
                "name": student_name,
                "feature": feature
            })

    print(
        f"Loaded {len(registered_features)} registered face features."
    )

    # Show loaded students
    students = sorted(
        set(item["name"] for item in registered_features)
    )

    if students:
        print("Registered students:")

        for student in students:
            print(f"  - {student}")
    else:
        print("No registered students found.")


# --------------------------------------------------
# Recognize a face
# --------------------------------------------------

def recognize_face(image, face):

    if not registered_features:
        return "Unknown", 0.0

    # Align detected face
    aligned_face = recognizer.alignCrop(
        image,
        face
    )

    # Extract feature
    feature = recognizer.feature(
        aligned_face
    )

    # Best match
    best_score = -1
    best_name = "Unknown"

    # Compare against every registered face
    for registered_feature in registered_features:

        score = recognizer.match(
            feature,
            registered_feature["feature"],
            cv2.FaceRecognizerSF_FR_COSINE
        )

        if score > best_score:
            best_score = score
            best_name = registered_feature["name"]

    # Recognition threshold
    threshold = 0.363

    if best_score >= threshold:
        return best_name, best_score

    return "Unknown", best_score