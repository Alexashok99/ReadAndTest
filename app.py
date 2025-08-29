
# main.py
import os
import csv
import random
import tkinter as tk
from tkinter import StringVar
from tkinter import messagebox  # Added for potential error handling
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
try:
    # Python 3.9+ -> zoneinfo
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None



class Settings:
    """
    Global UI Settings for the app.
    Sab constants/config yaha store rahenge.
    """

    # --- Window ---
    THEME = ("pulse", "minty", "simplex", "flatly", "darkly", "solar", "cyborg", "vapor")          # Default theme
    TITLE = "ReadAndTest  Author: BIJAY MAHTO"
    WSIZE = (950, 600)       # Window size
    POS = (100, 50)          # Window position
    ICON = "icon.ico"         # (Optional)

    # --- Layout ---
    LFRAME_SIZE = (250, 350)
    PAD_SMALL = 4
    PAD_MEDIUM = 8
    PAD_LARGE = 12

    # --- Button Sizes ---
    SM_BTN_WIDTH = 25
    MD_BTN_WIDTH = 35
    LG_BTN_WIDTH = 45

    # --- Fonts ---
    FONT_TITLE = ("Arial", 16, "bold")
    FONT_SUBTITLE = ("Arial", 12, "bold")
    FONT_NORMAL = ("Arial", 11)

    # --- Bootstrap Colors ---
    COLOURS = [
        "primary", "secondary", "success", "info",
        "warning", "danger", "light", "dark"
    ]

    MOTIVATION_LINES = (
                    "Aaj ka chhota target → kal ka bada success.",
                    "Daily 30 minute focused practice — consistency banati hai champion.",
                    "Speed + Accuracy = Result. Fast solve karna seekho, phir check karo.",
                    "Ek topic roz — 30 din me 30 topics complete.",
                    "Vocabulary roz 5 naye shabd + unke synonyms yaad karo.",
                    "Math tricks roz 10 minute — mental calculation tez hota hai.",
                    "GK ko daily chhote cards me revise karo — repetition important hai.",
                    "Previous year papers do — pattern samajh jaoge aur confidence aayega.",
                    "Har galti se seekho — mistake ko note karo aur dubara na dohrao.",
                    "Revision is king — jo padha uska review roz 15 minute karo.",
                    "Exam-focused padhai — unnecessary cheezein chhodo, syllabus pe tikho.",
                    "Small wins collect karo — har complete topic ek win hai.",
                    "Breaks lo, par study time disciplined rakho — Pomodoro try karo.",
                    "Mock test karo, time-bound practice se speed aur time-management aata hai.",
                    "Plan banao, daily target set karo, aur usko complete karo.",
                    "Distractions hatao — phone thoda door rakho jab padhai karo.",
                    "Healthy routine — sahi neend aur thoda exercise dimaag tez rakhta hai.",
                    "Aaj se ek habit banao: roz padhai + chhota revision.",
                    "Focus problems ko tod do — ek-ek part solve karo, sab saath nahi.",
                    "Confidence build karne ke liye small tests roz do.",
                    "Hard work + Smart strategy = Exam Crack. Dono chahiye.",
                    "Don't compare — apni speed aur progress pe focus karo.",
                    "Jitna practice, utna clarity — practice ko routine banao.",
                    "Aaj se disciplined raho — kal result tumhara hoga."
                )

    # --- Bootstrap Style Modifiers ---
    STYLESES = ["", "-outline", "-link"]

    # Detailed description (Hindi) with simple bullets and motivation
    DETAILS_TEXT = (
            "🎯 ReadAndTest — SSC CGL & Railway Prep Partner\n\n"
            "Ye app specially aapke exam (SSC CGL / Railway) ke liye banaaya gaya hai — unnecessary cheezein nahi.\n\n"
            "🔹 Features:\n"
            "  • Concise Notes — topic-wise, jaldi padhne layak format.\n"
            "  • Quick Quizzes — real-test jaisa experience, shuffle options aur question navigation.\n"
            "  • Progress Summary — score, time taken, aur weak-points dikhayein.\n"
            "  • Daily Target Reminder — chhote, achievable goals jo aap roz complete kar sakte ho.\n"
            "  • Motivation & Consistency — har din thoda padhoge to exam pass karna mumkin hai.\n\n"
            "📌 Aapka goal:\n"
            "Roz 1 chhota target complete karo — vocabulary, fast math tricks, ya 1 mini-quiz.\n\n"
            "💪 App ka promise:\n"
            "Time waste nahi hone denge — sirf exam-focused content. Aaj se consistency — kal se improvement.\n\n"
            "— “Aaj ka chhota target → kal ka bada success.”\n"
            "— “Daily 30 minute focus — CGL crack karne ki disha.”\n"
            "— “Speed + Accuracy = Result. Roz practice karo.”\n"
        )
    
    SAMPLE_NOTES = """
                        🚀 चलो शुरुआत करते हैं! पढ़ाई ही सफलता की असली चाबी है।\n\n
                        💡 याद रखो:
                        हर बार पढ़ाई करने का मतलब है,
                        सपनों के और क़रीब पहुँचना।

                        💡 ध्यान रहे:
                        आज की मेहनत ही कल की सफलता की पहचान होगी।

                        💡 मत भूलो:
                        पढ़ाई का हर एक घंटा,
                        तुम्हारे सपनों की नींव मजबूत करता है।

                        💡 सच्चाई ये है:
                        मेहनत कभी बेकार नहीं जाती,
                        वो देर से सही, लेकिन फल ज़रूर देती है।

                        💡 प्रेरणा लो:
                        जो आज थक कर रुक जाते हैं,
                        वो कल मंज़िल से पीछे रह जाते हैं।

                        💡 याद रखो:
                        हर छोटा कदम,
                        बड़े सपनों की ओर बढ़ाता है।

                        💡 ध्यान रहे:
                        किताबें सिर्फ पन्ने नहीं,
                        तुम्हारे सपनों के दरवाज़े हैं।

                        💡 मत भूलो:
                        आज का संघर्ष ही कल की मुस्कान है।"""
   
    @classmethod
    def get_random_motivation(cls):
        """Return a random motivational line from MOTIVATION_LINES.
        Accepts tuple/list/set/string. Returns empty string if nothing valid."""
        import random

        lines = getattr(cls, "MOTIVATION_LINES", None)
        if not lines:
            return ""

        # If string, split into lines
        if isinstance(lines, str):
            items = [l.strip() for l in lines.splitlines() if l.strip()]
        # If tuple/list/set or any iterable -> convert to list
        elif isinstance(lines, (list, tuple, set)):
            items = list(lines)
        else:
            # try to coerce any iterable to list (defensive)
            try:
                items = list(lines)
            except Exception:
                return ""

        # filter empties
        items = [i for i in items if isinstance(i, str) and i.strip()]
        if not items:
            return ""
        return random.choice(items)
    
    __MAJOR = 1
    __MINOR = 7
    __PATCH = 0
    _VERSION = F"Version: {__MAJOR}.{__MINOR}.{__PATCH}"



class BaseFrame(ttk.Frame):
    """Base frame: standardize constructor to accept (master, app=None)."""
    def __init__(self, master, app=None):
        super().__init__(master)
        self.app = app



class HomeRightFrame(BaseFrame):
    def __init__(self, master, app = None):
        super().__init__(master, app)

        self.btn_read_notes = ttk.Button(self, text="Read Notes",
                   bootstyle="primary-outline", width=Settings.SM_BTN_WIDTH,
                   command=lambda: app.switch_frames(ReadNotesFrame, ReadingControllFrame))
        self.btn_read_notes.pack(pady=Settings.PAD_LARGE)

        self.btn_quiz_time = ttk.Button(self, text="Quiz Time",
                   bootstyle="success-outline", width=Settings.SM_BTN_WIDTH,
                   command=lambda: app.switch_frames(QuizAttemptLeftFrame, QuizRightPanelFrame))
        self.btn_quiz_time.pack(pady=Settings.PAD_LARGE)

        ttk.Button(self, text="Close App",
                   bootstyle="danger-outline", width=Settings.SM_BTN_WIDTH,
                   command=app.destroy).pack(pady=Settings.PAD_LARGE)  # Fixed: False



