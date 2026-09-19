from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True)
class Point:
    x: float
    y: float


def sample_function(function: Callable[[float], float], xmin: float, xmax: float,
                    count: int = 800, jump_limit: float = 100.0) -> list[list[Point]]:
    """Sample into drawable segments, breaking domains and asymptote jumps."""
    segments: list[list[Point]] = [[]]
    step = (xmax - xmin) / max(1, count - 1)
    previous: Point | None = None
    for index in range(count):
        x = xmin + index * step
        try:
            y = float(function(x))
            if not math.isfinite(y):
                raise ValueError
            point = Point(x, y)
            if previous and abs(y - previous.y) > jump_limit:
                segments.append([])
            segments[-1].append(point)
            previous = point
        except (ArithmeticError, ValueError, TypeError, OverflowError):
            if segments[-1]:
                segments.append([])
            previous = None
    return [segment for segment in segments if len(segment) > 1]


def roots(function: Callable[[float], float], xmin: float, xmax: float, samples: int = 1200) -> list[float]:
    found: list[float] = []
    dx = (xmax - xmin) / samples
    x0 = xmin
    try:
        y0 = function(x0)
    except Exception:
        y0 = math.nan
    for index in range(1, samples + 1):
        x1 = xmin + index * dx
        try:
            y1 = function(x1)
            if math.isfinite(y0) and math.isfinite(y1) and y0 * y1 <= 0:
                left, right = x0, x1
                for _ in range(45):
                    middle = (left + right) / 2
                    ym = function(middle)
                    if function(left) * ym <= 0:
                        right = middle
                    else:
                        left = middle
                root = (left + right) / 2
                if not found or abs(root - found[-1]) > dx * 2:
                    found.append(root)
            y0 = y1
        except Exception:
            y0 = math.nan
        x0 = x1
    return found
