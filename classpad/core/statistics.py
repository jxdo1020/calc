from __future__ import annotations

import math
from statistics import mean, median, pstdev, stdev


def _quartiles(values: list[float]) -> tuple[float, float, float]:
    ordered = sorted(values)
    middle = len(ordered) // 2
    lower = ordered[:middle]
    upper = ordered[middle + (len(ordered) % 2):]
    return median(lower) if lower else ordered[0], median(ordered), median(upper) if upper else ordered[-1]


def one_variable(values: list[float]) -> dict[str, float]:
    if not values:
        raise ValueError("Data list is empty")
    q1, med, q3 = _quartiles(values)
    return {"n": float(len(values)), "mean": mean(values), "sum": sum(values),
            "sum²": sum(value * value for value in values), "σx": pstdev(values),
            "sx": stdev(values) if len(values) > 1 else math.nan,
            "min": min(values), "Q1": q1, "Med": med, "Q3": q3, "max": max(values)}


def linear_regression(xs: list[float], ys: list[float]) -> dict[str, float]:
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("Paired lists must have the same length")
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if not sxx or not syy:
        raise ValueError("Regression is undefined")
    a = sxy / sxx
    return {"a": a, "b": my - a * mx, "r": sxy / math.sqrt(sxx * syy)}


def normal_pdf(x: float, mean_value: float = 0, sd: float = 1) -> float:
    if sd <= 0:
        raise ValueError("Standard deviation must be positive")
    z = (x - mean_value) / sd
    return math.exp(-z * z / 2) / (sd * math.sqrt(2 * math.pi))


def normal_cdf(lower: float, upper: float, mean_value: float = 0, sd: float = 1) -> float:
    if sd <= 0:
        raise ValueError("Standard deviation must be positive")
    cdf = lambda x: 0.5 * (1 + math.erf((x - mean_value) / (sd * math.sqrt(2))))
    return cdf(upper) - cdf(lower)


def inverse_normal(probability: float, mean_value: float = 0, sd: float = 1) -> float:
    if not 0 < probability < 1 or sd <= 0:
        raise ValueError("Probability must be between zero and one")
    low, high = mean_value - 12 * sd, mean_value + 12 * sd
    for _ in range(100):
        mid = (low + high) / 2
        p = 0.5 * (1 + math.erf((mid - mean_value) / (sd * math.sqrt(2))))
        if p < probability:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def binomial_pdf(n: int, p: float, x: int) -> float:
    if n < 0 or not 0 <= p <= 1 or not 0 <= x <= n:
        raise ValueError("Invalid binomial parameters")
    return math.comb(n, x) * p ** x * (1 - p) ** (n - x)


def binomial_cdf(n: int, p: float, x: int) -> float:
    return sum(binomial_pdf(n, p, k) for k in range(0, min(x, n) + 1))
