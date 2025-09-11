# app.py
import os
import csv
import random
import time
from datetime import datetime
from typing import Optional, Dict, List, Any
import tkinter as tk
import tkinter.font as tkfont
from tkinter import StringVar, messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None


class Settings:
    THEME = ("pulse", "minty", "simplex", "flatly", "darkly", "solar", "cyborg", "vapor")
    TITLE = "ReadAndTest  Author: BIJAY MAHTO"
    WSIZE = (950, 600)
    POS = (100, 50)
    ICON = "icon.ico"

    MIN_PAD = 2
    PAD_SMALL = 4
    PADY = 5
    PAD_MEDIUM = 8
    PADX = 10
    PAD_LARGE = 12
    PAD_15 = 15

    MM_BTN_WIDTH = 15
    SM_BTN_WIDTH = 25
    MD_BTN_WIDTH = 35
    LG_BTN_WIDTH = 45

    FONT_FAMILY = "Calibri" #"Arial"
    FONT_FAMILY_SEGEO = "Segoe UI"
    FONT_SIZE = 11
    FONT_TITLE = (FONT_FAMILY, 16, "bold")
    FONT_SUBTITLE = (FONT_FAMILY, 12, "bold")
    FONT_NORMAL = (FONT_FAMILY, FONT_SIZE)
    FONT_SEGEO = (FONT_FAMILY_SEGEO, 9)

    # --- Helvetica ---
    FONT_HELVETICA_LARGE_BOLD = ("Helvetica", 16, "bold")
    FONT_HELVETICA_14_UNDLIN = ("Helvetica", 14, "underline")
    FONT_HELVETICA_NORMAL = ("Helvetica", 10)
    FONT_HELVETICA_BOLD = ("Helvetica", 10, "bold")
    FONT_HELVETICA_SM_BOLD: tuple = ("Helvetica", 9, "bold")
    BUTTONS_PER_ROW = 5

    PRIMARY_COLOR = "primary"
    SUCCESS_COLOR = "success"
    INFO_COLOR = "info"
    WARNING_COLOR = "warning"
    DANGER_COLOR = "danger"
    SECONDRY_COLOR = "secondary"

    INVERSE_SECONDARY = "inverse-secondary"
    INFO_OUT = "info-outline"
    SUCCESS_OUTLINE = "primary-outline"
    DANGER_OUTLINE = "danger-outline"

    MOTIVATION_LINES = (
        "Small goal today → big success tomorrow.",
        "30 minutes of focused practice every day — consistency builds champions.",
        "Speed + accuracy = results. Solve fast, then check carefully.",
        "Practice smart: short, focused sessions beat long, unfocused study.",
        "Turn mistakes into lessons — every error moves you forward.",
        "Consistency compounds — show up today, see progress tomorrow.",
    )


    DETAILS_TEXT = (
    "🎯 ReadAndTest — SSC CGL & Railway\n\n"
    "Focused notes + quick quizzes — real-test practice, shuffled questions, aur daily targets.\n\n"
    "• Concise topic-wise notes\n"
    "• Quick timed quizzes with instant feedback\n"
    "• Lightweight — sirf padhai aur practice\n"
)


    SAMPLE_NOTES = """
    🚀 Let's get started! Study is the real key to success.
    💡 Remember: Every study session brings you one step closer to your goal.
    📈 Tip: Focus on small, consistent practice — quality 30-minute sessions beat occasional marathon cramming.
    🔁 Quick routine:
    • Read the concept (5–10 mins)
    • Do a short practice quiz (10–15 mins)
    • Review mistakes and note shortcuts (5–10 mins)
    Keep going — steady effort builds big results.
    """


    @classmethod
    def get_random_motivation(cls):
        import random
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
    __MINOR = 1
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


