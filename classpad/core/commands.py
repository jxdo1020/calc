from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Command:
    key: str
    label: str
    category: str
    needs_variable: bool = False
    needs_value: bool = False


COMMANDS = {
    item.key: item for item in (
        Command("simplify", "Simplify", "Transformation"),
        Command("expand", "Expand", "Transformation"),
        Command("factor", "Factor", "Transformation"),
        Command("apart", "Partial Fraction", "Transformation", True),
        Command("solve", "Solve", "Equation/Inequality", True),
        Command("differentiate", "Differentiate", "Calculation", True),
        Command("integrate", "Integrate", "Calculation", True),
        Command("substitute", "Substitute", "Calculation", True, True),
        Command("approximate", "Approximate", "Calculation"),
    )
}
