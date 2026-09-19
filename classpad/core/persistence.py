from __future__ import annotations

import json
import os
from dataclasses import asdict
from pathlib import Path

from .models import HistoryEntry, Session, Settings


def default_state_path() -> Path:
    root = os.environ.get("APPDATA") or os.environ.get("XDG_CONFIG_HOME")
    folder = Path(root) / "OpenClassPad" if root else Path.home() / ".config" / "open-classpad"
    return folder / "session.json"


class SessionStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_state_path()

    def load(self) -> Session:
        if not self.path.exists():
            return Session()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            settings = Settings(**raw.get("settings", {}))
            history = [HistoryEntry.from_dict(item) for item in raw.get("history", [])]
            return Session(settings, raw.get("variables", {}), history,
                           raw.get("graphs", ["x^2-4", "", "", "", ""]),
                           raw.get("statistics", [[], [], []]))
        except (OSError, ValueError, TypeError):
            return Session()

    def save(self, session: Session) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(session)
        if not session.settings.persist_history:
            payload["history"] = []
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temporary.replace(self.path)
