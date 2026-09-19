from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from classpad.core.statistics import binomial_cdf, binomial_pdf, linear_regression, normal_cdf, normal_pdf, one_variable
from classpad.ui.theme import PANEL


class StatisticsApplication(tk.Frame):
    def __init__(self, master: tk.Misc, shell) -> None:
        super().__init__(master, bg=PANEL); self.shell = shell
        tools = tk.Frame(self, bg=PANEL); tools.pack(fill="x")
        for label, fn in (("⌂", shell.show_launcher), ("1-Var", self.summary), ("Linear Reg", self.regression),
                          ("Normal", self.normal), ("Binomial", self.binomial)):
            tk.Button(tools, text=label, command=fn).pack(side="left")
        grid = tk.Frame(self, bg="white"); grid.pack(fill="both", expand=True)
        self.lists = []
        for i in range(3):
            frame = tk.Frame(grid, bg="white"); frame.pack(side="left", fill="both", expand=True)
            tk.Label(frame, text=f"list{i+1}", bg="#dce8ed").pack(fill="x")
            box = tk.Text(frame, width=12, font=("Segoe UI", 11), wrap="none")
            box.insert("1.0", "\n".join(map(str, shell.session.statistics[i]))); box.pack(fill="both", expand=True); self.lists.append(box)
        self.output = tk.Text(self, height=10, state="disabled", font=("Consolas", 10)); self.output.pack(fill="x")

    def values(self, index: int) -> list[float]:
        text = self.lists[index].get("1.0", "end").replace(",", " ")
        values = [float(item) for item in text.split()]; self.shell.session.statistics[index] = values; return values

    def show(self, values: dict[str, float]) -> None:
        self.output.configure(state="normal"); self.output.delete("1.0", "end")
        self.output.insert("end", "\n".join(f"{key:>7} = {value:.10g}" for key, value in values.items())); self.output.configure(state="disabled")

    def summary(self) -> None:
        try: self.show(one_variable(self.values(0)))
        except ValueError as exc: messagebox.showerror("Statistics", str(exc), parent=self)

    def regression(self) -> None:
        try: self.show(linear_regression(self.values(0), self.values(1)))
        except ValueError as exc: messagebox.showerror("Statistics", str(exc), parent=self)

    def normal(self) -> None:
        value = simpledialog.askstring("Normal Distribution", "lower, upper, μ, σ:", initialvalue="-1,1,0,1", parent=self)
        if value:
            try:
                lower, upper, mean, sd = map(float, value.split(",")); self.show({"Normal CDF": normal_cdf(lower, upper, mean, sd), "PDF at upper": normal_pdf(upper, mean, sd)})
            except ValueError as exc: messagebox.showerror("Normal", str(exc), parent=self)

    def binomial(self) -> None:
        value = simpledialog.askstring("Binomial Distribution", "n, p, x:", initialvalue="10,0.5,3", parent=self)
        if value:
            try:
                n, p, x = value.split(","); self.show({"Binomial PD": binomial_pdf(int(n), float(p), int(x)), "Binomial CD": binomial_cdf(int(n), float(p), int(x))})
            except ValueError as exc: messagebox.showerror("Binomial", str(exc), parent=self)
