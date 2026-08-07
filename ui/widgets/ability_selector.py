"""AbilitySelector — grid of toggle buttons for weapon abilities."""

from typing import Callable, Dict, Optional
import customtkinter

from ui.styles import (
    COLOR_ABILITY_ACTIVE_BG, COLOR_ABILITY_ACTIVE_BORDER,
    COLOR_ABILITY_INACTIVE_BORDER, COLOR_NAV_HOVER,
)


ABILITIES = [
    "Torrent",
    "Blast",
    "Lethal Hits",
    "Devastating Wounds",
    "Sustained Hits",
    "Melta",
    "Ignore Cover",
    "Psychic",
]

# Map display names to state keys used in AppState weapon dicts
ABILITY_KEY_MAP = {
    "Torrent": "torrent",
    "Blast": "blast",
    "Lethal Hits": "lethal_hits",
    "Devastating Wounds": "devestating_wounds",
    "Sustained Hits": "sustained_hits_active",
    "Melta": "melta",
    "Ignore Cover": "ignore_cover",
    "Psychic": "psychic",
}


class AbilitySelector(customtkinter.CTkFrame):
    """Grid of toggle buttons for weapon abilities.

    Each ability can be toggled on/off. The component reports
    which abilities are active via get_active().
    """

    COLUMNS = 4  # Number of columns in the grid

    def __init__(self, master, on_change: Optional[Callable] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._on_change = on_change
        self._buttons: Dict[str, customtkinter.CTkButton] = {}
        self._states: Dict[str, bool] = {ability: False for ability in ABILITIES}

        # Section label
        label = customtkinter.CTkLabel(
            self, text="Abilities", font=customtkinter.CTkFont(weight="bold")
        )
        label.grid(row=0, column=0, columnspan=self.COLUMNS, pady=(4, 4), sticky="w")

        # Build toggle grid
        for idx, ability in enumerate(ABILITIES):
            row = (idx // self.COLUMNS) + 1
            col = idx % self.COLUMNS
            btn = customtkinter.CTkButton(
                self,
                text=ability,
                width=110,
                height=28,
                corner_radius=6,
                fg_color="transparent",
                border_width=1,
                border_color=COLOR_ABILITY_INACTIVE_BORDER,
                text_color=("gray10", "gray90"),
                hover_color=COLOR_NAV_HOVER,
                command=lambda a=ability: self._toggle(a),
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self._buttons[ability] = btn

    def _toggle(self, ability: str) -> None:
        """Toggle the given ability on/off and update visual state."""
        self._states[ability] = not self._states[ability]
        self._update_button_style(ability)
        if self._on_change:
            self._on_change()

    def _update_button_style(self, ability: str) -> None:
        """Apply active/inactive styling to a button."""
        btn = self._buttons[ability]
        if self._states[ability]:
            btn.configure(fg_color=COLOR_ABILITY_ACTIVE_BG, border_color=COLOR_ABILITY_ACTIVE_BORDER)
        else:
            btn.configure(fg_color="transparent", border_color=COLOR_ABILITY_INACTIVE_BORDER)

    def get_active(self) -> Dict[str, bool]:
        """Return a dict of ability_name -> active status for all abilities."""
        return dict(self._states)

    def set_active(self, abilities: Dict[str, bool]) -> None:
        """Set ability states from a dict. Keys not present are left unchanged."""
        for ability, active in abilities.items():
            if ability in self._states:
                self._states[ability] = active
                self._update_button_style(ability)
