# OpenMV 智能视觉机械臂项目

[English](README.md) | [中文](README_CN.md)

---

## 📌 项目简介

本项目是一个基于 **OpenMV 视觉模块** 和 **多自由度机械臂** 的集成开发系统。它集成了机械控制、机器视觉、深度学习 (TFLite/FOMO) 以及自动化算法。项目旨在为**工程创客**、**电子设计竞赛 (电赛)** 以及 **AI 机器人教育** 提供一套完整的软硬件参考方案。

---

## 🚀 核心功能

- **视觉识别与定位**：利用 OpenMV 进行颜色追踪、形状识别及 TFLite 深度学习模型推断（如 FOMO）。
- **坐标系转换**：建立相机像素坐标与机械臂空间坐标的映射。
- **多种应用场景**：
    - **24电赛E题**：针对 2024 年全国大学生电子设计竞赛 E 题（运动目标控制与识别）的完整方案。
    - **三子棋对弈**：结合图像识别与博弈算法实现智能对弈。
    - **智能分类**：通过 FOMO 模型实现物块/垃圾的快速识别与分拣。
- **教学与演示**：
    - **示教模式**：支持按键录制动作并回放。
    - **交互显示**：LCD 实时显示视觉画面与系统状态。

---

## 📂 项目结构

```text
OpenMV-Robot-Arm-Project/
├── firmware/                   # 机械臂控制板固件
└── openmv_examples/            # OpenMV Python 示例程序
    ├── Block Grasping and Palletizing/   # 物块抓取与码垛 (FOMO)
    ├── Calibration and Testing/          # 校准与功能自检
    ├── Garbage Classification/           # 垃圾分类识别
    ├── Initial Program/                  # 基础初始化程序
    ├── Key Teaching/                     # 按键示教录制
    ├── LCD Display & Key Control/        # 屏幕与按键交互
    ├── Load File and Move/               # 文件读取与执行
    ├── Problem E of the 2024/            # 2024电赛E题专项
    └── Tic-Tac-Toe Electromagnet/        # 电磁铁三子棋
```

---

## 🛠️ 硬件需求

1. **视觉模块**: OpenMV H7 / H7 Plus or higher.
2. **机械臂**: 支持串口通信的多自由度桌面级机械臂.
3. **显示器**: SPI LCD 屏幕 (可选).
4. **执行器**: 舵机夹爪或电磁铁.

---

## 📝 快速上手

### 1. 固件刷写
将 `firmware/` 目录下的 bin 文件刷入机械臂控制板。

### 2. 环境配置
1. 安装 [OpenMV IDE](https://openmv.io/pages/download)。
2. 将相应示例目录下的文件（`main.py`, `Robot_arm.py` 等）拷贝至 OpenMV 磁盘根目录。

### 3. 校准 (重要)
运行 `openmv_examples/Calibration and Testing/校准程序.py` 确保舵机中位及坐标对齐。

---

## 🤝 贡献与支持

本项目由 [星瞳科技 (SingTown)](https://singtown.com) 提供技术支持。

---