class HomeLeftFrame(BaseFrame):
    def __init__(self, master, app=None):
        super().__init__(master, app)

        # Title / Tagline
        ttk.Label(self, text="ReadAndTest — SSC CGL & Railway ke liye focused revision",
                  font=Settings.FONT_TITLE, anchor="w").pack(fill="x", pady=(Settings.PAD_MEDIUM, 6), padx=10)

        # Compact subtitle
        ttk.Label(self, text="Roz thoda, roz behtar — concise notes, quick quizzes aur daily targets.",
                  font=Settings.FONT_SUBTITLE, anchor="w").pack(fill="x", padx=10, pady=(0, Settings.PAD_MEDIUM))

        # Scrollable area for detailed description (so long text won't break layout)
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=6)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        # put the inner frame into the canvas
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)

        def _on_config(e):
            try:
                canvas.configure(scrollregion=canvas.bbox("all"))
            except Exception:
                pass
        scroll_frame.bind("<Configure>", _on_config)

        ttk.Label(scroll_frame, text=Settings.DETAILS_TEXT, wraplength=680, justify="left",
                  font=Settings.FONT_NORMAL).pack(anchor="w", padx=6, pady=6)

        # Bottom action buttons (aligned left+right)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=(Settings.PAD_SMALL, Settings.PAD_LARGE), padx=10)

        # Start Quiz button (if user wants to jump to quiz)
        def _start_quiz():
            app_obj = getattr(self, "app", None)
            if not app_obj:
                messagebox.showinfo("Info", "App reference not available.")
                return
            try:
                app_obj.switch_frames(QuizAttemptLeftFrame, QuizRightPanelFrame)
            except Exception:
                try:
                    app_obj.switch_frames(HomeLeftFrame, HomeRightFrame)
                except Exception:
                    messagebox.showinfo("Info", "Quiz frames not available.")

        ttk.Button(btn_frame, text="▶ Start Quick Quiz",
                   bootstyle="success", command=_start_quiz).pack(side=LEFT, padx=(0, 8))

        # Read Notes button (go to notes)
        def _open_notes():
            app_obj = getattr(self, "app", None)
            if not app_obj:
                messagebox.showinfo("Info", "App reference not available.")
                return
            try:
                app_obj.switch_frames(ReadNotesFrame, ReadingControllFrame)
            except Exception:
                messagebox.showinfo("Info", "Notes frames not available.")

        ttk.Button(btn_frame, text="📚 Read Notes",
                   bootstyle="primary-outline", command=_open_notes).pack(side=LEFT)

        # Small motivational helper (non-blocking)
        def _motivate():
            app_obj = getattr(self, "app", None)
            if not app_obj:
                messagebox.showinfo("Motivation", "Chhote steps roz — consistency se bada result aata hai.")
                return
            messagebox.showinfo("Motivation", "Chhote steps roz — consistency se bada result aata hai. Aaj ka target set karo aur shuru karo! 💪")

        ttk.Button(btn_frame, text="✨ Motivation",
                   bootstyle="info-outline", command=_motivate).pack(side=RIGHT)
        
    
        # Motivational label (initial random)
        self._last_mot = None
        self._mot_label = ttk.Label(self, text=self._pick_random_mot(), font=("Helvetica", 10, "italic"), bootstyle = "success")
        # place it where you want; example: below tagline
        self._mot_label.pack(anchor="w", padx=10, pady=(4, 8))

        # start rotator (every 3 seconds). Change interval as you like.
        self._mot_after_id = self.after(3000, self._rotate_motivation)

    def _pick_random_mot(self):
        """Pick a random motivation but try to avoid repeating the last one."""
        for _ in range(6):  # try a few times to avoid immediate repeat
            s = Settings.get_random_motivation()
            if not s:
                return ""
            if s != self._last_mot:
                self._last_mot = s
                return s
        # fallback (if only one item or unlucky), return whatever
        self._last_mot = s
        return s

    def _rotate_motivation(self):
        """Update label and reschedule."""
        try:
            new_text = self._pick_random_mot()
            self._mot_label.config(text=new_text)
            # schedule next change
            self._mot_after_id = self.after(3000, self._rotate_motivation)
        except Exception:
            self._mot_after_id = None

    def destroy(self):
        # cancel scheduled callback
        try:
            if getattr(self, "_mot_after_id", None):
                self.after_cancel(self._mot_after_id)
        except Exception:
            pass
        super().destroy()



class ReadNotesFrame(BaseFrame):
    def __init__(self, master, app=None, text=None):
        super().__init__(master, app)
        # allow frame to expand fully
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.notes_text = text if text else Settings.SAMPLE_NOTES
        self._create_text_view()


    def _select_font_family(self):
        """Pick a font family likely to support multiple languages (Devanagari + Latin).
        Falls back to system default if none available."""
        import tkinter.font as tkfont
        candidates = [
            "Noto Sans Devanagari", "Noto Sans", "DejaVu Sans", "Lohit Devanagari",
            "Mangal", "Nirmala UI", "Segoe UI", "Liberation Sans", "Arial", "Helvetica"
        ]
        for fam in candidates:
            try:
                f = tkfont.Font(family=fam, size=12)
                # if created successfully, return this family
                return fam
            except Exception:
                continue
        # final fallback to default font name
        try:
            default = tkfont.nametofont("TkDefaultFont").actual().get("family", "Helvetica")
        except Exception:
            default = "Helvetica"
        return default


    def _create_text_view(self):
        import tkinter.font as tkfont

        # Outer container (grid-managed) so it fills parent
        container = ttk.Frame(self, bootstyle="light")
        container.grid(row=0, column=0, sticky=NSEW)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # choose font family that can render many languages
        font_family = self._select_font_family()
        text_font = tkfont.Font(family=font_family, size=13)

        # Text widget + scrollbar (no canvas — ensures it fills whole space)
        self.txt = tk.Text(
            container,
            wrap="word",
            font=text_font,
            relief="flat",
            bd=0,
            padx=10,
            pady=8
        )

        vscroll = ttk.Scrollbar(container, orient="vertical", command=self.txt.yview)
        self.txt.configure(yscrollcommand=vscroll.set)

        # layout: text expands to fill, scrollbar sticks to right
        self.txt.grid(row=0, column=0, sticky=NSEW)
        vscroll.grid(row=0, column=1, sticky=NS)

        # Insert content preserving paragraphs
        content = self.notes_text or ""
        # Normalize newlines (convert CRLF -> LF), keep paragraphs
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        self.txt.insert("1.0", content)

        # Optional: configure a paragraph tag for a bit of spacing and margins
        try:
            self.txt.tag_configure("p", spacing1=2, spacing3=8, lmargin1=4, lmargin2=4, rmargin=4, justify="left")
            # apply tag to entire content
            self.txt.tag_add("p", "1.0", "end")
        except Exception:
            pass

        # Make read-only
        self.txt.config(state="disabled")

        # Mouse wheel binding for smooth scrolling (cross-platform)
        def _on_mouse_wheel(event):
            try:
                num = getattr(event, "num", None)
                if num == 4:           # Linux scroll up
                    self.txt.yview_scroll(-1, "units")
                elif num == 5:         # Linux scroll down
                    self.txt.yview_scroll(1, "units")
                else:                  # Windows / macOS
                    self.txt.yview_scroll(int(-1 * (getattr(event, "delta", 0) / 120)), "units")
                return "break"   # prevent bubbling up
            except tk.TclError:
                return "break"

        # Bind only when mouse enters the text area
        def _bind_scroll(_=None):
            self.txt.bind_all("<MouseWheel>", _on_mouse_wheel)   # Windows/macOS
            self.txt.bind_all("<Button-4>", _on_mouse_wheel)     # Linux scroll up
            self.txt.bind_all("<Button-5>", _on_mouse_wheel)     # Linux scroll down

        # Unbind when mouse leaves the text area
        def _unbind_scroll(_=None):
            self.txt.unbind_all("<MouseWheel>")
            self.txt.unbind_all("<Button-4>")
            self.txt.unbind_all("<Button-5>")

        self.txt.bind("<Enter>", _bind_scroll)
        self.txt.bind("<Leave>", _unbind_scroll)

        # keep references for cleanup
        self._vscroll = vscroll
        self._mouse_bindings = True


    def destroy(self):
        # cleanup bindings if present
        try:
            if getattr(self, "txt", None) and self.txt.winfo_exists():
                self.txt.unbind("<MouseWheel>")
                self.txt.unbind("<Button-4>")
                self.txt.unbind("<Button-5>")
        except Exception:
            pass
        super().destroy()



