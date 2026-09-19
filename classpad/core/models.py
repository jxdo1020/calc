from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(slots=True)
class Settings:
    calculation_mode: str = "Standard"
    angle_mode: str = "Rad"
    complex_mode: str = "Real"
    precision: int = 10
    persist_history: bool = True
    axes: bool = True
    grid: bool = True
    xmin: float = -7.7
    xmax: float = 7.7
    xscale: float = 1.0
    ymin: float = -5.2
    ymax: float = 5.2
    yscale: float = 1.0


@dataclass(slots=True)
class HistoryEntry:
    source: str
    input_text: str
    exact_text: str
    decimal_text: str
    expression_text: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "HistoryEntry":
        fields = {key: value[key] for key in cls.__dataclass_fields__ if key in value}
        return cls(**fields)


@dataclass(slots=True)
class Session:
    settings: Settings = field(default_factory=Settings)
    variables: dict[str, str] = field(default_factory=dict)
    history: list[HistoryEntry] = field(default_factory=list)
    graphs: list[str] = field(default_factory=lambda: ["x^2-4", "", "", "", ""])
    statistics: list[list[float]] = field(default_factory=lambda: [[], [], []])
