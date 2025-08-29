"""
PDF Viewer using ttkbootstrap + PyMuPDF (fitz) + Pillow

Features:
- Open a .pdf file and display pages as images inside a ttkbootstrap window
- Next / Previous page
- Zoom in / Zoom out and a Zoom slider
- Keyboard shortcuts: Left/Right arrows for prev/next, + / - for zoom, Ctrl+O to open

Requirements:
pip install ttkbootstrap pymupdf Pillow

Run: python pdf_viewer_ttkbootstrap.py

Note: PyMuPDF (fitz) renders pages directly, so you don't need poppler.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import fitz  # PyMuPDF
from PIL import Image, ImageTk


class PDFViewer(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("PDF Viewer - ttkbootstrap")
        self.geometry("900x700")

        # State
        self.doc = None
        self.page_index = 0
        self.zoom = 1.0  # scale multiplier
        self._tkimage = None

        # --- Top toolbar ---
        toolbar = ttk.Frame(self, padding=8)
        toolbar.pack(side=TOP, fill=X)

        self.open_btn = ttk.Button(toolbar, text="Open PDF", command=self.open_pdf)
        self.open_btn.pack(side=LEFT, padx=(0, 6))

        self.prev_btn = ttk.Button(toolbar, text="◀ Prev", command=self.prev_page, state=DISABLED)
        self.prev_btn.pack(side=LEFT)

        self.next_btn = ttk.Button(toolbar, text="Next ▶", command=self.next_page, state=DISABLED)
        self.next_btn.pack(side=LEFT, padx=(6, 12))

        self.zoom_out_btn = ttk.Button(toolbar, text="-", width=3, command=lambda: self.change_zoom(-0.1))
        self.zoom_out_btn.pack(side=LEFT)

        self.zoom_in_btn = ttk.Button(toolbar, text="+", width=3, command=lambda: self.change_zoom(0.1))
        self.zoom_in_btn.pack(side=LEFT, padx=(6, 8))

        self.zoom_label = ttk.Label(toolbar, text="Zoom: 100%")
        self.zoom_label.pack(side=LEFT)

        # Zoom slider
        self.zoom_slider = ttk.Scale(toolbar, from_=50, to=300, command=self._on_slider, orient=HORIZONTAL)
        self.zoom_slider.set(100)
        self.zoom_slider.pack(side=LEFT, fill=X, expand=True, padx=(10, 0))

        # Page indicator
        self.page_indicator = ttk.Label(toolbar, text="No file loaded")
        self.page_indicator.pack(side=RIGHT)

        # --- Main area with scrollbars ---
        main_fr = ttk.Frame(self)
        main_fr.pack(fill=BOTH, expand=True, padx=8, pady=(0,8))

        self.canvas = tk.Canvas(main_fr, background="#f8f9fa")
        self.v_scroll = ttk.Scrollbar(main_fr, orient=VERTICAL, command=self.canvas.yview)
        self.h_scroll = ttk.Scrollbar(main_fr, orient=HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.v_scroll.pack(side=RIGHT, fill=Y)
        self.h_scroll.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Image container inside canvas
        self.image_container = self.canvas.create_image(0, 0, anchor="nw")

        # Bindings
        self.bind_all("<Left>", lambda e: self.prev_page())
        self.bind_all("<Right>", lambda e: self.next_page())
        self.bind_all("+", lambda e: self.change_zoom(0.1))
        self.bind_all("-", lambda e: self.change_zoom(-0.1))
        self.bind_all("<Control-o>", lambda e: self.open_pdf())
        # Ctrl+Mousewheel for zoom (Windows / Mac/ Linux semantics vary)
        self.canvas.bind('<Control-MouseWheel>', self._on_ctrl_mousewheel)
        self.canvas.bind('<Control-Button-4>', self._on_ctrl_mousewheel)  # Linux scroll up
        self.canvas.bind('<Control-Button-5>', self._on_ctrl_mousewheel)  # Linux scroll down

    # ----------------- File / Rendering logic -----------------
    def open_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        try:
            doc = fitz.open(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open PDF:\n{e}")
            return

        self.doc = doc
        self.page_index = 0
        self.zoom = 1.0
        self.zoom_slider.set(100)
        self._update_buttons()
        self.render_page()

    def _update_buttons(self):
        if not self.doc:
            self.prev_btn.configure(state=DISABLED)
            self.next_btn.configure(state=DISABLED)
            self.page_indicator.configure(text="No file loaded")
        else:
            self.prev_btn.configure(state=NORMAL if self.page_index > 0 else DISABLED)
            self.next_btn.configure(state=NORMAL if self.page_index < len(self.doc) - 1 else DISABLED)
            self.page_indicator.configure(text=f"Page {self.page_index+1} / {len(self.doc)}")

    def prev_page(self):
        if not self.doc or self.page_index <= 0:
            return
        self.page_index -= 1
        self._update_buttons()
        self.render_page()

    def next_page(self):
        if not self.doc or self.page_index >= len(self.doc) - 1:
            return
        self.page_index += 1
        self._update_buttons()
        self.render_page()

    def change_zoom(self, delta):
        # delta is additive (e.g. 0.1) representing 10%
        new_zoom = max(0.2, min(5.0, self.zoom + delta))
        self.zoom = new_zoom
        self.zoom_slider.set(int(self.zoom * 100))
        self.render_page()

    def _on_slider(self, val):
        try:
            v = float(val)
            self.zoom = max(0.2, min(5.0, v / 100.0))
            self.zoom_label.configure(text=f"Zoom: {int(v)}%")
            self.render_page()
        except Exception:
            pass

    def _on_ctrl_mousewheel(self, event):
        # Windows event.delta positive when wheel up, negative when down
        delta = 0
        if hasattr(event, 'delta'):
            delta = 1 if event.delta > 0 else -1
        else:
            # On some X11 systems use num (Button-4 up / Button-5 down)
            if event.num == 4:
                delta = 1
            elif event.num == 5:
                delta = -1
        self.change_zoom(delta * 0.1)

    def render_page(self):
        if not self.doc:
            return
        page = self.doc.load_page(self.page_index)
        mat = fitz.Matrix(self.zoom, self.zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        # Convert fitz.Pixmap to PIL Image
        mode = "RGB"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)

        # Keep a reference to PhotoImage to avoid GC
        self._tkimage = ImageTk.PhotoImage(img)
        self.canvas.itemconfigure(self.image_container, image=self._tkimage)

        # Resize canvas scroll region to image size
        self.canvas.config(scrollregion=(0, 0, pix.width, pix.height))

        # Update indicator and buttons
        self.zoom_label.configure(text=f"Zoom: {int(self.zoom*100)}%")
        self._update_buttons()


if __name__ == "__main__":
    app = PDFViewer()
    app.mainloop()
