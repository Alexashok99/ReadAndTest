"""
Simple PDF viewer using ttkbootstrap + PyMuPDF (fitz) + Pillow
Features:
- Open PDF file
- Navigate pages (Prev / Next)
- Zoom in / Zoom out (with fit-to-window option)
- Scrollable canvas to view rendered PDF page image

Requirements:
pip install ttkbootstrap pymupdf pillow

Run:
python ttkbootstrap_pdf_viewer.py

Notes:
- PyMuPDF (imported as fitz) renders PDF pages to pixmaps which we convert to PIL images.
- Keep large PDFs in mind: rendering high-zoom pages can be memory-heavy. This example caches only current page.
"""

import os
import io
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk


class PDFViewer(ttk.Window):
    def __init__(self):
        super().__init__(title="PDF Viewer - ttkbootstrap", themename="pulse")
        self.geometry('900x700')
        self.minsize(480, 320)

        # PDF state
        self.doc = None
        self.current_page_index = 0
        self.zoom_factor = 1.0  # 1.0 = 100%
        self.photo_image = None

        # Top controls
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        open_btn = ttk.Button(toolbar, text="Open PDF", command=self.open_pdf)
        open_btn.pack(side=tk.LEFT, padx=4)

        prev_btn = ttk.Button(toolbar, text="⟨ Prev", command=self.prev_page)
        prev_btn.pack(side=tk.LEFT, padx=4)

        next_btn = ttk.Button(toolbar, text="Next ⟩", command=self.next_page)
        next_btn.pack(side=tk.LEFT, padx=4)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6)

        zoom_out = ttk.Button(toolbar, text="−", width=3, command=self.zoom_out)
        zoom_out.pack(side=tk.LEFT, padx=2)

        self.zoom_lbl = ttk.Label(toolbar, text=f"{int(self.zoom_factor*100)}%")
        self.zoom_lbl.pack(side=tk.LEFT)

        zoom_in = ttk.Button(toolbar, text="+", width=3, command=self.zoom_in)
        zoom_in.pack(side=tk.LEFT, padx=2)

        fit_btn = ttk.Button(toolbar, text="Fit to Width", command=self.fit_to_width)
        fit_btn.pack(side=tk.LEFT, padx=6)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=6)

        self.page_var = ttk.StringVar(value="Page: 0 / 0")
        page_label = ttk.Label(toolbar, textvariable=self.page_var)
        page_label.pack(side=tk.LEFT, padx=6)

        # Main canvas with scrollbars
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(main_frame, bg="#2a2a2a")
        self.hbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.vbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar.grid(row=1, column=0, sticky="ew")

        # Inside canvas we place an inner frame
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")

        # Label to hold image
        self.image_label = ttk.Label(self.inner_frame)
        self.image_label.pack()

        # Bind resizing and mouse wheel
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.bind_all('<MouseWheel>', self._on_mousewheel)  # Windows
        self.bind_all('<Button-4>', self._on_mousewheel)    # Linux scroll up
        self.bind_all('<Button-5>', self._on_mousewheel)    # Linux scroll down

    def open_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        try:
            self.doc = fitz.open(path)
            self.current_page_index = 0
            self.zoom_factor = 1.0
            self._render_current_page()
            self._update_page_label()
            self.title(f"PDF Viewer - {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open PDF:\n{e}")

    def _render_current_page(self):
        if not self.doc:
            return
        page = self.doc.load_page(self.current_page_index)
        mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        mode = "RGB"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        # Keep reference
        self.photo_image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=self.photo_image)

        # Update canvas scroll region to image size
        self.inner_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _update_page_label(self):
        total = len(self.doc) if self.doc else 0
        self.page_var.set(f"Page: {self.current_page_index+1} / {total}")
        self.zoom_lbl.configure(text=f"{int(self.zoom_factor*100)}%")

    def next_page(self):
        if not self.doc:
            return
        if self.current_page_index < len(self.doc)-1:
            self.current_page_index += 1
            self._render_current_page()
            self._update_page_label()

    def prev_page(self):
        if not self.doc:
            return
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self._render_current_page()
            self._update_page_label()

    def zoom_in(self):
        if not self.doc:
            return
        # incremental zoom
        self.zoom_factor *= 1.25
        self._render_current_page()
        self._update_page_label()

    def zoom_out(self):
        if not self.doc:
            return
        self.zoom_factor /= 1.25
        # prevent too small
        if self.zoom_factor < 0.1:
            self.zoom_factor = 0.1
        self._render_current_page()
        self._update_page_label()

    def fit_to_width(self):
        if not self.doc:
            return
        # Fit current page width to canvas width
        page = self.doc.load_page(self.current_page_index)
        rect = page.rect
        canvas_width = max(self.canvas.winfo_width(), 100)
        # compute zoom so that page width * zoom = canvas_width
        self.zoom_factor = canvas_width / rect.width
        # clamp
        if self.zoom_factor < 0.1:
            self.zoom_factor = 0.1
        self._render_current_page()
        self._update_page_label()

    def _on_canvas_configure(self, event):
        # keep scroll region correct
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _on_mousewheel(self, event):
        # allow scroll inside canvas
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, 'units')
        else:
            self.canvas.yview_scroll(1, 'units')


if __name__ == '__main__':
    app = PDFViewer()
    app.mainloop()
