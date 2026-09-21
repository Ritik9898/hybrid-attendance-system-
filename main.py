import cv2

from app.face.detector import detect_faces


# Open the default camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

print("Camera started.")
print("Press Q to quit.")

while True:

    # Capture a frame
    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read camera frame.")
        break

    # Detect faces
    faces = detect_faces(frame)

    # Check whether faces were detected
    if faces is not None:

        for face in faces:

            # First four values are:
            # x, y, width, height
            x, y, width, height = face[:4].astype(int)

            # Draw rectangle around face
            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2
            )

    # Display camera
    cv2.imshow(
        "Hybrid Attendance System - Face Detection",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release camera
camera.release()

# Close OpenCV windows
cv2.destroyAllWindows()

print("Camera stopped.")