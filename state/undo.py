"""Undo stack — stores state snapshots for undo support."""

import copy
from typing import Optional


class UndoStack:
    """Fixed-size stack of state snapshots."""

    def __init__(self, max_size: int = 50):
        self._stack: list = []
        self._max_size = max_size

    def push(self, snapshot: dict) -> None:
        """Push a deep copy of the snapshot onto the stack."""
        self._stack.append(copy.deepcopy(snapshot))
        if len(self._stack) > self._max_size:
            self._stack.pop(0)

    def pop(self) -> Optional[dict]:
        """Pop and return the most recent snapshot, or None if empty."""
        if self._stack:
            return self._stack.pop()
        return None

    def can_undo(self) -> bool:
        """Return True if there is at least one snapshot to restore."""
        return len(self._stack) > 0

    def clear(self) -> None:
        """Clear all snapshots."""
        self._stack.clear()

    def __len__(self) -> int:
        return len(self._stack)
