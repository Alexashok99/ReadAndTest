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
#Internet connection check ke liye socket import karein
import socket 

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
    WARNING_OUTLINE = "warning-outline"
    INFO_OUT = "info-outline"
    USER_TAG_COLOR = "info"
    ASSISTANT_TAG_COLOR = "success"

    #-------- AI Related--------------------
    AVAILABLE_MODELS = ["gemini-2.5-flash", 
                        "gemini-2.5-pro", 
                        "gemini-2.5-flash-lite", 
                        "gemini-2.0-flash", 
                        "gemini-2.0-flash-lite", 
                        "gemini-1.5-flash",
                        ]
    MODEL_NAME = AVAILABLE_MODELS[0]
    APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'QuickRevise')
    os.makedirs(APP_DATA_DIR, exist_ok=True)
    API_KEY_FILE = os.path.join(APP_DATA_DIR, "api_key.txt")

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

    # Internet check karne ke liye ek static method banayein
    @staticmethod
    def check_internet(host="8.8.8.8", port=53, timeout=3):
        """
        Internet connection check karne ke liye ek host se connect karne ki koshish karein.
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    __MAJOR = 2
    __MINOR = 3
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


class ApiKeyManager:
    """Handles saving and loading the API key from a local file."""
    
    @staticmethod
    def save_key(api_key: str) -> None:
        try:
            with open(Settings.API_KEY_FILE, "w") as f:
                f.write(api_key)
        except IOError as e:
            messagebox.showerror("Save Error", f"Could not save API key: {e}")

    @staticmethod
    def load_key() -> Optional[str]:
        if not os.path.exists(Settings.API_KEY_FILE):
            return None
        try:
            with open(Settings.API_KEY_FILE, "r") as f:
                return f.read().strip()
        except IOError as e:
            messagebox.showerror("Load Error", f"Could not load API key: {e}")
            return None


class HomePage(BaseFrame):
    """The main page of the application, containing the chat interface."""
    def __init__(self, master, app):
        super().__init__(master, app)
        self.pack(fill=BOTH, expand=YES)

        self.home_page_container = ttk.Frame(self)
        self.home_page_container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.home_page_container.grid_rowconfigure(1, weight=1)
        self.home_page_container.grid_columnconfigure(1, weight=4)

        self.create_top_bar()
        self.create_button_area()
        self.create_main_chat_area()
        self.process_response_queue()

        # BUG FIX: App start hone par check karein ki API key hai ya nahi.
        if not self.app.api_key:
            self.disable_chat_for_api_key()

    def create_top_bar(self):
        top_bar_frame = ttk.Frame(self.home_page_container)
        top_bar_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW, pady=(0, 10))
        
        ttk.Label(top_bar_frame, text="Gemini AI Chat", font=Settings.FONT_SUBTITLE, bootstyle=Settings.SUCCESS_COLOR).pack(side=LEFT, padx=(0, 10))

        self.status_var = StringVar(value="Online")
        self.status_label = ttk.Label(top_bar_frame, textvariable=self.status_var, font=Settings.FONT_SEGEO, bootstyle=Settings.INFO_COLOR)
        self.status_label.pack(side=LEFT, fill=X, expand=YES)
        
        theme_frame = ttk.Frame(top_bar_frame)
        theme_frame.pack(side=RIGHT)
        ttk.Label(theme_frame, text="Theme:", font=Settings.FONT_SEGEO).pack(side=LEFT, padx=(0, 5))
        current_theme = self.app.style.theme_use()
        self._theme_var = tk.StringVar(value=current_theme)
        theme_combobox = ttk.Combobox(theme_frame, values=Settings.THEME, textvariable=self._theme_var, state="readonly", width=12)
        theme_combobox.pack(side=LEFT)
        theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)

        # --- MODEL CHANGER COMBOBOX (START) ---
        model_frame = ttk.Frame(top_bar_frame)
        model_frame.pack(side=RIGHT, padx=(10, 0)) # Theme selector se pehle pack karein

        ttk.Label(model_frame, text="Model:", font=Settings.FONT_SEGEO).pack(side=LEFT, padx=(0, 5))
        
        self.app.model_var = tk.StringVar(value=Settings.MODEL_NAME) # MainApp mein variable banayein
        model_combobox = ttk.Combobox(
            model_frame, 
            values=Settings.AVAILABLE_MODELS, 
            textvariable=self.app.model_var, 
            state="readonly", 
            width=18 # Thoda chauda
        )
        model_combobox.pack(side=LEFT)
        model_combobox.bind("<<ComboboxSelected>>", self.on_model_change)
        # --- MODEL CHANGER COMBOBOX (END) ---

    def change_theme(self, event=None):
        self.app.style.theme_use(self._theme_var.get())
        self.apply_chat_colors()

    def apply_chat_colors(self):
        user_color = self.app.style.colors.get(Settings.USER_TAG_COLOR)
        assistant_color = self.app.style.colors.get(Settings.ASSISTANT_TAG_COLOR)
        self.chat_display.tag_config("user", font=Settings.FONT_CHAT_BOLD, foreground=user_color)
        self.chat_display.tag_config("assistant", font=Settings.FONT_CHAT, foreground=assistant_color)

    def create_button_area(self):
        button_frame = ttk.Frame(self.home_page_container, padding=5)
        button_frame.grid(row=1, column=0, sticky=NSEW, padx=(0, 10))
        ttk.Button(button_frame, 
                   text="Read Notes", 
                   bootstyle=Settings.SUCCESS_OUTLINE, 
                   width=Settings.SM_BTN_WIDTH, 
                   command=lambda: print("READ NOTES")
                   ).pack(pady=Settings.PAD_MEDIUM, fill=X)
        
        ttk.Button(button_frame, 
                   text="Quiz Time", 
                   bootstyle=Settings.SUCCESS_OUTLINE, 
                   width=Settings.SM_BTN_WIDTH, command=lambda: print("QUIZ TIME")).pack(pady=Settings.PAD_MEDIUM, fill=X)
        
        ttk.Button(button_frame, 
                   text="Clear Chat", 
                   bootstyle=Settings.DANGER_OUTLINE, 
                   width=Settings.SM_BTN_WIDTH, 
                   command=self.clear_chat
                   ).pack(pady=Settings.PAD_MEDIUM, fill=X)
        
        ttk.Button(button_frame, 
                   text="Change API Key", 
                   bootstyle=Settings.INFO_OUT, 
                   width=Settings.SM_BTN_WIDTH, 
                   command=lambda: self.app.show_api_key_dialog(from_menu=True)
                   ).pack(pady=Settings.PAD_MEDIUM, fill=X)
        
        ttk.Button(button_frame, 
                   text="Close App", 
                   bootstyle=Settings.DANGER_OUTLINE, 
                   width=Settings.SM_BTN_WIDTH, 
                   command=self.app.destroy
                   ).pack(pady=Settings.PAD_MEDIUM, fill=X)

    def create_main_chat_area(self):
        main_area_frame = ttk.Frame(self.home_page_container)
        main_area_frame.grid(row=1, column=1, sticky=NSEW)
        main_area_frame.rowconfigure(0, weight=1)
        main_area_frame.columnconfigure(0, weight=1)

        # --- HINDI TEXT FIX: Added spacing3=10 for better line spacing ---
        self.chat_display = scrolledtext.ScrolledText(
            main_area_frame, wrap=tk.WORD, font=Settings.FONT_CHAT, 
            state=DISABLED, padx=8, pady=8, spacing3=10
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        
        self.apply_chat_colors()
        
        self.input_entry = ttk.Text(main_area_frame, height=Settings.INPUT_HEIGHT, font=Settings.FONT_CHAT, padx=8, pady=8)
        self.input_entry.grid(row=1, column=0, sticky=NSEW, pady=(Settings.PAD_MEDIUM, 0))
        self.input_entry.focus_set()
        self.send_button = ttk.Button(main_area_frame, text="Send", command=self.send_message, bootstyle=Settings.SUCCESS_COLOR)
        self.send_button.grid(row=1, column=1, sticky="nsew", pady=(Settings.PAD_MEDIUM, 0), padx=(Settings.PAD_SMALL, 0))
        self.input_entry.bind('<Return>', self.handle_return)
        self.add_message("Assistant", "Hello! How can I help you today?")

    def handle_return(self, event):
        if not (event.state & 1):
            self.send_message()
            return "break"

    def send_message(self):
        # BUG FIX: Message bhejne se pehle check karein ki API key hai ya nahi
        if not self.app.api_key:
            messagebox.showwarning("API Key Missing", "Please set your API key using the 'Change API Key' button before sending a message.")
            return
            
        # BUG FIX: Message bhejne se pehle internet connection check karein
        if not Settings.check_internet():
            Settings.show_toast(title="Connection Error", 
                                message="No internet connection detected. Please check your network and try again.", 
                                bootstyle=DANGER)
            # messagebox.showerror("Connection Error", "No internet connection detected. Please check your network and try again.")
            self.status_var.set("Offline")
            return

        if self.app.is_processing: return
        user_input = self.input_entry.get("1.0", tk.END).strip()
        if not user_input: return
        self.add_message("User", user_input)
        self.input_entry.delete("1.0", tk.END)
        self.app.is_processing = True
        self.send_button.config(state=DISABLED)
        self.status_var.set("AI is typing...")
        self.add_message("Assistant", "...", is_typing=True)
        
        thread = threading.Thread(target=self.get_ai_response, args=(user_input,), daemon=True)
        thread.start()

    def get_ai_response(self, user_input: str):
        self.app.chat_history.append({"role": "user", "parts": [user_input]})
        try:
            genai.configure(api_key=self.app.api_key)
            model = genai.GenerativeModel(Settings.MODEL_NAME)
            limited_history = self.app.chat_history[-20:]
            response = model.generate_content(limited_history)
            ai_response = response.text
            self.app.chat_history.append({"role": "model", "parts": [ai_response]})
            self.app.response_queue.put({'status': 'success', 'data': ai_response})
        except Exception as e:
            self.app.chat_history.pop()
            error_message = f"An error occurred. Please check API key/internet."
            self.app.response_queue.put({'status': 'error', 'data': error_message, 'exception': e})

    def process_response_queue(self):
        try:
            response_data = self.app.response_queue.get_nowait()
            self.update_last_message(response_data['data'])
            
            if response_data['status'] == 'error':
                 self.status_var.set("Error!")
                 messagebox.showerror("API Error", f"Details: {response_data['exception']}")
            else:
                 self.status_var.set("Online")
            
            self.app.is_processing = False
            self.send_button.config(state=NORMAL)
        except queue.Empty:
            pass
        finally:
            self.after(100, self.process_response_queue)

    def add_message(self, sender: str, message: str, is_typing: bool = False):
        self.chat_display.config(state=NORMAL)
        sender_tag = "user" if sender.lower() == "user" else "assistant"
        if self.chat_display.index('end-1c') != "1.0": self.chat_display.insert(tk.END, "\n")
        display_sender = "You" if sender.lower() == "user" else "AI"
        self.chat_display.insert(tk.END, f"{display_sender}: \n", sender_tag)
        self.chat_display.insert(tk.END, message)
        self.typing_start_index = self.chat_display.index(f'end-{len(message)+1}c')
        self.chat_display.see(tk.END)
        self.chat_display.config(state=DISABLED)

    def update_last_message(self, new_message: str):
        self.chat_display.config(state=NORMAL)
        if hasattr(self, 'typing_start_index'):
            self.chat_display.delete(self.typing_start_index, tk.END)
            self.chat_display.insert(tk.END, new_message)
            del self.typing_start_index
        self.chat_display.see(tk.END)
        self.chat_display.config(state=DISABLED)

    def clear_chat(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear the chat history?"):
            self.chat_display.config(state=NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=DISABLED)
            self.app.chat_history.clear()
            self.add_message("Assistant", "Chat cleared. How can I help you next?")

    def on_model_change(self, event=None):
        """Jab user naya model chunta hai to yeh function chalta hai."""
        new_model = self.app.model_var.get()
        Settings.MODEL_NAME = new_model # Settings class mein model ka naam update karein
        
        # User ko batayein ki model badal gaya hai
        self.add_message("Assistant", f"Model changed to: {new_model}")
        
    # Chat ko enable aur disable karne ke liye functions.
    def enable_chat(self):
        """Chat input aur send button ko enable karta hai."""
        self.input_entry.config(state=NORMAL)
        self.send_button.config(state=NORMAL)
        self.add_message("Assistant", "API Key has been set. You can now start chatting!")

    def disable_chat_for_api_key(self):
        """API key na hone par chat ko disable karta hai."""
        self.input_entry.config(state=DISABLED)
        self.send_button.config(state=DISABLED)
        self.add_message("Assistant", "Welcome! Please set your API key using the 'Change API Key' button to enable the chat.")


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
       
        self.current_frame = None

        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=BOTH, expand=YES)
        self.main_container.grid_columnconfigure(0, weight=1, uniform="group1")
        self.main_container.grid_rowconfigure(0, weight=20, uniform="group2")
        self.main_container.grid_rowconfigure(1, weight=1, uniform="group2")

        self.api_key = ApiKeyManager.load_key()
        self.is_processing = False
        self.chat_history = []
        self.response_queue = queue.Queue()

        # BUG FIX: Hamesha main frame banayein, bhale hi API key na ho.
        self.main_frame()
        
        # BUG FIX: Agar API key nahi hai, to dialog dikhayein.
        if not self.api_key:
            # 'after' ka upyog karein taaki main window pehle draw ho jaye.
            self.after(100, lambda: self.show_api_key_dialog(from_menu=False))
            
        self.bottom_bar()

    def main_frame(self):
        self.main_area_frame = ttk.Frame(self.main_container)
        self.main_area_frame.grid(row=0, column=0, sticky=NSEW)
        self.current_frame = HomePage(self.main_area_frame, app=self)
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

    def show_api_key_dialog(self, from_menu: bool = False):
        dialog = ttk.Toplevel(self)
        dialog.title("Enter API Key")
        dialog.geometry("400x150")
        dialog.transient(self)
        dialog.grab_set()
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        main_frame = ttk.Frame(dialog, padding=Settings.PAD_LARGE)
        main_frame.pack(fill=BOTH, expand=YES)
        ttk.Label(main_frame, text="Please enter your Gemini API key:").pack(pady=Settings.PAD_SMALL)
        key_entry = ttk.Entry(main_frame, show="*")
        key_entry.pack(fill=X, pady=Settings.PAD_SMALL)
        key_entry.focus_set()
        def save_and_close():
            key = key_entry.get().strip()
            if key:
                self.api_key = key
                ApiKeyManager.save_key(key)
                dialog.destroy()
                # BUG FIX: Key save hone ke baad, agar HomePage hai to chat ko enable karein.
                if self.current_frame and isinstance(self.current_frame, HomePage):
                    self.current_frame.enable_chat()
                ToastNotification("API Key Saved", "Your API key has been saved successfully.", bootstyle=SUCCESS, duration=3000).show_toast()
            else:
                messagebox.showwarning("Empty Key", "API key cannot be empty.", parent=dialog)
        ttk.Button(main_frame, text="Save", command=save_and_close, bootstyle=SUCCESS).pack(pady=Settings.PAD_MEDIUM)
        dialog.bind('<Return>', lambda e: save_and_close())
        
        # BUG FIX: Agar dialog ko 'x' se band kiya jaye to app ko band na karein.
        # Sirf dialog ko destroy karein.
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()