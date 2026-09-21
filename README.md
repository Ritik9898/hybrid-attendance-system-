# 🔐 Hybrid Attendance System

A secure and automated attendance management system that combines **Face Recognition** and **Device Verification** to reduce proxy attendance.

The system uses a webcam to identify a registered student and verifies the registered device before marking attendance. Attendance records are stored in a SQLite database and displayed through a web-based dashboard.

---

## 🚀 Features

- 👤 Face Detection using OpenCV YuNet
- 🧠 Face Recognition using OpenCV SFace
- 📷 Real-time webcam verification
- 💻 Device verification
- 🗄️ SQLite database for attendance records
- 🌐 Flask-based backend
- 📊 Web dashboard for attendance history
- 🔒 Prevents duplicate attendance on the same day
- ✅ Displays face and device verification status
- 📅 Stores attendance date and time
- 🐍 Built with Python

---

## 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │      Webcam      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Face Detection  │
                    │     (YuNet)      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Face Recognition │
                    │     (SFace)      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Device Verify    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Attendance Logic │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ SQLite Database  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Web Dashboard    │
                    │     (Flask)      │
                    └──────────────────┘
```
