
# # gui/home_left_frame.py

# import ttkbootstrap as ttk
# # from logic.switch_logic import FrameSwitcher as logic
# # from logic.reader_controller import ReaderController
# # from gui import subject_left_frame, reader_right_frame
# # from gui import quiz_left_frame, quiz_right_frame
# # from setting.settings import WIDTH


# SM_BTN_WIDTH = 25

# class ReadingControllFrame(ttk.Frame):
#     def __init__(self, master, app, path=None):
#         super().__init__(master, bootstyle="secondary")
#         self.app = app
#         self.reader_controller = None
#         # self.file_path = r"data/chapter_one_notes.txt"
#         self.file_path = path
        
#         # Create buttons
#         ttk.Button(self, text="Load File", 
#                    bootstyle="danger",
#                    width=SM_BTN_WIDTH,
#                    command=self.load_file
#                    ).pack(pady=10)

#         ttk.Button(self, text="View Text", 
#                    bootstyle="primary",
#                    width=SM_BTN_WIDTH,
#                    command=self.view_text_file
#                    ).pack(pady=10)


#         ttk.Button(self, text="Back", 
#                    bootstyle="warning",
#                    width=SM_BTN_WIDTH,
#                    command=self.go_back
#                    ).pack(pady=10)
        
#         ttk.Button(self, text="Quit", 
#                    bootstyle="danger",
#                    width=SM_BTN_WIDTH,
#                    command=app.destroy
#                    ).pack(pady=10)

#     def load_file(self):
#         """Load the text file and initialize the reader controller"""
#         # try:
#         #     # Get the text display frame from the app
#         #     text_frame = self.app.get_current_right_frame()
            
#         #     if hasattr(text_frame, 'enqueue_line'):
#         #         # Initialize reader controller
#         #         self.reader_controller = ReaderController(
#         #             file_path=self.file_path,
#         #             display_callback=text_frame.enqueue_line,
#         #             completion_callback=text_frame.file_done if hasattr(text_frame, 'file_done') else None
#         #         )
#         #         print("File loaded successfully")
#         #     else:
#         #         print("Error: Current frame doesn't support text display")
                
#         # except Exception as e:
#         #     print(f"Error loading file: {e}")

#         print("LOAD FILE")

#     def view_text_file(self):
#         """Start reading the file"""
#         # if self.reader_controller:
#         #     self.reader_controller.start_reading()
#         # else:
#         #     print("Please load a file first")
#         print("PALY")


#     def go_back(self):
#         """Go back to previous screen"""
#         # if self.reader_controller:
#         #     self.reader_controller.stop_reading()
#         # logic.switch_frame(self.app, subject_left_frame.ReaderLeftFrameS, reader_right_frame.ReaderRightFrame)
#         print("GO BACK")





# class QuizAttemptLeftFrame(ttk.Frame):
#     def __init__(self, master):
#         super().__init__(master)

#         # Grid Layout
#         self.grid_columnconfigure(0, weight=1, uniform="group1")
#         self.grid_rowconfigure(0, weight=3, uniform="group2")
#         self.grid_rowconfigure(1, weight=3, uniform="group2")
#         self.grid_rowconfigure(2, weight=26, uniform="group2")
#         self.grid_rowconfigure(3, weight=3, uniform="group2")
#         self.grid_propagate(False)

#         self.quiz_data = []          # List of dicts {question, option1-4, answer}
#         self.current_q_index = 0
#         self.selected_answers = {}   # {q_index: selected_option}

#         # <<< ADD THIS LINE >>>
#         self.answer_var = tk.StringVar()   # single variable used by Radiobuttons across questions

#         self.s = Settings()
#         self.tob_view_area()
#         self.second_tob_view_area()
#         self.question_options_view_area()
#         self.bottom_view_area()

#     def tob_view_area(self):
#         self.top_area_frame = ttk.Frame(self)
#         self.top_area_frame.grid(row=0, column=0, sticky=NSEW)

#         self.section_name_label = ttk.Label(self.top_area_frame, text="SECTIONS", anchor="w", bootstyle="secondary", font=("Helvetica", 11, "bold"))
#         self.section_name_label.pack(side=LEFT, padx=10, pady=5)

#         self.test_name_label = ttk.Label(self.top_area_frame, text="Test", anchor="e", 
#                              bootstyle="inverse-primary", font=("Helvetica", 11, "bold"))
#         self.test_name_label.pack(side=LEFT, padx=10, pady=5)

#         self.total_left_time_label = ttk.Label(self.top_area_frame, text="Time Left: 00:05:53", anchor="e", 
#                              bootstyle="danger", font=("Helvetica", 11, "bold"))
#         self.total_left_time_label.pack(side=RIGHT, padx=10, pady=5)

