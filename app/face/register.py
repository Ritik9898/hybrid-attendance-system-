import cv2
import os
import sys
import re

from app.face.detector import detect_faces


# --------------------------------------------------
# Get project root directory
# --------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)


# --------------------------------------------------
# Get student name
# --------------------------------------------------

if len(sys.argv) < 2:
    print("ERROR: Student name is required.")
    print("Example:")
    print("python -m app.face.register \"Test Student\"")
    sys.exit(1)

student_name = sys.argv[1].strip()


# --------------------------------------------------
# Create safe folder name
# --------------------------------------------------

folder_name = re.sub(
    r"[^a-zA-Z0-9_-]+",
    "_",
    student_name
).strip("_").lower()


if not folder_name:
    print("ERROR: Invalid student name.")
    sys.exit(1)


# --------------------------------------------------
# Face storage folder
# --------------------------------------------------

SAVE_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data",
    "faces",
    folder_name
)

os.makedirs(
    SAVE_FOLDER,
    exist_ok=True
)


# --------------------------------------------------
# Open webcam
# --------------------------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    sys.exit(1)


print("----------------------------------------")
print("Face Registration Started")
print("----------------------------------------")
print(f"Student: {student_name}")
print(f"Folder: {SAVE_FOLDER}")
print("Look at the camera.")
print("Press Q to quit.")
print("----------------------------------------")


image_count = 0
max_images = 20


# --------------------------------------------------
# Capture face images
# --------------------------------------------------

while image_count < max_images:

    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read camera frame.")
        break

    # Detect faces
    faces = detect_faces(frame)

    if faces is not None and len(faces) > 0:

        # Take the first detected face
        face = faces[0]

        x, y, width, height = face[:4].astype(int)

        # Keep coordinates inside the frame
        x = max(0, x)
        y = max(0, y)

        width = min(
            width,
            frame.shape[1] - x
        )

        height = min(
            height,
            frame.shape[0] - y
        )

        # Crop face
        face_image = frame[
            y:y + height,
            x:x + width
        ]

        # Save face image
        filename = os.path.join(
            SAVE_FOLDER,
            f"face_{image_count + 1}.jpg"
        )

        cv2.imwrite(
            filename,
            face_image
        )

        image_count += 1

        # Draw rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            2
        )

        # Capture count
        cv2.putText(
            frame,
            f"Captured: {image_count}/{max_images}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "No face detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    # Show camera
    cv2.imshow(
        "Face Registration",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# Release camera
# --------------------------------------------------

camera.release()

cv2.destroyAllWindows()


# --------------------------------------------------
# Final message
# --------------------------------------------------

print("----------------------------------------")
print("Registration completed.")
print(f"Student: {student_name}")
print(f"Images captured: {image_count}")
print(f"Saved in: {SAVE_FOLDER}")
print("----------------------------------------")