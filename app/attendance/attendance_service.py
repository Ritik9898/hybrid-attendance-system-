from app.database.attendance_db import (
    mark_attendance,
    get_connection
)


def process_attendance(
    student_name,
    face_verified,
    device_verified
):
    """
    Decide whether attendance should be marked.

    Attendance is allowed only when:
    1. Face is verified
    2. Device is verified
    """

    if not face_verified:
        return False, "Face verification failed."

    if not device_verified:
        return False, "Device verification failed."

    # Check whether attendance is already marked today
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM attendance
        WHERE student_name = ?
        AND attendance_date = date('now', 'localtime')
        """,
        (student_name,)
    )

    existing_record = cursor.fetchone()

    connection.close()

    if existing_record:
        return False, "Attendance already marked today."

    # Both checks passed
    mark_attendance(
        student_name,
        face_verified,
        device_verified
    )

    return True, "Attendance marked successfully."