class HomePage(BaseFrame):
    def __init__(self, master, app=None, text=None):
        super().__init__(master, app)

        self.home_page_container = ttk.Frame(self)
        self.home_page_container.pack(fill=BOTH, expand=YES)

        self.home_page_container.grid_rowconfigure(0, weight=2, uniform="group1")
        self.home_page_container.grid_rowconfigure(1, weight=18, uniform="group1")
        self.home_page_container.grid_columnconfigure(0, weight=1, uniform="group")
        self.home_page_container.grid_columnconfigure(1, weight=4, uniform="group")

        self.home_page_top_bar()
        self.home_page_main_area()
        self.home_page_button_area()

    def home_page_top_bar(self):
        top_bar_frame = ttk.Frame(self.home_page_container)
        top_bar_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        left_wrap = ttk.Frame(top_bar_frame)
        left_wrap.pack(side=LEFT)

        self.frame_name_var = StringVar(value="Home Page")
        self.frame_name_label = ttk.Label(
            left_wrap,
            textvariable=self.frame_name_var,
            bootstyle=Settings.SUCCESS_COLOR,
            font=Settings.FONT_SUBTITLE,
            anchor=W,
        )
        self.frame_name_label.pack(side=LEFT, padx=Settings.PAD_LARGE, fill="x", expand=True)

        right_wrap = ttk.Frame(top_bar_frame)
        right_wrap.pack(side=RIGHT)

        self.search_entry = ttk.Entry(right_wrap, width=26, state="disabled")
        self.search_button = ttk.Button(
            right_wrap,
            text="🔍 Search",
            state="disabled",
            bootstyle=Settings.INFO_OUT,
            command=self.search_action,
        )

        ttk.Label(right_wrap, text="Theme:", font=Settings.FONT_SEGEO, bootstyle=Settings.INFO_COLOR).pack(
            side=LEFT, padx=(4, 2)
        )

        try:
            current_theme = self.winfo_toplevel().style.theme_use()
        except Exception:
            current_theme = Settings.THEME[0]

        self._theme_var = tk.StringVar(value=current_theme)
        self.theme_combobox = ttk.Combobox(
            right_wrap, values=Settings.THEME, textvariable=self._theme_var, state="readonly", width=12
        )
        self.theme_combobox.pack(side=LEFT, padx=(8, 4))
        self.theme_combobox.bind("<<ComboboxSelected>>", lambda e: self.change_theme(self._theme_var.get()))

        self.search_entry.pack(side=LEFT, padx=Settings.PAD_SMALL)
        self.search_button.pack(side=LEFT, padx=Settings.PAD_SMALL)

    def home_page_button_area(self):
        button_frame = ttk.Frame(self.home_page_container)
        button_frame.grid(row=1, column=0, sticky=NSEW)

        self.btn_read_notes = ttk.Button(
            button_frame,
            text="Read Notes",
            bootstyle=Settings.SUCCESS_OUTLINE,
            width=Settings.SM_BTN_WIDTH,
            command=lambda: (self.app.switch_frame(ReadingNotes) if self.app else None),
        )
        self.btn_read_notes.pack(pady=Settings.PAD_LARGE)

        self.btn_quiz_time = ttk.Button(
            button_frame,
            text="Quiz Time",
            bootstyle=Settings.SUCCESS_OUTLINE,
            width=Settings.SM_BTN_WIDTH,
            command=lambda: (self.app.switch_frame(QuizPage) if self.app else None),
        )
        self.btn_quiz_time.pack(pady=Settings.PAD_LARGE)

        ttk.Button(
            button_frame,
            text="Close App",
            bootstyle=Settings.DANGER_OUTLINE,
            width=Settings.SM_BTN_WIDTH,
            command=lambda: self.winfo_toplevel().destroy(),
        ).pack(pady=Settings.PAD_LARGE)


    def home_page_main_area(self):
        main_area_frame = ttk.Frame(self.home_page_container)
        main_area_frame.grid(row=1, column=1, sticky=tk.NSEW)

        ttk.Label(
            main_area_frame,
            text="ReadAndTest — SSC CGL & Railway ke liye focused revision",
            font=Settings.FONT_TITLE,
            anchor="w",
        ).pack(fill="x", pady=(Settings.PAD_MEDIUM, 6), padx=10)

        ttk.Label(
            main_area_frame,
            text="Roz thoda, roz behtar — concise notes, quick quizzes aur daily targets.",
            font=Settings.FONT_SUBTITLE,
            anchor="w",
        ).pack(fill="x", padx=10, pady=(0, Settings.PAD_MEDIUM))

        container = ttk.Frame(main_area_frame)
        container.pack(fill="both", expand=True, padx=10, pady=6)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        # create window and keep window id so we can resize it on canvas configure
        self._canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # details label inside scroll_frame — keep reference to update wraplength on resize
        self._details_label = ttk.Label(
            scroll_frame,
            text=Settings.DETAILS_TEXT,
            wraplength=680,   # initial value; will be updated on resize
            justify="left",
            font=Settings.FONT_NORMAL
        )
        self._details_label.pack(anchor="w", padx=6, pady=6)

        def _on_frame_config(e):
            try:
                canvas.configure(scrollregion=canvas.bbox("all"))
            except Exception:
                pass

        def _on_canvas_config(e):
            try:
                # make the scroll_frame width equal to canvas width so content wraps nicely
                canvas.itemconfigure(self._canvas_window, width=e.width)
                canvas.configure(scrollregion=canvas.bbox("all"))
                # update wraplength of details label (leave some padding)
                try:
                    new_wrap = max(200, e.width - 40)
                    self._details_label.configure(wraplength=new_wrap)
                except Exception:
                    pass
            except Exception:
                pass

        scroll_frame.bind("<Configure>", _on_frame_config)
        canvas.bind("<Configure>", _on_canvas_config)

        self._last_mot = None
        # use Settings constant for bootstyle
        self._mot_label = ttk.Label(
            main_area_frame,
            text=self._pick_random_mot(),
            font=("Helvetica", 10, "italic"),
            bootstyle=Settings.SUCCESS_COLOR
        )
        self._mot_label.pack(anchor="w", padx=10, pady=(4, 8))
        self._mot_after_id = self.after(3000, self._rotate_motivation)


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

    def destroy(self):
        try:
            if getattr(self, "_mot_after_id", None):
                self.after_cancel(self._mot_after_id)
        except Exception:
            pass
        super().destroy()

    def change_theme(self, theme_name):
        try:
            self.winfo_toplevel().style.theme_use(theme_name)
        except Exception as e:
            messagebox.showerror("Theme Error", f"Could not change theme:\n{e}")

    def search_action(self):
        query = self.search_entry.get()
        print(f"Searching: {query}")


