# 🔐 Hybrid Attendance System

A secure attendance management system that combines **Face Recognition** and **Device Verification** to reduce unauthorized or proxy attendance.

The system uses **Python, OpenCV, Flask, SQLite, HTML, CSS, and JavaScript** to provide an end-to-end attendance workflow with a web dashboard.

---

## 🚀 Project Overview

Traditional attendance systems can allow proxy attendance when one student marks attendance for another.

This project combines two verification layers:

1. 👤 **Face Recognition** – verifies the student's identity.
2. 💻 **Device Verification** – verifies that attendance is being attempted from a registered device.

Attendance is marked only when the required verification conditions are satisfied.

---

## ✨ Features

- 👤 Face detection using OpenCV YuNet
- 🧠 Face recognition using OpenCV SFace
- 💻 Registered device verification
- 🗄️ SQLite database for attendance records
- 🔌 Flask REST API
- 🌐 Web-based attendance dashboard
- 📊 Attendance history
- 🔒 Duplicate attendance prevention
- ✅ Face verification status
- ✅ Device verification status
- 🔄 Automatic dashboard refresh
- 📁 Organized Python project structure

---

## 🏗️ System Architecture

```text
              ┌─────────────────┐
              │     Webcam      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Face Detection │
              │     YuNet       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Face Recognition│
              │     SFace       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Student Identity│
              └────────┬────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
     ┌───────────────┐   ┌────────────────┐
     │ Face Verified │   │ Device         │
     │               │   │ Verification   │
     └───────┬───────┘   └───────┬────────┘
             │                   │
             └─────────┬─────────┘
                       ▼
              ┌─────────────────┐
              │ Attendance      │
              │ Service         │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ SQLite Database │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Flask REST API  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Web Dashboard   │
              └─────────────────┘
