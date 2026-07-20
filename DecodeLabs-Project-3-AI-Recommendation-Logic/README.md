# 🎯 Project 3: AI Recommendation Logic
### Building the Digital Matchmaker — From Raw Preferences to Intelligent Recommendations

This repository artifact contains the complete engineering workflow for **Project 3**, developed as part of the **DecodeLabs AI Industrial Training Program (Batch 2026)**. It features a standalone production-grade content-based recommendation system designed to mitigate choice overload by mapping user skill matrices straight onto logical career trajectories.

---

## 📌 Architectural Core Concepts

Unlike classification paradigms that mapping categorical groups reactively, this engine deploys **Active Prediction** algorithms driving client-side personalized recommendations.

### 🧠 Content-Based Filtering Approach
- **The Justification:** Built specifically to eliminate the **User Cold Start** Achilles' heel without requiring massive community behavioral dataset history.
- **The Mechanism:** Operates directly on core item profiles (Job Roles) and maps target user vectors exclusively to identical attribute structures.

### 📐 Feature Vector Math & Weighting Models
- **Vector Space Mapping:** Translates qualitative string objects into quantitative numeric vectors to bypass natural language processing boundaries.
- **TF-IDF Paradigm:** Upgrades from basic binary overlapping checks to **Term Frequency-Inverse Document Frequency (TF-IDF)** matrix weighting. This dampens common generic words logarithmically while emphasizing unique, highly descriptive technology tags (e.g., `AWS`, `Automation`).
- **Cosine Similarity Engine:** Evaluates distance orientation via the cosine angle formula:
  $$\cos(\theta) = \frac{A \cdot B}{\Vert{}A\Vert{} \Vert{}B\Vert{}}$$
  This returns an absolute normalized correlation value between $0.0$ and $1.0$, rendering a natural percentage match invariant to text length distribution scales.

---

## 🚀 The 4-Step Ranking Assembly Line

1. **Ingestion Layer:** Captures the current user state via interface fields requiring a baseline density constraint of at least 3 token inputs.
2. **Scoring Layer:** Runs iterative similarity computations comparing the processed query array against rows in `raw_skills.csv`.
3. **Sorting Layer:** Cascades raw floats into a descending data layout structure pushing high-affinity items to the top stack.
4. **Filtering Layer:** Truncates records past the threshold boundary to serve an explicit **Top-3 (Top-N)** dashboard preview.

---

## 🛠️ Technology Manifest
- **Python 3**
- **Pandas:** Handles vector array modifications.
- **Scikit-Learn:** Drives the underlying `TfidfVectorizer` and mathematical `cosine_similarity` matrix calculations.
- **Tkinter (Native GUI Engine):** Renders a custom premium dark-mode desktop theme utilizing centralized token states without external interface packages.

---

## 📂 Project Directory Layout
```text
Project-3-AI-Recommendation-Logic/
│
├── tech_recommender.py     # Main Content-Based Recommender & UI Dashboard
├── raw_skills.csv          # Matrix Source Dataset (Job Roles & Skills)
├── requirements.txt        # System Dependencies Manifest File
└── screenshots/            # System Validation States
    ├── welcome.png         # Standby Workspace Screen
    ├── conversation.png    # Live Recommender Execution Logs Panel
    └── exit.png            # Validated Telemetry Metrics Output