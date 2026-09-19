from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog

from classpad.core.commands import COMMANDS
from classpad.core.engine import CalculatorError, ClassPadEngine
from classpad.core.parser import ClassPadSyntaxError
from classpad.ui.theme import BLUE, PANEL
from classpad.ui.widgets import HistoryView, SoftKeyboard


class MainApplication(tk.Frame):
    def __init__(self, master: tk.Misc, shell) -> None:
        super().__init__(master, bg=PANEL)
        self.shell = shell
        self.engine = ClassPadEngine(shell.session.settings, shell.session.variables)
        toolbar = tk.Frame(self, bg=PANEL)
        toolbar.pack(fill="x")
        for text, command in (("⌂", shell.show_launcher), ("↶", self.reuse), ("✂", self.clear),
                              ("x?", lambda: self.run_command("solve")), ("d/dx", lambda: self.run_command("differentiate")),
                              ("∫", lambda: self.run_command("integrate"))):
            tk.Button(toolbar, text=text, command=command, width=4, bg=PANEL).pack(side="left")
        self.history = HistoryView(self, self.put)
        self.history.pack(fill="both", expand=True)
        for item in shell.session.history:
            self.history.append(item.input_text, item.exact_text)
        entrybar = tk.Frame(self, bg=BLUE, padx=5, pady=5)
        entrybar.pack(fill="x")
        tk.Label(entrybar, text="▶", bg=BLUE, fg="white").pack(side="left")
        self.entry = tk.Entry(entrybar, font=("Cambria Math", 14), relief="flat")
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entry.bind("<Return>", lambda _: self.evaluate(False))
        tk.Button(entrybar, text="EXE", command=lambda: self.evaluate(False), bg="#f3a23a").pack(side="left")
        tk.Button(entrybar, text="≈", command=lambda: self.evaluate(True)).pack(side="left")
        self.keyboard = SoftKeyboard(self, self.insert, self.evaluate)
        self.keyboard.pack(fill="x", ipady=2)
        self.entry.focus_set()

    def selected(self) -> str:
        return self.history.selected_text or self.entry.get().strip()

    def insert(self, value: str) -> None:
        if value == "←": self.entry.delete(max(0, self.entry.index("insert") - 1))
        elif value == "CLR": self.entry.delete(0, "end")
        else: self.entry.insert("insert", value)
        self.entry.focus_set()

    def put(self, value: str) -> None:
        self.entry.delete(0, "end"); self.entry.insert(0, value); self.entry.focus_set()

    def reuse(self) -> None:
        if self.selected(): self.put(self.selected())

    def clear(self) -> None:
        self.shell.session.history.clear(); self.history.clear()

    def evaluate(self, approximate: bool = False) -> None:
        source = self.entry.get().strip()
        if not source: return
        try:
            result = self.engine.evaluate(source, approximate)
            item = self.engine.history_entry(source, result)
            self.shell.session.history.append(item)
            self.history.append(source, item.decimal_text if approximate else item.exact_text)
            self.entry.delete(0, "end"); self.shell.refresh_status()
        except (ClassPadSyntaxError, CalculatorError, TypeError, ValueError) as exc:
            messagebox.showerror("Calculation", str(exc), parent=self)

    def run_command(self, command: str) -> None:
        source = self.selected()
        if not source: return
        definition = COMMANDS[command]
        options = {}
        if definition.needs_variable:
            value = simpledialog.askstring(definition.label, "Variable:", initialvalue="x", parent=self)
            if not value: return
            options["variable"] = value
        if definition.needs_value:
            value = simpledialog.askstring(definition.label, "Substitute value:", parent=self)
            if value is None: return
            options["value"] = value
        try:
            result = self.engine.apply(command, source, **options)
            item = self.engine.history_entry(f"{definition.label}({source})", result, "Interactive")
            self.shell.session.history.append(item); self.history.append(item.input_text, item.exact_text)
        except (CalculatorError, ClassPadSyntaxError, ValueError, TypeError) as exc:
            messagebox.showerror(definition.label, str(exc), parent=self)
