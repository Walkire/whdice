"""Settings Page — theme toggle and simulation count configuration."""

import customtkinter

from state.app_state import AppState


SIMULATION_COUNT_OPTIONS = ["10000", "50000", "100000", "250000", "500000"]


class SettingsPage(customtkinter.CTkFrame):
    """Page for application settings: theme toggle and simulation count.

    Requirements: 7.6
    """

    def __init__(self, master, state: AppState, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Title ---
        title = customtkinter.CTkLabel(
            self, text="Settings",
            font=customtkinter.CTkFont(size=18, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 12))

        # --- Settings form ---
        form = customtkinter.CTkFrame(self, fg_color="transparent")
        form.grid(row=1, column=0, sticky="nw", padx=16, pady=(0, 16))
        form.grid_columnconfigure(1, weight=1)

        # Theme toggle
        theme_label = customtkinter.CTkLabel(form, text="Appearance Mode:", anchor="w")
        theme_label.grid(row=0, column=0, padx=(0, 12), pady=8, sticky="w")

        self._theme_var = customtkinter.StringVar(
            value=customtkinter.get_appearance_mode()
        )
        self._theme_menu = customtkinter.CTkOptionMenu(
            form,
            variable=self._theme_var,
            values=["Dark", "Light", "System"],
            width=160,
            command=self._on_theme_change,
        )
        self._theme_menu.grid(row=0, column=1, pady=8, sticky="w")

        # Simulation count
        sim_label = customtkinter.CTkLabel(form, text="Simulation Count:", anchor="w")
        sim_label.grid(row=1, column=0, padx=(0, 12), pady=8, sticky="w")

        self._sim_count_var = customtkinter.StringVar(value="100000")
        self._sim_count_menu = customtkinter.CTkOptionMenu(
            form,
            variable=self._sim_count_var,
            values=SIMULATION_COUNT_OPTIONS,
            width=160,
            command=self._on_sim_count_change,
        )
        self._sim_count_menu.grid(row=1, column=1, pady=8, sticky="w")

    def _on_theme_change(self, value: str) -> None:
        """Apply the selected theme."""
        customtkinter.set_appearance_mode(value.lower())

    def _on_sim_count_change(self, value: str) -> None:
        """Store the selected simulation count in app state for other pages."""
        # Store as an attribute on state for results/graph pages to read
        try:
            self._state.simulation_count = int(value)
        except (ValueError, TypeError):
            self._state.simulation_count = 100000

    def get_simulation_count(self) -> int:
        """Return the currently configured simulation count."""
        try:
            return int(self._sim_count_var.get())
        except (ValueError, TypeError):
            return 100000
