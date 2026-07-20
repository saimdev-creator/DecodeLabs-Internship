"""
Project Name: AI Recommendation Logic — Premium Tech Stack Recommender (Project 3)
Developer: Muhammad Saim Rizwan (BS Computer Science Student)
Training Program: DecodeLabs AI Industrial Training — Batch 2026
Technology: Python 3, Pandas, Scikit-Learn (TF-IDF + Cosine Similarity), Tkinter
Description: End-to-end content-based filtering recommendation engine with a
             clean, professional dark-mode desktop interface built on native
             Tkinter widgets (no external UI dependencies required).
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, font
import tkinter.scrolledtext as scrolledtext
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==============================================================================
#  RECOMMENDATION ENGINE — CONTENT-BASED FILTERING (TF-IDF + COSINE SIMILARITY)
# ==============================================================================
class ContentBasedRecommenderEngine:
    """
    Encapsulates the machine learning pipeline. Responsible for loading the
    job-role dataset, vectorizing the 'Required Skills' column with TF-IDF,
    and scoring a user's skill-set against every role via cosine similarity.
    """

    def __init__(self, csv_path: str = "raw_skills.csv"):
        self.csv_path = csv_path
        self.vectorizer = TfidfVectorizer()
        self.df = None
        self.tfidf_matrix = None
        self._load_and_vectorize_dataset()

    def _load_and_vectorize_dataset(self):
        """Loads the dataset from disk and fits the TF-IDF vector space."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(
                f"Dataset not found: '{self.csv_path}'. "
                f"Place it in the same folder as this script."
            )
        self.df = pd.read_csv(self.csv_path)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["Required Skills"])

    def generate_top_n_recommendations(self, user_skills_list, top_n: int = 3):
        """
        Given a list of user-provided skills, returns the top-N closest
        job roles ranked by cosine similarity score (0.0 - 1.0).
        """
        user_joined_string = " ".join(user_skills_list)
        user_vector = self.vectorizer.transform([user_joined_string])
        similarity_scores = cosine_similarity(user_vector, self.tfidf_matrix).flatten()

        results_df = self.df.copy()
        results_df["Match Score"] = similarity_scores
        top_matches = results_df.sort_values(by="Match Score", ascending=False).head(top_n)

        recommendations = []
        for _, row in top_matches.iterrows():
            recommendations.append({
                "role": row["Job Role"],
                "score": float(row["Match Score"]),
                "core_tags": row["Required Skills"],
            })
        return recommendations


# ==============================================================================
#  DESIGN TOKENS — CENTRALIZED THEME (single source of truth for styling)
# ==============================================================================
class Theme:
    BG              = "#0f1115"   # app background
    SURFACE         = "#161922"   # panels / header / footer
    CARD            = "#1c202b"   # recommendation cards
    CARD_BORDER     = "#262b38"
    INPUT_BG        = "#12141a"
    BORDER          = "#262b38"

    ACCENT          = "#6366f1"   # primary indigo accent
    ACCENT_HOVER    = "#4f52d6"
    ACCENT_SOFT     = "#232544"   # accent tint for badges

    SUCCESS         = "#34d399"
    DANGER          = "#f87171"
    WARNING         = "#fbbf24"

    TEXT_PRIMARY    = "#f5f6fa"
    TEXT_SECONDARY  = "#9aa1b2"
    TEXT_MUTED      = "#5c6478"

    FONT_FAMILY     = "Segoe UI"
    MONO_FAMILY     = "Consolas"


