import cv2

from app.face.detector import detect_faces
from app.face.recognizer import (
    load_registered_faces,
    recognize_face
)
from app.utils.device_verifier import is_registered_device
from app.database.attendance_db import initialize_database
from app.attendance.attendance_service import process_attendance


# ---------------------------------------
# Initialize database
# ---------------------------------------

initialize_database()


# ---------------------------------------
# Load registered face features
# ---------------------------------------

load_registered_faces()


# ---------------------------------------
# Verify device
# ---------------------------------------

device_verified = is_registered_device()

print(
    f"Registered device: {device_verified}"
)


# ---------------------------------------
# Start camera
# ---------------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()


print()
print("Hybrid Attendance System Started")
print("Look at the camera.")
print("Press Q to quit.")
print()


attendance_message = ""
attendance_color = (255, 255, 255)


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

            # Face coordinates
            x, y, width, height = face[:4].astype(int)


            # Recognize face
            name, score = recognize_face(
                frame,
                face
            )


            # Default values
            face_verified = name != "Unknown"


            # If recognized
            if face_verified:

                # Verify device
                if device_verified:

                    success_attendance, message = process_attendance(
                        name,
                        True,
                        True
                    )

                    attendance_message = message

                    if success_attendance:
                        attendance_color = (0, 255, 0)
                    else:
                        attendance_color = (0, 255, 255)

                else:

                    attendance_message = (
                        "Device verification failed."
                    )

                    attendance_color = (0, 0, 255)

            else:

                attendance_message = (
                    "Unknown person."
                )

                attendance_color = (0, 0, 255)


            # Draw face rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                attendance_color,
                2
            )


            # Show name and score
            identity_text = (
                f"{name} ({score:.2f})"
            )

            cv2.putText(
                frame,
                identity_text,
                (x, max(y - 10, 30)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                attendance_color,
                2
            )


    # Show attendance message
    cv2.putText(
        frame,
        attendance_message,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        attendance_color,
        2
    )


    # Show device status
    device_text = (
        "Device: VERIFIED"
        if device_verified
        else "Device: NOT VERIFIED"
    )

    cv2.putText(
        frame,
        device_text,
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        attendance_color,
        2
    )


    # Display camera
    cv2.imshow(
        "Hybrid Attendance System",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ---------------------------------------
# Cleanup
# ---------------------------------------

camera.release()
cv2.destroyAllWindows()

print()
print("Hybrid Attendance System stopped.")