# OpenMV Intelligent Vision Robot Arm Project

[English](README.md) | [中文](README_CN.md)

---

## 📌 Introduction

This project is an integrated development system based on the **OpenMV vision module** and a **multi-DOF robot arm**. It integrates mechanical control, computer vision, deep learning (TFLite/FOMO), and automation algorithms. The project is designed to provide a complete hardware and software reference solution for **Engineering Makers**, **Electronic Design Contests (EDC)**, and **AI Robotics Education**.

---

## 🚀 Core Features

- **Vision Recognition & Positioning**: Utilizing OpenMV for color tracking, shape recognition, and TFLite deep learning model inference (e.g., FOMO).
- **Coordinate Transformation**: Establishing the mapping between camera pixel coordinates and robot arm spatial coordinates.
- **Various Scenarios**:
    - **2024 EDC Problem E**: A complete solution for Problem E (Target Control and Recognition) of the 2024 National Undergraduate Electronic Design Contest.
    - **Tic-Tac-Toe**: Intelligent gameplay combining image recognition and game algorithms.
    - **Intelligent Sorting**: Fast recognition and sorting of blocks/garbage using the FOMO model.
- **Teaching & Demo**:
    - **Teaching Mode**: Supports recording and replaying movements via buttons.
    - **Interactive Display**: Real-time display of vision feed and system status on an LCD.

---

## 📂 Project Structure

```text
OpenMV-Robot-Arm-Project/
├── firmware/                   # Robot arm control board firmware
└── openmv_examples/            # OpenMV Python examples
    ├── Block Grasping and Palletizing/   # Block sorting & stacking (FOMO)
    ├── Calibration and Testing/          # Calibration & functional self-test
    ├── Garbage Classification/           # Garbage recognition & sorting
    ├── Initial Program/                  # Basic initialization
    ├── Key Teaching/                     # Movement recording & playback
    ├── LCD Display & Key Control/        # Display & peripheral interaction
    ├── Load File and Move/               # Load moves from file
    ├── Problem E of the 2024/            # 2024 EDC Problem E solution
    └── Tic-Tac-Toe Electromagnet/        # Tic-Tac-Toe with electromagnet
```

---

## 🛠️ Hardware Requirements

1. **Vision Module**: OpenMV H7 / H7 Plus or higher.
2. **Robot Arm**: Desktop multi-DOF arm with UART support.
3. **Display**: SPI LCD screen (optional).
4. **Actuator**: Gripper or Electromagnet.

---

## 📝 Quick Start

### 1. Firmware Flashing
Flash the bin files in `firmware/` to the robot arm control board. (Pre-flashed by factory default)

### 2. Environment Setup
1. Install [OpenMV IDE](https://openmv.io/pages/download).
2. Copy files from the example directory to the OpenMV disk root.

### 3. Calibration
Run `openmv_examples/Calibration and Testing/calibration.py` to ensure proper servo alignment and coordinate mapping. (Used to calibrate servo angles and robot arm reset position when they are inaccurate)

---

## 🤝 Support

Supported by [SingTown](https://singtown.com).

---
