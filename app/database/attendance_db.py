import sqlite3
import os
from datetime import datetime


# Get project root directory
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)


# Database location
DATABASE_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "attendance.db"
)


def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """
    Create the attendance table if it doesn't exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            attendance_date TEXT NOT NULL,
            attendance_time TEXT NOT NULL,
            face_verified INTEGER NOT NULL,
            device_verified INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


def mark_attendance(
    student_name,
    face_verified,
    device_verified
):
    """
    Store an attendance record.
    """

    now = datetime.now()

    attendance_date = now.strftime("%Y-%m-%d")
    attendance_time = now.strftime("%H:%M:%S")

    status = "Present"

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO attendance (
            student_name,
            attendance_date,
            attendance_time,
            face_verified,
            device_verified,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        student_name,
        attendance_date,
        attendance_time,
        int(face_verified),
        int(device_verified),
        status
    ))

    connection.commit()

    connection.close()


def get_attendance():
    """
    Get all attendance records.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            student_name,
            attendance_date,
            attendance_time,
            face_verified,
            device_verified,
            status
        FROM attendance
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records