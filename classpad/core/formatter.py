from __future__ import annotations

import re


SUPERSCRIPTS = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def natural_text(text: str) -> str:
    """Produce a compact copyable display form without leaking Python notation."""
    text = str(text).replace("**", "^").replace("sqrt", "√").replace("pi", "π")
    text = re.sub(r"\^\((-?\d+)\)", lambda m: m.group(1).translate(SUPERSCRIPTS), text)
    text = re.sub(r"\^(-?\d+)", lambda m: m.group(1).translate(SUPERSCRIPTS), text)
    text = text.replace("*", "·").replace("I", "i").replace("oo", "∞")
    return text
