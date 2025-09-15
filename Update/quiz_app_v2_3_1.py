# main.py
import os
import csv
import random
import time
from datetime import datetime
from typing import Optional, Dict, List, Any
import google.generativeai as genai
import threading
import queue
#_____________________--------------_____________________________
import tkinter as tk
import tkinter.font as tkfont
from tkinter import StringVar, messagebox, filedialog, scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

class Settings:
    THEME = ("pulse", "minty", "simplex", "flatly", "darkly", "solar", "cyborg", "vapor")
    TITLE = "QuickRevise App    Author: BIJAY MAHTO"
    WSIZE = (950, 600)
    POS = (100, 50)
    ICON = "icon.ico"

    # --- PADDING & SIZING ---
    MIN_PAD = 2
    PAD_SMALL = 5
    PAD_MEDIUM = 10
    PAD_LARGE = 15

    INPUT_HEIGHT = 4
    MM_BTN_WIDTH = 15
    SM_BTN_WIDTH = 25
    MD_BTN_WIDTH = 35
    LG_BTN_WIDTH = 45

    # --- FONTS ---
    FONT_FAMILY = "Calibri" #"Arial"
    FONT_SEGEO_FAMILY = "Segoe UI"
    FONT_SIZE = 11
    FONT_TITLE = (FONT_FAMILY, 16, "bold")
    FONT_SUBTITLE = (FONT_FAMILY, 12, "bold")
    FONT_NORMAL = (FONT_FAMILY, FONT_SIZE)
    FONT_SEGEO = (FONT_SEGEO_FAMILY, 9)
    FONT_BUTTON = (FONT_FAMILY, 10, "bold")
    FONT_CHAT = (FONT_FAMILY, 11)
    FONT_CHAT_BOLD = (FONT_FAMILY, 11, "bold")

    # ---FONT Helvetica ---
    FONT_HELVETICA_LARGE_BOLD = ("Helvetica", 16, "bold")
    FONT_HELVETICA_14_UNDLIN = ("Helvetica", 14, "underline")
    FONT_HELVETICA_NORMAL = ("Helvetica", 10)
    FONT_HELVETICA_BOLD = ("Helvetica", 10, "bold")
    FONT_HELVETICA_ITALIC = ("Helvetica", 10, "italic")
    FONT_HELVETICA_SM_BOLD: tuple = ("Helvetica", 9, "bold")
    BUTTONS_PER_ROW = 5

    # --- COLORS & STYLES ---
    PRIMARY_COLOR = "primary"
    SUCCESS_COLOR = "success"
    INFO_COLOR = "info"
    WARNING_COLOR = "warning"
    DANGER_COLOR = "danger"
    SECONDRY_COLOR = "secondary"

    INVERSE_SECONDARY = "inverse-secondary"
    SUCCESS_OUTLINE = "primary-outline"
    DANGER_OUTLINE = "danger-outline"
    INFO_OUT = "info-outline"
    USER_TAG_COLOR = "info"
    ASSISTANT_TAG_COLOR = "success"


    MOTIVATION_LINES = (
        "Small goal today → big success tomorrow.",
        "30 minutes of focused practice every day — consistency builds champions.",
        "Speed + accuracy = results. Solve fast, then check carefully.",
        "Practice smart: short, focused sessions beat long, unfocused study.",
        "Turn mistakes into lessons — every error moves you forward.",
        "Consistency compounds — show up today, see progress tomorrow.",
        "Embrace the struggle; that's where growth happens.",
        "One more problem, one more concept, one step closer.",
        "Discipline will take you where motivation can't.",
        "Analyze your mistakes. They are your best teachers.",
        "Master the fundamentals. A strong base builds a high tower.",
        "Progress, not perfection. Just keep moving.",
        "Your only competition is who you were yesterday.",
        "Rest is part of the process. Recharge to come back stronger.",
    )


    @classmethod
    def get_random_motivation(cls):
        lines = getattr(cls, "MOTIVATION_LINES", None)
        if not lines:
            return ""
        if isinstance(lines, str):
            items = [l.strip() for l in lines.splitlines() if l.strip()]
        elif isinstance(lines, (list, tuple, set)):
            items = list(lines)
        else:
            try:
                items = list(lines)
            except Exception:
                return ""
        items = [i for i in items if isinstance(i, str) and i.strip()]
        if not items:
            return ""
        return random.choice(items)
    
    @staticmethod
    def show_toast(title: str, message: str, bootstyle: Optional[str] = None, duration: int = 3000, parent: Optional[tk.Misc] = None):
        """
        Helper to show a toast. Uses Settings.*_COLOR as default bootstyles when not provided.
        If parent is given, tries to position toast relative to parent window.
        """
        if bootstyle is None:
            bootstyle = Settings.INFO_COLOR

        position = (40, 40, "ne")
        try:
            if parent:
                x = parent.winfo_rootx() + 20
                y = parent.winfo_rooty() + 20
                position = (x, y, "ne")
        except Exception:
            # fallback to default
            position = (40, 40, "ne")

        try:
            toast = ToastNotification(
                title=title,
                message=message,
                bootstyle=bootstyle,
                duration=duration,
                position=position,
            )
            toast.show_toast()
        except Exception:
            # If toast fails (headless env etc.), fall back to messagebox
            try:
                messagebox.showinfo(title, message)
            except Exception:
                # last resort: print to console
                print(f"{title}: {message}")   

    __MAJOR = 2
    __MINOR = 2
    __PATCH = 1
    _VERSION = f"Version: {__MAJOR}.{__MINOR}.{__PATCH}"

    @classmethod
    def get_version(cls):
        return cls._VERSION