#     def second_tob_view_area(self):
#         self.top_second_area_frame = ttk.Frame(self, bootstyle="light")
#         self.top_second_area_frame.grid(row=1, column=0, sticky=NSEW)

#         q_lbl = ttk.Label(self.top_second_area_frame, text="Question No. 5", anchor="w", font=("Helvetica", 11, "bold"))
#         q_lbl.pack(side=LEFT, padx=10, pady=5)

#         time_lbl = ttk.Label(self.top_second_area_frame, text="Time: 00:53", anchor="e", 
#                              bootstyle="info", font=("Helvetica", 11, "bold"))
#         time_lbl.pack(side=LEFT, padx=40, pady=5)

#         self.btn_pause_quiz = ttk.Button(self.top_second_area_frame, text="Pause", bootstyle="danger-outline")
#         self.btn_pause_quiz.pack(side=RIGHT, padx=10, pady=5)

#     # ---------- Question + Options with Scrollbar ----------
#     def question_options_view_area(self):
#         frame = ttk.Frame(self, bootstyle="light")
#         frame.grid(row=2, column=0, sticky=NSEW)
#         frame.grid_rowconfigure(0, weight=1)
#         frame.grid_columnconfigure(0, weight=1)

#         # Create canvas + scrollbar
#         canvas = tk.Canvas(frame, highlightthickness=0)
#         scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
#         scroll_frame = ttk.Frame(canvas)
#         self.scroll_frame = scroll_frame


#         # Configure canvas window
#         canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
#         canvas.configure(yscrollcommand=scrollbar.set)

#         canvas.grid(row=0, column=0, sticky=NSEW)
#         scrollbar.grid(row=0, column=1, sticky=NS)

#         # Make scrollregion update
#         def on_configure(event):
#             canvas.configure(scrollregion=canvas.bbox("all"))

#         scroll_frame.bind("<Configure>", on_configure)

#         # -------- Add Options (demo static - uses instance answer_var so show_question can control it) --------
#         # ensure instance var is cleared for demo display
#         self.answer_var.set("")
#         options = [] #["51/40", "68/39", "59/40", "61/50"]

#         for opt in options:
#             r = ttk.Radiobutton(scroll_frame, text=opt, value=opt,
#                                 variable=self.answer_var)
#             r.pack(anchor="w", padx=30, pady=3)


#     # ---------- Bottom Bar (Buttons) ----------
#     def bottom_view_area(self):
#         frame = ttk.Frame(self)
#         frame.grid(row=3, column=0, sticky=NSEW)

#         self.mark_review = ttk.Button(frame, text="Mark for Review & Next", bootstyle="secondary-outline")
#         self.clear_response = ttk.Button(frame, text="Clear Response", bootstyle="danger-outline")
#         self.btn_save_next = ttk.Button(frame, text="Save & Next", bootstyle="success", width=self.s.SM_BTN_WIDTH)

#         # save reference so we can use it
#         # self.btn_save_next = self.btn_save_next

#         self.mark_review.pack(side=LEFT, padx=10, pady=5)
#         self.clear_response.pack(side=LEFT, padx=10, pady=5)
#         self.btn_save_next.pack(side=RIGHT, padx=30, pady=5)

#         # bind to next_question (function we'll add)
#         self.btn_save_next.config(command=self.next_question)

#     def load_quiz(self):
#         """Called when right-panel 'Load Quiz' button clicked.
#            Opens CSV, reads rows into self.quiz_data and shows first question."""
#         file_path = filedialog.askopenfilename(
#             title="Select Quiz CSV",
#             filetypes=[("CSV Files", "*.csv")]
#         )
#         if not file_path:
#             return

#         try:
#             with open(file_path, "r", encoding="utf-8") as f:
#                 reader = csv.DictReader(f)
#                 # expect headers: question,option1,option2,option3,option4,answer
#                 self.quiz_data = [row for row in reader if row.get("question")]
#         except Exception as e:
#             messagebox.showerror("Error", f"Could not load quiz:\n{e}")
#             return

#         if not self.quiz_data:
#             messagebox.showwarning("Empty", "CSV has no questions or wrong headers.")
#             return

#         # reset indexes / answers and show first
#         self.current_q_index = 0
#         self.selected_answers.clear()
#         self.show_question()

#     def show_question(self):
#         """Render current question into self.scroll_frame using self.answer_var."""
#         if not self.quiz_data:
#             return

#         # clear old widgets
#         for w in self.scroll_frame.winfo_children():
#             w.destroy()

#         qdata = self.quiz_data[self.current_q_index]
#         q_text = qdata.get("question", "").strip()

