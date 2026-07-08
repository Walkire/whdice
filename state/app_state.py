"""Central application state — no Tkinter dependencies."""

import copy
from typing import Callable, List, Optional

from enums import RerollType

ATTACKER_DEFAULTS = {
    "name": "",
    "attacks": "6",
    "score": 3,
    "strength": 5,
    "ap": 1,
    "damage": "2",
    "critical_hit": 6,
    "critical_wound": 6,
    "torrent": False,
    "reroll_hits": RerollType.NO_REROLL.value,
    "reroll_wounds": RerollType.NO_REROLL.value,
    "reroll_damage": RerollType.NO_REROLL.value,
    "sustained_hits": "0",
    "lethal_hits": False,
    "devestating_wounds": False,
    "blast": False,
    "ignore_cover": False,
    "plus_wound": False,
    "plus_hit": False,
    "melta": False,
    "melta_value": "2",
    "psychic": False,
}

DEFENDER_DEFAULTS = {
    "toughness": 3,
    "save": 5,
    "invuln": 0,
    "wounds": 1,
    "feel_no_pain": 0,
    "model_count": 10,
    "minus_damage": "None",
    "minus_wound": "None",
    "reroll_save": RerollType.NO_REROLL.value,
    "plus_save": False,
    "cover": False,
    "minus_hit": False,
}


class AppState:
    """Central state manager. All values are plain Python types."""

    def __init__(self):
        self.attacker: dict = {**ATTACKER_DEFAULTS}
        self.defender: dict = {**DEFENDER_DEFAULTS}
        self.weapons: List[dict] = []
        self.results: Optional[list] = None
        self._listeners: List[Callable] = []
        self._undo_stack = None  # Set externally via set_undo_stack
        self._notifying: bool = False  # Re-entrancy guard

    # --- Undo support ---

    def set_undo_stack(self, undo_stack) -> None:
        """Attach an UndoStack instance for automatic snapshot on mutations."""
        self._undo_stack = undo_stack

    def _push_undo(self) -> None:
        """Push current state onto undo stack before a mutation."""
        if self._notifying:
            return  # Don't push undo for changes triggered by notify/restore
        if self._undo_stack is not None:
            self._undo_stack.push(self.snapshot())

    # --- Subscriptions ---

    def subscribe(self, listener: Callable) -> None:
        """Register a callback invoked on every state change."""
        self._listeners.append(listener)

    def _notify(self) -> None:
        if self._notifying:
            return  # Prevent re-entrant notifications
        self._notifying = True
        try:
            for listener in self._listeners:
                listener()
        finally:
            self._notifying = False

    # --- Attacker ---

    def update_attacker(self, **kwargs) -> None:
        """Update attacker fields. Only known keys are applied."""
        if self._notifying:
            return  # Ignore updates triggered by notification callbacks
        self._push_undo()
        for key, value in kwargs.items():
            if key in self.attacker:
                self.attacker[key] = value
        self._notify()

    # --- Defender ---

    def update_defender(self, **kwargs) -> None:
        """Update defender fields. Only known keys are applied."""
        if self._notifying:
            return  # Ignore updates triggered by notification callbacks
        self._push_undo()
        for key, value in kwargs.items():
            if key in self.defender:
                self.defender[key] = value
        self._notify()

    # --- Weapons ---

    def add_weapon(self, weapon: dict) -> None:
        """Append a weapon to the list."""
        self._push_undo()
        self.weapons.append(copy.deepcopy(weapon))
        self._notify()

    def remove_weapon(self, index: int) -> None:
        """Remove weapon at the given index."""
        if 0 <= index < len(self.weapons):
            self._push_undo()
            self.weapons.pop(index)
            self._notify()

    def reorder_weapons(self, from_idx: int, to_idx: int) -> None:
        """Move weapon from from_idx to to_idx."""
        if from_idx == to_idx:
            return
        if not (0 <= from_idx < len(self.weapons)):
            return
        if not (0 <= to_idx < len(self.weapons)):
            return
        self._push_undo()
        weapon = self.weapons.pop(from_idx)
        self.weapons.insert(to_idx, weapon)
        self._notify()

    def duplicate_weapon(self, index: int) -> None:
        """Duplicate the weapon at the given index, inserting the copy after it."""
        if 0 <= index < len(self.weapons):
            self._push_undo()
            weapon_copy = copy.deepcopy(self.weapons[index])
            self.weapons.insert(index + 1, weapon_copy)
            self._notify()

    # --- Snapshot (for undo/autosave) ---

    def snapshot(self) -> dict:
        """Return a deep copy of the current state."""
        return {
            "attacker": copy.deepcopy(self.attacker),
            "defender": copy.deepcopy(self.defender),
            "weapons": copy.deepcopy(self.weapons),
        }

    def restore(self, snapshot: dict) -> None:
        """Restore state from a snapshot dict."""
        self.attacker = copy.deepcopy(snapshot.get("attacker", {**ATTACKER_DEFAULTS}))
        self.defender = copy.deepcopy(snapshot.get("defender", {**DEFENDER_DEFAULTS}))
        self.weapons = copy.deepcopy(snapshot.get("weapons", []))
        self._notify()