class BaseFrame(ttk.Frame):
    # --- Base and Right Panel Classes ---
    def __init__(self, master: tk.Misc, app: Optional[tk.Toplevel] = None) -> None:
        super().__init__(master)
        self.app = app if app else self.winfo_toplevel()


class QuizRightPanelFrame(BaseFrame):
    # यह क्लास अपरिवर्तित है
    def __init__(self, master: tk.Misc, app: Optional[tk.Toplevel] = None) -> None:
        super().__init__(master, app)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.q_buttons: List[ttk.Button] = []
        self.status_labels: Dict[str, ttk.Label] = {}
        self._create_widgets()

    def _create_widgets(self) -> None:
        self._status_area()
        self._section_area()
        self._bottom_buttons_area()

    def _status_area(self) -> None:
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        status_data = [
            ("Answered", "success"), ("Marked", "warning"),
            ("Not Visited", "info"), ("Marked and answered", "primary"),
            ("Not Answered", "danger")
        ]
        for i, (text, style) in enumerate(status_data):
            self._create_status_row(frame, i, text, style)
            
    def _create_status_row(self, parent: ttk.Frame, row_idx: int, text: str, style: str) -> None:
        row_frame = ttk.Frame(parent)
        row_frame.pack(anchor="w", fill="x", padx=10, pady=1)
        lbl_count = ttk.Label(row_frame, text="0", bootstyle=f"{style}-inverse", width=3, anchor='c')
        lbl_count.pack(side="left", padx=(0, 5))
        lbl_text = ttk.Label(row_frame, text=text, font=Settings.FONT_HELVETICA_NORMAL)
        lbl_text.pack(side="left")
        self.status_labels[text] = lbl_count

    def _section_area(self) -> None:
        outer_frame = ttk.Frame(self)
        outer_frame.grid(row=1, column=0, sticky="nsew", pady=5, padx=2)
        outer_frame.grid_rowconfigure(1, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)
        ttk.Label(outer_frame, text="SECTION : टेस्ट", font=("Helvetica", 10, "bold"), bootstyle="inverse-info").grid(row=0, column=0, sticky="ew", pady=2)
        canvas_frame = ttk.Frame(outer_frame)
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)
        self._canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self._canvas_window, width=e.width))
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)

    def _on_mousewheel(self, event: tk.Event) -> None:
        num = getattr(event, "num", None)
        delta = getattr(event, "delta", 0)
        if num == 4 or delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif num == 5 or delta < 0:
            self.canvas.yview_scroll(1, "units")

    def _bottom_buttons_area(self) -> None:
        frame = ttk.Frame(self)
        frame.grid(row=2, column=0, sticky="ew", pady=5, padx=2)
        frame.grid_columnconfigure(0, weight=1)
        self.quiz_load_btn = ttk.Button(frame, text="Load Quiz", bootstyle=Settings.INFO_OUT)
        self.quiz_submit_button = ttk.Button(frame, text="Submit Test", bootstyle=Settings.SUCCESS_COLOR)
        self.quiz_load_btn.pack(side="left", expand=True, fill='x', padx=5, pady=5)
        self.quiz_submit_button.pack(side="left", expand=True, fill='x', padx=5, pady=5)

    def create_question_buttons(self, total_questions: int, jump_command: callable) -> None:
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        self.q_buttons.clear()
        for i in range(total_questions):
            btn = ttk.Button(self.scroll_frame, text=str(i + 1), width=3, bootstyle="secondary-outline", command=lambda idx=i: jump_command(idx))
            btn.grid(row=i // Settings.BUTTONS_PER_ROW, column=i % Settings.BUTTONS_PER_ROW, padx=5, pady=5)
            self.q_buttons.append(btn)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_status_counts(self, counts: Dict[str, int]) -> None:
        for key, value in counts.items():
            if key in self.status_labels:
                self.status_labels[key].config(text=str(value))


class QuizAttemptLeftFrame(BaseFrame):

    def __init__(self, master: tk.Misc, app: Optional[tk.Toplevel] = None) -> None:
        super().__init__(master, app)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.right_panel: Optional[QuizRightPanelFrame] = None
        self._q_timer_id: Optional[str] = None
        self._date_after_id: Optional[str] = None
        
        # --- Quiz State ---
        self.quiz_data: List[Dict[str, Any]] = []
        self.current_q_index: int = 0
        self.selected_answers: Dict[int, str] = {}
        self.marked_for_review: set[int] = set()
        self.visited_questions: set[int] = set()
        self.shuffle_options: bool = False
        self.shuffle_questions: bool = False
        self.question_start_time: float = 0.0
        
        self.answer_var = tk.StringVar()
        
        # --- Updated Timer Logic ---
        self.is_countdown_mode: bool = False
        self.remaining_seconds: int = 0
        self.elapsed_seconds: int = 0
        self._quiz_timer_id: Optional[str] = None
        
        self._create_widgets()
        self._start_periodic_date_update()

    def _reset_quiz(self) -> None:
        """क्विज़ की स्थिति को उसकी प्रारंभिक अवस्था में रीसेट करता है।"""
        self.stop_question_timer()
        self.stop_quiz_timer()
        
        self.quiz_data.clear()
        self.selected_answers.clear()
        self.marked_for_review.clear()
        self.visited_questions.clear()
        self.current_q_index = 0
        self.answer_var.set("")
        
        self.question_start_time = 0.0
        self.is_countdown_mode = False
        self.remaining_seconds = 0
        self.elapsed_seconds = 0

        # --- नया लॉजिक: UI को रीसेट करें ---
        self.total_time_label.config(text="Total Time: 00:00")
        self.time_limit_entry.config(state="normal")
        self.time_limit_entry.delete(0, tk.END)

        self.test_name_label.config(text="Test")
        self.question_number_label.config(text="Please Load Quiz File")
        self.question_take_time_lbl.config(text="Time: 00:00")

        for w in self.scroll_frame.winfo_children():
            w.destroy()

        if self.right_panel:
            for btn in self.right_panel.q_buttons:
                btn.destroy()
            self.right_panel.q_buttons.clear()
            self.right_panel.update_status_counts({k: 0 for k in self.right_panel.status_labels})
            self.right_panel.quiz_load_btn.config(state="normal")
        
        self.mark_review.config(state="normal")
        self.clear_response.config(state="normal")
        self.btn_save_next.config(state="normal")
        self.toggle_btn.config(state="normal")

    def _create_widgets(self) -> None:
        self._top_view_area()
        self._second_tob_view_area()
        self._question_options_view_area()
        self._bottom_view_area()

    def _top_view_area(self) -> None:
        self.top_area_frame = ttk.Frame(self)
        self.top_area_frame.grid(row=0, column=0, sticky="ew")
        
        self.total_time_label = ttk.Label(self.top_area_frame, text="Total Time: 00:00", anchor="w", bootstyle=DANGER, font=Settings.FONT_HELVETICA_BOLD)
        self.total_time_label.pack(side="right", padx=10, pady=5)
        
        self.test_name_label = ttk.Label(self.top_area_frame, text="Test", anchor="e", bootstyle="primary", font=Settings.FONT_HELVETICA_BOLD)
        self.test_name_label.pack(side="left", padx=10, pady=5)
        
        self.today_date = ttk.Label(self.top_area_frame, text=self._get_today_date_str(), anchor="e", bootstyle=SUCCESS, font=Settings.FONT_HELVETICA_BOLD)
        self.today_date.pack(side="right", padx=10, pady=5)

        time_input_frame = ttk.Frame(self.top_area_frame)
        time_input_frame.pack(side="right", padx=10, pady=5)
        ttk.Label(time_input_frame, text="Time Limit (min):", font=Settings.FONT_HELVETICA_NORMAL).pack(side="left", padx=(0, 5))
        self.time_limit_entry = ttk.Entry(time_input_frame, width=5)
        self.time_limit_entry.pack(side="left")

        self.toggle_btn = ttk.Checkbutton(self.top_area_frame, text='Mode: EASY', bootstyle="round-toggle", command=self.toggle_action)
        self.toggle_btn.pack(side="right", padx=10, pady=5)

    def _second_tob_view_area(self) -> None:
        self.top_second_area_frame = ttk.Frame(self)
        self.top_second_area_frame.grid(row=1, column=0, sticky="ew")
        self.question_number_label = ttk.Label(self.top_second_area_frame, text="Please Load Quiz File", anchor="w", font=Settings.FONT_HELVETICA_BOLD)
        self.question_number_label.pack(side="left", padx=10, pady=5)
        self.question_take_time_lbl = ttk.Label(self.top_second_area_frame, text="Time: 00:00", anchor="e", bootstyle="info", font=Settings.FONT_HELVETICA_BOLD)
        self.question_take_time_lbl.pack(side="left", padx=40, pady=5)
        self.btn_quit_quiz = ttk.Button(self.top_second_area_frame, text="Quit", bootstyle="danger-outline", command=self.quit_quiz)
        self.btn_quit_quiz.pack(side="right", padx=10, pady=5)

    def _question_options_view_area(self) -> None:
        frame = ttk.Frame(self, bootstyle="light")
        frame.grid(row=2, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        canvas = tk.Canvas(frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def _bottom_view_area(self) -> None:
        frame = ttk.Frame(self)
        frame.grid(row=3, column=0, sticky="ew")
        self.mark_review = ttk.Button(frame, text="Mark for Review & Next", command=self.mark_for_review, bootstyle="secondary-outline")
        self.clear_response = ttk.Button(frame, text="Clear Response", command=self.clear_current_response, bootstyle="danger-outline")
        self.btn_save_next = ttk.Button(frame, text="Save & Next", command=self.next_question, bootstyle="success", width=Settings.MM_BTN_WIDTH)
        self.mark_review.pack(side="left", padx=10, pady=5)
        self.clear_response.pack(side="left", padx=10, pady=5)
        self.btn_save_next.pack(side="right", padx=30, pady=5)

    def _record_time_spent(self) -> None:
        if self.question_start_time == 0.0 or not self.quiz_data:
            return
        
        elapsed_time = time.time() - self.question_start_time
        if 0 <= self.current_q_index < len(self.quiz_data):
            self.quiz_data[self.current_q_index]['_time_taken'] += elapsed_time
    
    def load_quiz(self) -> None:
        file_path = filedialog.askopenfilename(title="Select Quiz CSV", filetypes=[("CSV Files", "*.csv")])
        if not file_path: return

        # सही किया गया: UI को रीसेट करने से पहले टाइम लिमिट पढ़ें
        time_input_str = self.time_limit_entry.get().strip()
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames or "question" not in [h.strip().lower() for h in reader.fieldnames if h]:
                    messagebox.showerror("Invalid CSV", "CSV must contain a 'question' header.")
                    return
                rows = [row for row in reader if row.get("question", "").strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Could not load quiz:\n{e}")
            return
        if not rows:
            messagebox.showwarning("Empty", "The selected CSV file has no valid questions.")
            return
        
        # अब जब हमारे पास समय और फ़ाइल है, तो सब कुछ रीसेट करें
        self._reset_quiz() 
        
        # अब, सहेजे गए time_input_str का उपयोग करके टाइमर मोड सेट करें
        try:
            time_limit_min = int(time_input_str)
            if time_limit_min > 0 and time_limit_min < 181 :
                self.is_countdown_mode = True
                self.remaining_seconds = time_limit_min * 60
                self.total_time_label.config(text=f"Left Time: {time_limit_min:02d}:00")
            else:
                self.is_countdown_mode = False
        except ValueError:
            self.is_countdown_mode = False

        for row in rows:
            row['_time_taken'] = 0.0
            opts = [row.get(k, "").strip() for k in ("option1", "option2", "option3", "option4") if row.get(k, "").strip()]
            row['_shuffled_options'] = random.sample(opts, k=len(opts)) if self.shuffle_options else list(opts)
        
        self.quiz_data = rows
        if self.shuffle_questions:
            random.shuffle(self.quiz_data)

        filename = os.path.basename(file_path)
        self.test_name_label.config(text=os.path.splitext(filename)[0].replace("_", " ").title())
        
        self.right_panel.quiz_load_btn.config(state="disabled")
        self.toggle_btn.config(state="disabled")
        self.time_limit_entry.config(state="disabled")

        self._start_quiz_timer()
        self.start_question_timer()
        if self.right_panel:
            self.right_panel.create_question_buttons(len(self.quiz_data), self.show_question)
        self.show_question(0)

    def _calculate_results(self) -> Dict[str, Any]:
        results = {
            "total": len(self.quiz_data), "correct": 0, "answered": 0,
            "total_time_on_answered": 0,
            "fastest_q": {"num": "-", "time": float('inf')},
            "slowest_q": {"num": "-", "time": 0.0}
        }
        for i, q in enumerate(self.quiz_data):
            given = str(self.selected_answers.get(i, "")).strip()
            ans = str(q.get("answer", "")).strip()
            time_taken = q.get('_time_taken', 0.0)
            if given:
                results["answered"] += 1
                results["total_time_on_answered"] += time_taken
                if time_taken < results["fastest_q"]["time"]:
                    results["fastest_q"] = {"num": i + 1, "time": time_taken}
                if time_taken > results["slowest_q"]["time"]:
                    results["slowest_q"] = {"num": i + 1, "time": time_taken}
                if given == ans:
                    results["correct"] += 1
        return results

    def _display_summary(self, results: Dict[str, Any]) -> None:
        def format_time_always_mmss(seconds_float: float) -> str:
            seconds_float = max(0, seconds_float)
            mins, secs = divmod(seconds_float, 60)
            return f"{int(mins):02d}:{int(secs):02d}"
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        wrong = results["answered"] - results["correct"]
        unattempted = results["total"] - results["answered"]
        accuracy = (results["correct"] / results["answered"] * 100) if results["answered"] > 0 else 0
        avg_time = (results["total_time_on_answered"] / results["answered"]) if results["answered"] > 0 else 0
        total_time_spent = sum(q.get('_time_taken', 0.0) for q in self.quiz_data)
        test_name = self.test_name_label.cget("text")
        ttk.Label(self.scroll_frame, text=f"--- Test Summary: {test_name} ---", font=Settings.FONT_HELVETICA_LARGE_BOLD, bootstyle="success").pack(anchor="center", padx=Settings.PAD_LARGE, pady=(10, 15))
        stats_container = ttk.Frame(self.scroll_frame)
        stats_container.pack(fill='x', padx=15, pady=5)
        stats_container.columnconfigure((0, 1), weight=1)
        stats_frame_left = ttk.Frame(stats_container, padding=(10, 5))
        stats_frame_left.grid(row=0, column=0, sticky="nsew", padx=5)
        stats_frame_right = ttk.Frame(stats_container, padding=(10, 5))
        stats_frame_right.grid(row=0, column=1, sticky="nsew", padx=5)
        stats1 = [("🏆 Score", f"{results['correct']}/{results['total']}"), ("✅ Correct", str(results['correct'])), ("❌ Wrong", str(wrong)), ("⚪ Unattempted", str(unattempted)), ("🎯 Accuracy", f"{accuracy:.2f}%")]
        for i, (label, value) in enumerate(stats1):
            ttk.Label(stats_frame_left, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=0, sticky='w', padx=5, pady=3)
            ttk.Label(stats_frame_left, text=value, font=Settings.FONT_HELVETICA_NORMAL).grid(row=i, column=1, sticky='w', padx=5, pady=3)
        avg_time_str, fastest_q_str, slowest_q_str = "00:00", "N/A", "N/A"
        if results["answered"] > 0:
            avg_time_str = format_time_always_mmss(avg_time)
            fastest_q, slowest_q = results.get('fastest_q'), results.get('slowest_q')
            if fastest_q and 'num' in fastest_q and 'time' in fastest_q:
                fastest_q_str = f"Q{fastest_q['num']} ({format_time_always_mmss(fastest_q['time'])})"
            if slowest_q and 'num' in slowest_q and 'time' in slowest_q:
                slowest_q_str = f"Q{slowest_q['num']} ({format_time_always_mmss(slowest_q['time'])})"
        stats2 = [("⏱ Total Time", format_time_always_mmss(total_time_spent)), ("⌛ Avg. Time / Ques", avg_time_str), ("⚡ Fastest Ques", fastest_q_str), ("🐢 Slowest Ques", slowest_q_str)]
        for i, (label, value) in enumerate(stats2):
            ttk.Label(stats_frame_right, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=0, sticky='w', padx=5, pady=3)
            ttk.Label(stats_frame_right, text=value, font=Settings.FONT_HELVETICA_NORMAL, bootstyle=Settings.INFO_COLOR).grid(row=i, column=1, sticky='w', padx=5, pady=3)
        ttk.Separator(self.scroll_frame, orient="horizontal").pack(fill="x", pady=20, padx=10)
        ttk.Label(self.scroll_frame, text="📌 Question-wise Analysis:", font=Settings.FONT_HELVETICA_14_UNDLIN).pack(anchor="w", padx=15, pady=(5, 10))
        for i, q in enumerate(self.quiz_data):
            given = str(self.selected_answers.get(i, "")).strip()
            ans = str(q.get("answer", "")).strip()
            time_taken = q.get('_time_taken', 0.0)
            q_frame = ttk.Frame(self.scroll_frame, padding=10, borderwidth=1, relief="solid")
            q_frame.pack(fill='x', padx=15, pady=6)
            header_frame = ttk.Frame(q_frame)
            header_frame.pack(fill='x')
            ttk.Label(header_frame, text=f"Q{i+1}: {q['question']}", wraplength=700, font=Settings.FONT_HELVETICA_NORMAL).pack(side='left', anchor='w')
            ttk.Label(header_frame, text=f"({format_time_always_mmss(time_taken)})", bootstyle=Settings.DANGER_COLOR).pack(side='right', anchor='e')
            is_correct, is_unanswered = (given and given == ans), not given
            result_style = Settings.WARNING_COLOR if is_unanswered else Settings.SUCCESS_COLOR if is_correct else Settings.DANGER_COLOR
            result_text = "🤷‍♂️ Not Answered" if is_unanswered else "✅ Correct" if is_correct else "❌ Incorrect"
            ttk.Separator(q_frame, orient="horizontal").pack(fill="x", pady=5)
            if is_correct:
                ttk.Label(q_frame, text=f"{result_text}: {ans}", bootstyle=result_style, font=Settings.FONT_HELVETICA_BOLD).pack(anchor='w')
            else:
                ttk.Label(q_frame, text=result_text, bootstyle=result_style, font=Settings.FONT_HELVETICA_BOLD).pack(anchor='w', pady=(0, 5))
                answer_detail_frame = ttk.Frame(q_frame)
                answer_detail_frame.pack(fill='x', padx=10)
                if not is_unanswered:
                    ttk.Label(answer_detail_frame, text="Your Answer:", font=Settings.FONT_HELVETICA_BOLD).grid(row=0, column=0, sticky='w')
                    ttk.Label(answer_detail_frame, text=given, bootstyle=Settings.DANGER_COLOR).grid(row=0, column=1, sticky='w', padx=5)
                ttk.Label(answer_detail_frame, text="Correct Answer:", font=Settings.FONT_HELVETICA_BOLD).grid(row=1, column=0, sticky='w')
                ttk.Label(answer_detail_frame, text=ans, bootstyle=Settings.SUCCESS_COLOR, font=Settings.FONT_HELVETICA_SM_BOLD).grid(row=1, column=1, sticky='w', padx=5)

    def _cleanup_after_submit(self) -> None:
        if self.right_panel:
            for btn in self.right_panel.q_buttons:
                btn.destroy()
            self.right_panel.q_buttons.clear()
            self.right_panel.quiz_load_btn.config(state="normal")

        self.mark_review.config(state="disabled")
        self.clear_response.config(state="disabled")
        self.btn_save_next.config(state="disabled")
        self.toggle_btn.config(state="normal")
        self.time_limit_entry.config(state="normal")
        self.question_number_label.config(text="Test Submitted - Summary")

    def submit_quiz(self) -> None:
        if not self.quiz_data:
            # This check is now complex, let's simplify. If countdown isn't running, it's safe to show.
            if not self.is_countdown_mode or self.remaining_seconds > 0:
                 messagebox.showwarning("No Quiz", "Load a quiz first.")
            return
        
        ask_confirmation = not self.is_countdown_mode or self.remaining_seconds > 0
        if ask_confirmation and not messagebox.askyesno("Submit Test", "Do you want to submit the test?"):
            return

        self._record_time_spent()
        self.stop_question_timer()
        self.stop_quiz_timer()
        if self.answer_var.get():
            self.selected_answers[self.current_q_index] = self.answer_var.get().strip()
        
        results = self._calculate_results()
        self._display_summary(results)
        self._cleanup_after_submit()
        
    def quit_quiz(self):
        if self.quiz_data and not messagebox.askyesno("Quit Quiz", "Are you sure you want to quit the quiz?"):
            return
        self.stop_quiz_timer()
        self._reset_quiz()

    def _get_app(self):
        return self.winfo_toplevel()

    def update_status_and_buttons(self) -> None:
        if not self.quiz_data or not self.right_panel: return
        self._update_right_button_style(self.current_q_index)
        total, answered_set = len(self.quiz_data), {i for i, v in self.selected_answers.items() if v}
        counts = {"Answered": len(answered_set), "Marked": len(self.marked_for_review), "Marked and answered": len(answered_set & self.marked_for_review), "Not Visited": total - len(self.visited_questions), "Not Answered": total - len(answered_set)}
        self.right_panel.update_status_counts(counts)

    def _update_right_button_style(self, index: int) -> None:
        if not (self.right_panel and 0 <= index < len(self.right_panel.q_buttons)): return
        btn = self.right_panel.q_buttons[index]
        is_answered, is_marked, is_visited = bool(self.selected_answers.get(index)), index in self.marked_for_review, index in self.visited_questions
        style_map = {(True, True): "primary", (False, True): "warning", (True, False): "success", (False, False): "danger" if is_visited else "secondary-outline"}
        btn.config(bootstyle=style_map.get((is_answered, is_marked), "secondary-outline"))
    
    def show_question(self, index: Optional[int] = None) -> None:
        self._record_time_spent()
        
        if index is not None: self.current_q_index = index
        if not (0 <= self.current_q_index < len(self.quiz_data)): return
        
        self.visited_questions.add(self.current_q_index)
        for w in self.scroll_frame.winfo_children(): w.destroy()
        
        qdata = self.quiz_data[self.current_q_index]
        self.question_number_label.config(text=f"Question No. {self.current_q_index + 1} / {len(self.quiz_data)}")
        ttk.Label(self.scroll_frame, text=f"Q{self.current_q_index + 1}: {qdata['question']}", wraplength=700, font=("Helvetica", 12)).pack(anchor="w", padx=15, pady=10)
        
        self.answer_var.set(self.selected_answers.get(self.current_q_index, ""))
        for opt_text in qdata.get('_shuffled_options', []):
            ttk.Radiobutton(self.scroll_frame, text=opt_text, value=opt_text, variable=self.answer_var).pack(anchor="w", padx=30, pady=3)
        
        self.update_status_and_buttons()
        self.question_start_time = time.time()

    def _update_and_move_next(self) -> None:
        if not self.quiz_data: return
        
        current_answer = self.answer_var.get()
        if current_answer: self.selected_answers[self.current_q_index] = current_answer
        else: self.selected_answers.pop(self.current_q_index, None)
        
        self.update_status_and_buttons()
        
        if self.current_q_index < len(self.quiz_data) - 1:
            self.show_question(self.current_q_index + 1)
        else:
            self.show_question(self.current_q_index)
            messagebox.showinfo("End", "This is the last question.")

    def next_question(self) -> None: 
        self._update_and_move_next()

    def mark_for_review(self) -> None:
        self.marked_for_review.add(self.current_q_index)
        self._update_and_move_next()

    def clear_current_response(self) -> None:
        idx = self.current_q_index
        self.answer_var.set("")
        self.selected_answers.pop(idx, None)
        self.marked_for_review.discard(idx)
        self.update_status_and_buttons()
        
    def start_question_timer(self) -> None:
        self.stop_question_timer()
        self._q_timer_id = self.after(1000, self._update_question_timer)

    def _update_question_timer(self) -> None:
        try:
            if not (0 <= self.current_q_index < len(self.quiz_data)): return
            accumulated_time = self.quiz_data[self.current_q_index].get('_time_taken', 0.0)
            elapsed_since_visit = time.time() - self.question_start_time
            current_total = accumulated_time + elapsed_since_visit
            mins, secs = divmod(current_total, 60)
            self.question_take_time_lbl.config(text=f"Time: {int(mins):02d}:{int(secs):02d}")
            self._q_timer_id = self.after(1000, self._update_question_timer)
        except (tk.TclError, IndexError):
            self._q_timer_id = None
    
    def stop_question_timer(self) -> None:
        if self._q_timer_id:
            self.after_cancel(self._q_timer_id)
            self._q_timer_id = None
    
    def _start_quiz_timer(self) -> None:
        self.stop_quiz_timer()
        self._quiz_timer_id = self.after(1000, self._update_quiz_timer)

    def _update_quiz_timer(self) -> None:
        try:
            if self.is_countdown_mode:
                # --- काउंटडाउन लॉजिक ---
                if self.remaining_seconds > 0:
                    self.remaining_seconds -= 1
                    mins, secs = divmod(self.remaining_seconds, 60)
                    self.total_time_label.config(text=f"Left Time: {mins:02d}:{secs:02d}")
                    # जब तक समय बचा है, तभी टाइमर को फिर से चलाएं
                    self._quiz_timer_id = self.after(1000, self._update_quiz_timer)
                else:
                    # --- समय समाप्त होने पर ---
                    # टाइमर लूप को फिर से शुरू न करें
                    self.total_time_label.config(text="Time's Up!")
                    messagebox.showinfo("Time's Up!", "The quiz time is over. Submitting the test automatically.")
                    self.submit_quiz()
            else:
                # --- काउंट-अप लॉजिक ---
                self.elapsed_seconds += 1
                mins, secs = divmod(self.elapsed_seconds, 60)
                self.total_time_label.config(text=f"Total Time: {mins:02d}:{secs:02d}")
                # टाइमर को फिर से चलाएं
                self._quiz_timer_id = self.after(1000, self._update_quiz_timer)

        except tk.TclError:
            self._quiz_timer_id = None

    def stop_quiz_timer(self) -> None:
        if self._quiz_timer_id:
            self.after_cancel(self._quiz_timer_id)
            self._quiz_timer_id = None

    def _get_today_date_str(self) -> str: 
        return datetime.now().strftime("Date: %d %b %Y")
    
    def _start_periodic_date_update(self) -> None:
        self.stop_periodic_date_update()
        self._date_after_id = self.after(60_000, self._periodic_update_date_label)

    def _periodic_update_date_label(self) -> None:
        try:
            self.today_date.config(text=self._get_today_date_str())
            self._date_after_id = self.after(60_000, self._periodic_update_date_label)
        except tk.TclError: self._date_after_id = None
    
    def stop_periodic_date_update(self) -> None:
        if self._date_after_id:
            self.after_cancel(self._date_after_id)
            self._date_after_id = None
            
    def toggle_action(self) -> None:
        self.shuffle_options = not self.shuffle_options
        self.shuffle_questions = not self.shuffle_questions
        self.toggle_btn.config(text="Mode: HARD" if self.shuffle_options else "Mode: EASY")

    def destroy(self) -> None:
        self.stop_question_timer()
        self.stop_quiz_timer()
        self.stop_periodic_date_update()
        super().destroy()


class QuizPage(BaseFrame):
    def __init__(self, master: tk.Misc, app: Optional[tk.Toplevel] = None) -> None:
        super().__init__(master, app)
        self.pack(fill="both", expand=True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=4, uniform="group")
        self.grid_columnconfigure(1, weight=1, uniform="group")
        self.left_frame = QuizAttemptLeftFrame(self, app=app)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame = QuizRightPanelFrame(self, app=app)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.left_frame.right_panel = self.right_frame
        self.right_frame.quiz_load_btn.config(command=self.left_frame.load_quiz)
        self.right_frame.quiz_submit_button.config(command=self.left_frame.submit_quiz)


class MainApp(ttk.Window):
    def __init__(self):
        super().__init__(themename=Settings.THEME[3])
        self.title(Settings.TITLE)
        self.geometry(f"{Settings.WSIZE[0]}x{Settings.WSIZE[1]}+{Settings.POS[0]}+{Settings.POS[1]}")
        self.minsize(*Settings.WSIZE)
        try:
            self.iconbitmap(Settings.ICON)
        except Exception as e:
            Settings.show_toast(title="Icon Error", message=f"Icon file not found Exception: {e}", bootstyle=WARNING)

        # self.history = []
        self.current_frame = None

        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=BOTH, expand=YES)
        self.main_container.grid_columnconfigure(0, weight=1, uniform="group1")
        self.main_container.grid_rowconfigure(0, weight=20, uniform="group2")
        self.main_container.grid_rowconfigure(1, weight=1, uniform="group2")

        self.main_frame()

        self.bottom_bar()

    def main_frame(self):
        self.main_area_frame = ttk.Frame(self.main_container)
        self.main_area_frame.grid(row=0, column=0, sticky=NSEW)
        self.current_frame = QuizPage(self.main_area_frame, app=self)
        self.current_frame.pack(fill=BOTH, expand=YES)

    def bottom_bar(self):
        self.bottom_bar_frame = ttk.Frame(self.main_container)
        self.bottom_bar_frame.grid(row=1, column=0, sticky=NSEW)

        self._last_mot = None
        self._mot_label = ttk.Label(self.bottom_bar_frame, 
                                    text=self._pick_random_mot(), 
                                    bootstyle=Settings.SUCCESS_COLOR,
                                    font=Settings.FONT_HELVETICA_ITALIC
                                    )
        self._mot_label.pack(side=LEFT, anchor=CENTER, padx=Settings.PAD_MEDIUM)
        self._mot_after_id = self.after(3000, self._rotate_motivation)


        self.bottom_bar_vesion_label = ttk.Label(self.bottom_bar_frame, text=Settings.get_version(), bootstyle=Settings.INVERSE_SECONDARY)
        self.bottom_bar_vesion_label.pack(side=RIGHT, pady=Settings.PAD_SMALL, padx=Settings.PAD_LARGE)

    def switch_frame(self, frame_class, *args, **kwargs):
        if self.current_frame:
            # self.history.append(self.current_frame.__class__)
            try:
                self.current_frame.destroy()
            except Exception as e:
                Settings.show_toast(title="Frame Load Error", message=f"Exception: {e}")
        self.current_frame = frame_class(self.main_area_frame, app=self, *args, **kwargs)
        self.current_frame.pack(fill=BOTH, expand=YES)

    def _pick_random_mot(self):
        for _ in range(6):
            s = Settings.get_random_motivation()
            if not s:
                return ""
            if s != self._last_mot:
                self._last_mot = s
                return s
        self._last_mot = s
        return s

    def _rotate_motivation(self):
        try:
            new_text = self._pick_random_mot()
            self._mot_label.config(text=new_text)
            self._mot_after_id = self.after(3000, self._rotate_motivation)
        except Exception:
            self._mot_after_id = None

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()