from flask import Flask, jsonify, render_template

from app.database.attendance_db import (
    initialize_database,
    get_attendance
)


# Create Flask application
server = Flask(__name__)


# Initialize database when server starts
initialize_database()


@server.route("/")
def home():
    """
    Open the dashboard.
    """
    return render_template("index.html")


@server.route("/api/attendance")
def attendance():
    """
    Return attendance records as JSON.
    """

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


if __name__ == "__main__":
    server.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )