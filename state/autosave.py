"""Auto-save — persists and restores application state to/from JSON."""

import json
import os
from typing import Optional


class AutoSave:
    """Saves and loads application state to a local JSON file."""

    def __init__(self, filepath: str = ".warhammer_state.json"):
        self._filepath = filepath

    def save(self, state: dict) -> None:
        """Write state dict to the auto-save file as JSON."""
        try:
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except (OSError, TypeError):
            # Fail silently — auto-save is best-effort
            pass

    def load(self) -> Optional[dict]:
        """Load and return state from the auto-save file, or None on failure."""
        if not os.path.exists(self._filepath):
            return None
        try:
            with open(self._filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError, ValueError):
            return None