class ReadingNotes(BaseFrame):
    def __init__(self, master, app=None, text=None):
        super().__init__(master, app)

        self.file_content = None
        self.file_path = None

        # container: packed into this frame; internal layout uses grid
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=4, uniform="group")
        self.container.grid_columnconfigure(1, weight=1, uniform="group")

        self.notes_text = text if text else Settings.SAMPLE_NOTES
        self._create_text_view()
        self.read_notes_right_frame()

    def _select_font_family(self):
        candidates = [
            "Noto Sans Devanagari",
            "Helvetica",
            "Noto Sans",
            "DejaVu Sans",
            "Lohit Devanagari",
            "Mangal",
            "Nirmala UI",
            "Segoe UI",
            "Liberation Sans",
            "Arial",
        ]
        for fam in candidates:
            try:
                tkfont.Font(family=fam, size=12)
                return fam
            except Exception:
                continue
        try:
            return tkfont.nametofont("TkDefaultFont").actual().get("family", "Helvetica")
        except Exception:
            return "Helvetica"

    def _create_text_view(self):
        left_container = ttk.Frame(self.container, bootstyle="light")
        left_container.grid(row=0, column=0, sticky=tk.NSEW)
        left_container.grid_rowconfigure(0, weight=1)
        left_container.grid_columnconfigure(0, weight=1)

        container = ttk.Frame(left_container, bootstyle="light")
        container.grid(row=0, column=0, sticky=tk.NSEW)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        font_family = self._select_font_family()
        text_font = tkfont.Font(family=font_family, size=13)

        self.txt = tk.Text(container, wrap="word", font=text_font, relief="flat", bd=0, padx=10, pady=8)
        vscroll = ttk.Scrollbar(container, orient="vertical", command=self.txt.yview)
        self.txt.configure(yscrollcommand=vscroll.set)

        self.txt.grid(row=0, column=0, sticky=tk.NSEW)
        vscroll.grid(row=0, column=1, sticky=tk.NS)

        content = (self.notes_text or "").replace("\r\n", "\n").replace("\r", "\n")
        self.txt.insert("1.0", content)

        try:
            self.txt.tag_configure("p", spacing1=2, spacing3=8, lmargin1=4, lmargin2=4, rmargin=4, justify="left")
            self.txt.tag_add("p", "1.0", "end")
        except Exception:
            pass

        self.txt.config(state="disabled")

        def _on_mouse_wheel(event):
            try:
                num = getattr(event, "num", None)
                if num == 4:
                    self.txt.yview_scroll(-1, "units")
                elif num == 5:
                    self.txt.yview_scroll(1, "units")
                else:
                    delta = getattr(event, "delta", 0)
                    self.txt.yview_scroll(int(-1 * (delta / 120)), "units")
                return "break"
            except tk.TclError:
                return "break"

        self.txt.bind("<MouseWheel>", _on_mouse_wheel)
        self.txt.bind("<Button-4>", _on_mouse_wheel)
        self.txt.bind("<Button-5>", _on_mouse_wheel)

    def view_text_file(self):
        """Show currently loaded file content in the text widget."""
        if not self.file_content:
            return
        try:
            self.txt.config(state="normal")
            self.txt.delete("1.0", "end")
            content = (self.file_content or "").replace("\r\n", "\n").replace("\r", "\n")
            self.txt.insert("1.0", content)
            try:
                self.txt.tag_configure("p", spacing1=2, spacing3=8, lmargin1=4, lmargin2=4, rmargin=4, justify="left")
                self.txt.tag_add("p", "1.0", "end")
            except Exception:
                pass
            self.txt.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Could not display file:\n{e}")

    def destroy(self):
        try:
            self.txt.unbind("<MouseWheel>")
            self.txt.unbind("<Button-4>")
            self.txt.unbind("<Button-5>")
        except Exception:
            pass
        super().destroy()

    def read_notes_right_frame(self):
        right = ttk.Frame(self.container)
        right.grid(row=0, column=1, sticky=tk.NSEW)

        ttk.Button(right, text="Load File", bootstyle=Settings.SUCCESS_COLOR, width=Settings.SM_BTN_WIDTH, command=self.load_file).pack(pady=10)
        ttk.Button(right, text="Back", bootstyle=Settings.WARNING_COLOR, width=Settings.SM_BTN_WIDTH, command=self.go_back).pack(pady=10)
        ttk.Button(right, text="Close App", bootstyle=Settings.DANGER_COLOR, width=Settings.SM_BTN_WIDTH, command=lambda: self.winfo_toplevel().destroy()).pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return  # User cancelled

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.file_content = f.read()
            self.file_path = file_path
            self.view_text_file()

            file_name = os.path.basename(file_path)
            Settings.show_toast(title="Success",
                                message=f"File loaded successfully:\n{file_name}",
                                duration=4000,
                                bootstyle=Settings.SUCCESS_COLOR,
                                parent=self.winfo_toplevel())
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")

    def go_back(self):
        if self.app:
            self.app.switch_frame(HomePage)
            Settings.show_toast(title="Home Page", message="You are at Home Page")


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
    """क्विज़ के प्रयास के लिए मुख्य फ्रेम, जिसमें प्रश्न, विकल्प और नियंत्रण बटन होते हैं।"""
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
        self.q_seconds: int = 0
        self.shuffle_options: bool = False
        self.shuffle_questions: bool = False
        self.question_start_time: float = 0.0
        
        self.answer_var = tk.StringVar()
        
        self._create_widgets()
        self._start_periodic_date_update()

    def _reset_quiz(self) -> None:
        """क्विज़ की स्थिति को उसकी प्रारंभिक अवस्था में रीसेट करता है।"""
        self.stop_question_timer()
        self.quiz_data.clear()
        self.selected_answers.clear()
        self.marked_for_review.clear()
        self.visited_questions.clear()
        self.current_q_index = 0
        self.q_seconds = 0
        self.answer_var.set("")

        self.test_name_label.config(text="Test")
        self.question_number_label.config(text="Please Load Quiz File")
        self.question_take_time_lbl.config(text="Time: 00:00:00")

        for w in self.scroll_frame.winfo_children():
            w.destroy()

        if self.right_panel:
            for btn in self.right_panel.q_buttons:
                btn.destroy()
            self.right_panel.q_buttons.clear()
            self.right_panel.update_status_counts({k: 0 for k in self.right_panel.status_labels})
            self.right_panel.quiz_load_btn.config(state="normal")
        
        # FIX: क्विज़ रीसेट होने पर बटनों को फिर से सक्षम करें
        self.mark_review.config(state="normal")
        self.clear_response.config(state="normal")
        self.btn_save_next.config(state="normal")
        self.toggle_btn.config(state="normal")

    def _create_widgets(self) -> None:
        self._tob_view_area()
        self._second_tob_view_area()
        self._question_options_view_area()
        self._bottom_view_area()

    def _tob_view_area(self) -> None:
        # यह मेथड अपरिवर्तित है
        self.top_area_frame = ttk.Frame(self)
        self.top_area_frame.grid(row=0, column=0, sticky="ew")
        self.section_name_label = ttk.Label(self.top_area_frame, text="SECTIONS", anchor="w", bootstyle="secondary", font=Settings.FONT_HELVETICA_BOLD)
        self.section_name_label.pack(side="left", padx=10, pady=5)
        self.test_name_label = ttk.Label(self.top_area_frame, text="Test", anchor="e", bootstyle="primary", font=Settings.FONT_HELVETICA_BOLD)
        self.test_name_label.pack(side="left", padx=10, pady=5)
        self.total_left_time_label = ttk.Label(self.top_area_frame, text=self._get_today_date_str(), anchor="e", bootstyle="danger", font=Settings.FONT_HELVETICA_BOLD)
        self.total_left_time_label.pack(side="right", padx=10, pady=5)
        self.toggle_btn = ttk.Checkbutton(self.top_area_frame, text='Mode: EASY', bootstyle="round-toggle", command=self.toggle_action)
        self.toggle_btn.pack(side="right", padx=10, pady=5)

    def _second_tob_view_area(self) -> None:
        # यह मेथड अपरिवर्तित है
        self.top_second_area_frame = ttk.Frame(self)
        self.top_second_area_frame.grid(row=1, column=0, sticky="ew")
        self.question_number_label = ttk.Label(self.top_second_area_frame, text="Please Load Quiz File", anchor="w", font=Settings.FONT_HELVETICA_BOLD)
        self.question_number_label.pack(side="left", padx=10, pady=5)
        self.question_take_time_lbl = ttk.Label(self.top_second_area_frame, text="Time: 00:00:00", anchor="e", bootstyle="info", font=Settings.FONT_HELVETICA_BOLD)
        self.question_take_time_lbl.pack(side="left", padx=40, pady=5)
        self.btn_quit_quiz = ttk.Button(self.top_second_area_frame, text="Quit", bootstyle="danger-outline", command=self.quit_quiz)
        self.btn_quit_quiz.pack(side="right", padx=10, pady=5)

    def _question_options_view_area(self) -> None:
        # यह मेथड अपरिवर्तित है
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
        # यह मेथड अपरिवर्तित है
        frame = ttk.Frame(self)
        frame.grid(row=3, column=0, sticky="ew")
        self.mark_review = ttk.Button(frame, text="Mark for Review & Next", command=self.mark_for_review, bootstyle="secondary-outline")
        self.clear_response = ttk.Button(frame, text="Clear Response", command=self.clear_current_response, bootstyle="danger-outline")
        self.btn_save_next = ttk.Button(frame, text="Save & Next", command=self.next_question, bootstyle="success", width=Settings.MM_BTN_WIDTH)
        self.mark_review.pack(side="left", padx=10, pady=5)
        self.clear_response.pack(side="left", padx=10, pady=5)
        self.btn_save_next.pack(side="right", padx=30, pady=5)

    def _record_time_spent(self) -> None:
        """वर्तमान प्रश्न पर बिताए गए समय की गणना करता है और उसे संग्रहीत करता है।"""
        if self.question_start_time == 0.0 or not self.quiz_data:
            return
        
        elapsed_time = time.time() - self.question_start_time
        if 0 <= self.current_q_index < len(self.quiz_data):
            # FIX: समय को ओवरराइट करने के बजाय जोड़ें
            self.quiz_data[self.current_q_index]['_time_taken'] += elapsed_time
    
    def load_quiz(self) -> None:
        """CSV फ़ाइल से क्विज़ लोड करता है और UI को तैयार करता है।"""
        file_path = filedialog.askopenfilename(title="Select Quiz CSV", filetypes=[("CSV Files", "*.csv")])
        if not file_path: return

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
        
        self._reset_quiz()

        for i, row in enumerate(rows):
            # FIX: प्रत्येक प्रश्न के लिए '_time_taken' को 0 से शुरू करें
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
        
        self.start_question_timer()
        if self.right_panel:
            self.right_panel.create_question_buttons(len(self.quiz_data), self.show_question)
        self.show_question(0)
    
    def _calculate_results(self) -> Dict[str, Any]:
        """सबमिट किए गए क्विज़ के परिणामों की गणना करता है।"""
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


    # def _display_summary(self, results: Dict[str, Any]) -> None:
    #     """Displays the results in the main display area in a more attractive way."""
        
    #     def format_time_always_mmss(seconds_float: float) -> str:
    #         """Formats seconds into MM:SS format, always."""
    #         seconds_float = max(0, seconds_float)
    #         mins, secs = divmod(seconds_float, 60)
    #         return f"{int(mins):02d}:{int(secs):02d}"

    #     # Clear old widgets
    #     for w in self.scroll_frame.winfo_children():
    #         w.destroy()

    #     # Calculate statistics
    #     wrong = results["answered"] - results["correct"]
    #     unattempted = results["total"] - results["answered"]
    #     accuracy = (results["correct"] / results["answered"] * 100) if results["answered"] > 0 else 0
    #     avg_time = (results["total_time_on_answered"] / results["answered"]) if results["answered"] > 0 else 0
        
    #     # --- Header ---
    #     test_name = self.test_name_label.cget("text")
    #     ttk.Label(
    #         self.scroll_frame, 
    #         text=f"--- Test Summary: {test_name} ---", 
    #         font=Settings.FONT_HELVETICA_LARGE_BOLD, 
    #         bootstyle="success"
    #     ).pack(anchor="center", padx=Settings.PAD_15, pady=(10, 15))

    #     # --- Main Statistics Frame ---
    #     stats_container = ttk.Frame(self.scroll_frame)
    #     stats_container.pack(fill='x', padx=15, pady=5)
    #     stats_container.columnconfigure((0, 1), weight=1)

    #     # Two column frames for stats
    #     stats_frame_left = ttk.Frame(stats_container, padding=(10, 5))
    #     stats_frame_left.grid(row=0, column=0, sticky="nsew", padx=5)

    #     stats_frame_right = ttk.Frame(stats_container, padding=(10, 5))
    #     stats_frame_right.grid(row=0, column=1, sticky="nsew", padx=5)

    #     # Left Column: Score and Accuracy
    #     stats1 = [
    #         ("🏆 Score", f"{results['correct']}/{results['total']}"),
    #         ("✅ Correct", str(results['correct'])),
    #         ("❌ Wrong", str(wrong)),
    #         ("⚪ Unattempted", str(unattempted)),
    #         ("🎯 Accuracy", f"{accuracy:.2f}%"),
    #     ]
    #     for i, (label, value) in enumerate(stats1):
    #         ttk.Label(stats_frame_left, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=0, sticky='w', padx=5, pady=3)
    #         ttk.Label(stats_frame_left, text=value, font=Settings.FONT_HELVETICA_NORMAL).grid(row=i, column=1, sticky='w', padx=5, pady=3)

    #     # Right Column: Time Analysis (with fix for ValueError)
    #     if results["answered"] > 0:
    #         avg_time_str = format_time_always_mmss(avg_time)
    #         fastest_q_str = f"Q{results['fastest_q']['num']} ({format_time_always_mmss(results['fastest_q']['time'])})"
    #         slowest_q_str = f"Q{results['slowest_q']['num']} ({format_time_always_mmss(results['slowest_q']['time'])})"
    #     else:
    #         avg_time_str = "00:00"
    #         fastest_q_str = "N/A"
    #         slowest_q_str = "N/A"

    #     stats2 = [
    #         ("⏱ Total Time", format_time_always_mmss(self.q_seconds)),
    #         ("⌛ Avg. Time / Ques", avg_time_str),
    #         ("⚡ Fastest Ques", fastest_q_str),
    #         ("🐢 Slowest Ques", slowest_q_str),
    #     ]
    #     for i, (label, value) in enumerate(stats2):
    #         ttk.Label(stats_frame_right, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=0, sticky='w', padx=5, pady=3)
    #         ttk.Label(stats_frame_right, text=value, font=Settings.FONT_HELVETICA_NORMAL, bootstyle=Settings.INFO_COLOR).grid(row=i, column=1, sticky='w', padx=5, pady=3)

    #     ttk.Separator(self.scroll_frame, orient="horizontal").pack(fill="x", pady=20, padx=10)
        
    #     # --- Question-wise Analysis ---
    #     ttk.Label(
    #         self.scroll_frame, 
    #         text="📌 Question-wise Analysis:", 
    #         font=Settings.FONT_HELVETICA_14_UNDLIN, 
    #     ).pack(anchor="w", padx=15, pady=(5, 10))
        
    #     for i, q in enumerate(self.quiz_data):
    #         given = str(self.selected_answers.get(i, "")).strip()
    #         ans = str(q.get("answer", "")).strip()
    #         time_taken = q.get('_time_taken', 0.0)

    #         # Create a "card" for each question
    #         q_frame = ttk.Frame(self.scroll_frame, padding=10, borderwidth=1, relief="solid")
    #         q_frame.pack(fill='x', padx=15, pady=6)
            
    #         # Header for the question and time taken
    #         header_frame = ttk.Frame(q_frame)
    #         header_frame.pack(fill='x')
    #         ttk.Label(
    #             header_frame, 
    #             text=f"Q{i+1}: {q['question']}", 
    #             wraplength=700, 
    #             font=Settings.FONT_HELVETICA_NORMAL,
    #         ).pack(side='left', anchor='w')
    #         ttk.Label(header_frame, text=f"({format_time_always_mmss(time_taken)})", bootstyle=Settings.DANGER_COLOR).pack(side='right', anchor='e')

    #         is_correct = (given and given == ans)
    #         is_unanswered = not given

    #         result_style = Settings.WARNING_COLOR if is_unanswered else Settings.SUCCESS_COLOR if is_correct else Settings.DANGER_COLOR
    #         result_text = "🤷‍♂️ Not Answered" if is_unanswered else "✅ Correct" if is_correct else "❌ Incorrect"
            
    #         ttk.Separator(q_frame, orient="horizontal").pack(fill="x", pady=5)

    #         # Display the result
    #         if is_correct:
    #             ttk.Label(q_frame, text=f"{result_text}: {ans}", bootstyle=result_style, font=Settings.FONT_HELVETICA_BOLD).pack(anchor='w')
    #         else:
    #             ttk.Label(q_frame, text=result_text, bootstyle=result_style, font=Settings.FONT_HELVETICA_BOLD).pack(anchor='w', pady=(0, 5))
                
    #             # A separate frame to show the answers
    #             answer_detail_frame = ttk.Frame(q_frame)
    #             answer_detail_frame.pack(fill='x', padx=10)

    #             if not is_unanswered:
    #                 ttk.Label(answer_detail_frame, text="Your Answer:", font=Settings.FONT_HELVETICA_BOLD).grid(row=0, column=0, sticky='w')
    #                 ttk.Label(answer_detail_frame, text=given, bootstyle=Settings.DANGER_COLOR).grid(row=0, column=1, sticky='w', padx=5)

    #             ttk.Label(answer_detail_frame, text="Correct Answer:", font=Settings.FONT_HELVETICA_BOLD).grid(row=1, column=0, sticky='w')
    #             ttk.Label(answer_detail_frame, text=ans, bootstyle=Settings.SUCCESS_COLOR, font=Settings.FONT_HELVETICA_SM_BOLD).grid(row=1, column=1, sticky='w', padx=5)


    def _display_summary(self, results: Dict[str, Any]) -> None:
        """Displays the results in the main display area in a more attractive way."""
        
        def format_time_always_mmss(seconds_float: float) -> str:
            """Formats seconds into MM:SS format, always."""
            seconds_float = max(0, seconds_float)
            mins, secs = divmod(seconds_float, 60)
            return f"{int(mins):02d}:{int(secs):02d}"

        # Clear old widgets
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        # Calculate statistics
        wrong = results["answered"] - results["correct"]
        unattempted = results["total"] - results["answered"]
        accuracy = (results["correct"] / results["answered"] * 100) if results["answered"] > 0 else 0
        avg_time = (results["total_time_on_answered"] / results["answered"]) if results["answered"] > 0 else 0
        
        # --- Header ---
        test_name = self.test_name_label.cget("text")
        ttk.Label(
            self.scroll_frame, 
            text=f"--- Test Summary: {test_name} ---", 
            font=Settings.FONT_HELVETICA_LARGE_BOLD, 
            bootstyle="success"
        ).pack(anchor="center", padx=Settings.PAD_15, pady=(10, 15))

        # --- Main Statistics Frame ---
        stats_container = ttk.Frame(self.scroll_frame)
        stats_container.pack(fill='x', padx=15, pady=5)
        stats_container.columnconfigure((0, 1), weight=1)

        # Two column frames for stats
        stats_frame_left = ttk.Frame(stats_container, padding=(10, 5))
        stats_frame_left.grid(row=0, column=0, sticky="nsew", padx=5)

        stats_frame_right = ttk.Frame(stats_container, padding=(10, 5))
        stats_frame_right.grid(row=0, column=1, sticky="nsew", padx=5)

        # Left Column: Score and Accuracy
        stats1 = [
            ("🏆 Score", f"{results['correct']}/{results['total']}"),
            ("✅ Correct", str(results['correct'])),
            ("❌ Wrong", str(wrong)),
            ("⚪ Unattempted", str(unattempted)),
            ("🎯 Accuracy", f"{accuracy:.2f}%"),
        ]
        for i, (label, value) in enumerate(stats1):
            ttk.Label(stats_frame_left, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=0, sticky='w', padx=5, pady=3)
            ttk.Label(stats_frame_left, text=value, font=Settings.FONT_HELVETICA_NORMAL).grid(row=i, column=1, sticky='w', padx=5, pady=3)

        # Right Column: Time Analysis (with fix for ValueError and improved robustness)
        avg_time_str = "00:00"
        fastest_q_str = "N/A"
        slowest_q_str = "N/A"

        if results["answered"] > 0:
            avg_time_str = format_time_always_mmss(avg_time)
            # Safely access fastest_q data to prevent KeyError
            fastest_q = results.get('fastest_q')
            if fastest_q and 'num' in fastest_q and 'time' in fastest_q:
                fastest_q_str = f"Q{fastest_q['num']} ({format_time_always_mmss(fastest_q['time'])})"
            
            # Safely access slowest_q data to prevent KeyError
            slowest_q = results.get('slowest_q')
            if slowest_q and 'num' in slowest_q and 'time' in slowest_q:
                slowest_q_str = f"Q{slowest_q['num']} ({format_time_always_mmss(slowest_q['time'])})"

        stats2 = [
            ("⏱ Total Time", format_time_always_mmss(self.q_seconds)),
            ("⌛ Avg. Time / Ques", avg_time_str),
            ("⚡ Fastest Ques", fastest_q_str),
            ("🐢 Slowest Ques", slowest_q_str),
        ]
        for i, (label, value) in enumerate(stats2):
            ttk.Label(stats_frame_right, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=0, sticky='w', padx=5, pady=3)
            ttk.Label(stats_frame_right, text=value, font=Settings.FONT_HELVETICA_NORMAL, bootstyle=Settings.INFO_COLOR).grid(row=i, column=1, sticky='w', padx=5, pady=3)

        ttk.Separator(self.scroll_frame, orient="horizontal").pack(fill="x", pady=20, padx=10)
        
        # --- Question-wise Analysis ---
        ttk.Label(
            self.scroll_frame, 
            text="📌 Question-wise Analysis:", 
            font=Settings.FONT_HELVETICA_14_UNDLIN, 
        ).pack(anchor="w", padx=15, pady=(5, 10))
        
        for i, q in enumerate(self.quiz_data):
            given = str(self.selected_answers.get(i, "")).strip()
            ans = str(q.get("answer", "")).strip()
            time_taken = q.get('_time_taken', 0.0)

            # Create a "card" for each question
            q_frame = ttk.Frame(self.scroll_frame, padding=10, borderwidth=1, relief="solid")
            q_frame.pack(fill='x', padx=15, pady=6)
            
            # Header for the question and time taken
            header_frame = ttk.Frame(q_frame)
            header_frame.pack(fill='x')
            ttk.Label(
                header_frame, 
                text=f"Q{i+1}: {q['question']}", 
                wraplength=700, 
                font=Settings.FONT_HELVETICA_NORMAL,
            ).pack(side='left', anchor='w')
            ttk.Label(header_frame, text=f"({format_time_always_mmss(time_taken)})", bootstyle=Settings.DANGER_COLOR).pack(side='right', anchor='e')

            is_correct = (given and given == ans)
            is_unanswered = not given

            result_style = Settings.WARNING_COLOR if is_unanswered else Settings.SUCCESS_COLOR if is_correct else Settings.DANGER_COLOR
            result_text = "🤷‍♂️ Not Answered" if is_unanswered else "✅ Correct" if is_correct else "❌ Incorrect"
            
            ttk.Separator(q_frame, orient="horizontal").pack(fill="x", pady=5)

            # Display the result
            if is_correct:
                ttk.Label(q_frame, text=f"{result_text}: {ans}", bootstyle=result_style, font=Settings.FONT_HELVETICA_BOLD).pack(anchor='w')
            else:
                ttk.Label(q_frame, text=result_text, bootstyle=result_style, font=Settings.FONT_HELVETICA_BOLD).pack(anchor='w', pady=(0, 5))
                
                # A separate frame to show the answers
                answer_detail_frame = ttk.Frame(q_frame)
                answer_detail_frame.pack(fill='x', padx=10)

                if not is_unanswered:
                    ttk.Label(answer_detail_frame, text="Your Answer:", font=Settings.FONT_HELVETICA_BOLD).grid(row=0, column=0, sticky='w')
                    ttk.Label(answer_detail_frame, text=given, bootstyle=Settings.DANGER_COLOR).grid(row=0, column=1, sticky='w', padx=5)

                ttk.Label(answer_detail_frame, text="Correct Answer:", font=Settings.FONT_HELVETICA_BOLD).grid(row=1, column=0, sticky='w')
                ttk.Label(answer_detail_frame, text=ans, bootstyle=Settings.SUCCESS_COLOR, font=Settings.FONT_HELVETICA_SM_BOLD).grid(row=1, column=1, sticky='w', padx=5)


    def _cleanup_after_submit(self) -> None:
        """सबमिशन के बाद UI घटकों को साफ और रीसेट करता है।"""
        if self.right_panel:
            for btn in self.right_panel.q_buttons:
                btn.destroy()
            self.right_panel.q_buttons.clear()
            self.right_panel.quiz_load_btn.config(state="normal")
            # स्टेटस काउंट को 0 पर रीसेट करें
            # self.right_panel.update_status_counts({k: 0 for k in self.right_panel.status_labels})

        self.mark_review.config(state="disabled")
        self.clear_response.config(state="disabled")
        self.btn_save_next.config(state="disabled")
        self.toggle_btn.config(state="normal")
        self.question_number_label.config(text="Test Submitted - Summary")

    def submit_quiz(self) -> None:
        """वर्तमान क्विज़ सत्र को समाप्त करता है और विस्तृत परिणाम प्रदर्शित करता है।"""
        if not self.quiz_data:
            messagebox.showwarning("No Quiz", "Load a quiz first.")
            return
        if not messagebox.askyesno("Submit Test", "Do you want to submit the test?"):
            return

        # अंतिम प्रश्न का समय और उत्तर रिकॉर्ड करें
        self._record_time_spent()
        self.stop_question_timer()
        if self.answer_var.get():
            self.selected_answers[self.current_q_index] = self.answer_var.get().strip()
        
        results = self._calculate_results()
        self._display_summary(results)
        self._cleanup_after_submit()
        
    def quit_quiz(self):
        if self.quiz_data and not messagebox.askyesno("Quit Quiz", "Are you sure you want to quit the quiz?"):
            return
        # REFACTOR: Call the single reset method.
        self._reset_quiz()

        app = self._get_app()
        if app:
            try:
                app.switch_frame(HomePage)
            except Exception:
                try:
                    app.change_frame("Home")
                except Exception:
                    pass

    def _get_app(self):
        return self.winfo_toplevel()

    def update_status_and_buttons(self) -> None:
        if not self.quiz_data or not self.right_panel: return
        self._update_right_button_style(self.current_q_index)
        total = len(self.quiz_data)
        answered_set = {i for i, v in self.selected_answers.items() if v}
        counts = {
            "Answered": len(answered_set),
            "Marked": len(self.marked_for_review),
            "Marked and answered": len(answered_set & self.marked_for_review),
            "Not Visited": total - len(self.visited_questions),
            "Not Answered": total - len(answered_set)
        }
        self.right_panel.update_status_counts(counts)

    def _update_right_button_style(self, index: int) -> None:
        # यह मेथड अपरिवर्तित है
        if not (self.right_panel and 0 <= index < len(self.right_panel.q_buttons)): return
        btn = self.right_panel.q_buttons[index]
        is_answered = bool(self.selected_answers.get(index))
        is_marked = index in self.marked_for_review
        is_visited = index in self.visited_questions
        style_map = {
            (True, True): "primary", (False, True): "warning",
            (True, False): "success", (False, False): "danger" if is_visited else "secondary-outline"
        }
        style = style_map.get((is_answered, is_marked), "secondary-outline")
        btn.config(bootstyle=style)
    
    def show_question(self, index: Optional[int] = None) -> None:
        """दिए गए इंडेक्स पर प्रश्न प्रदर्शित करता है।"""
        self._record_time_spent() # पिछले प्रश्न के लिए समय रिकॉर्ड करें
        
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
        self.question_start_time = time.time() # नए प्रश्न के लिए टाइमर शुरू करें

    def _update_and_move_next(self) -> None:
        """उत्तर सहेजता है और अगले प्रश्न पर जाता है।"""
        if not self.quiz_data: return
        
        current_answer = self.answer_var.get()
        if current_answer: self.selected_answers[self.current_q_index] = current_answer
        else: self.selected_answers.pop(self.current_q_index, None)
        
        self.update_status_and_buttons()
        
        if self.current_q_index < len(self.quiz_data) - 1:
            self.show_question(self.current_q_index + 1)
        else:
            self.show_question(self.current_q_index) # अंतिम प्रश्न पर बने रहें
            messagebox.showinfo("End", "This is the last question.")

    def next_question(self) -> None: self._update_and_move_next()
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
            self.q_seconds += 1
            hrs, rem = divmod(self.q_seconds, 3600)
            mins, secs = divmod(rem, 60)
            self.question_take_time_lbl.config(text=f"Time: {hrs:02d}:{mins:02d}:{secs:02d}")
            self._q_timer_id = self.after(1000, self._update_question_timer)
        except tk.TclError:
            self._q_timer_id = None
    
    def stop_question_timer(self) -> None:
        if self._q_timer_id:
            self.after_cancel(self._q_timer_id)
            self._q_timer_id = None

    def _get_today_date_str(self) -> str: return datetime.now().strftime("Date: %d %b %Y")
    
    def _start_periodic_date_update(self) -> None:
        self.stop_periodic_date_update()
        self._date_after_id = self.after(60_000, self._periodic_update_date_label)

    def _periodic_update_date_label(self) -> None:
        try:
            self.total_left_time_label.config(text=self._get_today_date_str())
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
        super().__init__(themename=Settings.THEME[4])
        self.title(Settings.TITLE)
        self.geometry(f"{Settings.WSIZE[0]}x{Settings.WSIZE[1]}+{Settings.POS[0]}+{Settings.POS[1]}")
        self.minsize(*Settings.WSIZE)
        try:
            self.iconbitmap(Settings.ICON)
        except Exception as e:
            # print(f"Icon file not found Exception: {e}")
            Settings.show_toast(title="Icon Error", message=f"Icon file not found Exception: {e}", bootstyle=WARNING)

        self.history = []
        self.future = []
        self.current_frame = None

        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=BOTH, expand=YES)
        self.main_container.grid_columnconfigure(0, weight=1, uniform="group1")
        self.main_container.grid_rowconfigure(0, weight=20, uniform="group2")
        self.main_container.grid_rowconfigure(1, weight=1, uniform="group2")

        self.main_frame()
        self.bottom_bar()

        # expose frame refs (optional)
        self.left_frame = None
        self.right_frame = None

    def main_frame(self):
        self.main_area_frame = ttk.Frame(self.main_container)
        self.main_area_frame.grid(row=0, column=0, sticky=NSEW)
        self.current_frame = HomePage(self.main_area_frame, app=self)
        self.current_frame.pack(fill=BOTH, expand=YES)

    def bottom_bar(self):
        self.bottom_bar_frame = ttk.Frame(self.main_container, bootstyle="light")
        self.bottom_bar_frame.grid(row=1, column=0, sticky=NSEW)
        self.bottom_bar_status_label = ttk.Label(self.bottom_bar_frame, text="Status: OK", bootstyle=Settings.INVERSE_SECONDARY)
        self.bottom_bar_status_label.pack(side=LEFT, pady=Settings.PAD_SMALL, padx=Settings.PAD_MEDIUM)
        self.bottom_bar_vesion_label = ttk.Label(self.bottom_bar_frame, text=Settings.get_version(), bootstyle=Settings.INVERSE_SECONDARY)
        self.bottom_bar_vesion_label.pack(side=RIGHT, pady=Settings.PAD_SMALL, padx=Settings.PAD_LARGE)

    def switch_frame(self, frame_class, *args, **kwargs):
        if self.current_frame:
            self.history.append(self.current_frame.__class__)
            try:
                self.current_frame.destroy()
            except Exception:
                pass
        self.current_frame = frame_class(self.main_area_frame, app=self, *args, **kwargs)
        self.current_frame.pack(fill=BOTH, expand=YES)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
