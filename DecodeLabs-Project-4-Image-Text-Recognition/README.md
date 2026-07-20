# 🤖 DecodeLabs Image & Text Recognition Studio (Project 4)
### Developer: Muhammad Saim Rizwan
Program: AI Industrial Training (Batch 2026) | BS Computer Science

---

## 🌌 Project Overview
This is a production-grade Computer Vision workstation that combines deep-learning-based object detection via MobileNet-SSD (Caffe Architecture) with dynamic **Optical Character Recognition (OCR) text extraction[cite: 1]. Wrapped inside a premium, cyberpunk-inspired Tkinter graphical user interface, the application processes local image matrices and extracts text blocks in real-time.

---

## 📁 System Architecture & Files
- `main.py`: Core framework containing the Tkinter interface loops and deep engine pipelines[cite: 1].
- `deploy.prototxt`: Neural layer topology configuration file[cite: 1].
- `MobileNetSSD_deploy.caffemodel`: Weight matrix for the pre-trained neural network (21 unique target classes)[cite: 1].
- `requirements.txt`: Complete tracking file for external framework packages[cite: 1].
- `screenshots/`: Directory containing target execution verification files[cite: 1].

---

## ⚡ Environmental Prerequisites & Dependencies
To run the live dynamic OCR engine successfully, the system requires the underlying Tesseract binary executable engine to be installed locally on the host machine.

### 🛠️ Step 1: Install Core Tesseract Engine (Windows)
1. Download the executable installer from the official UB Mannheim Tesseract Repository.
2. Install the program using standard configuration paths. The default integration vector mapped in `main.py` is:
   `C:\Program Files\Tesseract-OCR\tesseract.exe`

### 💻 Step 2: Initialize System Environment
Activate your virtual terminal partition[cite: 1] and run package sync distributions:
```powershell
# 1. Activate Environment Partition
venv\Scripts\activate

# 2. Sync Package Matrix
pip install -r requirements.txt

# 3. Boot Core Application
python main.py