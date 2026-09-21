import cv2
import os

from detector import detect_faces


# Get project root directory
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)


# Folder where registered face images will be saved
SAVE_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data",
    "faces",
    "ritik"
)


# Create folder if it doesn't exist
os.makedirs(SAVE_FOLDER, exist_ok=True)


# Open webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()


print("Face Registration Started")
print("Look at the camera.")
print("Press Q to quit.")

image_count = 0
max_images = 20


while image_count < max_images:

    # Capture frame
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

        # Draw rectangle around face
        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            2
        )

        # Show capture count
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


# Release camera
camera.release()

# Close camera window
cv2.destroyAllWindows()


print("Registration completed.")
print(
    f"{image_count} face images saved in {SAVE_FOLDER}"
)