#         ttk.Label(self.scroll_frame, text=f"Q{self.current_q_index+1}: {q_text}",
#                   wraplength=700, font=("Helvetica", 12)).pack(anchor="w", padx=15, pady=10)

#         # prepare variable and previous selection if any
#         prev = self.selected_answers.get(self.current_q_index, "")
#         self.answer_var.set(prev)

#         # show options (option1..option4)
#         for opt_key in ("option1", "option2", "option3", "option4"):
#             opt = qdata.get(opt_key, "").strip()
#             if not opt:
#                 continue
#             r = ttk.Radiobutton(self.scroll_frame, text=opt, value=opt, variable=self.answer_var)
#             r.pack(anchor="w", padx=30, pady=3)

#         # update any UI labels (like Question No.) if you want:
#         # try to update the small label in second_tob_view_area if present
#         try:
#             # if there's a label showing question number, update it
#             for child in getattr(self, "top_second_area_frame").winfo_children():
#                 # naive: update first label text if it's the question no label
#                 pass
#         except Exception:
#             pass

#     def next_question(self):
#         """Save current selection and go to next question (if any)."""
#         if not self.quiz_data:
#             return
#         # save current answer
#         self.selected_answers[self.current_q_index] = self.answer_var.get()

#         if self.current_q_index < len(self.quiz_data) - 1:
#             self.current_q_index += 1
#             self.show_question()
#         else:
#             messagebox.showinfo("End", "This is the last question.")

#     def submit_quiz(self):
#         """Calculate score and show result."""
#         if not self.quiz_data:
#             messagebox.showwarning("No Quiz", "Load a quiz first.")
#             return

#         # save current selection
#         self.selected_answers[self.current_q_index] = self.answer_var.get()

#         total = len(self.quiz_data)
#         correct = 0
#         wrong_details = []
#         for i, q in enumerate(self.quiz_data):
#             given = self.selected_answers.get(i, "").strip()
#             ans = q.get("answer", "").strip()
#             if given and given == ans:
#                 correct += 1
#             else:
#                 # collect wrong details optionally
#                 wrong_details.append((i+1, q.get("question", ""), given, ans))

#         messagebox.showinfo("Result", f"Score: {correct}/{total}\nCorrect: {correct}\nWrong: {total-correct}")




# main.py
import tkinter as tk
from tkinter import StringVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *   # NSEW, LEFT, RIGHT, EW etc used throughout
from tkinter import messagebox
from tkinter import filedialog
import csv


class Settings:
    """
    Global UI Settings for the app.
    Keep this as a static container of constants.
    """
    THEME = ("pulse", "minty", "simplex", "flatly", "darkly", "solar", "cyborg", "vapor")
    TITLE = "ReadAndTest"
    WSIZE = (950, 600)
    POS = (100, 50)
    ICON = "icon.ico"

    PAD_SMALL = 4
    PAD_MEDIUM = 8
    PAD_LARGE = 12

    SM_BTN_WIDTH = 25
    MD_BTN_WIDTH = 35
    LG_BTN_WIDTH = 45

    FONT_TITLE = ("Arial", 16, "bold")
    FONT_SUBTITLE = ("Arial", 12, "bold")
    FONT_NORMAL = ("Arial", 11)

    SAMPLE_NOTES = """पत्थर और पौधा
    ... (omitted here for brevity; same content as your original SAMPLE_NOTES) ...
    """


class BaseFrame(ttk.Frame):
    """Base frame: standardize constructor to accept (master, app=None)."""
    def __init__(self, master, app=None):
        super().__init__(master)
        self.app = app


class HomeRightFrame(BaseFrame):
    def __init__(self, master, app=None):
        super().__init__(master, app)

        self.btn_read_notes = ttk.Button(
            self, text="Read Notes",
            bootstyle="primary-outline", width=Settings.SM_BTN_WIDTH,
            command=lambda: app.switch_frames(ReadNotesFrame, ReadingControlFrame)
        )
        self.btn_read_notes.pack(pady=Settings.PAD_LARGE)

        self.btn_quiz_time = ttk.Button(
            self, text="Quiz Time",
            bootstyle="success-outline", width=Settings.SM_BTN_WIDTH,
            command=lambda: app.switch_frames(QuizAttemptLeftFrame, QuizRightPanelFrame)
        )
        self.btn_quiz_time.pack(pady=Settings.PAD_LARGE)

        ttk.Button(
            self, text="Quit",
            bootstyle="danger-outline", width=Settings.SM_BTN_WIDTH,
            command=app.destroy
        ).pack(pady=Settings.PAD_LARGE)


