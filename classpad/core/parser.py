from __future__ import annotations

import re


class ClassPadSyntaxError(ValueError):
    pass


FUNCTIONS = {
    "abs", "acos", "apart", "asin", "atan", "binomial", "ceiling", "collect",
    "conjugate", "cos", "det", "diff", "expand", "exp", "factor", "floor",
    "im", "integrate", "limit", "ln", "log", "nsolve", "re", "simplify",
    "sin", "solve", "sqrt", "subs", "sum", "tan", "together",
}


def _rewrite_combinatorics(text: str) -> str:
    atom = r"(?:\d+(?:\.\d+)?|[A-Za-z]\w*|\([^()]++\))"
    # Python's re has no possessive dependency here; the simple forms cover keypad use.
    atom = r"(?:\d+(?:\.\d+)?|[A-Za-z]\w*|\([^()]+\))"
    text = re.sub(rf"({atom})\s*C\s*({atom})", r"binomial(\1,\2)", text)
    text = re.sub(rf"({atom})\s*P\s*({atom})", r"factorial(\1)/factorial((\1)-(\2))", text)
    return text


def normalize(source: str) -> str:
    """Translate calculator notation into a restricted SymPy-readable expression."""
    if len(source) > 1000:
        raise ClassPadSyntaxError("Expression is too long")
    text = source.strip().replace("×", "*").replace("÷", "/").replace("−", "-")
    text = text.replace("π", "pi").replace("√", "sqrt").replace("^", "**")
    text = re.sub(r"\bln\s*\(", "log(", text, flags=re.I)
    text = _rewrite_combinatorics(text)
    # e followed by a power is the exponential constant, not a variable name.
    text = re.sub(r"(?<![A-Za-z_])e\s*\*\*", "E**", text)
    text = re.sub(r"\bi\b", "I", text)
    # Insert multiplication at token boundaries. Function-name + '(' is excluded.
    text = re.sub(r"(?<=[0-9)])(?=[A-Za-z(])", "*", text)
    text = re.sub(r"(?<=[A-Za-z)])(?=\d)", "*", text)
    text = re.sub(r"(?<=\))(?=[A-Za-z(])", "*", text)
    text = re.sub(r"\b([A-Za-z_]\w*)\s*\(",
                  lambda m: m.group(0) if m.group(1).lower() in FUNCTIONS or m.group(1) == "factorial" else m.group(1) + "*(",
                  text)
    if "__" in text or re.search(r"[\[\]{};'\"\\:]", text):
        raise ClassPadSyntaxError("Unsupported syntax")
    if not re.fullmatch(r"[A-Za-z0-9_+\-*/().,=<>\s]*", text):
        raise ClassPadSyntaxError("Unsupported character")
    return text


def split_assignment(source: str) -> tuple[str, str] | None:
    if ":=" not in source:
        return None
    name, value = (part.strip() for part in source.split(":=", 1))
    if not re.fullmatch(r"[A-Za-z]\w*", name):
        raise ClassPadSyntaxError("Invalid variable name")
    return name, value


def split_equation(source: str) -> tuple[str, str] | None:
    if "=" not in source or ":=" in source:
        return None
    parts = source.split("=")
    if len(parts) != 2:
        raise ClassPadSyntaxError("Equation must have two sides")
    return parts[0].strip(), parts[1].strip()
