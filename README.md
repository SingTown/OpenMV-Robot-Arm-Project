
# OpenMV 智能视觉机械臂项目 (OpenMV Intelligent Vision Robot Arm Project)

[中文](README.md) | [English](README_EN.md) (Note: Keeping it bilingual in one file as requested)

---

## 📌 项目简介 / Introduction

**[ZH]** 本项目是一个基于 **OpenMV 视觉模块** 和 **多自由度机械臂** 的集成开发系统。它集成了机械控制、机器视觉、深度学习 (TFLite/FOMO) 以及自动化算法。项目旨在为**工程创客**、**电子设计竞赛 (电赛)** 以及 **AI 机器人教育** 提供一套完整的软硬件参考方案。

**[EN]** This project is an integrated development system based on the **OpenMV vision module** and a **multi-DOF robot arm**. It integrates mechanical control, computer vision, deep learning (TFLite/FOMO), and automation algorithms. The project is designed to provide a complete hardware and software reference solution for **Engineering Makers**, **Electronic Design Contests (EDC)**, and **AI Robotics Education**.

---

## 🚀 核心功能 / Core Features

- **视觉识别与定位 (Vision Recognition & Positioning)**：利用 OpenMV 进行颜色追踪、形状识别及 TFLite 深度学习模型推断（如 FOMO）。
- **坐标系转换 (Coordinate Transformation)**：建立相机像素坐标与机械臂空间坐标的映射。
- **多种应用场景 (Various Scenarios)**：
    - **24电赛E题 (2024 EDC Problem E)**：针对 2024 年全国大学生电子设计竞赛 E 题（运动目标控制与识别）的完整方案。
    - **三子棋对弈 (Tic-Tac-Toe)**：结合图像识别与博弈算法实现智能对弈。
    - **智能分类 (Intelligent Sorting)**：通过 FOMO 模型实现物块/垃圾的快速识别与分拣。
- **教学与演示 (Teaching & Demo)**：
    - **示教模式 (Teaching Mode)**：支持按键录制动作并回放。
    - **交互显示 (Interactive Display)**：LCD 实时显示视觉画面与系统状态。

---

## 📂 项目结构 / Project Structure

```text
OpenMV-Robot-Arm-Project/
├── firmware/                   # 机械臂控制板固件 / Robot arm control board firmware
└── openmv_examples/            # OpenMV Python 示例程序 / OpenMV Python examples
    ├── Block Grasping and Palletizing/   # 物块抓取与码垛 / Block sorting & stacking (FOMO)
    ├── Calibration and Testing/          # 校准与功能自检 / Calibration & functional self-test
    ├── Garbage Classification/           # 垃圾分类识别 / Garbage recognition & sorting
    ├── Initial Program/                  # 基础初始化程序 / Basic initialization
    ├── Key Teaching/                     # 按键示教录制 / Movement recording & playback
    ├── LCD Display & Key Control/        # 屏幕与按键交互 / Display & peripheral interaction
    ├── Load File and Move/               # 文件读取与执行 / Load moves from file
    ├── Problem E of the 2024/            # 2024电赛E题专项 / 2024 EDC Problem E solution
    └── Tic-Tac-Toe Electromagnet/        # 电磁铁三子棋 / Tic-Tac-Toe with electromagnet
```

---

## 🛠️ 硬件需求 / Hardware Requirements

1. **视觉模块 (Vision Module)**: OpenMV H7 / H7 Plus or higher.
2. **机械臂 (Robot Arm)**: 支持串口通信的多自由度桌面级机械臂 / Desktop multi-DOF arm with UART support.
3. **显示器 (Display)**: SPI LCD screen (optional).
4. **执行器 (Actuator)**: 舵机夹爪或电磁铁 / Gripper or Electromagnet.

---

## 📝 快速上手 / Quick Start

### 1. 固件刷写 / Firmware Flashing
将 `firmware/` 目录下的 bin 文件刷入机械臂控制板。
Flash the bin files in `firmware/` to the robot arm control board.

### 2. 环境配置 / Environment Setup
1. 安装 [OpenMV IDE](https://openmv.io/pages/download)。
2. 将相应示例目录下的文件（`main.py`, `Robot_arm.py` 等）拷贝至 OpenMV 磁盘根目录。
3. Copy files from the example directory to the OpenMV disk root.

### 3. 校准 (重要) / Calibration (Crucial)
运行 `openmv_examples/Calibration and Testing/校准程序.py` 确保舵机中位及坐标对齐。
Run the calibration script to ensure proper servo alignment and coordinate mapping.

---

## 🤝 贡献与支持 / Support

本项目由 [星瞳科技 (SingTown)](https://singtown.com) 提供技术支持。
Supported by [SingTown](https://singtown.com).

---


