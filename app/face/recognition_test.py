import cv2

from app.face.detector import detect_faces
from app.face.recognizer import (
    load_registered_faces,
    recognize_face
)


# Load registered face features
load_registered_faces()


# Open webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()


print("Face Recognition Started")
print("Look at the camera.")
print("Press Q to quit.")


while True:

    # Capture frame
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read camera frame.")
        break


    # Detect faces
    faces = detect_faces(frame)


    if faces is not None:

        for face in faces:

            # Get face coordinates
            x, y, width, height = face[:4].astype(int)


            # Recognize face
            name, score = recognize_face(
                frame,
                face
            )


            # Draw face rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2
            )


            # Display name and similarity score
            text = f"{name} ({score:.2f})"

            cv2.putText(
                frame,
                text,
                (x, max(y - 10, 30)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )


    # Show camera
    cv2.imshow(
        "Hybrid Attendance - Face Recognition",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release camera
camera.release()

cv2.destroyAllWindows()

print("Face Recognition Stopped.")