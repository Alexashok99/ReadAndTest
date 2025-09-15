# test.py
import os
import csv
import random
import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
from typing import Optional, Dict, List, Any
import time # <-- नया इम्पोर्ट

# --- Settings Class ---
class Settings:
    """अनुप्रयोग के लिए सभी सेटिंग्स और स्थिरांकों को संग्रहीत करता है"""
    INFO_OUT: str = "info-outline"
    SUCCESS_COLOR: str = "success"
    MM_BTN_WIDTH: int = 15

    FONT_HELVETICA_NORMAL: tuple = ("Helvetica", 10)
    FONT_HELVETICA_BOLD: tuple = ("Helvetica", 11, "bold")
    BUTTONS_PER_ROW: int = 5

# --- Base and Right Panel Classes ---
class BaseFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, app: Optional[tk.Toplevel] = None) -> None:
        super().__init__(master)
        self.app = app if app else self.winfo_toplevel()

class QuizRightPanelFrame(BaseFrame):
    # ... (यह क्लास अपरिवर्तित है) ...
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
        self.question_start_time: float = 0.0 # <-- नया वेरिएबल
        
        self.answer_var = tk.StringVar()

        # --- Quiz State ---
        # ... (अन्य वेरिएबल्स) ...
        # self.shuffle_questions: bool = False
        
        # नया स्टेट वेरिएबल
        self.in_review_mode: bool = False
        
        self._create_widgets()
        self._start_periodic_date_update()

    def _reset_quiz(self) -> None:
        # ... (यह मेथड अपरिवर्तित है)
        self.stop_question_timer()
        self.in_review_mode = False # <-- यह लाइन जोड़ें
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
            for btn in self.right_panel.scroll_frame.winfo_children():
                btn.destroy()
            self.right_panel.q_buttons.clear()
            self.right_panel.update_status_counts({k: 0 for k in self.right_panel.status_labels})
            self.right_panel.quiz_load_btn.config(state="normal")
        
        self.toggle_btn.config(state="normal")


    def _create_widgets(self) -> None:
        self._tob_view_area()
        self._second_tob_view_area()
        self._question_options_view_area()
        self._bottom_view_area()

    def _tob_view_area(self) -> None:
        # ... (यह मेथड अपरिवर्तित है)
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
        # ... (यह मेथड अपरिवर्तित है)
        self.top_second_area_frame = ttk.Frame(self)
        self.top_second_area_frame.grid(row=1, column=0, sticky="ew")
        self.question_number_label = ttk.Label(self.top_second_area_frame, text="Please Load Quiz File", anchor="w", font=Settings.FONT_HELVETICA_BOLD)
        self.question_number_label.pack(side="left", padx=10, pady=5)
        self.question_take_time_lbl = ttk.Label(self.top_second_area_frame, text="Time: 00:00:00", anchor="e", bootstyle="info", font=Settings.FONT_HELVETICA_BOLD)
        self.question_take_time_lbl.pack(side="left", padx=40, pady=5)
        self.btn_quit_quiz = ttk.Button(self.top_second_area_frame, text="Quit", bootstyle="danger-outline", command=self.quit_quiz)
        self.btn_quit_quiz.pack(side="right", padx=10, pady=5)

    def _question_options_view_area(self) -> None:
        # ... (यह मेथड अपरिवर्तित है)
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
        # ... (यह मेथड अपरिवर्तित है)
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
            self.quiz_data[self.current_q_index]['_time_taken'] = elapsed_time
    
    def load_quiz(self) -> None:
        # ... (यह मेथड अपरिवर्तित है)
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
    
    # def submit_quiz(self) -> None:
    #     """वर्तमान क्विज़ सत्र को समाप्त करता है और विस्तृत परिणाम प्रदर्शित करता है।"""
    #     if not self.quiz_data:
    #         messagebox.showwarning("No Quiz", "Load a quiz first.")
    #         return
    #     if not messagebox.askyesno("Submit Test", "Do you want to submit the test?"):
    #         return

    #     # अंतिम प्रश्न का समय और उत्तर रिकॉर्ड करें
    #     self._record_time_spent()
    #     self.stop_question_timer()
    #     if self.answer_var.get():
    #         self.selected_answers[self.current_q_index] = self.answer_var.get().strip()
        
    #     # --- 1. परिणाम की गणना ---
    #     total = len(self.quiz_data)
    #     correct = 0
    #     answered_questions_count = 0
    #     total_time_on_answered = 0
        
    #     fastest_q = {"num": "-", "time": float('inf')}
    #     slowest_q = {"num": "-", "time": 0.0}

    #     for i, q in enumerate(self.quiz_data):
    #         given = str(self.selected_answers.get(i, "")).strip()
    #         ans = str(q.get("answer", "")).strip()
    #         time_taken = q.get('_time_taken', 0.0)

    #         if given:
    #             answered_questions_count += 1
    #             total_time_on_answered += time_taken
    #             if time_taken < fastest_q["time"]:
    #                 fastest_q = {"num": i + 1, "time": time_taken}
    #             if time_taken > slowest_q["time"]:
    #                 slowest_q = {"num": i + 1, "time": time_taken}

    #         if given and given == ans:
    #             correct += 1
        
    #     for w in self.scroll_frame.winfo_children():
    #         w.destroy()

    #     # --- 3. नए विश्लेषण की गणना ---
    #     wrong = answered_questions_count - correct
    #     unattempted = total - answered_questions_count
    #     accuracy = (correct / answered_questions_count * 100) if answered_questions_count > 0 else 0
    #     avg_time = (total_time_on_answered / answered_questions_count) if answered_questions_count > 0 else 0
    #     total_time_str = time.strftime("%H:%M:%S", time.gmtime(self.q_seconds))

    #     # --- 4. सारांश (Summary) प्रदर्शित करें ---
    #     test_name = self.test_name_label.cget("text")
    #     ttk.Label(self.scroll_frame, text=f"--- Test Summary: {test_name} ---", font=("Helvetica", 16, "bold"), bootstyle="success").pack(anchor="w", padx=15, pady=(10, 10))
        
    #     stats_frame = ttk.Frame(self.scroll_frame)
    #     stats_frame.pack(fill='x', padx=15, pady=5)
        
    #     stats1 = [
    #         ("🏆 Score", f"{correct}/{total}"), ("✅ Correct", str(correct)),
    #         ("❌ Wrong", str(wrong)), ("⚪ Unattempted", str(unattempted)),
    #         ("🎯 Accuracy", f"{accuracy:.2f}%"),
    #     ]
    #     stats2 = [
    #         ("⏱ Total Time", total_time_str), (" Avg. Time / Ques", f"{avg_time:.2f} sec"),
    #         (" Fastest Ques", f"Q{fastest_q['num']} ({fastest_q['time']:.2f}s)"),
    #         (" Slowest Ques", f"Q{slowest_q['num']} ({slowest_q['time']:.2f}s)"),
    #     ]

    #     for i, (label, value) in enumerate(stats1):
    #         ttk.Label(stats_frame, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=0, sticky='w', padx=5, pady=2)
    #         ttk.Label(stats_frame, text=value, bootstyle="primary").grid(row=i, column=1, sticky='w', padx=5, pady=2)
        
    #     for i, (label, value) in enumerate(stats2):
    #         ttk.Label(stats_frame, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=2, sticky='w', padx=20, pady=2)
    #         ttk.Label(stats_frame, text=value, bootstyle="info").grid(row=i, column=3, sticky='w', padx=5, pady=2)

    #     ttk.Separator(self.scroll_frame, orient="horizontal").pack(fill="x", pady=15, padx=10)
        
    #     ttk.Label(self.scroll_frame, text="📌 Question-wise Analysis:", font=("Helvetica", 14, "underline"), bootstyle="danger").pack(anchor="w", padx=15, pady=(10, 5))
        
    #     for i, q in enumerate(self.quiz_data):
    #         given = str(self.selected_answers.get(i, "")).strip()
    #         ans = str(q.get("answer", "")).strip()
    #         time_taken = q.get('_time_taken', 0.0)

    #         q_frame = ttk.Frame(self.scroll_frame, padding=10, borderwidth=1, relief="solid")
    #         q_frame.pack(fill='x', padx=15, pady=5)
            
    #         header_frame = ttk.Frame(q_frame)
    #         header_frame.pack(fill='x')
    #         ttk.Label(header_frame, text=f"Q{i+1}: {q['question']}", wraplength=700).pack(side='left', anchor='w')
    #         ttk.Label(header_frame, text=f"({time_taken:.1f}s)", bootstyle="secondary").pack(side='right', anchor='e')

    #         is_correct = (given and given == ans)
    #         is_unanswered = not given

    #         result_style = "warning" if is_unanswered else "success" if is_correct else "danger"
    #         result_text = "🤷‍♂️ Not Answered" if is_unanswered else "✅ Correct" if is_correct else "❌ Incorrect"
            
    #         ttk.Label(q_frame, text=result_text, bootstyle=result_style, font=Settings.FONT_HELVETICA_BOLD).pack(anchor='w', pady=(5,0))
            
    #         if not is_correct:
    #             if not is_unanswered:
    #                 ttk.Label(q_frame, text=f"   Your Answer: {given}", bootstyle="danger").pack(anchor='w')
    #             ttk.Label(q_frame, text=f"   Correct Answer: {ans}", bootstyle="success").pack(anchor='w')

    #     self.question_number_label.config(text="Test Submitted - Summary")
    #     if self.right_panel:
    #         self.right_panel.quiz_load_btn.config(state="normal")
    #     self.toggle_btn.config(state="normal")


    # def submit_quiz(self) -> None:
    #         """
    #         क्विज़ समाप्त करता है, परिणामों की गणना करता है,
    #         बटनों को समीक्षा के लिए अपडेट करता है, और रिव्यू मोड में प्रवेश करता है।
    #         """
    #         if not self.quiz_data or self.in_review_mode:
    #             return
    #         if not messagebox.askyesno("Submit Test", "Do you want to submit the test?"):
    #             return

    #         # अंतिम प्रश्न का समय और उत्तर रिकॉर्ड करें
    #         self._record_time_spent()
    #         self.stop_question_timer()
    #         if self.answer_var.get():
    #             self.selected_answers[self.current_q_index] = self.answer_var.get().strip()
            
    #         # --- रिव्यू मोड सक्रिय करें ---
    #         self.in_review_mode = True
            
    #         # --- नीचे के नेविगेशन बटनों को अक्षम करें ---
    #         self.mark_review.config(state="disabled")
    #         self.clear_response.config(state="disabled")
    #         self.btn_save_next.config(state="disabled")

    #         # --- राइट पैनल के बटनों को सही/गलत के अनुसार अपडेट करें ---
    #         self._update_buttons_for_review()
            
    #         # --- परिणाम प्रदर्शन (जैसा पहले था वैसा ही) ---
    #         total = len(self.quiz_data)
    #         # ... (बाकी परिणाम गणना और प्रदर्शन का कोड यहाँ आएगा) ...
    #         # (यह हिस्सा अपरिवर्तित है, इसलिए संक्षिप्तता के लिए छोड़ा गया है)
            
    #         # बस यह सुनिश्चित करें कि आप डेटा या बटन क्लियर न करें।
            
    #         # Load Quiz और Mode बटन को फिर से सक्षम करें
    #         if self.right_panel:
    #             self.right_panel.quiz_load_btn.config(state="normal")
    #         self.toggle_btn.config(state="normal")

    #         # उपयोगकर्ता को सूचित करें कि वे अब समीक्षा कर सकते हैं
    #         messagebox.showinfo("Quiz Submitted", "Quiz has been submitted. You can now review your answers by clicking the question numbers on the right.")
            
    #         # पहले प्रश्न पर जाएं ताकि समीक्षा शुरू हो सके
    #         self.show_question(0)


    def submit_quiz(self) -> None:
        """
        क्विज़ समाप्त करता है, परिणामों की गणना करता है, विस्तृत सारांश दिखाता है,
        बटनों को समीक्षा के लिए अपडेट करता है, और रिव्यू मोड में प्रवेश करता है।
        """
        if not self.quiz_data or self.in_review_mode:
            return
        if not messagebox.askyesno("Submit Test", "Do you want to submit the test?"):
            return

        # अंतिम प्रश्न का समय और उत्तर रिकॉर्ड करें
        self._record_time_spent()
        self.stop_question_timer()
        if self.answer_var.get():
            self.selected_answers[self.current_q_index] = self.answer_var.get().strip()
        
        # --- रिव्यू मोड सक्रिय करें ---
        self.in_review_mode = True
        
        # --- नीचे के नेविगेशन बटनों को अक्षम करें ---
        self.mark_review.config(state="disabled")
        self.clear_response.config(state="disabled")
        self.btn_save_next.config(state="disabled")

        # --- राइट पैनल के बटनों को सही/गलत के अनुसार अपडेट करें ---
        self._update_buttons_for_review()
        
        # --- BUG FIX: विस्तृत परिणाम प्रदर्शन (यह हिस्सा गायब था) ---
        
        # 1. परिणाम की गणना
        total = len(self.quiz_data)
        correct = 0
        answered_questions_count = 0
        total_time_on_answered = 0
        fastest_q = {"num": "-", "time": float('inf')}
        slowest_q = {"num": "-", "time": 0.0}

        for i, q in enumerate(self.quiz_data):
            given = str(self.selected_answers.get(i, "")).strip()
            ans = str(q.get("answer", "")).strip()
            time_taken = q.get('_time_taken', 0.0)

            if given:
                answered_questions_count += 1
                total_time_on_answered += time_taken
                if time_taken < fastest_q["time"]:
                    fastest_q = {"num": i + 1, "time": time_taken}
                if time_taken > slowest_q["time"]:
                    slowest_q = {"num": i + 1, "time": time_taken}
            if given and given == ans:
                correct += 1
        
        # 2. मुख्य प्रदर्शन क्षेत्र साफ़ करें
        for w in self.scroll_frame.winfo_children():
            w.destroy()

        # 3. नए विश्लेषण की गणना
        wrong = answered_questions_count - correct
        unattempted = total - answered_questions_count
        accuracy = (correct / answered_questions_count * 100) if answered_questions_count > 0 else 0
        avg_time = (total_time_on_answered / answered_questions_count) if answered_questions_count > 0 else 0
        total_time_str = time.strftime("%H:%M:%S", time.gmtime(self.q_seconds))

        # 4. सारांश (Summary) प्रदर्शित करें
        test_name = self.test_name_label.cget("text")
        ttk.Label(self.scroll_frame, text=f"--- Test Summary: {test_name} ---", font=("Helvetica", 16, "bold"), bootstyle="success").pack(anchor="w", padx=15, pady=(10, 10))
        
        stats_frame = ttk.Frame(self.scroll_frame)
        stats_frame.pack(fill='x', padx=15, pady=5)
        
        stats1 = [
            ("🏆 Score", f"{correct}/{total}"), ("✅ Correct", str(correct)),
            ("❌ Wrong", str(wrong)), ("⚪ Unattempted", str(unattempted)),
            ("🎯 Accuracy", f"{accuracy:.2f}%"),
        ]
        stats2 = [
            ("⏱ Total Time", total_time_str), (" Avg. Time / Ques", f"{avg_time:.2f} sec"),
            (" Fastest Ques", f"Q{fastest_q['num']} ({fastest_q['time']:.2f}s)"),
            (" Slowest Ques", f"Q{slowest_q['num']} ({slowest_q['time']:.2f}s)"),
        ]

        for i, (label, value) in enumerate(stats1):
            ttk.Label(stats_frame, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            ttk.Label(stats_frame, text=value, bootstyle="primary").grid(row=i, column=1, sticky='w', padx=5, pady=2)
        
        for i, (label, value) in enumerate(stats2):
            ttk.Label(stats_frame, text=f"{label}:", font=Settings.FONT_HELVETICA_BOLD).grid(row=i, column=2, sticky='w', padx=20, pady=2)
            ttk.Label(stats_frame, text=value, bootstyle="info").grid(row=i, column=3, sticky='w', padx=5, pady=2)

        ttk.Separator(self.scroll_frame, orient="horizontal").pack(fill="x", pady=15, padx=10)
        
        ttk.Label(self.scroll_frame, text="📌 Click on question numbers on the right to review.", font=("Helvetica", 12, "italic"), bootstyle="info").pack(anchor="w", padx=15, pady=(10, 5))
        
        # --- अंत ---

        # Load Quiz और Mode बटन को फिर से सक्षम करें
        if self.right_panel:
            self.right_panel.quiz_load_btn.config(state="normal")
        self.toggle_btn.config(state="normal")

    def quit_quiz(self) -> None:
        if self.quiz_data and not messagebox.askyesno("Quit Quiz", "Are you sure you want to quit the quiz?"):
            return
        self._reset_quiz()

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
        # ... (यह मेथड अपरिवर्तित है)
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
        self._record_time_spent() # Record time for the previous question
        
        if index is not None: self.current_q_index = index
        if not (0 <= self.current_q_index < len(self.quiz_data)): return
        
        self.visited_questions.add(self.current_q_index)
        for w in self.scroll_frame.winfo_children(): w.destroy()
        
        qdata = self.quiz_data[self.current_q_index]
        self.question_number_label.config(text=f"Question No. {self.current_q_index + 1} / {len(self.quiz_data)}")
        ttk.Label(self.scroll_frame, text=f"Q{self.current_q_index + 1}: {qdata['question']}", wraplength=700, font=("Helvetica", 12)).pack(anchor="w", padx=15, pady=10)
        
        self.answer_var.set(self.selected_answers.get(self.current_q_index, ""))
        # for opt_text in qdata.get('_shuffled_options', []):
        #     ttk.Radiobutton(self.scroll_frame, text=opt_text, value=opt_text, variable=self.answer_var).pack(anchor="w", padx=30, pady=3)
        
        # self.update_status_and_buttons()
        # self.question_start_time = time.time() # Start timer for the new question

        # --- यह लूप बदलें ---
        user_answer = self.selected_answers.get(self.current_q_index, "").strip()
        correct_answer = qdata.get("answer", "").strip()

        for opt_text in qdata.get('_shuffled_options', []):
            r = ttk.Radiobutton(self.scroll_frame, text=opt_text, value=opt_text, variable=self.answer_var)
            
            # रिव्यू मोड में स्टाइलिंग और अक्षम करना
            if self.in_review_mode:
                r.config(state="disabled") # उत्तर बदलने से रोकें
                if opt_text == correct_answer:
                    r.config(bootstyle="success") # सही उत्तर को हरा दिखाएं
                elif opt_text == user_answer:
                    r.config(bootstyle="danger") # यूजर के गलत उत्तर को लाल दिखाएं
            
            r.pack(anchor="w", padx=30, pady=3)
        
        self.update_status_and_buttons()
        self.question_start_time = time.time()

    def _update_and_move_next(self) -> None:
        if not self.quiz_data: return
        # Record time *before* changing index or saving answer
        self._record_time_spent()
        
        current_answer = self.answer_var.get()
        if current_answer: self.selected_answers[self.current_q_index] = current_answer
        else: self.selected_answers.pop(self.current_q_index, None)
        
        self.update_status_and_buttons()
        
        if self.current_q_index < len(self.quiz_data) - 1:
            self.show_question(self.current_q_index + 1)
        else:
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

    def _update_buttons_for_review(self) -> None:
            """सबमिशन के बाद राइट पैनल के बटनों को सही/गलत के अनुसार अपडेट करता है।"""
            if not self.right_panel: return

            for i, q_data in enumerate(self.quiz_data):
                if i >= len(self.right_panel.q_buttons): continue

                btn = self.right_panel.q_buttons[i]
                user_answer = self.selected_answers.get(i, "").strip()
                correct_answer = q_data.get("answer", "").strip()

                if not user_answer:
                    # अनुत्तरित (Unanswered)
                    btn.config(bootstyle="light") 
                elif user_answer == correct_answer:
                    # सही (Correct)
                    btn.config(bootstyle="success")
                else:
                    # गलत (Incorrect)
                    btn.config(bootstyle="danger")


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

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    root.title("Quiz Application")
    root.geometry("1100x650")
    app = QuizPage(root)
    root.mainloop()