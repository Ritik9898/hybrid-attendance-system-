import sqlite3
import os
from datetime import datetime


# ==========================================================
# PROJECT PATH
# ==========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)


# ==========================================================
# DATABASE PATH
# ==========================================================

DATABASE_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "attendance.db"
)


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    os.makedirs(
        os.path.dirname(DATABASE_PATH),
        exist_ok=True
    )

    return sqlite3.connect(DATABASE_PATH)


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------
        # Attendance table
        # ----------------------------------------------

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


        # ----------------------------------------------
        # Students table
        # ----------------------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Active'
            )
        """)


        connection.commit()

    finally:

        connection.close()


# ==========================================================
# ADD STUDENT
# ==========================================================

def add_student(
    name,
    course,
    status="Active"
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # ----------------------------------------------
        # CHECK DUPLICATE STUDENT
        # ----------------------------------------------

        cursor.execute("""
            SELECT id
            FROM students
            WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))
        """, (
            name,
        ))

        existing_student = cursor.fetchone()


        if existing_student:

            raise sqlite3.IntegrityError(
                f'Student "{name}" already exists.'
            )


        # ----------------------------------------------
        # INSERT NEW STUDENT
        # ----------------------------------------------

        cursor.execute("""
            INSERT INTO students (
                name,
                course,
                status
            )
            VALUES (?, ?, ?)
        """, (
            name,
            course,
            status
        ))


        connection.commit()

        return cursor.lastrowid

    finally:

        connection.close()


# ==========================================================
# GET ALL STUDENTS
# ==========================================================

def get_students():

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                name,
                course,
                status
            FROM students
            ORDER BY id DESC
        """)

        students = cursor.fetchall()

        return students

    finally:

        connection.close()


# ==========================================================
# MARK ATTENDANCE
# ==========================================================

def mark_attendance(
    student_name,
    face_verified,
    device_verified
):

    now = datetime.now()

    attendance_date = now.strftime(
        "%Y-%m-%d"
    )

    attendance_time = now.strftime(
        "%H:%M:%S"
    )

    status = "Present"


    connection = get_connection()
    cursor = connection.cursor()

    try:

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

    finally:

        connection.close()


# ==========================================================
# GET ATTENDANCE
# ==========================================================

def get_attendance():

    connection = get_connection()
    cursor = connection.cursor()

    try:

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

        return records

    finally:

        connection.close()