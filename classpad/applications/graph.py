from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import sympy as sp

from classpad.core.graphing import roots, sample_function
from classpad.core.parser import normalize
from classpad.ui.theme import BLUE, PANEL


class GraphApplication(tk.Frame):
    COLORS = ["#1b6ca8", "#d34e4e", "#439552", "#8c5aae", "#d08a24"]

    def __init__(self, master: tk.Misc, shell) -> None:
        super().__init__(master, bg=PANEL); self.shell = shell; self.trace_index = 0
        tools = tk.Frame(self, bg=PANEL); tools.pack(fill="x")
        for label, fn in (("⌂", shell.show_launcher), ("Graph", self.draw), ("Table", self.table),
                          ("Trace", self.trace), ("Root", self.find_roots), ("V-Window", self.view_window)):
            tk.Button(tools, text=label, command=fn).pack(side="left")
        editor = tk.Frame(self, bg="white"); editor.pack(fill="x")
        self.enabled: list[tk.BooleanVar] = []; self.entries: list[tk.Entry] = []
        for i in range(5):
            active = tk.BooleanVar(value=bool(shell.session.graphs[i])); self.enabled.append(active)
            tk.Checkbutton(editor, variable=active, bg="white").grid(row=i, column=0)
            tk.Label(editor, text=f"y{i+1}=", fg=self.COLORS[i], bg="white").grid(row=i, column=1)
            entry = tk.Entry(editor); entry.insert(0, shell.session.graphs[i]); entry.grid(row=i, column=2, sticky="ew"); self.entries.append(entry)
        editor.grid_columnconfigure(2, weight=1)
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1); self.canvas.pack(fill="both", expand=True)
        self.readout = tk.Label(self, text="", anchor="w", bg=BLUE, fg="white"); self.readout.pack(fill="x")
        self.canvas.bind("<Configure>", lambda _: self.draw())

    def functions(self):
        x = sp.Symbol("x"); result = []
        for active, entry in zip(self.enabled, self.entries):
            if active.get() and entry.get().strip():
                expression = sp.sympify(normalize(entry.get()), locals={"x": x})
                result.append((entry.get(), sp.lambdify(x, expression, modules="math")))
        return result

    def draw(self) -> None:
        self.shell.session.graphs = [entry.get() for entry in self.entries]
        c = self.canvas; c.delete("all"); w, h = max(c.winfo_width(), 2), max(c.winfo_height(), 2); s = self.shell.session.settings
        px = lambda x: (x - s.xmin) / (s.xmax - s.xmin) * w
        py = lambda y: h - (y - s.ymin) / (s.ymax - s.ymin) * h
        if s.grid:
            x = math.ceil(s.xmin / s.xscale) * s.xscale
            while x <= s.xmax: c.create_line(px(x), 0, px(x), h, fill="#e1e5e6"); x += s.xscale
            y = math.ceil(s.ymin / s.yscale) * s.yscale
            while y <= s.ymax: c.create_line(0, py(y), w, py(y), fill="#e1e5e6"); y += s.yscale
        if s.axes:
            c.create_line(0, py(0), w, py(0), fill="#333"); c.create_line(px(0), 0, px(0), h, fill="#333")
        try:
            for index, (_, function) in enumerate(self.functions()):
                for segment in sample_function(function, s.xmin, s.xmax, w, (s.ymax-s.ymin)*2):
                    coords = [coordinate for point in segment for coordinate in (px(point.x), py(point.y))]
                    c.create_line(*coords, fill=self.COLORS[index], width=2)
        except Exception as exc: self.readout.configure(text=f"Graph ERROR: {exc}")

    def trace(self) -> None:
        funcs = self.functions()
        if not funcs: return
        x = simpledialog.askfloat("Trace", "x =", initialvalue=0, parent=self)
        if x is not None:
            try: self.readout.configure(text=f"Trace  y1   x={x:.8g}   y={funcs[0][1](x):.8g}")
            except Exception: self.readout.configure(text="Trace: Undefined")

    def find_roots(self) -> None:
        funcs = self.functions(); s = self.shell.session.settings
        if funcs:
            values = roots(funcs[0][1], s.xmin, s.xmax)
            self.readout.configure(text="Root: " + (", ".join(f"({x:.8g}, 0)" for x in values) or "No Solution"))

    def table(self) -> None:
        dialog = tk.Toplevel(self); dialog.title("Table"); dialog.geometry("430x400")
        funcs = self.functions(); tree = ttk.Treeview(dialog, columns=["x"]+[f"y{i+1}" for i in range(len(funcs))], show="headings")
        for col in tree["columns"]: tree.heading(col, text=col); tree.column(col, width=85, anchor="e")
        start, end, step = -5.0, 5.0, 1.0; x = start
        while x <= end + step/2:
            values = [f"{x:g}"]
            for _, function in funcs:
                try: values.append(f"{function(x):.8g}")
                except Exception: values.append("Undefined")
            tree.insert("", "end", values=values); x += step
        tree.pack(fill="both", expand=True)

    def view_window(self) -> None:
        s = self.shell.session.settings
        value = simpledialog.askstring("View Window", "Xmin, Xmax, Xscale, Ymin, Ymax, Yscale:",
            initialvalue=f"{s.xmin}, {s.xmax}, {s.xscale}, {s.ymin}, {s.ymax}, {s.yscale}", parent=self)
        if value:
            try: s.xmin, s.xmax, s.xscale, s.ymin, s.ymax, s.yscale = map(float, value.split(",")); self.draw()
            except ValueError: messagebox.showerror("View Window", "Enter six numeric values", parent=self)