class HomeLeftFrame(BaseFrame):
    def __init__(self, master, app=None):
        super().__init__(master, app)
        ttk.Label(self, text="🏠 Home Left Frame", font=Settings.FONT_TITLE).pack(pady=Settings.PAD_MEDIUM)
        ttk.Button(self, text="Dummy Action", bootstyle="secondary-outline",
                   command=lambda: print("Dummy")).pack(pady=Settings.PAD_SMALL)


class ReadNotesFrame(BaseFrame):
    def __init__(self, master, app=None, text=None):
        super().__init__(master, app)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.notes_text = text if text else Settings.SAMPLE_NOTES
        self.read_notes_area()

    def read_notes_area(self):
        frame = ttk.Frame(self, bootstyle="light")
        frame.grid(row=0, column=0, sticky=NSEW)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scroll_frame.bind("<Configure>", on_configure)

        # Scoped mouse-wheel: bind when mouse enters canvas, unbind when leaves.
        def _on_mouse_wheel(event):
            # cross-platform handling
            num = getattr(event, "num", None)
            if num == 4:
                canvas.yview_scroll(-1, "units")
            elif num == 5:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(int(-1 * (getattr(event, "delta", 0) / 120)), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mouse_wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        # also handle Linux wheel events
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<Button-4>", _on_mouse_wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<Button-4>"))
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<Button-5>", _on_mouse_wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<Button-5>"))

        q_lbl = ttk.Label(scroll_frame, text=self.notes_text, wraplength=700, font=("Helvetica", 12))
        q_lbl.pack(anchor="w", padx=15, pady=10)


class ReadingControlFrame(BaseFrame):
    """
    Controls for reading area (load .txt, view text, navigation).
    NOTE: renamed from ReadingControllFrame -> ReadingControlFrame (single 'l').
    """
    def __init__(self, master, app=None, path=None):
        super().__init__(master, app)
        self.reader_controller = None
        self.file_path = path
        self.file_content = None

        # Create buttons (use Settings class attributes)
        ttk.Button(self, text="Load File",
                   bootstyle="danger",
                   width=Settings.SM_BTN_WIDTH,
                   command=self.load_file).pack(pady=10)

        ttk.Button(self, text="View Text",
                   bootstyle="primary",
                   width=Settings.SM_BTN_WIDTH,
                   command=self.view_text_file).pack(pady=10)

        ttk.Button(self, text="Back",
                   bootstyle="warning",
                   width=Settings.SM_BTN_WIDTH,
                   command=self.go_back).pack(pady=10)

        ttk.Button(self, text="Quit",
                   bootstyle="danger",
                   width=Settings.SM_BTN_WIDTH,
                   command=app.destroy).pack(pady=10)

    def load_file(self):
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
        if not self.file_content:
            messagebox.showwarning("No File", "Please load a .txt file first")
            return

        # Use factory lambda that accepts master (we keep it simple)
        # Better: supply a two-arg factory to be fully consistent with _instantiate_frame
        factory = lambda master, app=None: ReadNotesFrame(master, app, text=self.file_content)
        self.app.switch_frames(factory, ReadingControlFrame)

    def go_back(self):
        self.app.change_frame("Back")


