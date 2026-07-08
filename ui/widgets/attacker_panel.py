"""AttackerPanel — scrollable composite widget for attacker configuration."""

from typing import Callable, Dict, Optional
import customtkinter

from enums import RerollType
from state.app_state import ATTACKER_DEFAULTS
from ui.widgets.stat_row import StatRow
from ui.widgets.ability_selector import AbilitySelector
from ui.widgets.keyword_selector import KeywordSelector


# Reroll options as plain string lists
REROLL_OPTIONS = [e.value for e in RerollType]


class AttackerPanel(customtkinter.CTkScrollableFrame):
    """Composite widget containing all attacker configuration inputs.

    Composes StatRows for core stats, an AbilitySelector for toggles,
    and a KeywordSelector for reroll dropdowns.
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
            self, text="Core Stats", font=customtkinter.CTkFont(weight="bold")
        )
        stats_label.pack(anchor="w", padx=4, pady=(8, 4))

        core_stats = [
            ("name", "Name:", "entry", None, ATTACKER_DEFAULTS["name"]),
            ("attacks", "Attacks:", "entry", None, ATTACKER_DEFAULTS["attacks"]),
            ("score", "BS/WS:", "entry", None, ATTACKER_DEFAULTS["score"]),
            ("strength", "Strength:", "entry", None, ATTACKER_DEFAULTS["strength"]),
            ("ap", "AP:", "entry", None, ATTACKER_DEFAULTS["ap"]),
            ("damage", "Damage:", "entry", None, ATTACKER_DEFAULTS["damage"]),
            ("critical_hit", "Critical Hit:", "entry", None, ATTACKER_DEFAULTS["critical_hit"]),
            ("critical_wound", "Critical Wound:", "entry", None, ATTACKER_DEFAULTS["critical_wound"]),
            ("melta_value", "Melta Value:", "entry", None, ATTACKER_DEFAULTS["melta_value"]),
            ("sustained_hits", "Sustained Hits:", "entry", None, ATTACKER_DEFAULTS["sustained_hits"]),
        ]

        for key, label, wtype, options, default in core_stats:
            row = StatRow(self, label=label, widget_type=wtype, options=options, default=default, on_change=_guarded_change)
            row.pack(fill="x", padx=4, pady=2)
            self._stat_rows[key] = row

        # --- Abilities Section ---
        self._ability_selector = AbilitySelector(self, on_change=_guarded_change)
        self._ability_selector.pack(fill="x", padx=4, pady=(12, 4))

        # --- Keywords / Rerolls Section ---
        keywords = {
            "Reroll Hits": REROLL_OPTIONS,
            "Reroll Wounds": REROLL_OPTIONS,
            "Reroll Damage": REROLL_OPTIONS,
        }
        self._keyword_selector = KeywordSelector(self, keywords=keywords, on_change=_guarded_change)
        self._keyword_selector.pack(fill="x", padx=4, pady=(12, 4))

        # --- Additional Modifiers (checkboxes) ---
        mod_label = customtkinter.CTkLabel(
            self, text="Modifiers", font=customtkinter.CTkFont(weight="bold")
        )
        mod_label.pack(anchor="w", padx=4, pady=(12, 4))

        modifier_checks = [
            ("plus_hit", "+1 to Hit", ATTACKER_DEFAULTS["plus_hit"]),
            ("plus_wound", "+1 to Wound", ATTACKER_DEFAULTS["plus_wound"]),
        ]
        for key, label, default in modifier_checks:
            row = StatRow(self, label=label, widget_type="checkbox", default=default, on_change=_guarded_change)
            row.pack(fill="x", padx=4, pady=2)
            self._stat_rows[key] = row

    def get_values(self) -> Dict:
        """Return all attacker config values as a plain dict."""
        values = {}

        # Core stats
        for key, row in self._stat_rows.items():
            values[key] = row.get_value()

        # Convert numeric fields
        for int_key in ("score", "strength", "ap", "critical_hit", "critical_wound"):
            try:
                val = values[int_key]
                if val == "" or val is None:
                    values[int_key] = ATTACKER_DEFAULTS[int_key]
                else:
                    values[int_key] = int(val)
            except (ValueError, TypeError):
                values[int_key] = ATTACKER_DEFAULTS[int_key]

        # Boolean fields from checkboxes
        for bool_key in ("plus_hit", "plus_wound"):
            values[bool_key] = bool(values.get(bool_key))

        # String fields that should default to "0" when empty
        for str_key in ("attacks", "damage", "sustained_hits", "melta_value"):
            val = values.get(str_key, "")
            if val == "" or val is None:
                values[str_key] = ATTACKER_DEFAULTS[str_key]

        # Abilities
        abilities = self._ability_selector.get_active()
        values["torrent"] = abilities.get("Torrent", False)
        values["blast"] = abilities.get("Blast", False)
        values["lethal_hits"] = abilities.get("Lethal Hits", False)
        values["devestating_wounds"] = abilities.get("Devastating Wounds", False)
        values["melta"] = abilities.get("Melta", False)
        values["ignore_cover"] = abilities.get("Ignore Cover", False)
        values["psychic"] = abilities.get("Psychic", False)

        # Keywords (rerolls)
        selections = self._keyword_selector.get_selections()
        values["reroll_hits"] = selections.get("Reroll Hits", RerollType.NO_REROLL.value)
        values["reroll_wounds"] = selections.get("Reroll Wounds", RerollType.NO_REROLL.value)
        values["reroll_damage"] = selections.get("Reroll Damage", RerollType.NO_REROLL.value)

        return values

    def set_values(self, values: Dict) -> None:
        """Populate the panel from a values dict."""
        self._suppress_change = True
        try:
            # Core stats
            for key, row in self._stat_rows.items():
                if key in values:
                    row.set_value(values[key])

            # Abilities
            ability_map = {
                "Torrent": values.get("torrent", False),
                "Blast": values.get("blast", False),
                "Lethal Hits": values.get("lethal_hits", False),
                "Devastating Wounds": values.get("devestating_wounds", False),
                "Melta": values.get("melta", False),
                "Ignore Cover": values.get("ignore_cover", False),
                "Psychic": values.get("psychic", False),
            }
            self._ability_selector.set_active(ability_map)

            # Keywords
            keyword_map = {
                "Reroll Hits": values.get("reroll_hits", RerollType.NO_REROLL.value),
                "Reroll Wounds": values.get("reroll_wounds", RerollType.NO_REROLL.value),
                "Reroll Damage": values.get("reroll_damage", RerollType.NO_REROLL.value),
            }
            self._keyword_selector.set_selections(keyword_map)
        finally:
            self._suppress_change = False

    def reset(self) -> None:
        """Reset all inputs to default values."""
        self._suppress_change = True
        try:
            self.set_values(ATTACKER_DEFAULTS)
        finally:
            self._suppress_change = False
