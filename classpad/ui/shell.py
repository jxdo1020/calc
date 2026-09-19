from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from classpad.applications.graph import GraphApplication
from classpad.applications.main import MainApplication
from classpad.applications.statistics import StatisticsApplication
from classpad.applications.tools import MatrixApplication, NumericSolverApplication, SystemApplication
from classpad.core.persistence import SessionStore
from classpad.ui.theme import APP_ICONS, BG, BLUE, BLUE_DARK, PANEL


class ClassPadShell(tk.Tk):
    def __init__(self, store: SessionStore | None = None) -> None:
        super().__init__(); self.store = store or SessionStore(); self.session = self.store.load()
        self.title("Open ClassPad"); self.geometry("520x820"); self.minsize(360, 590); self.configure(bg=BG)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.header = tk.Frame(self, bg=BLUE_DARK, height=34); self.header.pack(fill="x"); self.header.pack_propagate(False)
        self.title_label = tk.Label(self.header, text="Application", bg=BLUE_DARK, fg="white", font=("Segoe UI", 11, "bold")); self.title_label.pack(side="left", padx=9)
        tk.Label(self.header, text="ClassPad II", bg=BLUE_DARK, fg="#dcecf4").pack(side="right", padx=9)
        self.content = tk.Frame(self, bg=BG); self.content.pack(fill="both", expand=True)
        self.status = tk.Label(self, relief="sunken", anchor="w", bg="#eef2f3", font=("Segoe UI", 9)); self.status.pack(fill="x")
        self.refresh_status(); self.show_launcher()

    def replace(self, widget_type, title: str) -> None:
        for child in self.content.winfo_children(): child.destroy()
        self.title_label.configure(text=title); widget_type(self.content, self).pack(fill="both", expand=True)

    def show_launcher(self) -> None:
        for child in self.content.winfo_children(): child.destroy()
        self.title_label.configure(text="Application")
        canvas = tk.Canvas(self.content, bg=BG, highlightthickness=0); canvas.pack(fill="both", expand=True)
        body = tk.Frame(canvas, bg=BG); window = canvas.create_window((0,0), window=body, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window, width=e.width)); body.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        supported = {"Main": MainApplication, "Graph & Table": GraphApplication, "Statistics": StatisticsApplication,
                     "Numeric Solver": NumericSolverApplication, "Matrix": MatrixApplication, "System": SystemApplication}
        names = ["Main", "Graph & Table", "Statistics", "Spreadsheet", "Numeric Solver", "Matrix", "Geometry", "Conics", "3D Graph", "Sequence", "Financial", "System"]
        for index, name in enumerate(names):
            cell = tk.Frame(body, bg=BG, padx=7, pady=9); cell.grid(row=index//3, column=index%3, sticky="nsew")
            glyph, color = APP_ICONS[name]
            action = (lambda n=name, w=supported.get(name): self.replace(w, n)) if name in supported else (lambda n=name: messagebox.showinfo(n, "This application is not implemented yet.\nSee LIMITATIONS.md.", parent=self))
            tk.Button(cell, text=glyph, command=action, bg=color, fg="white", font=("Segoe UI Symbol", 25, "bold"), width=4, height=2, relief="raised").pack()
            tk.Label(cell, text=name, bg=BG, wraplength=120, font=("Segoe UI", 9)).pack(pady=(3,0))
        for column in range(3): body.grid_columnconfigure(column, weight=1)

    def refresh_status(self) -> None:
        s = self.session.settings; self.status.configure(text=f"  {s.angle_mode}     {s.calculation_mode}     {s.complex_mode}     Kbd")

    def close(self) -> None:
        try: self.store.save(self.session)
        finally: self.destroy()
