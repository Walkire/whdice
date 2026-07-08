"""Defender Page — hosts the DefenderPanel for configuring defender stats."""

import customtkinter

from state.app_state import AppState
from ui.styles import BUTTON_HEIGHT, PAGE_PAD_X
from ui.widgets.defender_panel import DefenderPanel


class DefenderPage(customtkinter.CTkFrame):
    """Page for configuring defender unit stats.

    Hosts a DefenderPanel and a reset button.
    """

    def __init__(self, master, state: AppState, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Defender panel (scrollable form)
        self._panel = DefenderPanel(self, on_change=self._on_panel_change)
        self._panel.grid(row=0, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(PAGE_PAD_X, 4))

        # Bottom bar with reset button
        bottom_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        bottom_bar.grid(row=1, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(4, PAGE_PAD_X))

        self._reset_btn = customtkinter.CTkButton(
            bottom_bar,
            text="Reset",
            command=self._reset,
            height=BUTTON_HEIGHT,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
        )
        self._reset_btn.pack(side="left")

        # Load current defender state into panel
        self._panel.set_values(self._state.defender)

        # Listen for external state changes
        self._state.subscribe(self._on_state_change)

    def _on_panel_change(self) -> None:
        """Sync panel values to state when user edits a field."""
        values = self._panel.get_values()
        self._state.update_defender(**values)

    def _reset(self) -> None:
        """Reset the panel to defaults."""
        self._panel.reset()
        self._on_panel_change()

    def _on_state_change(self) -> None:
        """Called when state changes externally (e.g. undo). Refresh panel."""
        self._panel.set_values(self._state.defender)
