from __future__ import annotations

from dataclasses import dataclass
from tokenize import TokenError
from typing import Any

from .formatter import natural_text
from .models import HistoryEntry, Settings
from .parser import ClassPadSyntaxError, normalize, split_assignment, split_equation

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        convert_xor, factorial_notation, implicit_multiplication_application,
        parse_expr, standard_transformations,
    )
except ImportError as exc:  # pragma: no cover - friendly installed-app failure
    raise RuntimeError("Open ClassPad requires SymPy. Run: pip install -r requirements.txt") from exc


class CalculatorError(ValueError):
    pass


@dataclass(slots=True)
class Evaluation:
    expression: Any
    exact: Any
    decimal: Any


class ClassPadEngine:
    """Compatibility layer. No UI code may call SymPy directly."""

    def __init__(self, settings: Settings, variables: dict[str, str] | None = None) -> None:
        self.settings = settings
        self.variables = variables if variables is not None else {}
        self._transformations = standard_transformations + (
            convert_xor, factorial_notation, implicit_multiplication_application,
        )

    def _locals(self) -> dict[str, Any]:
        values: dict[str, Any] = {
            "E": sp.E, "I": sp.I, "pi": sp.pi, "oo": sp.oo,
            "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
            "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
            "sqrt": sp.sqrt, "log": sp.log, "exp": sp.exp, "abs": sp.Abs,
            "factorial": sp.factorial, "binomial": sp.binomial,
        }
        for name, value in self.variables.items():
            values[name] = self._parse(value, values)
        return values

    def _parse(self, source: str, local: dict[str, Any] | None = None) -> Any:
        try:
            return parse_expr(normalize(source), local_dict=local or self._locals(),
                              transformations=self._transformations, evaluate=True)
        except (TypeError, ValueError, SyntaxError, TokenError) as exc:
            raise ClassPadSyntaxError("Syntax ERROR") from exc

    def evaluate(self, source: str, approximate: bool = False) -> Evaluation:
        assignment = split_assignment(source)
        if assignment:
            name, value_source = assignment
            value = self._parse(value_source)
            self.variables[name] = str(value)
            exact = sp.simplify(value)
            return Evaluation(sp.Symbol(name), exact, sp.N(exact, self.settings.precision))
        equation = split_equation(source)
        expression = sp.Eq(self._parse(equation[0]), self._parse(equation[1])) if equation else self._parse(source)
        exact = expression if isinstance(expression, sp.Equality) else sp.simplify(expression)
        if exact.has(sp.zoo, sp.nan) or exact is sp.zoo:
            raise CalculatorError("Undefined")
        decimal = sp.N(exact, self.settings.precision)
        return Evaluation(expression, decimal if approximate else exact, decimal)

    def apply(self, command: str, source: str, **options: str) -> Evaluation:
        equation = split_equation(source)
        expression = sp.Eq(self._parse(equation[0]), self._parse(equation[1])) if equation else self._parse(source)
        variable = sp.Symbol(options.get("variable", "x"))
        try:
            operations = {
                "simplify": lambda: sp.simplify(expression),
                "expand": lambda: sp.expand(expression),
                "factor": lambda: sp.factor(expression),
                "apart": lambda: sp.apart(expression, variable),
                "differentiate": lambda: sp.diff(expression, variable, int(options.get("order", "1"))),
                "integrate": lambda: sp.integrate(expression, variable),
                "solve": lambda: sp.solve(expression, variable),
                "substitute": lambda: expression.subs(variable, self._parse(options["value"])),
                "approximate": lambda: sp.N(expression, self.settings.precision),
            }
            result = operations[command]()
        except KeyError as exc:
            raise CalculatorError("Command requires an option") from exc
        except (ValueError, TypeError, NotImplementedError) as exc:
            raise CalculatorError("Math ERROR") from exc
        return Evaluation(expression, result, sp.N(result, self.settings.precision) if not isinstance(result, list) else result)

    def history_entry(self, source: str, result: Evaluation, origin: str = "Main") -> HistoryEntry:
        return HistoryEntry(origin, source, natural_text(sp.sstr(result.exact)),
                            natural_text(sp.sstr(result.decimal)), sp.sstr(result.expression))