# ==============================================================================
#  GUI — PREMIUM PROFESSIONAL DESKTOP WORKSPACE
# ==============================================================================
class TechStackRecommenderApp:
    """Main application window: input deck, results dashboard, telemetry log."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.theme = Theme

        try:
            self.engine = ContentBasedRecommenderEngine()
        except Exception as startup_error:
            messagebox.showerror("Startup Error", str(startup_error))
            self.root.destroy()
            return

        self._configure_window()
        self._load_fonts()
        self._build_header()
        self._build_input_panel()

        self.workspace = tk.Frame(self.root, bg=self.theme.BG)
        self.workspace.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        self._build_empty_state()
        self._build_footer()
        self._center_window()

    # ---------------------------------------------------------------- setup
    def _configure_window(self):
        self.root.title("Tech Stack Recommender — DecodeLabs AI Training, Project 3")
        self.root.geometry("1080x780")
        self.root.minsize(880, 640)
        self.root.configure(bg=self.theme.BG)

    def _load_fonts(self):
        t = self.theme
        self.f_title      = font.Font(family=t.FONT_FAMILY, size=16, weight="bold")
        self.f_subtitle   = font.Font(family=t.FONT_FAMILY, size=9)
        self.f_section    = font.Font(family=t.FONT_FAMILY, size=12, weight="bold")
        self.f_card_role  = font.Font(family=t.FONT_FAMILY, size=13, weight="bold")
        self.f_label_bold = font.Font(family=t.FONT_FAMILY, size=9, weight="bold")
        self.f_body       = font.Font(family=t.FONT_FAMILY, size=10)
        self.f_small      = font.Font(family=t.FONT_FAMILY, size=8)
        self.f_badge      = font.Font(family=t.FONT_FAMILY, size=10, weight="bold")
        self.f_mono       = font.Font(family=t.MONO_FAMILY, size=9)

    def _center_window(self):
        self.root.update_idletasks()
        w, h = 1080, 780
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # --------------------------------------------------------------- header
    def _build_header(self):
        t = self.theme
        header = tk.Frame(self.root, bg=t.SURFACE, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        border = tk.Frame(self.root, bg=t.BORDER, height=1)
        border.pack(fill="x")

        text_box = tk.Frame(header, bg=t.SURFACE)
        text_box.pack(side="left", padx=24, pady=12)

        tk.Label(text_box, text="Tech Stack Recommender", bg=t.SURFACE,
                 fg=t.TEXT_PRIMARY, font=self.f_title, anchor="w").pack(anchor="w")
        tk.Label(text_box, text="Content-based career matching · TF-IDF + Cosine Similarity",
                 bg=t.SURFACE, fg=t.TEXT_SECONDARY, font=self.f_subtitle, anchor="w").pack(anchor="w")

        badge = tk.Label(header, text="PROJECT 3", bg=t.ACCENT_SOFT, fg=t.ACCENT,
                          font=self.f_label_bold, padx=10, pady=4)
        badge.pack(side="right", padx=24)

    # ---------------------------------------------------------- input panel
    def _build_input_panel(self):
        t = self.theme
        panel = tk.Frame(self.root, bg=t.SURFACE, highlightbackground=t.BORDER,
                          highlightthickness=1)
        panel.pack(fill="x", padx=24, pady=16)

        inner = tk.Frame(panel, bg=t.SURFACE)
        inner.pack(fill="x", padx=20, pady=16)

        # Left: guidance copy
        guidance = tk.Frame(inner, bg=t.SURFACE)
        guidance.pack(side="left", fill="y")
        tk.Label(guidance, text="Your skill set", bg=t.SURFACE, fg=t.TEXT_PRIMARY,
                 font=self.f_label_bold, anchor="w").pack(anchor="w")
        tk.Label(guidance, text="Enter at least 3 comma-separated skills for an accurate match.",
                 bg=t.SURFACE, fg=t.TEXT_MUTED, font=self.f_small, anchor="w").pack(anchor="w", pady=(2, 0))

        # Right: entry + action button
        controls = tk.Frame(inner, bg=t.SURFACE)
        controls.pack(side="right")

        entry_wrap = tk.Frame(controls, bg=t.INPUT_BG, highlightbackground=t.BORDER,
                               highlightthickness=1)
        entry_wrap.pack(side="left", padx=(0, 10))

        self.skills_entry = tk.Entry(
            entry_wrap, width=38, bg=t.INPUT_BG, fg=t.TEXT_PRIMARY,
            insertbackground=t.TEXT_PRIMARY, relief="flat", font=self.f_body,
            highlightthickness=0, bd=0,
        )
        self.skills_entry.pack(padx=10, pady=8)
        self.skills_entry.insert(0, "Python, Cloud Computing, Automation")
        self.skills_entry.bind("<Return>", lambda e: self._run_recommendation())
        self.skills_entry.bind(
            "<FocusIn>", lambda e: entry_wrap.configure(highlightbackground=t.ACCENT))
        self.skills_entry.bind(
            "<FocusOut>", lambda e: entry_wrap.configure(highlightbackground=t.BORDER))

        self.run_btn = tk.Button(
            controls, text="Find Matches", bg=t.ACCENT, fg="#ffffff",
            activebackground=t.ACCENT_HOVER, activeforeground="#ffffff",
            font=self.f_label_bold, relief="flat", padx=18, pady=9,
            bd=0, cursor="hand2", command=self._run_recommendation,
        )
        self.run_btn.pack(side="left")
        self.run_btn.bind("<Enter>", lambda e: self.run_btn.configure(bg=t.ACCENT_HOVER))
        self.run_btn.bind("<Leave>", lambda e: self.run_btn.configure(bg=t.ACCENT))

    # -------------------------------------------------------- empty state
    def _build_empty_state(self):
        self._clear_workspace()
        t = self.theme
        wrap = tk.Frame(self.workspace, bg=t.BG)
        wrap.pack(expand=True)

        tk.Label(wrap, text="⌁", bg=t.BG, fg=t.TEXT_MUTED,
                 font=font.Font(family=t.FONT_FAMILY, size=28)).pack()
        tk.Label(wrap, text="No matches computed yet", bg=t.BG, fg=t.TEXT_PRIMARY,
                 font=self.f_section).pack(pady=(8, 2))
        tk.Label(wrap, text="Enter your skills above and click \"Find Matches\" to begin.",
                 bg=t.BG, fg=t.TEXT_MUTED, font=self.f_body).pack()

    # --------------------------------------------------------------- footer
    def _build_footer(self):
        t = self.theme
        border = tk.Frame(self.root, bg=t.BORDER, height=1)
        border.pack(fill="x", side="bottom")

        footer = tk.Frame(self.root, bg=t.SURFACE, height=40)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        self.status_dot = tk.Label(footer, text="●", bg=t.SURFACE, fg=t.WARNING, font=self.f_body)
        self.status_dot.pack(side="left", padx=(20, 4))

        self.status_lbl = tk.Label(footer, text="Standby — vector space ready",
                                    bg=t.SURFACE, fg=t.TEXT_SECONDARY, font=self.f_small)
        self.status_lbl.pack(side="left")

        tk.Label(footer, text="Muhammad Saim Rizwan · DecodeLabs AI Industrial Training",
                 bg=t.SURFACE, fg=t.TEXT_MUTED, font=self.f_small).pack(side="right", padx=20)

    # ------------------------------------------------------------ workspace
    def _clear_workspace(self):
        for child in self.workspace.winfo_children():
            child.destroy()

    def _run_recommendation(self):
        raw_text = self.skills_entry.get().strip()
        tokens = [tok.strip() for tok in raw_text.replace(",", " ").split() if tok.strip()]

        if len(tokens) < 3:
            messagebox.showwarning(
                "More Skills Needed",
                f"Only {len(tokens)} skill(s) detected. Please provide at least 3 "
                f"for a reliable match.",
            )
            return

        matches = self.engine.generate_top_n_recommendations(tokens, top_n=3)
        self._render_results(tokens, matches)

        self.status_dot.configure(fg=self.theme.SUCCESS)
        self.status_lbl.configure(text="Top-3 recommendations computed successfully")

    def _render_results(self, tokens, matches):
        self._clear_workspace()
        t = self.theme

        tk.Label(self.workspace, text="Top Career Matches", bg=t.BG, fg=t.TEXT_PRIMARY,
                 font=self.f_section, anchor="w").pack(anchor="w", pady=(0, 12))

        cards_row = tk.Frame(self.workspace, bg=t.BG)
        cards_row.pack(fill="x")

        for i, item in enumerate(matches, start=1):
            self._build_match_card(cards_row, i, item, tokens)

        self._build_telemetry_console(tokens)

    def _build_match_card(self, parent, rank, item, tokens):
        t = self.theme
        match_pct = item["score"] * 100

        card = tk.Frame(parent, bg=t.CARD, highlightbackground=t.CARD_BORDER,
                         highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=(0 if rank == 1 else 8, 0))

        inner = tk.Frame(card, bg=t.CARD)
        inner.pack(fill="both", expand=True, padx=18, pady=16)

        # Rank + score row
        top_row = tk.Frame(inner, bg=t.CARD)
        top_row.pack(fill="x", pady=(0, 10))
        tk.Label(top_row, text=f"RANK {rank}", bg=t.ACCENT_SOFT, fg=t.ACCENT,
                  font=self.f_label_bold, padx=8, pady=3).pack(side="left")
        tk.Label(top_row, text=f"{match_pct:.1f}%", bg=t.CARD, fg=t.SUCCESS,
                  font=self.f_badge).pack(side="right")

        # Role title
        tk.Label(inner, text=item["role"], bg=t.CARD, fg=t.TEXT_PRIMARY,
                  font=self.f_card_role, anchor="w", justify="left",
                  wraplength=260).pack(fill="x", pady=(0, 10))

        # Progress bar (visual match strength indicator)
        bar_track = tk.Frame(inner, bg=t.BORDER, height=6)
        bar_track.pack(fill="x", pady=(0, 14))
        bar_track.pack_propagate(False)
        fill_width_ratio = max(0.02, min(1.0, item["score"]))
        bar_fill = tk.Frame(bar_track, bg=t.ACCENT)
        bar_fill.place(relx=0, rely=0, relheight=1, relwidth=fill_width_ratio)

        # Matched vs missing skills
        user_skills_lower = [s.lower() for s in tokens]
        matched = [tok for tok in tokens if tok.lower() in item["core_tags"].lower()]
        missing = [s for s in item["core_tags"].split() if s.lower() not in user_skills_lower]

        tk.Label(inner, text="MATCHED SKILLS", bg=t.CARD, fg=t.TEXT_MUTED,
                  font=self.f_small, anchor="w").pack(fill="x")
        tk.Label(inner, text=", ".join(matched) if matched else "None detected",
                  bg=t.CARD, fg=t.SUCCESS, font=self.f_body, anchor="w",
                  justify="left", wraplength=260).pack(fill="x", pady=(2, 10))

        tk.Label(inner, text="SUGGESTED GAPS", bg=t.CARD, fg=t.TEXT_MUTED,
                  font=self.f_small, anchor="w").pack(fill="x")
        tk.Label(inner, text=", ".join(missing) if missing else "Full alignment",
                  bg=t.CARD, fg=t.DANGER, font=self.f_body, anchor="w",
                  justify="left", wraplength=260).pack(fill="x", pady=(2, 0))

    def _build_telemetry_console(self, tokens):
        t = self.theme
        console = tk.Frame(self.workspace, bg=t.SURFACE, highlightbackground=t.BORDER,
                            highlightthickness=1)
        console.pack(fill="both", expand=True, pady=(20, 0))

        header = tk.Frame(console, bg=t.SURFACE)
        header.pack(fill="x", padx=16, pady=(12, 6))
        tk.Label(header, text="Processing Log", bg=t.SURFACE, fg=t.TEXT_PRIMARY,
                  font=self.f_label_bold).pack(side="left")

        log = scrolledtext.ScrolledText(
            console, bg=t.INPUT_BG, fg=t.TEXT_SECONDARY, font=self.f_mono,
            insertbackground=t.TEXT_PRIMARY, relief="flat", height=6,
            padx=12, pady=10, bd=0,
        )
        log.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        lines = [
            f"[INFO] Ingested {len(tokens)} skill token(s): {tokens}",
            "[INFO] Fitting query vector against TF-IDF matrix...",
            "[INFO] Computing cosine similarity across all job roles...",
            "[INFO] Sorting results by descending match score...",
            "[DONE] Top-3 recommendations rendered to dashboard.",
        ]
        for line in lines:
            log.insert(tk.END, line + "\n")
        log.config(state="disabled")


# ==============================================================================
#  ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = TechStackRecommenderApp(root)
    root.mainloop()