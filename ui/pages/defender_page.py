"""Defender Page — hosts the DefenderPanel for configuring defender stats."""

import customtkinter

from state.app_state import AppState
from state.template_manager import TemplateManager
from ui.styles import BUTTON_HEIGHT, PAGE_PAD_X
from ui.widgets.defender_panel import DefenderPanel


class DefenderPage(customtkinter.CTkFrame):
    """Page for configuring defender unit stats.

    Hosts a DefenderPanel, a reset button, and a save-to-template button.
    """

    def __init__(self, master, state: AppState, template_manager: TemplateManager = None, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state
        self._tm = template_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Defender panel (scrollable form)
        self._panel = DefenderPanel(self, on_change=self._on_panel_change)
        self._panel.grid(row=0, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(PAGE_PAD_X, 4))

        # Bottom bar with buttons
        bottom_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        bottom_bar.grid(row=1, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(4, PAGE_PAD_X))

        self._save_template_btn = customtkinter.CTkButton(
            bottom_bar,
            text="Save as Template",
            command=self._save_as_template,
            height=BUTTON_HEIGHT,
        )
        self._save_template_btn.pack(side="left")

        self._reset_btn = customtkinter.CTkButton(
            bottom_bar,
            text="Reset",
            command=self._reset,
            height=BUTTON_HEIGHT,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
        )
        self._reset_btn.pack(side="left", padx=(8, 0))

        # Load current defender state into panel
        self._panel.set_values(self._state.defender)

        # Listen for external state changes
        self._state.subscribe(self._on_state_change)

    def _on_panel_change(self) -> None:
        """Sync panel values to state when user edits a field."""
        values = self._panel.get_values()
        self._state.update_defender(**values)

    def _save_as_template(self) -> None:
        """Save the current defender config as a template."""
        if not self._tm:
            return
        data = dict(self._state.defender)
        dialog = customtkinter.CTkInputDialog(
            text="Enter a name for this template:",
            title="Save Template",
        )
        name = dialog.get_input()
        if not name or not name.strip():
            return
        data["name"] = name.strip()
        self._tm.create_template(data)

    def _reset(self) -> None:
        """Reset the panel to defaults."""
        self._panel.reset()
        self._on_panel_change()

    def _on_state_change(self) -> None:
        """Called when state changes externally (e.g. undo). Refresh panel."""
        self._panel.set_values(self._state.defender)