class QuizRightPanelFrame(BaseFrame):
    def __init__(self, master, app=None):
        super().__init__(master, app)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.status_area()
        self.section_area()
        self.bottom_buttons_area()

    def status_area(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, sticky=EW, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(6, weight=1)

        self.status_labels = {}
        self.status_data_result = [
            ("Answered", "success", 0),
            ("Marked", "secondary", 0),
            ("Not Visited", "info", 0),
            ("Marked and answered", "primary", 0),  # use primary instead of unsupported 'purple'
            ("Not Answered", "danger", 0)
        ]

        for i, (text, style, count) in enumerate(self.status_data_result):
            row = ttk.Frame(frame)
            row.grid(row=i, column=1, sticky=W, pady=2)

            lbl_count = ttk.Label(row, text=str(count), bootstyle=f"{style}-inverse")
            lbl_count.pack(side=LEFT, padx=5)

            lbl_text = ttk.Label(row, text=text, font=("Helvetica", 10))
            lbl_text.pack(side=LEFT, padx=5)

            self.status_labels[text] = lbl_count

    def section_area(self):
        outer_frame = ttk.Frame(self)
        outer_frame.grid(row=1, column=0, sticky=NSEW, pady=5, padx=2)
        outer_frame.grid_columnconfigure(0, weight=1)

        section_lbl = ttk.Label(outer_frame, text="SECTION : टेस्ट",
                                font=("Helvetica", 10, "bold"), bootstyle="inverse-info")
        section_lbl.grid(row=0, column=0, sticky=EW, pady=2)

        canvas_frame = ttk.Frame(outer_frame)
        canvas_frame.grid(row=1, column=0, sticky=NSEW)
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)

        # Mouse wheel bound to the canvas only (calls the same helper as ReadNotesFrame)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)

    def create_question_buttons(self, total_questions):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        self.q_buttons = []
        for i in range(total_questions):
            btn = ttk.Button(self.scroll_frame, text=str(i + 1), width=3, bootstyle="secondary-outline",
                             command=lambda idx=i: self.jump_to_question(idx))
            btn.grid(row=i // 5, column=i % 5, padx=5, pady=5)
            self.q_buttons.append(btn)

    def jump_to_question(self, index):
        if hasattr(self.app, "left_frame") and self.app.left_frame:
            self.app.left_frame.show_question(index)

    def _on_mousewheel(self, event):
        num = getattr(event, "num", None)
        if num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (getattr(event, "delta", 0) / 120)), "units")

    def bottom_buttons_area(self):
        frame = ttk.Frame(self)
        frame.grid(row=2, column=0, sticky=EW, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(4, weight=1)

        btn_container = ttk.Frame(frame)
        btn_container.grid(row=0, column=1, columnspan=3, sticky=NSEW)

        self.quiz_load_btn = ttk.Button(btn_container, text="Load Quiz", bootstyle="info-outline")
        self.quiz_submit_button = ttk.Button(btn_container, text="Submit Test", bootstyle="success")

        self.quiz_load_btn.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.quiz_submit_button.pack(side=LEFT, expand=True, padx=5, pady=5)

    def update_status_counts(self, counts: dict):
        for key, value in counts.items():
            if key in self.status_labels:
                self.status_labels[key].config(text=str(value))


class QuizAttemptLeftFrame(BaseFrame):
    def __init__(self, master, app=None):
        super().__init__(master, app)

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=3, uniform="group2")
        self.grid_rowconfigure(1, weight=3, uniform="group2")
        self.grid_rowconfigure(2, weight=26, uniform="group2")
        self.grid_rowconfigure(3, weight=3, uniform="group2")
        self.grid_propagate(False)

        self.right_panel = None

        self.quiz_data = []
        self.current_q_index = 0
        self.selected_answers = {}
        self.marked_for_review = set()
        self.visited_questions = set()

        self.answer_var = tk.StringVar()

        # method name fixes
        self.top_view_area()
        self.top_second_view_area()
        self.question_options_view_area()
        self.bottom_view_area()

    def top_view_area(self):
        self.top_area_frame = ttk.Frame(self)
        self.top_area_frame.grid(row=0, column=0, sticky=NSEW)

        self.section_name_label = ttk.Label(self.top_area_frame, text="SECTIONS", anchor="w",
                                            bootstyle="secondary", font=("Helvetica", 11, "bold"))
        self.section_name_label.pack(side=LEFT, padx=10, pady=5)

        self.test_name_label = ttk.Label(self.top_area_frame, text="Test", anchor="e",
                                         bootstyle="inverse-primary", font=("Helvetica", 11, "bold"))
        self.test_name_label.pack(side=LEFT, padx=10, pady=5)

        self.total_left_time_label = ttk.Label(self.top_area_frame, text="Time Left: 00:05:53", anchor="e",
                                               bootstyle="danger", font=("Helvetica", 11, "bold"))
        self.total_left_time_label.pack(side=RIGHT, padx=10, pady=5)

    def top_second_view_area(self):
        self.top_second_area_frame = ttk.Frame(self, bootstyle="light")
        self.top_second_area_frame.grid(row=1, column=0, sticky=NSEW)

        self.question_number_label = ttk.Label(self.top_second_area_frame, text="Please Load Quiz File",
                                               anchor="w", font=("Helvetica", 11, "bold"))
        self.question_number_label.pack(side=LEFT, padx=10, pady=5)

        self.question_take_time_lbl = ttk.Label(self.top_second_area_frame, text="Time: 00:53", anchor="e",
                                                bootstyle="info", font=("Helvetica", 11, "bold"))
        self.question_take_time_lbl.pack(side=LEFT, padx=40, pady=5)

        self.btn_pause_quiz = ttk.Button(self.top_second_area_frame, text="Pause", bootstyle="danger-outline")
        self.btn_pause_quiz.pack(side=RIGHT, padx=10, pady=5)

    def question_options_view_area(self):
        frame = ttk.Frame(self, bootstyle="light")
        frame.grid(row=2, column=0, sticky=NSEW)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        self.scroll_frame = scroll_frame

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scroll_frame.bind("<Configure>", on_configure)

        self.answer_var.set("")

    def bottom_view_area(self):
        frame = ttk.Frame(self)
        frame.grid(row=3, column=0, sticky=NSEW)

        self.mark_review = ttk.Button(frame, text="Mark for Review & Next", bootstyle="secondary-outline")
        self.clear_response = ttk.Button(frame, text="Clear Response", bootstyle="danger-outline")
        self.btn_save_next = ttk.Button(frame, text="Save & Next", bootstyle="success", width=Settings.SM_BTN_WIDTH)

        self.mark_review.pack(side=LEFT, padx=10, pady=5)
        self.clear_response.pack(side=LEFT, padx=10, pady=5)
        self.btn_save_next.pack(side=RIGHT, padx=30, pady=5)

        self.mark_review.config(command=self.mark_for_review)
        self.clear_response.config(command=self.clear_current_response)
        self.btn_save_next.config(command=self.next_question)

    def _get_app(self):
        return self.winfo_toplevel()

    def update_right_button(self, index):
        app = self._get_app()
        if not app:
            return
        right = getattr(app, "right_frame", None)
        if not right or not hasattr(right, "q_buttons"):
            return
        if index < 0 or index >= len(right.q_buttons):
            return

        btn = right.q_buttons[index]
        answered = bool(self.selected_answers.get(index))
        marked = (index in self.marked_for_review)

        # normalize styles -> map any custom to supported bootstrap styles
        if marked and answered:
            style = "primary"       # marked + answered (use primary)
        elif marked:
            style = "warning"
        elif answered:
            style = "success"
        else:
            style = "secondary-outline"

        try:
            btn.config(bootstyle=style)
        except Exception:
            btn.configure(bootstyle=style)

    def update_all_buttons(self):
        for i in range(len(self.quiz_data)):
            self.update_right_button(i)

    def load_quiz(self):
        file_path = filedialog.askopenfilename(title="Select Quiz CSV", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.quiz_data = [row for row in reader if row.get("question")]
        except Exception as e:
            messagebox.showerror("Error", f"Could not load quiz:\n{e}")
            return

        if not self.quiz_data:
            messagebox.showwarning("Empty", "CSV has no questions or wrong headers.")
            return

        self.current_q_index = 0
        self.selected_answers.clear()
        self.marked_for_review.clear()
        self.answer_var.set("")
        self.visited_questions.clear()
        self.show_question()

        if self.right_panel:
            self.right_panel.create_question_buttons(len(self.quiz_data))
        self.update_status_area()

    def show_question(self, index=None):
        if not self.quiz_data:
            return
        if index is not None:
            self.current_q_index = index

        self.visited_questions.add(self.current_q_index)

        for w in self.scroll_frame.winfo_children():
            w.destroy()

        qdata = self.quiz_data[self.current_q_index]
        q_text = qdata.get("question", "").strip()

        self.question_number_label.config(text=f"Question No. {self.current_q_index+1} / {len(self.quiz_data)}")

        ttk.Label(self.scroll_frame, text=f"Q{self.current_q_index+1}: {q_text}", wraplength=700,
                  font=("Helvetica", 12)).pack(anchor="w", padx=15, pady=10)

        prev = self.selected_answers.get(self.current_q_index, "")
        self.answer_var.set(prev)

        options_show = ("option1", "option2", "option3", "option4")
        for opt_key in options_show:
            opt = qdata.get(opt_key, "").strip()
            if not opt:
                continue
            r = ttk.Radiobutton(self.scroll_frame, text=opt, value=opt, variable=self.answer_var)
            r.pack(anchor="w", padx=30, pady=3)

        self.update_right_button(self.current_q_index)
        self.update_status_area()

    def next_question(self):
        if not self.quiz_data:
            return
        self.selected_answers[self.current_q_index] = self.answer_var.get()
        self.update_right_button(self.current_q_index)
        if self.current_q_index < len(self.quiz_data) - 1:
            self.current_q_index += 1
            self.show_question()
        else:
            messagebox.showinfo("End", "This is the last question.")
        self.update_status_area()

    def mark_for_review(self):
        if not self.quiz_data:
            return
        idx = self.current_q_index
        self.marked_for_review.add(idx)
        self.update_right_button(idx)
        messagebox.showinfo("Marked", f"Question {idx+1} marked for review.")
        self.update_status_area()

    def clear_current_response(self):
        if not self.quiz_data:
            return
        idx = self.current_q_index
        self.selected_answers.pop(idx, None)
        self.answer_var.set("")
        self.marked_for_review.discard(idx)
        self.update_right_button(idx)
        messagebox.showinfo("Cleared", f"Response (and mark) cleared for Question {idx+1}.")
        self.update_status_area()

    def submit_quiz(self):
        if not self.quiz_data:
            messagebox.showwarning("No Quiz", "Load a quiz first.")
            return
        self.selected_answers[self.current_q_index] = self.answer_var.get()

        total = len(self.quiz_data)
        correct = 0
        wrong_details = []
        for i, q in enumerate(self.quiz_data):
            given = self.selected_answers.get(i, "").strip()
            ans = q.get("answer", "").strip()
            if given and given == ans:
                correct += 1
            else:
                wrong_details.append((i + 1, q.get("question", ""), given, ans))

        marked_count = len(self.marked_for_review)
        marked_list = ", ".join(str(i + 1) for i in sorted(self.marked_for_review)) if marked_count else "None"

        messagebox.showinfo(
            "Result",
            f"Score: {correct}/{total}\nCorrect: {correct}\nWrong: {total - correct}\n\n"
            f"Marked for review: {marked_count}\nQuestions: {marked_list}"
        )

    def update_status_area(self):
        total = len(self.quiz_data)
        answered_set = {i for i in range(total) if str(self.selected_answers.get(i, "")).strip()}
        marked_set = {i for i in range(total) if i in self.marked_for_review}
        marked_and_answered = answered_set & marked_set
        not_answered_count = max(total - len(answered_set), 0)
        not_visited_count = max(total - len(self.visited_questions), 0)

        counts = {
            "Answered": len(answered_set),
            "Marked": len(marked_set),
            "Marked and answered": len(marked_and_answered),
            "Not Answered": not_answered_count,
            "Not Visited": not_visited_count
        }

        if self.right_panel:
            self.right_panel.update_status_counts(counts)


class App(ttk.Window, Settings):
    def __init__(self):
        super().__init__(themename=Settings.THEME[4])
        self.title(Settings.TITLE)
        self.geometry(f"{Settings.WSIZE[0]}x{Settings.WSIZE[1]}+{Settings.POS[0]}+{Settings.POS[1]}")
        self.minsize(*Settings.WSIZE)
        try:
            self.iconbitmap(Settings.ICON)
        except Exception as e:
            print(f"Icon file not found Exception: {e}")

        self.history = []
        self.future = []
        self.current_frame = None

        self.left_frame = None
        self.right_frame = None

        self.container = ttk.Frame(self)
        self.container.pack(fill=BOTH, expand=YES)

        self.container.grid_columnconfigure(0, weight=4, uniform="group1")
        self.container.grid_columnconfigure(1, weight=1, uniform="group1")
        self.container.grid_rowconfigure(0, weight=3, uniform="group2")
        self.container.grid_rowconfigure(1, weight=20, uniform="group2")
        self.container.grid_rowconfigure(2, weight=2, uniform="group2")
        self.container.grid_propagate(False)

        self.top_bar()
        self.main_left_view_area()
        self.main_right_btn_area()
        self.left_bottom_bar()
        self.right_bottom_bar()

    def top_bar(self):
        self.top_bar_frame = ttk.Frame(self.container, padding=Settings.PAD_SMALL)
        self.top_bar_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        left_wrap = ttk.Frame(self.top_bar_frame)
        left_wrap.pack(side=LEFT)

        ttk.Button(left_wrap, text="⬅ Back", bootstyle="info-outline",
                   command=lambda: self.change_frame("Back")).pack(side=LEFT, padx=Settings.PAD_SMALL)
        ttk.Button(left_wrap, text="➡ Forward", bootstyle="info-outline",
                   command=lambda: self.change_frame("Forward")).pack(side=LEFT, padx=Settings.PAD_SMALL)
        ttk.Button(left_wrap, text="🏠 Home", bootstyle="info-outline",
                   command=lambda: self.change_frame("Home")).pack(side=LEFT, padx=Settings.PAD_SMALL)

        self.frame_name_var = StringVar(value="Home")
        ttk.Label(left_wrap, textvariable=self.frame_name_var, bootstyle="success",
                  font=Settings.FONT_SUBTITLE).pack(side=LEFT, padx=Settings.PAD_MEDIUM)

        right_wrap = ttk.Frame(self.top_bar_frame)
        right_wrap.pack(side=RIGHT)

        self.search_entry = ttk.Entry(right_wrap, width=26)
        self.search_entry.pack(side=LEFT, padx=Settings.PAD_SMALL)
        ttk.Button(right_wrap, text="🔍 Search", bootstyle="info-outline",
                   command=self.search_action).pack(side=LEFT, padx=Settings.PAD_SMALL)

    def main_left_view_area(self):
        self.main_left_frame = ttk.Frame(self.container)
        self.main_left_frame.grid(row=1, column=0, sticky=NSEW)
        self.main_left_frame.grid_rowconfigure(0, weight=1)
        self.main_left_frame.grid_columnconfigure(0, weight=1)

        # pass app reference for consistency
        self.left_frame = HomeLeftFrame(self.main_left_frame, self)
        self.left_frame.pack(fill="both", expand=True)

    def main_right_btn_area(self):
        self.main_right_frame = ttk.Frame(self.container)
        self.main_right_frame.grid(row=1, column=1, sticky=NSEW)
        self.main_right_frame.grid_rowconfigure(0, weight=1)
        self.main_right_frame.grid_columnconfigure(0, weight=1)

        self.right_frame = HomeRightFrame(self.main_right_frame, self)
        self.right_frame.pack(fill="both", expand=True)

    def left_bottom_bar(self):
        self.left_bottom_bar_frame = ttk.Frame(self.container)
        self.left_bottom_bar_frame.grid(row=2, column=0, sticky=NSEW)
        ttk.Label(self.left_bottom_bar_frame, text="Status: OK", bootstyle="inverse-secondary").pack(pady=Settings.PAD_SMALL)

    def right_bottom_bar(self):
        self.right_bottom_bar_frame = ttk.Frame(self.container)
        self.right_bottom_bar_frame.grid(row=2, column=1, sticky=NSEW)
        ttk.Label(self.right_bottom_bar_frame, text="v1.0.0", bootstyle="inverse-secondary").pack(pady=Settings.PAD_SMALL)

    # ---------- factory + frame switching ----------
    def _instantiate_frame(self, factory, master):
        """
        Accept a class or a callable factory.
        Prefer calling with (master, self); fall back to (master,) then ().
        """
        if callable(factory):
            try:
                return factory(master, self)
            except TypeError:
                try:
                    return factory(master)
                except TypeError:
                    return factory()
        raise TypeError("Provided factory is not callable to produce a Frame")

    def _load_frame(self, left_factory, right_factory):
        if self.left_frame:
            self.left_frame.destroy()
        if self.right_frame:
            self.right_frame.destroy()

        self.left_frame = self._instantiate_frame(left_factory, self.main_left_frame)
        self.right_frame = self._instantiate_frame(right_factory, self.main_right_frame)

        self.left_frame.pack(fill="both", expand=True)
        self.right_frame.pack(fill="both", expand=True)

        # connect quiz controls if both are quiz frames
        if isinstance(self.left_frame, QuizAttemptLeftFrame) and isinstance(self.right_frame, QuizRightPanelFrame):
            self.left_frame.right_panel = self.right_frame
            self.right_frame.quiz_load_btn.config(command=self.left_frame.load_quiz)
            self.right_frame.quiz_submit_button.config(command=self.left_frame.submit_quiz)

        self.current_frame = (left_factory, right_factory)
        self.frame_name_var.set(
            (getattr(left_factory, "__name__", "CustomFrame")) + " + " + (getattr(right_factory, "__name__", "CustomFrame"))
        )

    def switch_frames(self, left_factory, right_factory):
        if self.left_frame:
            self.left_frame.destroy()
        if self.right_frame:
            self.right_frame.destroy()

        left = self._instantiate_frame(left_factory, self.main_left_frame)
        right = self._instantiate_frame(right_factory, self.main_right_frame)

        left.pack(fill="both", expand=True)
        right.pack(fill="both", expand=True)

        if isinstance(left, QuizAttemptLeftFrame) and isinstance(right, QuizRightPanelFrame):
            left.right_panel = right
            right.quiz_load_btn.config(command=left.load_quiz)
            right.quiz_submit_button.config(command=left.submit_quiz)

        if self.current_frame:
            self.history.append(self.current_frame)
            self.future.clear()

        self.current_frame = (left_factory, right_factory)
        self.frame_name_var.set((getattr(left_factory, "__name__", "CustomFrame")) + " + " + (getattr(right_factory, "__name__", "CustomFrame")))

    def change_frame(self, action):
        if action == "Back" and self.history:
            left_factory, right_factory = self.history.pop()
            if self.current_frame:
                self.future.append(self.current_frame)
            self._load_frame(left_factory, right_factory)
        elif action == "Forward" and self.future:
            left_factory, right_factory = self.future.pop()
            if self.current_frame:
                self.history.append(self.current_frame)
            self._load_frame(left_factory, right_factory)
        elif action == "Home":
            self.history.append(self.current_frame) if self.current_frame else None
            self.future.clear()
            self._load_frame(HomeLeftFrame, HomeRightFrame)

    def search_action(self):
        query = self.search_entry.get()
        print(f"Searching: {query}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