class ReadingControllFrame(BaseFrame):
    """
    Controls for reading area (load .txt, view text, navigation).
    NOTE: renamed from ReadingControllFrame -> ReadingControlFrame (single 'l').
    """
    def __init__(self, master, app = None, path=None):
        super().__init__(master, app)

        self.reader_controller = None
        # self.file_path = r"data/chapter_one_notes.txt"
        self.file_path = path

        self.file_content = None

        # Dictionary me buttons store karenge
        self.question_buttons = {}
        
        # Create buttons
        ttk.Button(self, text="Load File", 
                   bootstyle="danger",
                   width=Settings.SM_BTN_WIDTH,
                   command=self.load_file
                   ).pack(pady=10)

        ttk.Button(self, text="View Text", 
                   bootstyle="primary",
                   width=Settings.SM_BTN_WIDTH,
                   command=self.view_text_file
                   ).pack(pady=10)

        ttk.Button(self, text="Back", 
                   bootstyle="warning",
                   width=Settings.SM_BTN_WIDTH,
                   command=self.go_back
                   ).pack(pady=10)
        
        ttk.Button(self, text="Close App", 
                   bootstyle="danger",
                   width=Settings.SM_BTN_WIDTH,
                   command=app.destroy
                   ).pack(pady=10)


    def load_file(self):
        """Load only .txt file"""
        file_path = filedialog.askopenfilename(
            title="Select a Text File",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            self.file_path = file_path
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.file_content = f.read()
                messagebox.showinfo("Success", f"File loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file:\n{e}")


    def view_text_file(self):
        """Display loaded text file in ReadNotesFrame"""
        if not self.file_content:
            messagebox.showwarning("No File", "Please load a .txt file first")
            return

        # Left = ReadNotesFrame(text=content), Right = ReadingControllFrame
        self.app.switch_frames(
            lambda master: ReadNotesFrame(master, text=self.file_content),
            ReadingControllFrame
        )


    def go_back(self):
        """Go back using app history"""
        self.app.change_frame("Home")



class QuizRightPanelFrame(BaseFrame):
    def __init__(self, master, app = None):
        super().__init__(master, app)

        # Frame layout
        self.grid_rowconfigure(1, weight=1)   # middle area expandable
        self.grid_columnconfigure(0, weight=1)

        self.status_area()
        self.section_area()   # scrollable section
        self.bottom_buttons_area()


    # ---------- Status area ----------
    def status_area(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=EW, pady=5)
        
        # Center the status area content
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(6, weight=1)

        self.status_labels = {}   # 🔴 yaha store karenge

        self.status_data_result = [
            ("Answered", "success", 0),
            ("Marked", "secondary", 0),
            ("Not Visited", "info", 0),
            ("Marked and answered", "primary", 0),
            ("Not Answered", "danger", 0)
        ]

        for i, (text, style, count) in enumerate(self.status_data_result):
            row = ttk.Frame(frame)
            row.grid(row=i, column=1, sticky=W, pady=2)

            lbl_count = ttk.Label(row, text=str(count), bootstyle=f"{style}-inverse")
            lbl_count.pack(side=LEFT, padx=5)

            lbl_text = ttk.Label(row, text=text, font=("Helvetica", 10))
            lbl_text.pack(side=LEFT, padx=5)

            self.status_labels[text] = lbl_count   # 🔴 save kar liya


    # ---------- Section & Questions (scrollable) ----------
    def section_area(self):
        outer_frame = ttk.Frame(self)
        outer_frame.grid(row=1, column=0, sticky=NSEW, pady=5, padx=2)
        # outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1) # Center the content

        section_lbl = ttk.Label(
            outer_frame, text="SECTION : टेस्ट",
            font=("Helvetica", 10, "bold"), bootstyle="inverse-info"
        )
        section_lbl.grid(row=0, column=0, sticky=EW, pady=2)

        # Canvas + Scrollbar
        canvas_frame = ttk.Frame(outer_frame)
        canvas_frame.grid(row=1, column=0, sticky=NSEW)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)  # inner frame

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)
        self.canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)

        # MouseWheel binding (only on canvas area)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)     # Windows
        self.canvas.bind("<Button-4>", self._on_mousewheel)       # Linux
        self.canvas.bind("<Button-5>", self._on_mousewheel)


    def create_question_buttons(self, total_questions):
        """Create navigation buttons for each question."""
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        self.q_buttons = []

        for i in range(total_questions):
            btn = ttk.Button(
                self.scroll_frame,
                text=str(i+1),
                width=3,
                bootstyle="secondary-outline",
                command=lambda idx=i: self.jump_to_question(idx)
            )
            btn.grid(row=i//5, column=i%5, padx=5, pady=5)
            self.q_buttons.append(btn)


    def jump_to_question(self, index):
        """On click, show that question in left frame."""
        if hasattr(self.app, "left_frame") and self.app.left_frame:
            self.app.left_frame.show_question(index)


    def _on_mousewheel(self, event):
        """ Mousewheel scrolling fix (cross-platform) """
        try:
            num = getattr(event, "num", None)
            if num == 4:      # Linux scroll up
                self.canvas.yview_scroll(-1, "units")
            elif num == 5:    # Linux scroll down
                self.canvas.yview_scroll(1, "units")
            else:              # Windows / Mac
                self.canvas.yview_scroll(int(-1*(getattr(event, "delta", 0)/120)), "units")
        except tk.TclError:
            # canvas may have been destroyed — ignore
            return


    # # ---------- Bottom Buttons ----------
    def bottom_buttons_area(self):
        frame = ttk.Frame(self)
        frame.grid(row=2, column=0, sticky=EW, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(4, weight=1)

        btn_container = ttk.Frame(frame)
        btn_container.grid(row=0, column=1, columnspan=3, sticky=NSEW)

        # btn1 = ttk.Button(btn_container, text="Question Paper", bootstyle="info-outline")
        self.quiz_load_btn = ttk.Button(btn_container, text="Load Quiz", bootstyle="info-outline")
        self.quiz_submit_button = ttk.Button(btn_container, text="Submit Test", bootstyle="success")

        # btn1.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.quiz_load_btn.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.quiz_submit_button.pack(side=LEFT, expand=True, padx=5, pady=5)


    def update_status_counts(self, counts: dict):
        """
        counts ek dict hoga jaise:
        {
        "Answered": 3,
        "Marked": 2,
        "Not Visited": 10,
        "Marked and answered": 1,
        "Not Answered": 4
        }
        """
        for key, value in counts.items():
            if key in self.status_labels:
                self.status_labels[key].config(text=str(value))



class QuizAttemptLeftFrame(BaseFrame):
    def __init__(self, master, app = None):
        super().__init__(master, app)

        # Grid Layout
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=3, uniform="group2")
        self.grid_rowconfigure(1, weight=3, uniform="group2")
        self.grid_rowconfigure(2, weight=26, uniform="group2")
        self.grid_rowconfigure(3, weight=3, uniform="group2")
        self.grid_propagate(False)

        self.right_panel = None  # later App.switch_frames() will set this
        
        self.shuffle_options = False
        self.shuffle_questions = False  # अगर आप कभी बंद करना चाहें तो False कर दें

        self.quiz_data = []          # List of dicts {question, option1-4, answer}
        self.current_q_index = 0
        self.selected_answers = {}   # {q_index: selected_option}
        self.marked_for_review = set()  # indices marked for review

        self.visited_questions = set()

        self.q_seconds = 0        # total seconds passed for question timer
        self._q_timer_id = None   # after() id — use to cancel timer safely


        # single variable used by Radiobuttons across questions
        self.answer_var = tk.StringVar()

        self.s = Settings()
        self.tob_view_area()
        self.second_tob_view_area()
        self.question_options_view_area()
        self.bottom_view_area()


    def tob_view_area(self):
        self.top_area_frame = ttk.Frame(self)
        self.top_area_frame.grid(row=0, column=0, sticky=NSEW)

        self.section_name_label = ttk.Label(self.top_area_frame, text="SECTIONS", anchor="w", bootstyle="secondary", font=("Helvetica", 11, "bold"))
        self.section_name_label.pack(side=LEFT, padx=10, pady=5)
        # Test Name Label
        self.test_name_label = ttk.Label(self.top_area_frame, text="Test", anchor="e", 
                            bootstyle="primary", font=("Helvetica", 11, "bold"))
        self.test_name_label.pack(side=LEFT, padx=10, pady=5)
        # --- total_left_time_label now shows today's date ---
        self.total_left_time_label = ttk.Label(self.top_area_frame, text=self._get_today_date_str(), anchor="e", 
                            bootstyle="danger", font=("Helvetica", 11, "bold"))
        self.total_left_time_label.pack(side=RIGHT, padx=10, pady=5)
        # MODE HARD OR NOT
        self.toggle_btn = ttk.Radiobutton(self.top_area_frame, 
                                          text='Mode: EASY', 
                                          style='danger.TRadiobutton',
                                          command= self.toggle_action
                                          )
        self.toggle_btn.pack(side=RIGHT, padx=10, pady=5)

        # optional: keep the label updated every 60 seconds (catches midnight change)
        try:
            # cancel previous if exists
            if hasattr(self, "_date_after_id") and self._date_after_id:
                self.after_cancel(self._date_after_id)
        except Exception:
            pass
        # schedule periodic update
        self._date_after_id = self.after(60_000, self._periodic_update_date_label)


    def second_tob_view_area(self):
        self.top_second_area_frame = ttk.Frame(self)
        self.top_second_area_frame.grid(row=1, column=0, sticky=NSEW)

        self.question_number_label = ttk.Label(self.top_second_area_frame, text="Please Load Quiz File", anchor="w", font=("Helvetica", 11, "bold"))
        self.question_number_label.pack(side=LEFT, padx=10, pady=5)

        self.question_take_time_lbl = ttk.Label(self.top_second_area_frame, text="Time: 00:00:00", anchor="e", 
                             bootstyle="info", font=("Helvetica", 11, "bold"))
        self.question_take_time_lbl.pack(side=LEFT, padx=40, pady=5)

        self.btn_quit_quiz = ttk.Button(self.top_second_area_frame, text="Quit", bootstyle="danger-outline", command=self.quit_quiz)
        self.btn_quit_quiz.pack(side=RIGHT, padx=10, pady=5)

    # ---------- Question + Options with Scrollbar ----------
    def question_options_view_area(self):
        frame = ttk.Frame(self, bootstyle="light")
        frame.grid(row=2, column=0, sticky=NSEW)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Create canvas + scrollbar
        canvas = tk.Canvas(frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        self.scroll_frame = scroll_frame

        # Configure canvas window
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)

        # Make scrollregion update
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", on_configure)

        # demo: initially empty options (real options will be shown by show_question)
        self.answer_var.set("")
        # no static options here


    # ---------- Bottom Bar (Buttons) ----------
    def bottom_view_area(self):
        frame = ttk.Frame(self)
        frame.grid(row=3, column=0, sticky=NSEW)

        self.mark_review = ttk.Button(frame, text="Mark for Review & Next", bootstyle="secondary-outline")
        self.clear_response = ttk.Button(frame, text="Clear Response", bootstyle="danger-outline")
        self.btn_save_next = ttk.Button(frame, text="Save & Next", bootstyle="success", width=self.s.SM_BTN_WIDTH)

        self.mark_review.pack(side=LEFT, padx=10, pady=5)
        self.clear_response.pack(side=LEFT, padx=10, pady=5)
        self.btn_save_next.pack(side=RIGHT, padx=30, pady=5)

        # bind actions
        self.mark_review.config(command=self.mark_for_review)
        self.clear_response.config(command=self.clear_current_response)
        self.btn_save_next.config(command=self.next_question)


    def quit_quiz(self):
        """Confirm -> clear quiz data/UI -> go Home -> re-enable top-bar widgets."""
        do_quit = messagebox.askyesno("Quit Quiz", "Kya aap sach me quiz quit karna chahte ho?")
        if not do_quit:
            return


        # ---------- 1) Clear internal quiz state ----------
        try:
            self.selected_answers.clear()
        except Exception:
            self.selected_answers = {}

        try:
            self.marked_for_review.clear()
        except Exception:
            self.marked_for_review = set()

        try:
            self.visited_questions.clear()
        except Exception:
            self.visited_questions = set()

        self.quiz_data.clear()
        self.current_q_index = 0
        self.answer_var.set("")

        # ---------- 2) Clear left-panel question area (if exists) ----------
        if hasattr(self, "scroll_frame") and self.scroll_frame.winfo_exists():
            for w in self.scroll_frame.winfo_children():
                w.destroy()

        # reset labels in left-frame
        if hasattr(self, "question_number_label"):
            self.question_number_label.config(text="Please Load Quiz File")
        if hasattr(self, "test_name_label"):
            self.test_name_label.config(text="Test")
        # stop timer first
        self.stop_question_timer()
        self.q_seconds = 0
        if hasattr(self, "question_take_time_lbl"):
            self.question_take_time_lbl.config(text="Time: 00:00:00")

        # ---------- 3) Clear right-panel (question buttons + status) if present ----------
        # use self.right_panel (set when quiz frames connected) if available
        if getattr(self, "right_panel", None):
            try:
                for w in self.right_panel.scroll_frame.winfo_children():
                    w.destroy()
            except Exception:
                pass

            # reset status counts to zero (if method exists)
            try:
                self.right_panel.update_status_counts({
                    "Answered": 0, "Marked": 0, "Not Visited": 0,
                    "Marked and answered": 0, "Not Answered": 0
                })
            except Exception:
                pass

        # ---------- 4) Switch back to Home (via App) ----------
        app = self._get_app()
        if app:
            # Switch frames to Home
            try:
                app.switch_frames(HomeLeftFrame, HomeRightFrame)
            except Exception:
                # fallback: try to call change_frame("Home")
                try:
                    app.change_frame("Home")
                except Exception:
                    pass

            # ---------- 5) Re-enable top-bar widgets (if they were disabled on quiz start) ----------
            if getattr(app, "btn_back", None):
                try: app.btn_back.config(state="normal")
                except Exception: pass
            if getattr(app, "btn_forward", None):
                try: app.btn_forward.config(state="normal")
                except Exception: pass
            if getattr(app, "btn_home", None):
                try: app.btn_home.config(state="normal")
                except Exception: pass
            # if getattr(app, "search_button", None):
            #     try: app.search_button.config(state="normal")
            #     except Exception: pass
            # if getattr(app, "search_entry", None):
            #     try: app.search_entry.config(state="normal")
            #     except Exception: pass

        # NOTE: don't try to modify self.btn_quit_quiz AFTER switching frames,
        # because the widget will get destroyed during switch_frames (causes TclError).

    # ------------------ helper to access app & right panel safely ------------------
    def _get_app(self):
        """Return the top-level App object (if available)."""
        app = self.winfo_toplevel()
        return app


    def update_right_button(self, index):
        """Update the style of the corresponding button in right panel (if exists)."""
        app = self._get_app()
        if not app:
            return
        right = getattr(app, "right_frame", None)
        if not right or not hasattr(right, "q_buttons"):
            return
        if index < 0 or index >= len(right.q_buttons):
            return

        btn = right.q_buttons[index]

        # determine state
        answered = bool(str(self.selected_answers.get(index, "")).strip())
        marked = (index in self.marked_for_review)
        visited = index in self.visited_questions

        # Decide style (priority: marked+answered > marked-only > answered > not answered (red) > not visited)
        if marked and answered:
            style = "primary"       # marked + answered
        elif marked and not answered:
            style = "warning"       # marked only (but not answered)
        elif answered:
            style = "success"       # answered
        elif visited and not answered:
            # visited but left without answering -> make it red as requested
            style = "danger"
        else:
            # not visited -> subtle outline
            style = "secondary-outline"

        # apply style safely
        try:
            btn.config(bootstyle=style)
        except Exception:
            try:
                btn.configure(bootstyle=style)
            except Exception:
                # last-resort: ignore if the style name invalid for this widget
                pass


    def update_all_buttons(self):
        """Call update_right_button for all loaded questions."""
        for i in range(len(self.quiz_data)):
            self.update_right_button(i)

    # ------------------ Quiz control methods ------------------
    def load_quiz(self):
        file_path = filedialog.askopenfilename(
            title="Select Quiz CSV",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not file_path:
            return

        # Read CSV & basic validation
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                # require 'question' header (case-insensitive)
                if not any(h.lower() == "question" for h in headers):
                    messagebox.showerror("Invalid CSV", "CSV में कम से कम 'question' header होना चाहिए।")
                    return

                f.seek(0)
                reader = csv.DictReader(f)
                rows = []
                for i, row in enumerate(reader):
                    if row.get("question"):
                        # normalize whitespace on option/answer fields
                        for k in list(row.keys()):
                            if isinstance(row[k], str):
                                row[k] = row[k].strip()
                        row["_orig_index"] = i  # original file position
                        rows.append(row)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load quiz:\n{e}")
            return

        if not rows:
            messagebox.showwarning("Empty", "CSV has no questions or wrong headers.")
            return

        # Prepare options for each question and shuffled options
        for row in rows:
            opts = []
            for k in ("option1", "option2", "option3", "option4"):
                v = row.get(k, "")
                if v and str(v).strip():
                    opts.append(str(v).strip())
            # store canonical list and shuffled-per-session list
            row["_options"] = opts
            if self.shuffle_options and len(opts) > 1:
                # create a new shuffled list (so original opts stays intact if needed)
                row["_shuffled_options"] = random.sample(opts, k=len(opts))
            else:
                row["_shuffled_options"] = list(opts)

        # Assign quiz data and shuffle questions (random order each load)
        self.quiz_data = list(rows)
        # random.shuffle(self.quiz_data)
        if getattr(self, "shuffle_questions", False):
            random.shuffle(self.quiz_data)

        # Show test name (nice formatting)
        filename = os.path.basename(file_path)
        name = os.path.splitext(filename)[0]
        try:
            self.test_name_label.config(text=name.replace("_", " ").title())
        except Exception:
            pass

        # ✅ App reference
        app = self._get_app()
        if app:
            if getattr(app, "btn_back", None):
                app.btn_back.config(state="disabled")
            if getattr(app, "btn_forward", None):
                app.btn_forward.config(state="disabled")
            if getattr(app, "btn_home", None):
                app.btn_home.config(state="disabled")
            if getattr(app, "search_button", None):
                app.search_button.config(state="disabled")
            if getattr(app, "search_entry", None):
                app.search_entry.config(state="disabled")

        # Disable the Load Quiz button so user can't reload mid-attempt
        try:
            if getattr(self, "right_panel", None) and getattr(self.right_panel, "quiz_load_btn", None):
                self.right_panel.quiz_load_btn.config(state="disabled")
                self.toggle_btn.config(state="disabled")
            else:
                app = self._get_app()
                if app and getattr(app, "right_frame", None) and getattr(app.right_frame, "quiz_load_btn", None):
                    app.right_frame.quiz_load_btn.config(state="disabled")
                    self.toggle_btn.config(state="disabled")
        except Exception:
            pass

        # Reset quiz state
        self.current_q_index = 0
        self.selected_answers.clear()
        self.marked_for_review.clear()
        self.answer_var.set("")
        self.visited_questions.clear()
        self.option_buttons = []

        # Reset timer to 0 and start
        self.q_seconds = 0
        if hasattr(self, "question_take_time_lbl"):
            try:
                self.question_take_time_lbl.config(text="Time: 00:00:00")
            except Exception:
                pass
        self.start_question_timer()

        # Show first Q and create right panel buttons
        self.show_question()
        if self.right_panel:
            self.right_panel.create_question_buttons(len(self.quiz_data))

        # Update counts
        self.update_status_area()


    def show_question(self, index=None):
        """Render question (current or by index) using per-question shuffled options."""
        if not self.quiz_data:
            return

        # set index if provided
        if index is not None:
            # ensure index bounds
            if 0 <= index < len(self.quiz_data):
                self.current_q_index = index
            else:
                return

        # mark visited
        self.visited_questions.add(self.current_q_index)

        # clear old widgets in question area
        for w in self.scroll_frame.winfo_children():
            try:
                w.destroy()
            except Exception:
                pass
        self.option_buttons = []

        qdata = self.quiz_data[self.current_q_index]
        q_text = str(qdata.get("question", "")).strip()

        # show original file index (optional helpful info)
        orig_idx = qdata.get("_orig_index")
        orig_text = f" (orig {orig_idx+1})" if orig_idx is not None else ""

        # update question number label
        try:
            self.question_number_label.config(
                text=f"Question No. {self.current_q_index+1} / {len(self.quiz_data)}"
            )
        except Exception:
            pass

        ttk.Label(
            self.scroll_frame,
            text=f"Q{self.current_q_index+1}: {q_text}",
            wraplength=700,
            font=("Helvetica", 12)
        ).pack(anchor="w", padx=15, pady=10)

        # get shuffled options prepared earlier; fallback defensively
        opts = qdata.get("_shuffled_options")
        if not opts:
            opts = [qdata.get(k, "").strip() for k in ("option1", "option2", "option3", "option4") if qdata.get(k, "").strip()]

        # prepare variable and restore previous selection (value == option text)
        prev = self.selected_answers.get(self.current_q_index, "")
        self.answer_var.set(prev)

        # create radiobuttons using the opts order (shuffled)
        for opt_text in opts:
            # skip empty
            if not opt_text:
                continue
            r = ttk.Radiobutton(
                self.scroll_frame,
                text=opt_text,
                value=opt_text,
                variable=self.answer_var
            )
            r.pack(anchor="w", padx=30, pady=3)
            self.option_buttons.append(r)

        # update right-panel button style for this index
        self.update_right_button(self.current_q_index)

        # update status counts
        self.update_status_area()


    def next_question(self):
        """Save current selection and go to next question (if any)."""
        if not self.quiz_data:
            return
        # save current answer
        self.selected_answers[self.current_q_index] = self.answer_var.get()

        # update style for the question we just left
        self.update_right_button(self.current_q_index)

        if self.current_q_index < len(self.quiz_data) - 1:
            self.current_q_index += 1
            self.show_question()
        else:
            messagebox.showinfo("End", "This is the last question.")

        self.update_status_area()


    def mark_for_review(self):
        """Mark current question for review and then move to next question automatically (if exists)."""
        if not self.quiz_data:
            return

        # save current selection if any
        try:
            self.selected_answers[self.current_q_index] = self.answer_var.get().strip()
        except Exception:
            pass

        # mark current
        idx = self.current_q_index
        self.marked_for_review.add(idx)

        # update UI for this button
        self.update_right_button(idx)
        self.update_status_area()

        # move to next question automatically if there is one
        if self.current_q_index < len(self.quiz_data) - 1:
            self.current_q_index += 1
            self.show_question()
        else:
            messagebox.showinfo("End", "This is the last question.")
            # last question — stay here (silent). If you prefer, you could wrap to 0 or show a small non-blocking visual.
            

    def clear_current_response(self):
        """Clear selected answer for current question and also remove mark if present."""
        if not self.quiz_data:
            return
        idx = self.current_q_index
        # clear stored answer & variable
        if idx in self.selected_answers:
            self.selected_answers.pop(idx, None)
        self.answer_var.set("")

        # if it was marked for review, remove mark
        if idx in self.marked_for_review:
            self.marked_for_review.discard(idx)

        # update right-panel button style
        self.update_right_button(idx)
        # messagebox.showinfo("Cleared", f"Response (and mark) cleared for Question {idx+1}.")

        self.update_status_area()


    def submit_quiz(self):
        """Confirm, then calculate score and show summary inside the question area.
        No final OK popup (silent)."""
        if not self.quiz_data:
            messagebox.showwarning("No Quiz", "Load a quiz first.")
            return

        # ask confirmation before submitting
        do_submit = messagebox.askyesno("Submit Test", "Kya aap test submit karna chahte hain? (Yes/No)")
        if not do_submit:
            return

        # save current answer for the visible question
        self.selected_answers[self.current_q_index] = self.answer_var.get().strip()

        # stop timer
        try:
            self.stop_question_timer()
        except Exception:
            pass

        # compute total time string
        hrs, rem = divmod(self.q_seconds, 3600)
        mins, secs = divmod(rem, 60)
        total_time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"

        total = len(self.quiz_data)
        correct = 0
        wrong_details = []
        for i, q in enumerate(self.quiz_data):
            given = str(self.selected_answers.get(i, "")).strip()
            ans = str(q.get("answer", "")).strip()
            if given and given == ans:
                correct += 1
            else:
                wrong_details.append((i+1, q.get("question", ""), given or "<No Answer>", ans or "<No Key>"))

        wrong = total - correct
        not_answered_list = [str(i+1) for i in range(total) if not str(self.selected_answers.get(i, "")).strip()]
        not_answered_count = len(not_answered_list)
        marked_count = len(self.marked_for_review)
        marked_list = ", ".join(str(i+1) for i in sorted(self.marked_for_review)) if marked_count else "None"

        # --- Clear left question display and show the summary there ---
        try:
            for w in self.scroll_frame.winfo_children():
                w.destroy()
        except Exception:
            pass

        # Header with test name (if available)
        test_name = ""
        try:
            test_name = self.test_name_label.cget("text") if hasattr(self, "test_name_label") else ""
        except Exception:
            test_name = ""

        header_text = f"--- Test Summary ---"
        if test_name:
            header_text = f"--- Test Summary:- {test_name} ---"
        ttk.Label(self.scroll_frame, text=header_text, font=("Helvetica", 14, "bold"), bootstyle = "success").pack(anchor="w", padx=15, pady=(10,6))

        # Basic stats
        stats = [
            ("📋 Total Questions", str(total)),
            ("⏱ Total Time", total_time_str),
            ("🏆 Score", f"{correct}/{total}  ({(correct/total*100):.1f}%)"),
            ("✅ Correct", str(correct)),
            ("❌ Wrong", str(wrong)),
            ("⚪ Not Answered", str(not_answered_count)),
            ("🔖 Marked For Review", str(marked_count)),
            ("🗂 Marked Questions", marked_list),
        ]
        for label, value in stats:
            ttk.Label(self.scroll_frame, 
                      text=f"{label}: {value}", 
                      font=("Helvetica", 11),
                      bootstyle = "info",
                      ).pack(anchor="w", padx=20, pady=2)

        ttk.Separator(self.scroll_frame, orient="horizontal").pack(fill="x", pady=8, padx=10)

        # Show lists: not answered & wrong details (if any)
        # Show lists: not answered & wrong details
        if not_answered_count:
            ttk.Label(
                self.scroll_frame,
                text=f"⚠️ Not Answered Questions: {', '.join(not_answered_list)}",
                font=("Helvetica", 10, "italic"),
                bootstyle = "warning"
            ).pack(anchor="w", padx=25, pady=4)

        if wrong_details:
            ttk.Label(
                self.scroll_frame,
                text="📌 Wrong / Unanswered Details:",
                font=("Helvetica", 12, "underline"),
                bootstyle = "danger"
            ).pack(anchor="w", padx=20, pady=(10, 5))

            for idx, qtext, given, ans in wrong_details[:200]:
                lbl = ttk.Label(
                    self.scroll_frame,
                    text=f"Q{idx}: {qtext}\n    📝 Your: {given}   |   ✅ Ans: {ans}",
                    wraplength=700,
                    font=("Helvetica", 10),
                    bootstyle = "info"
                )
                lbl.pack(anchor="w", padx=30, pady=5)

        ttk.Label(self.scroll_frame, 
                  text="(Quiz cleared from memory — use Load Quiz to start new attempt)", 
                  bootstyle = "danger",
                  font=("Helvetica", 9, "italic")
                  ).pack(anchor="w", padx=15, pady=(10,20))

        # --- Clear internal state and right-panel UI ---
        try:
            self.selected_answers.clear()
        except Exception:
            self.selected_answers = {}

        try:
            self.marked_for_review.clear()
        except Exception:
            self.marked_for_review = set()

        try:
            self.visited_questions.clear()
        except Exception:
            self.visited_questions = set()

        # Clear right-panel buttons and reset status counts
        if getattr(self, "right_panel", None):
            try:
                for b in getattr(self.right_panel, "q_buttons", [])[:]:
                    try:
                        b.destroy()
                    except Exception:
                        pass
                self.right_panel.q_buttons = []
                try:
                    self.right_panel.update_status_counts({
                        "Answered": 0, "Marked": 0, "Not Visited": 0,
                        "Marked and answered": 0, "Not Answered": 0
                    })
                except Exception:
                    pass
            except Exception:
                pass

        # Clear quiz data
        try:
            self.quiz_data.clear()
        except Exception:
            self.quiz_data = []

        # Reset left-panel labels / vars
        if hasattr(self, "question_number_label"):
            self.question_number_label.config(text="Test Submitted - Summary")
        if hasattr(self, "test_name_label"):
            self.test_name_label.config(text="Test")
        self.current_q_index = 0
        self.answer_var.set("")
        self.q_seconds = 0
        if hasattr(self, "question_take_time_lbl"):
            try:
                self.question_take_time_lbl.config(text="Time: 00:00:00")
            except Exception:
                pass

        # NOTE: we removed the final messagebox popup intentionally (silent).
        # --- After clearing quiz data and UI (near the end of submit_quiz) ---
        # Re-enable Load Quiz button so user can load another CSV
        try:
            if getattr(self, "right_panel", None) and getattr(self.right_panel, "quiz_load_btn", None):
                self.right_panel.quiz_load_btn.config(state="normal")
                self.toggle_btn.config(state="normal")
            else:
                app = self._get_app()
                if app and getattr(app, "right_frame", None) and getattr(app.right_frame, "quiz_load_btn", None):
                    app.right_frame.quiz_load_btn.config(state="normal")
                    self.toggle_btn.config(state="normal")
        except Exception:
            pass


    def update_status_area(self):
        total = len(self.quiz_data)

        # Count ALL answered questions (across whole quiz)
        answered_set = {i for i in range(total) if str(self.selected_answers.get(i, "")).strip()}

        # Count ALL marked questions
        marked_set = {i for i in range(total) if i in self.marked_for_review}

        # Marked AND answered
        marked_and_answered = answered_set & marked_set

        # Not answered = total - answered (as you requested)
        not_answered_count = max(total - len(answered_set), 0)

        # Not visited = questions never shown to user yet
        not_visited_count = max(total - len(self.visited_questions), 0)

        counts = {
            "Answered": len(answered_set),                 # includes marked+answered
            "Marked": len(marked_set),                     # total marked (only-marked + marked+answered)
            "Marked and answered": len(marked_and_answered),
            "Not Answered": not_answered_count,            # total - answered
            "Not Visited": not_visited_count
        }

        if self.right_panel:
            self.right_panel.update_status_counts(counts)


    def start_question_timer(self):
        """Start/reset and begin the question timer from current self.q_seconds."""
        # ensure any previous timer is cancelled first
        self.stop_question_timer()
        # reset seconds if you want timer to start from 0 every load — caller can set q_seconds first
        # self.q_seconds = 0   # (we will reset before calling start in load_quiz)
        self._q_timer_id = self.after(1000, self._update_question_timer)  # schedule first tick after 1s


    def _update_question_timer(self):
        """Internal tick handler (called every 1s)."""
        try:
            # If widget/frame was destroyed, winfo_exists() will be False -> stop scheduling further ticks
            if not getattr(self, "question_take_time_lbl", None) or not self.winfo_exists():
                self._q_timer_id = None
                return

            # increment seconds and compute HH:MM:SS
            self.q_seconds += 1
            hrs, rem = divmod(self.q_seconds, 3600)
            mins, secs = divmod(rem, 60)
            # format like Time: 00:00:00
            self.question_take_time_lbl.config(text=f"Time: {hrs:02d}:{mins:02d}:{secs:02d}")

            # schedule next tick
            self._q_timer_id = self.after(1000, self._update_question_timer)
        except tk.TclError:
            # widget destroyed while callback executing — stop safely
            self._q_timer_id = None
            return


    def stop_question_timer(self):
        """Cancel any running timer and reset timer id."""
        try:
            if self._q_timer_id is not None:
                self.after_cancel(self._q_timer_id)
        except Exception:
            pass
        self._q_timer_id = None


    def _get_today_date_str(self):
        """Return formatted date string for Asia/Kolkata (fallback to local)."""
        try:
            if ZoneInfo is not None:
                now = datetime.now(ZoneInfo("Asia/Kolkata"))
            else:
                now = datetime.now()
        except Exception:
            now = datetime.now()
        return now.strftime("Date: %d %b %Y")   # Example: Date: 28 Aug 2025


    def _periodic_update_date_label(self):
        """Update date label periodically (every minute)."""
        try:
            if hasattr(self, "total_left_time_label") and self.total_left_time_label.winfo_exists():
                self.total_left_time_label.config(text=self._get_today_date_str())
                # schedule next update in 60 seconds
                self._date_after_id = self.after(60_000, self._periodic_update_date_label)
        except tk.TclError:
            # widget gone — stop scheduling
            self._date_after_id = None

    def toggle_action(self):
        self.shuffle_options = not self.shuffle_options
        self.shuffle_questions = not self.shuffle_questions  # Flip True/False

        if self.shuffle_options:
            self.toggle_btn.config(text="Mode: HARD")
            # print(f"Hard Mode Activated: {self.shuffle_options}")
        else:
            self.toggle_btn.config(text="Mode: EASY")
            # print(f"Hard Mode Deactivated: {self.shuffle_options}")


class App(ttk.Window, Settings):
    def __init__(self):
        super().__init__(themename=Settings.THEME[4])
        # --- Window Config ---
        self.title(Settings.TITLE)
        self.geometry(f"{Settings.WSIZE[0]}x{Settings.WSIZE[1]}+{Settings.POS[0]}+{Settings.POS[1]}")
        self.minsize(*Settings.WSIZE)
        try:
            self.iconbitmap(Settings.ICON)
        except Exception as e:
            print(f"Icon file not found Exception: {e}")

        self.history = []        # Frame history
        self.future = []         # Forward stack
        self.current_frame = None

        self.left_frame = None
        self.right_frame = None

        # --- Main Container ---
        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES)

        # Grid Layout
        self.container.grid_columnconfigure(0, weight=4, uniform="group1")
        self.container.grid_columnconfigure(1, weight=1, uniform="group1")
        self.container.grid_rowconfigure(0, weight=3, uniform="group2")
        self.container.grid_rowconfigure(1, weight=20, uniform="group2")
        self.container.grid_rowconfigure(2, weight=2, uniform="group2")
        self.container.grid_propagate(False)

        # --- Sections ---
        self.top_bar()
        self.main_left_view_area()
        self.main_right_btn_area()
        self.left_bottom_bar()
        self.right_bottom_bar()

    # ---------------- TOP BAR ----------------
    def top_bar(self):
        self.top_bar_frame = ttk.Frame(self.container,  padding=Settings.PAD_SMALL)
        self.top_bar_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # Left controls
        left_wrap = ttk.Frame(self.top_bar_frame)
        left_wrap.pack(side=LEFT)

        self.btn_back = ttk.Button(left_wrap, text="⬅ Back", bootstyle="info-outline",
                   command=lambda: self.change_frame("Back"))
        self.btn_back.pack(side=LEFT, padx=Settings.PAD_SMALL)

        self.btn_forward = ttk.Button(left_wrap, text="➡ Forward", bootstyle="info-outline",
                   command=lambda: self.change_frame("Forward"))
        self.btn_forward.pack(side=LEFT, padx=Settings.PAD_SMALL)

        self.btn_home = ttk.Button(left_wrap, text="🏠 Home", bootstyle="info-outline",
                   command=lambda: self.change_frame("Home"))
        self.btn_home.pack(side=LEFT, padx=Settings.PAD_SMALL)

        self.frame_name_var = StringVar(value="Home")
        self.frame_name_label = ttk.Label(left_wrap, textvariable=self.frame_name_var,
                    bootstyle="success", font=Settings.FONT_SUBTITLE, anchor="w")
        # Let label take remaining space but not push right_wrap off-screen
        self.frame_name_label.pack(side=LEFT, padx=Settings.PAD_MEDIUM, fill="x", expand=True)

        # Right controls (search group)
        right_wrap = ttk.Frame(self.top_bar_frame)
        right_wrap.pack(side=RIGHT)

        self.search_entry = ttk.Entry(right_wrap, width=26, state="disabled")
        self.search_button = ttk.Button(right_wrap, 
                                        text="🔍 Search", 
                                        bootstyle="info-outline",
                   command=self.search_action,
                   state="disabled"
                   )

        # optional small label
        ttk.Label(right_wrap, text="Theme:", font=("Segoe UI", 9), bootstyle="info").pack(side=LEFT, padx=(4,2))

                # --- THEME CHOOSER (Combobox) ---
        # get the current theme name (fallback to Settings.THEME[0] if unavailable)
        try:
            current_theme = getattr(self, "style", None).theme_use() if getattr(self, "style", None) else Settings.THEME[0]
        except Exception:
            current_theme = Settings.THEME[0]

        self._theme_var = tk.StringVar(value=current_theme)
        # readonly combobox so user can't type arbitrary text
        self.theme_combobox = ttk.Combobox(
            right_wrap,
            values=Settings.THEME,
            textvariable=self._theme_var,
            state="readonly",
            width=12
        )
        self.theme_combobox.pack(side=LEFT, padx=(8,4))
        # handle selection
        self.theme_combobox.bind("<<ComboboxSelected>>", lambda e: self.change_theme(self._theme_var.get()))

        self.search_entry.pack(side=LEFT, padx=Settings.PAD_SMALL)
        self.search_button.pack(side=LEFT, padx=Settings.PAD_SMALL)

    # ---------------- LEFT MAIN ----------------
    def main_left_view_area(self):
        self.main_left_frame = ttk.Frame(self.container,)
        self.main_left_frame.grid(row=1, column=0, sticky=NSEW)
        self.main_left_frame.grid_rowconfigure(0, weight=1)
        self.main_left_frame.grid_columnconfigure(0, weight=1)
       
        # initial left frame
        try:
            self.left_frame = HomeLeftFrame(self.main_left_frame, self)
        except TypeError:
            self.left_frame = HomeLeftFrame(self.main_left_frame)

        self.left_frame.pack(fill="both", expand=True)

    # ---------------- RIGHT MAIN ----------------
    def main_right_btn_area(self):
        self.main_right_frame = ttk.Frame(self.container,)
        self.main_right_frame.grid(row=1, column=1, sticky=NSEW)
        self.main_right_frame.grid_rowconfigure(0, weight=1)
        self.main_right_frame.grid_columnconfigure(0, weight=1)
        
        # initial right frame
        self.right_frame = HomeRightFrame(self.main_right_frame, self)
        self.right_frame.pack(fill="both", expand=True)

    # ---------------- BOTTOM BARS ----------------
    def left_bottom_bar(self):
        self.left_bottom_bar_frame = ttk.Frame(self.container,)
        self.left_bottom_bar_frame.grid(row=2, column=0, sticky=NSEW)
        ttk.Label(self.left_bottom_bar_frame, text="Status: OK",
                  bootstyle="inverse-secondary").pack(pady=Settings.PAD_SMALL)


    def right_bottom_bar(self):
        self.right_bottom_bar_frame = ttk.Frame(self.container,)
        self.right_bottom_bar_frame.grid(row=2, column=1, sticky=NSEW)
        ttk.Label(self.right_bottom_bar_frame, text=Settings._VERSION,
                  bootstyle="inverse-secondary").pack(pady=Settings.PAD_SMALL)


    def _load_frame(self, left_class, right_class):
        """internal method to load frames without modifying history"""
        if self.left_frame:
            self.left_frame.destroy()
        if self.right_frame:
            self.right_frame.destroy()

        # ध्यान दो → कुछ frames को app चाहिए, कुछ को नहीं
        try:
            self.left_frame = left_class(self.main_left_frame, self)
        except TypeError:
            self.left_frame = left_class(self.main_left_frame)
        try:
            self.right_frame = right_class(self.main_right_frame, self)
        except TypeError:
            self.right_frame = right_class(self.main_right_frame)

        self.left_frame.pack(fill="both", expand=True)
        self.right_frame.pack(fill="both", expand=True)

        # --- connect right-panel quiz buttons to left-panel methods (if both quiz frames)
        try:
            from __main__ import QuizAttemptLeftFrame, QuizRightPanelFrame
        except Exception:
            pass

        if isinstance(self.left_frame, QuizAttemptLeftFrame) and isinstance(self.right_frame, QuizRightPanelFrame):
            
            # ⬇️ yeh line ADD karo
            self.left_frame.right_panel = self.right_frame

            # bind right panel buttons to left frame methods
            self.right_frame.quiz_load_btn.config(command=self.left_frame.load_quiz)
            self.right_frame.quiz_submit_button.config(command=self.left_frame.submit_quiz)

        self.current_frame = (left_class, right_class)
        try:
            self.set_frame_title_by_instances(self.left_frame, self.right_frame)
        except Exception:
            # fallback: a safe default
            self.frame_name_var.set("HOME")

    # -------- SWITCH METHOD --------
    def switch_frames(self, left_class, right_class):
        if self.left_frame:
            self.left_frame.destroy()
        if self.right_frame:
            self.right_frame.destroy()

        # left
        # self.left_frame = left_class(self.main_left_frame) if callable(left_class) else left_class(self.main_left_frame)
        # left_class may be a callable that expects (master, app) or only (master)
        try:
            # if left_class is a factory/callable that accepts (master, app)
            self.left_frame = left_class(self.main_left_frame, self)
        except TypeError:
            # fallback: try only master
            self.left_frame = left_class(self.main_left_frame)

        # right
        try:
            self.right_frame = right_class(self.main_right_frame, self)
        except TypeError:
            self.right_frame = right_class(self.main_right_frame)

        self.left_frame.pack(fill="both", expand=True)
        self.right_frame.pack(fill="both", expand=True)

        # --- connect right-panel quiz buttons to left-panel methods (if both quiz frames)
        if isinstance(self.left_frame, QuizAttemptLeftFrame) and isinstance(self.right_frame, QuizRightPanelFrame):
            self.left_frame.right_panel = self.right_frame
            self.right_frame.quiz_load_btn.config(command=self.left_frame.load_quiz)
            self.right_frame.quiz_submit_button.config(command=self.left_frame.submit_quiz)


        if self.current_frame:
            self.history.append(self.current_frame)
            self.future.clear()

        self.current_frame = (left_class, right_class)
        try:
            self.set_frame_title_by_instances(self.left_frame, self.right_frame)
        except Exception:
            self.frame_name_var.set("HOME")

    #---------------- ACTION METHODS ----------------
    def change_frame(self, action):
        if action == "Back" and self.history:
            left_class, right_class = self.history.pop()
            if self.current_frame:
                self.future.append(self.current_frame)   # save current for forward
            self._load_frame(left_class, right_class)

        elif action == "Forward" and self.future:
            left_class, right_class = self.future.pop()
            if self.current_frame:
                self.history.append(self.current_frame)  # save current for back
            self._load_frame(left_class, right_class)

        elif action == "Home":
            self.history.append(self.current_frame) if self.current_frame else None
            self.future.clear()
            self._load_frame(HomeLeftFrame, HomeRightFrame)


    def search_action(self):
        query = self.search_entry.get()
        print(f"Searching: {query}")


    def set_frame_title_by_instances(self, left_inst, right_inst):
        """
        Set top-bar title to one of: HOME, QUIZ, NOTES based on the *instances* currently shown.
        left_inst / right_inst are the actual frame instances (not classes).
        """
        # import class names if needed (they are in same module so available)
        try:
            is_quiz = (
                isinstance(left_inst, QuizAttemptLeftFrame) or isinstance(right_inst, QuizAttemptLeftFrame) or
                isinstance(left_inst, QuizRightPanelFrame) or isinstance(right_inst, QuizRightPanelFrame)
            )
        except Exception:
            is_quiz = False

        try:
            is_notes = (
                isinstance(left_inst, ReadNotesFrame) or isinstance(right_inst, ReadNotesFrame) or
                isinstance(left_inst, ReadingControllFrame) or isinstance(right_inst, ReadingControllFrame)
            )
        except Exception:
            is_notes = False

        if is_quiz:
            self.frame_name_var.set("QUIZ")
        elif is_notes:
            self.frame_name_var.set("NOTES")
        else:
            self.frame_name_var.set("HOME")


    def change_theme(self, theme_name: str):
        """
        Change ttkbootstrap theme at runtime.
        Uses the app's Style instance (self.style) when available.
        """
        try:
            # In ttkbootstrap Window, style object is available at self.style
            style_obj = getattr(self, "style", None)
            if style_obj is None:
                # fallback to creating a Style singleton
                style_obj = ttk.Style()

            style_obj.theme_use(theme_name)   # <- this changes the whole app theme
            # force update UI
            try:
                self.update_idletasks()
            except Exception:
                pass

            # If you re-configure fonts/styles in your app, reapply them here.
            # Example (uncomment/use if you have custom font config):
            # style_obj.configure('TLabel', font=Settings.FONT_NORMAL)
            # style_obj.configure('TButton', font=Settings.FONT_NORMAL)

        except Exception as e:
            messagebox.showerror("Theme Error", f"Could not apply theme '{theme_name}':\n{e}")   


if __name__ == "__main__":
    app = App()
    app.mainloop()
