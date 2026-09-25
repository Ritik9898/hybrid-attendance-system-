from flask import Flask, jsonify, render_template, request
import os
import subprocess
import sys
import sqlite3

from app.database.attendance_db import (
    initialize_database,
    get_attendance,
    add_student,
    get_students
)


# ==========================================================
# FLASK APP
# ==========================================================

server = Flask(__name__)


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

initialize_database()


# ==========================================================
# HOME / DASHBOARD
# ==========================================================

@server.route("/")
def home():
    return render_template("index.html")


# ==========================================================
# ATTENDANCE API - GET
# ==========================================================

@server.route("/api/attendance", methods=["GET"])
def attendance():

    records = get_attendance()

    data = []

    for record in records:

        data.append({
            "id": record[0],
            "student_name": record[1],
            "date": record[2],
            "time": record[3],
            "face_verified": bool(record[4]),
            "device_verified": bool(record[5]),
            "status": record[6]
        })

    return jsonify(data)


# ==========================================================
# STUDENT API - GET ALL STUDENTS
# ==========================================================

@server.route("/api/students", methods=["GET"])
def students():

    records = get_students()

    data = []

    for record in records:

        data.append({
            "id": record[0],
            "name": record[1],
            "course": record[2],
            "status": record[3]
        })

    return jsonify(data)


# ==========================================================
# STUDENT API - ADD NEW STUDENT
# ==========================================================

@server.route("/api/students", methods=["POST"])
def create_student():

    try:

        # --------------------------------------------------
        # GET JSON DATA
        # --------------------------------------------------

        data = request.get_json(silent=True)

        if not data:

            return jsonify({
                "success": False,
                "message": "No student data received."
            }), 400


        # --------------------------------------------------
        # READ FORM VALUES
        # --------------------------------------------------

        name = str(
            data.get("name", "")
        ).strip()

        course = str(
            data.get("course", "")
        ).strip()

        status = str(
            data.get("status", "Active")
        ).strip()


        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if not name:

            return jsonify({
                "success": False,
                "message": "Student name is required."
            }), 400


        if not course:

            return jsonify({
                "success": False,
                "message": "Course is required."
            }), 400


        if status not in ["Active", "Inactive"]:

            return jsonify({
                "success": False,
                "message": "Invalid student status."
            }), 400


        # --------------------------------------------------
        # ADD STUDENT TO DATABASE
        # --------------------------------------------------

        try:

            student_id = add_student(
                name,
                course,
                status
            )

        except sqlite3.IntegrityError:

            return jsonify({
                "success": False,
                "message": f'Student "{name}" already exists.'
            }), 409


        # --------------------------------------------------
        # SUCCESS RESPONSE
        # --------------------------------------------------

        return jsonify({

            "success": True,

            "message": "Student added successfully.",

            "student": {

                "id": student_id,
                "name": name,
                "course": course,
                "status": status

            }

        }), 201


    except Exception as error:

        print(
            "ERROR ADDING STUDENT:",
            error
        )

        return jsonify({

            "success": False,
            "message": "Could not add student."

        }), 500


# ==========================================================
# START FACE REGISTRATION
# ==========================================================

@server.route("/api/register-face", methods=["POST"])
def register_face():

    try:

        # --------------------------------------------------
        # GET STUDENT DATA
        # --------------------------------------------------

        data = request.get_json(silent=True)

        if not data:

            return jsonify({

                "success": False,
                "message": "No student data received."

            }), 400


        student_name = str(
            data.get("name", "")
        ).strip()


        # --------------------------------------------------
        # VALIDATE STUDENT NAME
        # --------------------------------------------------

        if not student_name:

            return jsonify({

                "success": False,
                "message": "Student name is required."

            }), 400


        # --------------------------------------------------
        # PROJECT ROOT
        # --------------------------------------------------

        project_root = os.path.dirname(
            os.path.abspath(__file__)
        )


        # --------------------------------------------------
        # FACE REGISTRATION MODULE
        # --------------------------------------------------

        register_module = "app.face.register"


        # --------------------------------------------------
        # START FACE REGISTRATION CAMERA
        # --------------------------------------------------

        subprocess.Popen(

            [
                sys.executable,
                "-m",
                register_module,
                student_name
            ],

            cwd=project_root

        )


        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                f'Face registration started for "{student_name}".',

            "student_name": student_name

        })


    except Exception as error:

        print(
            "ERROR STARTING FACE REGISTRATION:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Could not start face registration."

        }), 500


# ==========================================================
# START ATTENDANCE CAMERA
# ==========================================================

@server.route("/api/start-attendance", methods=["POST"])
def start_attendance():

    try:

        # --------------------------------------------------
        # PROJECT ROOT
        # --------------------------------------------------

        project_root = os.path.dirname(
            os.path.abspath(__file__)
        )


        # --------------------------------------------------
        # ATTENDANCE SCRIPT
        # --------------------------------------------------

        attendance_script = os.path.join(

            project_root,
            "attendance_system.py"

        )


        # --------------------------------------------------
        # CHECK FILE EXISTS
        # --------------------------------------------------

        if not os.path.exists(attendance_script):

            return jsonify({

                "success": False,

                "message":
                    "attendance_system.py not found."

            }), 404


        # --------------------------------------------------
        # START CAMERA PROGRAM
        # --------------------------------------------------

        subprocess.Popen(

            [
                sys.executable,
                attendance_script
            ],

            cwd=project_root

        )


        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                "Attendance camera started."

        })


    except Exception as error:

        print(
            "ERROR STARTING ATTENDANCE:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                "Could not start attendance camera."

        }), 500


# ==========================================================
# HEALTH CHECK
# ==========================================================

@server.route("/api/health", methods=["GET"])
def health():

    return jsonify({

        "success": True,

        "message":
            "Hybrid Attendance System API is running."

    })


# ==========================================================
# RUN SERVER
# ==========================================================

if __name__ == "__main__":

    server.run(

        host="127.0.0.1",
        port=5000,
        debug=True

    )