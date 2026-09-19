from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from .theme import ACCENT, BLUE, INK, KEY, PANEL, SELECT


class HistoryView(tk.Frame):
    def __init__(self, master: tk.Misc, on_reuse: Callable[[str], None]) -> None:
        super().__init__(master, bg="white")
        self.on_reuse = on_reuse
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.body = tk.Frame(self.canvas, bg="white")
        self.body.bind("<Configure>", lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.window = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window, width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.selected_text = ""
        self.selected_widget: tk.Widget | None = None

    def clear(self) -> None:
        for child in self.body.winfo_children(): child.destroy()

    def append(self, input_text: str, output_text: str) -> None:
        row = tk.Frame(self.body, bg="white", pady=5)
        row.pack(fill="x", padx=7)
        inp = tk.Label(row, text=input_text, bg="white", fg=INK, anchor="w", font=("Segoe UI", 12))
        out = tk.Label(row, text=output_text, bg="white", fg=INK, anchor="e", font=("Cambria Math", 14, "bold"))
        inp.pack(fill="x"); out.pack(fill="x", pady=(3, 0))
        ttk.Separator(row).pack(fill="x", pady=(6, 0))
        for widget, text in ((inp, input_text), (out, output_text)):
            widget.bind("<Button-1>", lambda _, w=widget, t=text: self.select(w, t))
            widget.bind("<Double-Button-1>", lambda _, t=text: self.on_reuse(t))
        self.canvas.update_idletasks(); self.canvas.yview_moveto(1)

    def select(self, widget: tk.Widget, text: str) -> None:
        if self.selected_widget:
            self.selected_widget.configure(bg="white")
        widget.configure(bg=SELECT)
        self.selected_widget, self.selected_text = widget, text


class SoftKeyboard(tk.Frame):
    PAGES = {
        "mth": [["7", "8", "9", "÷", "√("], ["4", "5", "6", "×", "^"],
                ["1", "2", "3", "+", "−"], ["0", ".", "(", ")", "EXE"]],
        "abc": [["x", "y", "z", "a", "b"], ["c", "d", "e", "i", "π"],
                ["sin(", "cos(", "tan(", "ln(", "log("], [":=", ",", "←", "CLR", "EXE"]],
        "cat": [["diff(", "integrate(", "solve(", "factor(", "expand("],
                ["sqrt(", "abs(", "sum(", "limit(", "subs("],
                ["!", "C", "P", "∞", "≈"], [",", "(", ")", "←", "EXE"]],
    }

    def __init__(self, master: tk.Misc, insert: Callable[[str], None], execute: Callable[[bool], None]) -> None:
        super().__init__(master, bg=PANEL)
        self.insert, self.execute = insert, execute
        tabs = tk.Frame(self, bg=BLUE)
        tabs.pack(fill="x")
        for page in self.PAGES:
            tk.Button(tabs, text=page, relief="flat", command=lambda p=page: self.show(p),
                      bg=BLUE, fg="white", activebackground="#245b78").pack(side="left", fill="x", expand=True)
        self.keys = tk.Frame(self, bg=PANEL)
        self.keys.pack(fill="both", expand=True)
        self.show("mth")

    def show(self, page: str) -> None:
        for child in self.keys.winfo_children(): child.destroy()
        for r, row in enumerate(self.PAGES[page]):
            self.keys.grid_rowconfigure(r, weight=1)
            for c, label in enumerate(row):
                self.keys.grid_columnconfigure(c, weight=1)
                command = (lambda: self.execute(False)) if label == "EXE" else ((lambda: self.execute(True)) if label == "≈" else lambda v=label: self.insert(v))
                tk.Button(self.keys, text=label, command=command, bg=ACCENT if label == "EXE" else KEY,
                          font=("Segoe UI", 10), relief="raised", bd=1).grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
