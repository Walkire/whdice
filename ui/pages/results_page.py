"""Results Page — run simulation and display results in a table with progress bar."""

import threading
import tkinter as tk

import customtkinter

from classes.data import Data
from simulation import simulate
from state.app_state import AppState
from ui.styles import FONT_TITLE, FONT_BODY, BUTTON_HEIGHT, PAGE_PAD_X


SIMULATIONS = 100000


class ResultsPage(customtkinter.CTkFrame):
    """Page for running simulations and viewing per-weapon result breakdowns.

    Displays a run button, progress bar, results table, and wipe percentage.
    """

    def __init__(self, master, state: AppState, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state
        self._running = False
        self._last_results = None
        self._last_wipe = 0.0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(4, weight=1)

        # Top bar with Run button
        top_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(PAGE_PAD_X, 4))

        title = customtkinter.CTkLabel(
            top_bar, text="Simulation Results",
            font=customtkinter.CTkFont(size=FONT_TITLE[1], weight=FONT_TITLE[2])
        )
        title.pack(side="left")

        self._run_btn = customtkinter.CTkButton(
            top_bar,
            text="Run Simulation",
            command=self._run_simulation,
            height=BUTTON_HEIGHT,
        )
        self._run_btn.pack(side="right")

        # Progress bar
        self._progress = customtkinter.CTkProgressBar(self)
        self._progress.grid(row=1, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(4, 8))
        self._progress.set(0)

        # Results area — using a Tkinter Treeview for tabular data
        self._tree_frame = customtkinter.CTkFrame(self)
        self._tree_frame.grid(row=2, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(0, 4))
        self._tree_frame.grid_columnconfigure(0, weight=1)
        self._tree_frame.grid_rowconfigure(0, weight=1)

        columns = ("weapon", "attacks", "hits", "wounds", "saves", "damage", "fnp", "kills")
        self._tree = tk.ttk.Treeview(
            self._tree_frame, columns=columns, show="headings", height=15
        )

        # Configure columns
        col_headings = {
            "weapon": "Weapon",
            "attacks": "Attacks",
            "hits": "Hits",
            "wounds": "Wounds",
            "saves": "Failed Saves",
            "damage": "Damage",
            "fnp": "After FNP",
            "kills": "Kills",
        }
        for col, heading in col_headings.items():
            self._tree.heading(col, text=heading)
            width = 140 if col == "weapon" else 90
            self._tree.column(col, width=width, minwidth=60, anchor="center", stretch=True)

        self._tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for treeview
        scrollbar = tk.ttk.Scrollbar(self._tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Wipe percentage label
        self._wipe_label = customtkinter.CTkLabel(
            self, text="", font=customtkinter.CTkFont(size=FONT_BODY[1])
        )
        self._wipe_label.grid(row=3, column=0, sticky="w", padx=PAGE_PAD_X, pady=(4, 4))

        # Detail view — shows full breakdown when a weapon row is selected
        self._details = customtkinter.CTkTextbox(
            self, height=140, font=customtkinter.CTkFont(family="Consolas", size=12),
            state="disabled",
        )
        self._details.grid(row=4, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(0, PAGE_PAD_X))

        # Bind row selection
        self._tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _run_simulation(self) -> None:
        """Run the simulation in a background thread."""
        if self._running:
            return

        weapons = self._state.weapons
        if not weapons:
            self._wipe_label.configure(text="No weapons configured. Add weapons first.")
            return

        self._running = True
        self._run_btn.configure(state="disabled")
        self._progress.set(0)
        self._wipe_label.configure(text="Running simulation...")

        # Clear previous results
        for item in self._tree.get_children():
            self._tree.delete(item)

        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self._simulate_thread, daemon=True)
        thread.start()

    def _simulate_thread(self) -> None:
        """Execute the simulation (runs on background thread)."""
        try:
            # Convert state dicts to Data objects for the engine
            attacker_data = Data(**self._state.attacker)
            defender_data = Data(**self._state.defender)
            weapon_data_list = [Data(**w) for w in self._state.weapons]

            results, wipe_percent = simulate(
                attacker_data, defender_data, weapon_data_list, SIMULATIONS
            )

            # Schedule UI update on main thread
            self.after(0, lambda: self._display_results(results, wipe_percent))
        except Exception as e:
            self.after(0, lambda: self._display_error(str(e)))

    def _display_results(self, results: list, wipe_percent: float) -> None:
        """Populate the treeview with simulation results."""
        self._progress.set(1.0)
        self._running = False
        self._run_btn.configure(state="normal")

        # Store results for detail view and other pages
        self._last_results = results
        self._last_wipe = wipe_percent
        self._state.results = results

        for item in self._tree.get_children():
            self._tree.delete(item)

        sims = SIMULATIONS
        for i, r in enumerate(results):
            weapon = r.get("weapon")
            name = getattr(weapon, "name", None) or f"Weapon {r['id'] + 1}"
            self._tree.insert("", "end", iid=str(i), values=(
                name,
                f"{r['attacks'] / sims:.1f}",
                f"{r['hits'] / sims:.1f}",
                f"{r['wounds'] / sims:.1f}",
                f"{r['saves'] / sims:.1f}",
                f"{r['damage'] / sims:.1f}",
                f"{r['fnp'] / sims:.1f}",
                f"{r['kills'] / sims:.1f}",
            ))

        self._wipe_label.configure(text=f"Unit wiped: {wipe_percent}%")

        # Clear detail view
        self._details.configure(state="normal")
        self._details.delete("1.0", "end")
        self._details.insert("1.0", "Click a weapon row to see detailed breakdown.")
        self._details.configure(state="disabled")

    def _display_error(self, message: str) -> None:
        """Show an error message when simulation fails."""
        self._progress.set(0)
        self._running = False
        self._run_btn.configure(state="normal")
        self._wipe_label.configure(text=f"Error: {message}")

    def _on_row_select(self, event=None) -> None:
        """Show detailed breakdown for the selected weapon."""
        selected = self._tree.selection()
        if not selected or not self._last_results:
            return
        idx = int(selected[0])
        if idx < 0 or idx >= len(self._last_results):
            return

        text = self._format_detail(idx)
        self._details.configure(state="normal")
        self._details.delete("1.0", "end")
        self._details.insert("1.0", text)
        self._details.configure(state="disabled")

    def _format_detail(self, idx: int) -> str:
        """Format the full detail breakdown for a single weapon result."""
        r = self._last_results[idx]
        weapon = r.get("weapon")
        sims = SIMULATIONS
        defender = self._state.defender

        name = getattr(weapon, "name", None) or f"Weapon {r['id'] + 1}"
        lines = []
        lines.append(f"Weapon: {name}")
        lines.append(f"To Wound: {r['to_wound']}+")
        lines.append(f"Unit Wiped: {self._last_wipe}%")
        lines.append("")

        # Special rules
        sustained = getattr(weapon, "sustained_hits", "0")
        if sustained and sustained != "0":
            lines.append(f"Sustained Hits: {r['sustained'] / sims:.2f}")
        if getattr(weapon, "lethal_hits", False):
            lines.append(f"Lethal Hits: {r['crit_hit'] / sims:.2f}")
        if getattr(weapon, "devestating_wounds", False):
            lines.append(f"Devastating Wounds: {r['crit_wound'] / sims:.2f}")
        if getattr(weapon, "blast", False):
            model_count = defender.get("model_count", 10) if isinstance(defender, dict) else getattr(defender, "model_count", 10)
            lines.append(f"Blast: +{int(model_count / 5)} extra attacks")

        lines.append("")
        lines.append(f"Attacks:      {r['attacks'] / sims:.2f}")

        is_torrent = getattr(weapon, "torrent", False)
        if is_torrent:
            lines.append("Hits:         N/A (Torrent)")
        else:
            lines.append(f"Hits:         {r['hits'] / sims:.2f}")
        lines.append(f"Wounds:       {r['wounds'] / sims:.2f}")
        lines.append(f"After Saves:  {r['saves'] / sims:.2f}")
        lines.append(f"Damage:       {r['damage'] / sims:.2f}")

        fnp = defender.get("feel_no_pain", 0) if isinstance(defender, dict) else getattr(defender, "feel_no_pain", 0)
        lines.append(f"After FNP:    {r['fnp'] / sims:.2f}" if fnp else "After FNP:    -")

        model_count = defender.get("model_count", 1) if isinstance(defender, dict) else getattr(defender, "model_count", 1)
        lines.append(f"Kills:        {r['kills'] / sims:.2f}" if model_count > 1 else "Kills:        -")

        return "\n".join(lines)
