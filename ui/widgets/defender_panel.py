"""DefenderPanel — scrollable composite widget for defender configuration."""

from typing import Callable, Dict, Optional
import customtkinter

from enums import RerollType, MinusDamageType, MinusWoundType
from state.app_state import DEFENDER_DEFAULTS
from ui.widgets.stat_row import StatRow
from ui.widgets.keyword_selector import KeywordSelector


# Option lists from enums
REROLL_SAVE_OPTIONS = [e.value for e in RerollType if e != RerollType.FISH_ROLLS]
MINUS_DAMAGE_OPTIONS = [e.value for e in MinusDamageType]
MINUS_WOUND_OPTIONS = [e.value for e in MinusWoundType]


class DefenderPanel(customtkinter.CTkScrollableFrame):
    """Composite widget containing all defender configuration inputs.

    Composes StatRows for core defensive stats and a KeywordSelector
    for damage/wound reduction and reroll dropdowns.
    """

    def __init__(self, master, on_change: Optional[Callable] = None, **kwargs):
        super().__init__(master, **kwargs)

        self._on_change = on_change
        self._suppress_change = False  # Suppress callbacks during set_values
        self._stat_rows: Dict[str, StatRow] = {}

        def _guarded_change():
            if not self._suppress_change and self._on_change:
                self._on_change()

        # --- Core Stats Section ---
        stats_label = customtkinter.CTkLabel(
            self, text="Defensive Stats", font=customtkinter.CTkFont(weight="bold")
        )
        stats_label.pack(anchor="w", padx=4, pady=(8, 4))

        core_stats = [
            ("model_count", "Model Count:", "entry", None, DEFENDER_DEFAULTS["model_count"]),
            ("toughness", "Toughness:", "entry", None, DEFENDER_DEFAULTS["toughness"]),
            ("save", "Save:", "entry", None, DEFENDER_DEFAULTS["save"]),
            ("invuln", "Invuln:", "entry", None, DEFENDER_DEFAULTS["invuln"]),
            ("wounds", "Wounds:", "entry", None, DEFENDER_DEFAULTS["wounds"]),
            ("feel_no_pain", "Feel No Pain:", "entry", None, DEFENDER_DEFAULTS["feel_no_pain"]),
        ]

        for key, label, wtype, options, default in core_stats:
            row = StatRow(self, label=label, widget_type=wtype, options=options, default=default, on_change=_guarded_change)
            row.pack(fill="x", padx=4, pady=2)
            self._stat_rows[key] = row

        # --- Keywords / Modifiers Section ---
        keywords = {
            "Damage Reduction": MINUS_DAMAGE_OPTIONS,
            "Wound Reduction": MINUS_WOUND_OPTIONS,
            "Reroll Save": REROLL_SAVE_OPTIONS,
        }
        self._keyword_selector = KeywordSelector(self, keywords=keywords, on_change=_guarded_change)
        self._keyword_selector.pack(fill="x", padx=4, pady=(12, 4))

        # --- Modifier Checkboxes ---
        mod_label = customtkinter.CTkLabel(
            self, text="Modifiers", font=customtkinter.CTkFont(weight="bold")
        )
        mod_label.pack(anchor="w", padx=4, pady=(12, 4))

        modifier_checks = [
            ("plus_save", "+1 Save", DEFENDER_DEFAULTS["plus_save"]),
            ("cover", "Cover or Stealth", DEFENDER_DEFAULTS["cover"]),
            ("minus_hit", "-1 to Hit", DEFENDER_DEFAULTS["minus_hit"]),
        ]
        for key, label, default in modifier_checks:
            row = StatRow(self, label=label, widget_type="checkbox", default=default, on_change=_guarded_change)
            row.pack(fill="x", padx=4, pady=2)
            self._stat_rows[key] = row

    def get_values(self) -> Dict:
        """Return all defender config values as a plain dict."""
        values = {}

        # Core stats
        for key, row in self._stat_rows.items():
            values[key] = row.get_value()

        # Convert numeric fields
        for int_key in ("model_count", "toughness", "save", "invuln", "wounds", "feel_no_pain"):
            try:
                values[int_key] = int(values[int_key])
            except (ValueError, TypeError):
                values[int_key] = DEFENDER_DEFAULTS[int_key]

        # Boolean fields from checkboxes
        for bool_key in ("plus_save", "cover", "minus_hit"):
            values[bool_key] = bool(values.get(bool_key))

        # Keywords
        selections = self._keyword_selector.get_selections()
        values["minus_damage"] = selections.get("Damage Reduction", MinusDamageType.NO_MINUS.value)
        values["minus_wound"] = selections.get("Wound Reduction", MinusWoundType.NO_MINUS.value)
        values["reroll_save"] = selections.get("Reroll Save", RerollType.NO_REROLL.value)

        return values

    def set_values(self, values: Dict) -> None:
        """Populate the panel from a values dict."""
        self._suppress_change = True
        try:
            # Core stats
            for key, row in self._stat_rows.items():
                if key in values:
                    row.set_value(values[key])

            # Keywords
            keyword_map = {
                "Damage Reduction": values.get("minus_damage", MinusDamageType.NO_MINUS.value),
                "Wound Reduction": values.get("minus_wound", MinusWoundType.NO_MINUS.value),
                "Reroll Save": values.get("reroll_save", RerollType.NO_REROLL.value),
            }
            self._keyword_selector.set_selections(keyword_map)
        finally:
            self._suppress_change = False

    def reset(self) -> None:
        """Reset all inputs to default values."""
        self._suppress_change = True
        try:
            self.set_values(DEFENDER_DEFAULTS)
        finally:
            self._suppress_change = False
