# 🤖 Project 2: Data Classification Using AI
### From Raw Data to Intelligent Decision Making

This data engine is built as part of the **DecodeLabs Industrial Training Kit 2026 (Project 2)**. It establishes an absolute end-to-end supervised machine learning application pipeline utilizing the **K-Nearest Neighbors (KNN)** classification methodology on the classic Iris Benchmark matrix dataset.

---

## 📌 Project Overview
Instead of traditional hardcoded rule structures, this architecture processes numerical history to derive operational classification mapping boundaries dynamically. 

The application architecture effectively manages:
* **Feature Scaling Gatekeeper:** Normalizes dataset metrics utilizing `StandardScaler` transformations to establish a uniform structure ($Mean = 0, Variance = 1$).
* **Data Segment Isolation:** Shuffles dataset items and executes an explicit 80/20 train-test structural split validation.
- **Hyperparameter Tuning Control:** Implements a graphical error rate analysis component across multiple target variables to discover optimal parameter execution layers.
- **Deep Analytics Diagnostics Console:** Renders standard validation matrix evaluations directly onto a custom premium dark dashboard interface.

---

## 🚀 Key Architectural Features
- **Dictionary & Matrix Mapping:** Harnesses efficient array handling paradigms via modern data structures.
- **Input Sanitization Logic:** Performs continuous pipeline formatting tasks protecting processing steps from type mismatch faults.
- **Industrial Theme User Interface:** Sleek, high-contrast dark aesthetic built strictly with native standard Python graphical engines.

---

## 🛠 Technologies Used
- **Python 3**
- **Scikit-Learn** (Supervised Training Framework Engine)
- **Matplotlib** (Dynamic Hyperparameter Elbow Plotter)
- **NumPy** (High-Performance Scientific Vector Arrays)
- **Tkinter** (Graphical Workspace Layout Architecture)

---

## 📂 Project Directory Structure
```text
Project-2-Data-Classification-AI/
│
├── iris_classifier.py      # Core Machine Learning & GUI Application Code
├── README.md               # Project-Specific Technical Presentation
├── requirements.txt        # System Dependencies Manifest File
└── screenshots/            # Operational State Visual Identifiers
    ├── welcome.png         # System Initialization State Screen
    ├── elbow_plot.png      # Matplotlib Error Frequency Variance Graph
    ├── conversation.png    # Live Pipeline Evaluation Logs Window
    └── exit.png            # Validated Execution Success Output