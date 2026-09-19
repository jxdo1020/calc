from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from classpad.core.engine import ClassPadEngine
from classpad.core.parser import ClassPadSyntaxError
from classpad.ui.theme import PANEL


class NumericSolverApplication(tk.Frame):
    def __init__(self, master: tk.Misc, shell) -> None:
        super().__init__(master, bg=PANEL); self.shell = shell
        tk.Button(self, text="⌂", command=shell.show_launcher).grid(row=0, column=0, sticky="w")
        fields = (("Equation", "2.5=5e^(-0.0173x)"), ("Variable", "x"), ("Initial value", "1"))
        self.entries = []
        for row, (label, value) in enumerate(fields, 1):
            tk.Label(self, text=label, bg=PANEL).grid(row=row, column=0, sticky="e", padx=8, pady=8)
            entry = tk.Entry(self, font=("Cambria Math", 13)); entry.insert(0, value); entry.grid(row=row, column=1, sticky="ew"); self.entries.append(entry)
        tk.Button(self, text="Solve", command=self.solve, bg="#f3a23a").grid(row=4, column=1, sticky="ew", pady=10)
        self.result = tk.Label(self, text="", bg="white", font=("Cambria Math", 16), anchor="w"); self.result.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=8)
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(5, weight=1)

    def solve(self) -> None:
        try:
            import sympy as sp
            from classpad.core.parser import normalize, split_equation
            equation, variable, initial = (entry.get() for entry in self.entries); sides = split_equation(equation)
            if not sides: raise ValueError("Enter an equation")
            symbol = sp.Symbol(variable); expression = sp.sympify(normalize(sides[0]), locals={variable:symbol}) - sp.sympify(normalize(sides[1]), locals={variable:symbol})
            solution = sp.nsolve(expression, symbol, float(initial)); residual = abs(float(expression.subs(symbol, solution)))
            self.result.configure(text=f"{variable} = {solution:.12g}\nresidual = {residual:.3g}")
        except Exception as exc: messagebox.showerror("Numeric Solver", f"No Solution\n{exc}", parent=self)


class MatrixApplication(tk.Frame):
    def __init__(self, master: tk.Misc, shell) -> None:
        super().__init__(master, bg=PANEL); self.shell = shell
        bar = tk.Frame(self, bg=PANEL); bar.pack(fill="x")
        tk.Button(bar, text="⌂", command=shell.show_launcher).pack(side="left")
        for label, fn in (("det", self.det), ("inverse", self.inverse), ("transpose", self.transpose)):
            tk.Button(bar, text=label, command=fn).pack(side="left")
        tk.Label(self, text="Mat A  (one row per line; entries separated by spaces)", bg=PANEL).pack(anchor="w")
        self.editor = tk.Text(self, height=8, font=("Consolas", 14)); self.editor.insert("1.0", "1 2\n3 4"); self.editor.pack(fill="both", expand=True)
        self.output = tk.Label(self, text="", bg="white", font=("Cambria Math", 14), justify="left"); self.output.pack(fill="both", expand=True)

    def matrix(self):
        import sympy as sp
        return sp.Matrix([[sp.sympify(cell) for cell in row.split()] for row in self.editor.get("1.0", "end").splitlines() if row.strip()])

    def run(self, operation) -> None:
        try: self.output.configure(text=str(operation(self.matrix())))
        except Exception as exc: messagebox.showerror("Dimension ERROR", str(exc), parent=self)
    def det(self): self.run(lambda matrix: matrix.det())
    def inverse(self): self.run(lambda matrix: matrix.inv())
    def transpose(self): self.run(lambda matrix: matrix.T)


class SystemApplication(tk.Frame):
    def __init__(self, master: tk.Misc, shell) -> None:
        super().__init__(master, bg=PANEL); self.shell = shell; settings = shell.session.settings
        tk.Button(self, text="⌂", command=shell.show_launcher).pack(anchor="w")
        tk.Label(self, text="System", bg=PANEL, font=("Segoe UI", 17, "bold")).pack(pady=12)
        self.mode = tk.StringVar(value=settings.calculation_mode); self.angle = tk.StringVar(value=settings.angle_mode); self.complex = tk.StringVar(value=settings.complex_mode)
        self.selector("Calculation", self.mode, ("Standard", "Decimal")); self.selector("Angle", self.angle, ("Rad", "Deg", "Gra")); self.selector("Complex", self.complex, ("Real", "Complex"))
        tk.Button(self, text="Apply", command=self.apply, bg="#f3a23a").pack(fill="x", padx=35, pady=20)

    def selector(self, label, variable, values):
        frame = tk.LabelFrame(self, text=label, bg=PANEL); frame.pack(fill="x", padx=25, pady=6)
        for value in values: tk.Radiobutton(frame, text=value, variable=variable, value=value, bg=PANEL).pack(side="left", expand=True)

    def apply(self):
        s = self.shell.session.settings; s.calculation_mode = self.mode.get(); s.angle_mode = self.angle.get(); s.complex_mode = self.complex.get(); self.shell.refresh_status(); self.shell.store.save(self.shell.session)
