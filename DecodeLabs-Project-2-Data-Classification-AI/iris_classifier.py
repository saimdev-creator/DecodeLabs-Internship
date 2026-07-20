"""
Project Name: Data Classification Using AI (Project 2)
Developer: Muhammad Saim Rizwan (BS Computer Science Student)
Training Program: DecodeLabs AI Industrial Training – Batch 2026
Technology: Python 3, Scikit-Learn, Matplotlib, Tkinter GUI
Description: Complete machine learning pipeline using KNN on Iris Dataset
             featuring Feature Scaling, Train-Test Split, Elbow Method Plotting,
             and advanced matrix diagnostics evaluation.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, font
import numpy as np
import matplotlib.pyplot as plt

# Scikit-Learn ML Components
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report

# ==============================================================================
# 🧠 MACHINE LEARNING PIPELINE ENGINE
# ==============================================================================
class MLClassificationEngine:
    def __init__(self):
        # PHASE 1: INPUT & DATA UNDERSTANDING
        self.iris = load_iris()
        self.X = self.iris.data
        self.y = self.iris.target
        
        # Feature Scaling (The Gatekeeper Rule: Mean=0, Variance=1)
        self.scaler = StandardScaler()
        self.X_scaled = self.scaler.fit_transform(self.X)
        
        # PHASE 2: PROCESS & STRUCTURAL INTEGRITY SPLIT (80% Train, 20% Test)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X_scaled, self.y, test_size=0.20, random_state=42, stratify=self.y
        )
        self.optimal_k = 5 # Default fallback value until optimization

    def plot_elbow_method(self):
        """PHASE 3: TUNING THE ENGINE - Graphically locating 'The Elbow'"""
        error_rates = []
        k_values = range(1, 21) # Testing K from 1 to 20

        for k in k_values:
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(self.X_train, self.y_train)
            pred_k = knn.predict(self.X_test)
            error_rates.append(np.mean(pred_k != self.y_test))

        # Render Matplotlib Graph Plot
        plt.figure(figsize=(8, 5))
        plt.plot(k_values, error_rates, color='#00ff66', linestyle='dashed', 
                 marker='o', markerfacecolor='#ff5252', markersize=8)
        plt.title('PHASE 3: Error Rate vs. K Boundary Value (Locate The Elbow)')
        plt.xlabel('K Value (Neighbors)')
        plt.ylabel('Mean Error Rate')
        plt.xticks(k_values)
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.show()

    def run_final_pipeline(self, selected_k):
        """PHASE 4 & 5: OUTPUT, PREDICTION & RECOGNITION DIAGNOSTICS"""
        self.optimal_k = selected_k
        
        # Initialize and Train Model with selected K
        model = KNeighborsClassifier(n_neighbors=self.optimal_k)
        model.fit(self.X_train, self.y_train)
        
        # Generate Predictions
        predictions = model.predict(self.X_test)
        
        # Extract Calculations
        matrix = confusion_matrix(self.y_test, predictions)
        report = classification_report(self.y_test, predictions, target_names=self.iris.target_names)
        
        return matrix, report

# ==============================================================================
# 🎨 PREMIUM INDUSTRIAL WORKSPACE GUI
# ==============================================================================
class DecodeLabsMLGUI:
    def __init__(self, root):
        self.root = root
        self.engine = MLClassificationEngine()
        
        # Main Window Configurations
        self.root.title("DecodeLabs AI Industrial Training 2026 — Project 2")
        self.root.geometry("900x700") 
        self.root.configure(bg="#121212")
        
        # Layout Typographies
        self.title_font = font.Font(family="Consolas", size=14, weight="bold")
        self.console_font = font.Font(family="Consolas", size=11)
        self.ui_font = font.Font(family="Consolas", size=10)

        # Assemble Functional Areas
        self.build_header()
        self.build_control_panel()
        self.build_diagnostic_console()
        self.build_status_strip()
        
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        w, h = 900, 700
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def build_header(self):
        header = tk.Frame(self.root, bg="#1a1a1a", height=55, bd=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_lbl = tk.Label(
            header, 
            text="🤖 DECODELABS SUPERVISED DATA CLASSIFICATION ENGINE v1.0", 
            bg="#1a1a1a", 
            fg="#00ff66", 
            font=self.title_font
        )
        title_lbl.pack(side="left", padx=20)

    def build_control_panel(self):
        panel = tk.Frame(self.root, bg="#1e1e1e", bd=1, relief="solid", padx=15, pady=15)
        panel.pack(fill="x", padx=15, pady=10)

        # Dataset Diagnostic Overview Left Frame
        info_text = "📊 DATASET SNAPSHOT:\n• Target Samples: 150 Total (Balanced)\n• Dimensions: 4 Features Scaling Enabled\n• Nominal Classes: Setosa, Versicolor, Virginica"
        lbl_info = tk.Label(panel, text=info_text, bg="#1e1e1e", fg="#ffffff", font=self.ui_font, justify="left")
        lbl_info.pack(side="left", anchor="w")

        # Operations Right Frame
        btn_frame = tk.Frame(panel, bg="#1e1e1e")
        btn_frame.pack(side="right", fill="y")

        btn_elbow = tk.Button(
            btn_frame, text="[1. PLOT ELBOW GRAPH]", bg="#252525", fg="#ffca28",
            activebackground="#333333", activeforeground="#ffca28", font=self.ui_font,
            relief="solid", bd=1, padx=10, pady=5, cursor="hand2", command=self.engine.plot_elbow_method
        )
        btn_elbow.pack(fill="x", pady=2)

        # K-Value Selection Configuration Row
        k_row = tk.Frame(btn_frame, bg="#1e1e1e")
        k_row.pack(fill="x", pady=4)

        lbl_k = tk.Label(k_row, text="Select Target 'K' Value: ", bg="#1e1e1e", fg="#ffffff", font=self.ui_font)
        lbl_k.pack(side="left")

        self.k_spinner = tk.Spinbox(k_row, from_=1, to=20, width=5, bg="#1a1a1a", fg="#00ff66", 
                                    insertbackground="#ffffff", buttonbackground="#252525", relief="solid", font=self.ui_font)
        self.k_spinner.delete(0, "end")
        self.k_spinner.insert(0, "5") # Default value initialization
        self.k_spinner.pack(side="left", padx=5)

        btn_train = tk.Button(
            btn_frame, text="[2. EXECUTE DATA PIPELINE]", bg="#252525", fg="#00ff66",
            activebackground="#333333", activeforeground="#00ff66", font=self.ui_font,
            relief="solid", bd=1, padx=10, pady=5, cursor="hand2", command=self.execute_ml_pipeline
        )
        btn_train.pack(fill="x", pady=2)

    def build_diagnostic_console(self):
        container = tk.Frame(self.root, bg="#121212", padx=15, pady=5)
        container.pack(fill="both", expand=True)

        lbl_title = tk.Label(container, text="📋 SYSTEM DIAGNOSTICS LOG OUTPUT", bg="#121212", fg="#888888", font=self.ui_font)
        lbl_title.pack(anchor="w", pady=(0,5))

        self.console = scrolledtext.ScrolledText(
            container, wrap=tk.WORD, font=self.console_font, bg="#181818", fg="#ffffff",
            insertbackground="#ffffff", padx=15, pady=15, relief="solid", bd=1, highlightbackground="#2d2d2d"
        )
        self.console.pack(fill="both", expand=True)
        self.console.config(state="disabled")

    def build_status_strip(self):
        strip = tk.Frame(self.root, bg="#1a1a1a", padx=20, pady=5)
        strip.pack(fill="x")

        self.status_left = tk.Label(strip, text="● ML Pipeline status: System Awaiting Operational Sequence", bg="#1a1a1a", fg="#ffca28", font=self.ui_font)
        self.status_left.pack(side="left")

        developer_lbl = tk.Label(strip, text="Dev: M. Saim Rizwan (Batch 2026)", bg="#1a1a1a", fg="#888888", font=self.ui_font)
        developer_lbl.pack(side="right")

    def log_text(self, clean_message):
        self.console.config(state="normal")
        self.console.insert(tk.END, clean_message)
        self.console.config(state="disabled")
        self.console.see(tk.END)

    def execute_ml_pipeline(self):
        try:
            target_k = int(self.k_spinner.get())
        except ValueError:
            messagebox.showerror("Validation Error", "Please parse a valid numerical integer constraint for parameters.")
            return

        # Execute machine training and diagnostics retrieval
        matrix, classification_report_out = self.engine.run_final_pipeline(target_k)

        # Clear active interface console logs
        self.console.config(state="normal")
        self.console.delete(1.0, tk.END)
        self.console.config(state="disabled")

        # Format layout print sequences mapped onto output structures
        self.log_text("=======================================================================\n")
        self.log_text(f"🚀 PIPELINE LOG RUNTIME: SUCCESFULLY COMMITTED ARCHITECTURE WITH K = {target_k}\n")
        self.log_text("=======================================================================\n\n")
        
        self.log_text("📊 CONFUSION MATRIX DIAGNOSTICS LAYER:\n")
        self.log_text("-----------------------------------------------------------------------\n")
        self.log_text(f"  [Setosa]     Correctly Predicted: {matrix[0][0]} | Missed: {matrix[0][1] + matrix[0][2]}\n")
        self.log_text(f"  [Versicolor] Correctly Predicted: {matrix[1][1]} | Missed: {matrix[1][0] + matrix[1][2]}\n")
        self.log_text(f"  [Virginica]  Correctly Predicted: {matrix[2][2]} | Missed: {matrix[2][0] + matrix[2][1]}\n")
        self.log_text("-----------------------------------------------------------------------\n")
        self.log_text(f"Raw Array Notation:\n{matrix}\n\n\n")

        self.log_text("📈 MATHEMATICAL STRATEGIC EVALUATION (PRECISION, RECALL, F1-SCORE):\n")
        self.log_text("-----------------------------------------------------------------------\n")
        self.log_text(classification_report_out)
        self.log_text("=======================================================================\n")
        self.log_text("🟢 PIPELINE PROCESS SUCCESSFUL: Milestone verified for DecodeLabs Portfolio.\n")
        self.log_text("=======================================================================\n")

        self.status_left.config(text=f"● ML Pipeline status: Execution Complete (Optimal K={target_k})", fg="#00ff66")

# ==============================================================================
# ENTRY APPLICATION POINT INVOCATION
# ==============================================================================
if __name__ == "__main__":
    try:
        app_context = tk.Tk()
        app_instance = DecodeLabsMLGUI(app_context)
        app_context.mainloop()
    except Exception as execution_error:
        print(f"[FATAL ML ERROR] Execution halted abruptly: {execution_error}")