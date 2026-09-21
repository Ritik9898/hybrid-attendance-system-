import cv2
import os


# Get the project root directory
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)


# Path to the YuNet face detection model
MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "face_detection_yunet_2026may.onnx"
)


# Create YuNet face detector
face_detector = cv2.FaceDetectorYN.create(
    MODEL_PATH,
    "",
    (320, 320),
    0.6,
    0.3,
    5000
)


def detect_faces(frame):
    """
    Detect faces in the given camera frame.
    """

    height, width = frame.shape[:2]

    face_detector.setInputSize((width, height))

    _, faces = face_detector.detect(frame)

    return faces