import os
import sys
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pytesseract

# --- CONFIGURING TESSERACT WINDOWS BINARY VECTOR ---
# If your installation path is different, update this string variable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- PREMIUM CYBERPUNK PALETTE ---
BG_MAIN = "#0B0F19"       # Deep Void Black
BG_PANEL = "#161F33"      # Matte Navy Panel
TEXT_PRIMARY = "#FFFFFF"  # Pure White
ACCENT_CYAN = "#00F0FF"   # Electric Cyan (Detection Accent)
ACCENT_NEON = "#FF007F"   # Cyber Neon Pink (OCR Accent)
TEXT_MUTED = "#8A99AD"    # Slate Gray

class PerceptionStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 DECODELABS - PERCEPTION ENGINE v4.0")
        self.root.geometry("1280x760")
        self.root.configure(bg=BG_MAIN)
        
        # Paths for weights
        self.proto_path = "deploy.prototxt"
        self.model_path = "MobileNetSSD_deploy.caffemodel"
        
        # State Variables
        self.current_image_path = None
        self.cv_image = None
        
        # Classes for MobileNet SSD
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        
        # Initialize Deep Learning Model
        self.load_neural_network()
        
        # Build Interface
        self.create_header()
        self.create_workspace()
        self.create_status_bar()

    def load_neural_network(self):
        """Loads Caffe architecture safely with stable OpenCV 4.x support."""
        if not os.path.exists(self.proto_path) or not os.path.exists(self.model_path):
            messagebox.showerror("Model Error", f"Model files missing!\nEnsure deploy.prototxt and MobileNetSSD_deploy.caffemodel exist.")
            sys.exit(1)
        try:
            self.net = cv2.dnn.readNetFromCaffe(self.proto_path, self.model_path)
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to load Caffe Model: {str(e)}")
            sys.exit(1)

    def create_header(self):
        """Top layout bar with premium branding."""
        header = tk.Frame(self.root, bg=BG_PANEL, height=70, bd=0, highlightbackground=ACCENT_CYAN, highlightthickness=1)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="CORE PERCEPTION STUDIO", font=("Consolas", 18, "bold"), fg=ACCENT_CYAN, bg=BG_PANEL)
        title_label.pack(side=tk.LEFT, padx=25, pady=15)
        
        subtitle = tk.Label(header, text="[ OBJECT DETECTOR & TEXT RECOGNITION PIPELINE ]", font=("Consolas", 10), fg=TEXT_MUTED, bg=BG_PANEL)
        subtitle.pack(side=tk.LEFT, pady=22)

        # Main Load Action Button
        btn_browse = tk.Button(header, text="⚡ BROWSE SCENE IMAGE", font=("Consolas", 10, "bold"), 
                               bg=ACCENT_CYAN, fg=BG_MAIN, activebackground=TEXT_PRIMARY, activeforeground=BG_MAIN,
                               bd=0, padx=20, cursor="hand2", command=self.load_image)
        btn_browse.pack(side=tk.RIGHT, padx=25, pady=15)

    def create_workspace(self):
        """Builds the main side-by-side processing viewport panels."""
        self.workspace_frame = tk.Frame(self.root, bg=BG_MAIN)
        self.workspace_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure Grid Layout (50/50 division)
        self.workspace_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.workspace_frame.grid_columnconfigure(1, weight=1, uniform="equal")
        self.workspace_frame.grid_rowconfigure(0, weight=1)
        
        # --- LEFT PANEL: DETECTOR WORKSPACE ---
        left_container = tk.Frame(self.workspace_frame, bg=BG_PANEL, bd=0, highlightbackground="#1E2942", highlightthickness=1)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        lbl_left_title = tk.Label(left_container, text="NEURAL OBJECT DETECTION VIEWPORT", font=("Consolas", 11, "bold"), fg=ACCENT_CYAN, bg="#1C263E", anchor="w", padx=15, pady=8)
        lbl_left_title.pack(fill=tk.X)
        
        self.canvas_detect = tk.Canvas(left_container, bg=BG_MAIN, bd=0, highlightthickness=0)
        self.canvas_detect.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        btn_detect = tk.Button(left_container, text="RUN MODEL DETECTION", font=("Consolas", 11, "bold"), 
                               bg="#1F2E4D", fg=ACCENT_CYAN, activebackground=ACCENT_CYAN, activeforeground=BG_MAIN,
                               bd=1, relief="solid", highlightbackground=ACCENT_CYAN, pady=10, cursor="hand2", command=self.run_detection)
        btn_detect.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=15)

        # --- RIGHT PANEL: OCR TEXT RECOGNITION ---
        right_container = tk.Frame(self.workspace_frame, bg=BG_PANEL, bd=0, highlightbackground="#1E2942", highlightthickness=1)
        right_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        lbl_right_title = tk.Label(right_container, text="OPTICAL CHARACTER RECOGNITION (OCR)", font=("Consolas", 11, "bold"), fg=ACCENT_NEON, bg="#1C263E", anchor="w", padx=15, pady=8)
        lbl_right_title.pack(fill=tk.X)
        
        # Upper Display for Document preview
        self.canvas_ocr = tk.Canvas(right_container, bg=BG_MAIN, bd=0, highlightthickness=0, height=250)
        self.canvas_ocr.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Real-Time Output Console Panel
        lbl_console = tk.Label(right_container, text="EXTRACTED STRING ENGINE OUTPUT:", font=("Consolas", 9, "bold"), fg=TEXT_MUTED, bg=BG_PANEL, anchor="w")
        lbl_console.pack(fill=tk.X, padx=15, pady=(5,0))
        
        self.txt_ocr_output = tk.Text(right_container, bg=BG_MAIN, fg=TEXT_PRIMARY, insertbackground=ACCENT_NEON, font=("Consolas", 10), bd=1, relief="solid", highlightbackground="#1E2942", height=8)
        self.txt_ocr_output.pack(fill=tk.X, padx=15, pady=(5,10))
        
        btn_ocr = tk.Button(right_container, text="RUN OCR EXTRACTION", font=("Consolas", 11, "bold"), 
                            bg="#1F2E4D", fg=ACCENT_NEON, activebackground=ACCENT_NEON, activeforeground=BG_MAIN,
                            bd=1, relief="solid", highlightbackground=ACCENT_NEON, pady=10, cursor="hand2", command=self.run_ocr)
        btn_ocr.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=15)

    def create_status_bar(self):
        """Sleek bottom status reporter."""
        self.status_frame = tk.Frame(self.root, bg=BG_PANEL, height=30, bd=0)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.lbl_status = tk.Label(self.status_frame, text="SYSTEM READY // Connect a sample image matrix to initialize.", font=("Consolas", 9), fg=TEXT_MUTED, bg=BG_PANEL, anchor="w", padx=20)
        self.lbl_status.pack(fill=tk.X, pady=5)

    def load_image(self):
        """Secure file dialog vector to load any CV/PIL supported format."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")])
        if not file_path:
            return
            
        self.current_image_path = file_path
        self.cv_image = cv2.imread(file_path)
        
        # Clear fields
        self.txt_ocr_output.delete("1.0", tk.END)
        
        # Display image across both Viewport Canvas structures
        self.render_image_on_canvas(self.cv_image, self.canvas_detect)
        self.render_image_on_canvas(self.cv_image, self.canvas_ocr)
        self.update_status(f"Matrix Connected Successfully: {os.path.basename(file_path)}")

    def render_image_on_canvas(self, cv_img, canvas):
        """Autoscale and anchor rendering pipelines safely onto TK Canvas grids with layout updates."""
        canvas.delete("all")
        self.root.update_idletasks()
        
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1: canvas_width = 570
        if canvas_height <= 1: canvas_height = 420
        
        h, w, _ = cv_img.shape
        scale = min(canvas_width/w, canvas_height/h)
        nw, nh = int(w * scale), int(h * scale)
        
        resized = cv2.resize(cv_img, (nw, nh), interpolation=cv2.INTER_AREA)
        rgb_img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        pil_img = Image.fromarray(rgb_img)
        tk_img = ImageTk.PhotoImage(image=pil_img)
        
        if canvas == self.canvas_detect:
            self._img_ref1 = tk_img
            canvas.create_image(canvas_width//2, canvas_height//2, image=self._img_ref1, anchor=tk.CENTER)
        else:
            self._img_ref2 = tk_img
            canvas.create_image(canvas_width//2, canvas_height//2, image=self._img_ref2, anchor=tk.CENTER)
            
        canvas.update()

    def run_detection(self):
        """Executes MobileNet-SSD Caffe Blob forward pass processing."""
        if self.cv_image is None:
            messagebox.showwarning("Data Missing", "Please load an image before executing detection.")
            return
            
        self.update_status("Forward pass active // computing deep neural vectors...")
        self.root.update_idletasks()
        
        h, w = self.cv_image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(self.cv_image, (300, 300)), 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        
        output_img = self.cv_image.copy()
        detected_count = 0
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])
                label_text = self.CLASSES[idx]
                detected_count += 1
                
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                
                cv2.rectangle(output_img, (startX, startY), (endX, endY), (255, 240, 0), 2)
                text_y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.putText(output_img, f"{label_text.upper()} [{confidence*100:.1f}%]", (startX, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 240, 0), 2)
        
        self.render_image_on_canvas(output_img, self.canvas_detect)
        self.update_status(f"Detection pipeline resolved. Targets locked: {detected_count}")

    def run_ocr(self):
        """Runs true Optical Character Recognition using pytesseract engine."""
        if self.cv_image is None:
            messagebox.showwarning("Data Missing", "Please load an image matrix before running OCR parser.")
            return
            
        self.update_status("Parsing localized regions of interest for structural text strings...")
        self.root.update_idletasks()
        
        self.txt_ocr_output.delete("1.0", tk.END)
        
        try:
            # Converting CV BGR Matrix to PIL Image for Tesseract Ingestion
            rgb_img = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_img)
            
            # Running the extraction engine pass
            extracted_text = pytesseract.image_to_string(pil_img)
            
            # Formatting and cleaning the string output
            if not extracted_text.strip():
                extracted_text = "--- OCR WARNING ---\nExtraction completed but no readable alphanumeric characters were isolated inside the matrix."
            
            self.txt_ocr_output.insert(tk.END, extracted_text)
            self.update_status("OCR Live Processing Pipeline Resolved Successfully.")
            
        except Exception as e:
            error_msg = f"--- OCR ENGINE ERROR ---\nFailed to compute image text analysis matrix.\nReason: {str(e)}\n\nEnsure Tesseract software installer is set up on Windows."
            self.txt_ocr_output.insert(tk.END, error_msg)
            self.update_status("OCR pipeline broken. Check configuration logs.")

    def update_status(self, text):
        self.lbl_status.config(text=f"SYSTEM LOG // {text.upper()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PerceptionStudio(root)
    root.mainloop()