import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from datetime import datetime
import re

# -------------------------------
# Chatbot Logic (Backend)
# -------------------------------

class RuleBasedChatbot:
    def __init__(self):
        # Static responses mapping
        self.responses = {
            # Greetings
            "hello": "Hello! Nice to meet you.",
            "hi": "Hi there! How can I help you today?",
            "hey": "Hey! Welcome to DecodeLabs.",
            "good morning": "Good morning! Hope you're having a great day.",
            "good afternoon": "Good afternoon! How can I assist you?",
            "good evening": "Good evening! Nice to see you.",
            
            # Identity/About
            "who are you": "I am a Rule-Based AI Chatbot developed for DecodeLabs Project 1.",
            "what is your name": "My name is DecodeBot. I'm your AI assistant.",
            "tell me about yourself": "I'm DecodeBot, a rule-based chatbot created using Python and Tkinter.",
            
            # Help Menu
            "help": """Available commands:
• Hello, Hi, Hey - Greetings
• Who are you, What is your name - About me
• Date, Time - Current date and time
• Thanks, Thank you - Gratitude responses
• Help - Show this menu
• Exit, Quit, Bye - Close the chatbot""",
            
            # Gratitude
            "thanks": "You're welcome! Happy to help.",
            "thank you": "My pleasure! Feel free to ask anything.",
            "thankyou": "You're welcome! Have a great day.",
            "thx": "Anytime! I'm here to help.",
            
            # Farewell
            "bye": "Goodbye! Have a wonderful day.",
            "goodbye": "See you later! Take care.",
            "exit": "Goodbye! Thanks for chatting with me.",
            "quit": "Quitting now. Have a nice day!",
            
            # User state
            "how are you": "I'm just a program, but I'm functioning perfectly! How about you?",
            "what can you do": "I can chat with you, tell you the date and time, respond to greetings, and help with basic queries.",
            
            # Fun
            "tell me a joke": "Why do programmers prefer dark mode? Because light attracts bugs! 😄",
            "joke": "What do you call a fake noodle? An Impasta! 🍝",
            
            # Default
            "default": "I'm not sure I understand. Type 'help' to see what I can do!"
        }
        self.session_count = 0
        
    def get_response(self, user_input):
        """Get response based on user input using refined rule-based matching"""
        self.session_count += 1
        
        # Clean the input
        cleaned_input = user_input.strip().lower()
        cleaned_input = re.sub(r'[^\w\s]', '', cleaned_input) # Remove punctuation
        
        # 1. Check for dynamic content triggers (Date & Time)
        if any(x in cleaned_input for x in ["date", "what is the date", "current date"]):
            return f"Today's Date is {datetime.now().strftime('%d %B %Y')}"
            
        if any(x in cleaned_input for x in ["time", "what is the time", "current time"]):
            return f"Current Time is {datetime.now().strftime('%I:%M %p')}"
            
        # 2. Check for Exact Match
        if cleaned_input in self.responses:
            return self.responses[cleaned_input]
            
        # 3. Check for multi-word phrase containment to prevent collision errors
        for key, response in self.responses.items():
            if key != "default" and len(key.split()) > 1 and key in cleaned_input:
                return response
                
        # 4. Check individual word matches safely
        words = cleaned_input.split()
        for word in words:
            if word in self.responses and word != "default" and word not in ["hi", "he"]:
                return self.responses[word]
                
        return self.responses["default"]
    
    def get_session_count(self):
        return self.session_count


# -------------------------------
# Premium GUI Application
# -------------------------------

class PremiumChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.chatbot = RuleBasedChatbot()
        self.is_session_active = True
        
        # Setup Window Frame Configs
        self.root.title("DecodeLabs Rule-Based AI Chatbot")
        self.root.geometry("850x650")
        self.root.configure(bg="#121212")
        self.root.resizable(True, True)
        
        # System UI Font Styles
        self.header_font = font.Font(family="Consolas", size=16, weight="bold")
        self.chat_font = font.Font(family="Consolas", size=11)
        self.input_font = font.Font(family="Consolas", size=12)
        self.status_font = font.Font(family="Consolas", size=10)
        
        # Construct Component Interfaces
        self.create_header()
        self.create_chat_area()
        self.create_input_area()
        self.create_status_bar()
        
        # Input Controls Routing Bindings
        self.root.bind('<Return>', lambda event: self.send_message())
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.center_window()
        self.display_welcome()
        
    def center_window(self):
        self.root.update_idletasks()
        width, height = 850, 650
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_header(self):
        header_frame = tk.Frame(self.root, bg="#1e1e1e", height=60, bd=0)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="DECODELABS CHAT UTILITY V1.0",
            bg="#1e1e1e",
            fg="#00ff66",
            font=self.header_font
        )
        title.pack(side="left", padx=20, expand=False)
        
    def create_chat_area(self):
        chat_container = tk.Frame(self.root, bg="#121212", padx=15, pady=5)
        chat_container.pack(fill="both", expand=True)
        
        self.chat_area = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=self.chat_font,
            bg="#181818",
            fg="#ffffff",
            insertbackground="#ffffff",
            padx=15,
            pady=15,
            relief="solid",
            borderwidth=1,
            highlightbackground="#2d2d2d"
        )
        self.chat_area.pack(fill="both", expand=True)
        
        # Setup output formatting tags
        self.chat_area.tag_config("title_head", foreground="#00ff66", font=("Consolas", 12, "bold"))
        self.chat_area.tag_config("user_label", foreground="#33b5ff", font=("Consolas", 11, "bold"))
        self.chat_area.tag_config("user_msg", foreground="#ffffff", font=("Consolas", 11))
        self.chat_area.tag_config("bot_label", foreground="#ffca28", font=("Consolas", 11, "bold"))
        self.chat_area.tag_config("bot_msg", foreground="#e0e0e0", font=("Consolas", 11))
        self.chat_area.tag_config("system_alert", foreground="#ff5252", font=("Consolas", 11, "italic"))
        self.chat_area.tag_config("decorations", foreground="#444444", font=("Consolas", 11))
        
        self.chat_area.config(state="disabled")
        
    def create_input_area(self):
        input_container = tk.Frame(self.root, bg="#121212", padx=15, pady=10)
        input_container.pack(fill="x")
        
        input_frame = tk.Frame(input_container, bg="#1e1e1e", bd=1, relief="solid")
        input_frame.pack(fill="x")
        
        prompt_label = tk.Label(
            input_frame,
            text=" You > ",
            bg="#1e1e1e",
            fg="#33b5ff",
            font=("Consolas", 12, "bold")
        )
        prompt_label.pack(side="left", padx=5)
        
        self.entry = tk.Entry(
            input_frame,
            font=self.input_font,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="#33b5ff",
            relief="flat",
            bd=0
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=10)
        
        send_btn = tk.Button(
            input_frame,
            text="[SEND]",
            bg="#222222",
            fg="#00ff66",
            activebackground="#333333",
            activeforeground="#00ff66",
            font=("Consolas", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            cursor="hand2",
            command=self.send_message
        )
        send_btn.pack(side="right", fill="y")
        
        self.entry.focus()
        
    def create_status_bar(self):
        self.status_frame = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=4)
        self.status_frame.pack(fill="x")
        
        self.status_left = tk.Label(
            self.status_frame,
            text="● Engine: Connected",
            bg="#1e1e1e",
            fg="#00ff66",
            font=self.status_font
        )
        self.status_left.pack(side="left")
        
        self.status_right = tk.Label(
            self.status_frame,
            text="Interactions Counter: 0",
            bg="#1e1e1e",
            fg="#888888",
            font=self.status_font
        )
        self.status_right.pack(side="right")
        
    def display_welcome(self):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, "=======================================================\n", "decorations")
        self.chat_area.insert(tk.END, "        DECODELABS RULE-BASED AI CHATBOT\n", "title_head")
        self.chat_area.insert(tk.END, "=======================================================\n", "decorations")
        self.chat_area.insert(tk.END, "Hello! I am DecodeBot.\n", "bot_msg")
        self.chat_area.insert(tk.END, "Type 'help' to see available commands.\n", "bot_msg")
        self.chat_area.insert(tk.END, "Type 'exit' anytime to close the chatbot.\n", "bot_msg")
        self.chat_area.insert(tk.END, "=======================================================\n\n", "decorations")
        self.chat_area.config(state="disabled")
        
    def send_message(self):
        if not self.is_session_active:
            return
            
        user_input = self.entry.get().strip()
        if not user_input:
            return
            
        self.entry.delete(0, tk.END)
        
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, "You : ", "user_label")
        self.chat_area.insert(tk.END, f"{user_input}\n\n", "user_msg")
        
        # Get Bot response
        bot_response = self.chatbot.get_response(user_input)
        
        self.chat_area.insert(tk.END, "Bot : ", "bot_label")
        self.chat_area.insert(tk.END, f"{bot_response}\n\n", "bot_msg")
        
        # Update metrics count
        session_count = self.chatbot.get_session_count()
        self.status_right.config(text=f"Interactions Counter: {session_count}")
        
        # Intercept termination patterns
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            self.chat_area.insert(tk.END, f"Bot : Total messages in this session: {session_count}\n", "system_alert")
            self.chat_area.insert(tk.END, "=======================================================\n", "decorations")
            self.is_session_active = False
            self.entry.config(state="disabled")
            self.status_left.config(text="● Engine: Terminated", fg="#ff5252")
            
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)
        
    def on_closing(self):
        if not self.is_session_active:
            self.root.destroy()
        elif messagebox.askokcancel("Quit Application", "Are you sure you want to close the window?"):
            self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = PremiumChatbotGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"[Runtime Fatal Exception] Info: {e}")