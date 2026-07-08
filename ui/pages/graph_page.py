"""Graph Page — displays simulation results as charts using matplotlib."""

import tkinter as tk

import customtkinter

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from state.app_state import AppState
from ui.stats import compute_summary_stats
from ui.styles import FONT_TITLE, FONT_SECTION, BUTTON_HEIGHT, PAGE_PAD_X


SIMULATIONS = 100000


class GraphPage(customtkinter.CTkFrame):
    """Page displaying simulation results as graphs and summary statistics.

    Shows a damage distribution histogram, kill probability bar chart,
    and a summary statistics panel.
    """

    def __init__(self, master, state: AppState, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top bar
        top_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(PAGE_PAD_X, 4))

        title = customtkinter.CTkLabel(
            top_bar, text="Graphs & Statistics",
            font=customtkinter.CTkFont(size=FONT_TITLE[1], weight=FONT_TITLE[2]),
        )
        title.pack(side="left")

        self._refresh_btn = customtkinter.CTkButton(
            top_bar, text="Refresh", command=self._refresh, height=BUTTON_HEIGHT
        )
        self._refresh_btn.pack(side="right")

        if not HAS_MATPLOTLIB:
            self._show_fallback()
            return

        # Content area split: left = charts, right = summary stats
        content = customtkinter.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(0, PAGE_PAD_X))
        content.grid_columnconfigure(0, weight=3, minsize=400)
        content.grid_columnconfigure(1, weight=1, minsize=180)
        content.grid_rowconfigure(0, weight=1, minsize=300)

        # Chart area
        self._chart_frame = customtkinter.CTkFrame(content)
        self._chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        self._chart_frame.grid_columnconfigure(0, weight=1)
        self._chart_frame.grid_rowconfigure(0, weight=1)

        # Summary stats panel
        self._stats_frame = customtkinter.CTkFrame(content)
        self._stats_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        # Create matplotlib figure with two subplots
        self._fig = Figure(figsize=(8, 5), dpi=100)
        self._fig.set_facecolor("#2b2b2b")
        self._ax_damage = self._fig.add_subplot(211)
        self._ax_kills = self._fig.add_subplot(212)
        self._fig.tight_layout(pad=3.0)

        self._canvas = FigureCanvasTkAgg(self._fig, master=self._chart_frame)
        self._canvas_widget = self._canvas.get_tk_widget()
        self._canvas_widget.grid(row=0, column=0, sticky="nsew")

        # Stats labels
        self._stats_labels: dict = {}
        self._build_stats_panel()

        # Show placeholder
        self._show_no_data()

    def _show_fallback(self) -> None:
        """Show fallback message when matplotlib is not available."""
        label = customtkinter.CTkLabel(
            self,
            text="matplotlib is required for graphs.\nInstall with: pip install matplotlib",
            font=customtkinter.CTkFont(size=14),
        )
        label.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)

    def _build_stats_panel(self) -> None:
        """Build the summary statistics panel on the right side."""
        header = customtkinter.CTkLabel(
            self._stats_frame, text="Summary Statistics",
            font=customtkinter.CTkFont(size=14, weight="bold"),
        )
        header.pack(padx=12, pady=(12, 8))

        metrics = [
            ("Total Damage", "totals_damage"),
            ("Total After FNP", "totals_after_fnp"),
            ("Total Wounds", "totals_wounds"),
            ("Total Kills", "totals_kills"),
            ("", "spacer"),
            ("Per-Weapon Damage", "section_damage"),
            ("  Average", "damage_average"),
            ("  Median", "damage_median"),
            ("  Min", "damage_min"),
            ("  Max", "damage_max"),
            ("", "spacer2"),
            ("Per-Weapon Kills", "section_kills"),
            ("  Average", "kills_average"),
            ("  Median", "kills_median"),
            ("  Min", "kills_min"),
            ("  Max", "kills_max"),
        ]

        for label_text, key in metrics:
            if key.startswith("spacer"):
                spacer = customtkinter.CTkFrame(self._stats_frame, height=8, fg_color="transparent")
                spacer.pack(fill="x")
                continue

            if key.startswith("section"):
                lbl = customtkinter.CTkLabel(
                    self._stats_frame, text=label_text,
                    font=customtkinter.CTkFont(size=12, weight="bold"),
                    anchor="w",
                )
                lbl.pack(fill="x", padx=12, pady=(4, 0))
                continue

            row = customtkinter.CTkFrame(self._stats_frame, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=1)

            name_lbl = customtkinter.CTkLabel(row, text=label_text, anchor="w")
            name_lbl.pack(side="left")

            val_lbl = customtkinter.CTkLabel(row, text="—", anchor="e")
            val_lbl.pack(side="right")

            self._stats_labels[key] = val_lbl

    def _show_no_data(self) -> None:
        """Display a 'no data' placeholder in the chart area."""
        for ax in (self._ax_damage, self._ax_kills):
            ax.clear()
            ax.set_facecolor("#2b2b2b")
            ax.text(
                0.5, 0.5, "Run a simulation to see graphs",
                ha="center", va="center", color="#888888", fontsize=12,
                transform=ax.transAxes,
            )
            ax.set_xticks([])
            ax.set_yticks([])
        self._canvas.draw()

    def _refresh(self) -> None:
        """Refresh graphs from the current simulation results in state."""
        results = self._state.results
        if not results:
            self._show_no_data()
            return

        self._update_charts(results)
        self._update_stats(results)

    def _update_charts(self, results: list) -> None:
        """Redraw both charts with current results."""
        sims = SIMULATIONS

        # Extract per-weapon data
        weapon_names = []
        damage_values = []
        kill_values = []

        for r in results:
            weapon = r.get("weapon")
            name = getattr(weapon, "name", None) or f"Weapon {r['id'] + 1}"
            weapon_names.append(name)
            damage_values.append(r.get("damage", 0) / sims)
            kill_values.append(r.get("kills", 0) / sims)

        bar_color = "#1f6aa5"
        text_color = "#cccccc"

        # Damage distribution bar chart
        self._ax_damage.clear()
        self._ax_damage.set_facecolor("#2b2b2b")
        bars = self._ax_damage.bar(weapon_names, damage_values, color=bar_color, edgecolor="#3a8fd4")
        self._ax_damage.set_title("Average Damage per Weapon", color=text_color, fontsize=11)
        self._ax_damage.set_ylabel("Damage", color=text_color, fontsize=9)
        self._ax_damage.tick_params(colors=text_color, labelsize=8)
        self._ax_damage.spines["top"].set_visible(False)
        self._ax_damage.spines["right"].set_visible(False)
        self._ax_damage.spines["bottom"].set_color(text_color)
        self._ax_damage.spines["left"].set_color(text_color)

        # Add value labels on bars
        for bar, val in zip(bars, damage_values):
            self._ax_damage.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{val:.1f}", ha="center", va="bottom", color=text_color, fontsize=8,
            )

        # Kill probability bar chart
        self._ax_kills.clear()
        self._ax_kills.set_facecolor("#2b2b2b")
        bars = self._ax_kills.bar(weapon_names, kill_values, color="#2d8a4e", edgecolor="#3dba68")
        self._ax_kills.set_title("Average Kills per Weapon", color=text_color, fontsize=11)
        self._ax_kills.set_ylabel("Kills", color=text_color, fontsize=9)
        self._ax_kills.tick_params(colors=text_color, labelsize=8)
        self._ax_kills.spines["top"].set_visible(False)
        self._ax_kills.spines["right"].set_visible(False)
        self._ax_kills.spines["bottom"].set_color(text_color)
        self._ax_kills.spines["left"].set_color(text_color)

        for bar, val in zip(bars, kill_values):
            self._ax_kills.text(
                bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{val:.1f}", ha="center", va="bottom", color=text_color, fontsize=8,
            )

        self._fig.tight_layout(pad=3.0)
        self._canvas.draw()

    def _update_stats(self, results: list) -> None:
        """Update the summary statistics panel."""
        stats = compute_summary_stats(results, SIMULATIONS)
        if not stats:
            return

        # Update total labels
        totals = stats.get("totals", {})
        self._set_stat("totals_damage", totals.get("damage", 0))
        self._set_stat("totals_after_fnp", totals.get("after_fnp", 0))
        self._set_stat("totals_wounds", totals.get("wounds", 0))
        self._set_stat("totals_kills", totals.get("kills", 0))

        # Update per-weapon damage stats
        damage_stats = stats.get("damage", {})
        self._set_stat("damage_average", damage_stats.get("average", 0))
        self._set_stat("damage_median", damage_stats.get("median", 0))
        self._set_stat("damage_min", damage_stats.get("min", 0))
        self._set_stat("damage_max", damage_stats.get("max", 0))

        # Update per-weapon kills stats
        kills_stats = stats.get("kills", {})
        self._set_stat("kills_average", kills_stats.get("average", 0))
        self._set_stat("kills_median", kills_stats.get("median", 0))
        self._set_stat("kills_min", kills_stats.get("min", 0))
        self._set_stat("kills_max", kills_stats.get("max", 0))

    def _set_stat(self, key: str, value) -> None:
        """Set a stat label's text value."""
        label = self._stats_labels.get(key)
        if label:
            label.configure(text=f"{value}")
