"""Compare Templates Page — run weapons against all templates and show comparison."""

import threading
import tkinter as tk

import customtkinter

from classes.data import Data
from simulation import simulate
from state.app_state import AppState, DEFENDER_DEFAULTS
from state.template_manager import TemplateManager
from ui.styles import FONT_TITLE, BUTTON_HEIGHT, PAGE_PAD_X


SIMULATIONS = 100000


class ComparePage(customtkinter.CTkFrame):
    """Page for comparing current weapons against all saved defender templates.

    Runs the simulation against each template and displays a summary table
    showing avg kills, damage, and wipe % for each template.
    Clicking a row shows the per-weapon detail breakdown for that template.
    """

    def __init__(self, master, state: AppState, template_manager: TemplateManager, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state
        self._tm = template_manager
        self._running = False
        self._comparison_data = []  # Full results per template

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(4, weight=1)

        # Top bar
        top_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(PAGE_PAD_X, 4))

        title = customtkinter.CTkLabel(
            top_bar, text="Template Comparison",
            font=customtkinter.CTkFont(size=FONT_TITLE[1], weight=FONT_TITLE[2]),
        )
        title.pack(side="left")

        self._run_btn = customtkinter.CTkButton(
            top_bar,
            text="Run Comparison",
            command=self._run_comparison,
            height=BUTTON_HEIGHT,
        )
        self._run_btn.pack(side="right")

        # Progress bar
        self._progress = customtkinter.CTkProgressBar(self)
        self._progress.grid(row=1, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(4, 8))
        self._progress.set(0)

        # Results table
        self._tree_frame = customtkinter.CTkFrame(self)
        self._tree_frame.grid(row=2, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(0, 4))
        self._tree_frame.grid_columnconfigure(0, weight=1)
        self._tree_frame.grid_rowconfigure(0, weight=1)

        columns = ("template", "avg_kills", "avg_damage", "wipe_pct")
        self._tree = tk.ttk.Treeview(
            self._tree_frame, columns=columns, show="headings", height=12
        )

        col_headings = {
            "template": "Template",
            "avg_kills": "Avg Kills",
            "avg_damage": "Avg Damage",
            "wipe_pct": "Wipe %",
        }
        for col, heading in col_headings.items():
            self._tree.heading(col, text=heading, command=lambda c=col: self._sort_column(c))
            width = 180 if col == "template" else 100
            self._tree.column(col, width=width, minwidth=60, anchor="center", stretch=True)

        self._tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.ttk.Scrollbar(self._tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Status label
        self._status_label = customtkinter.CTkLabel(self, text="")
        self._status_label.grid(row=3, column=0, sticky="w", padx=PAGE_PAD_X, pady=(4, 4))

        # Detail view — per-weapon breakdown for selected template
        self._details = customtkinter.CTkTextbox(
            self, height=160, font=customtkinter.CTkFont(family="Consolas", size=12),
            state="disabled",
        )
        self._details.grid(row=4, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(0, PAGE_PAD_X))

        # Bind row selection
        self._tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _run_comparison(self) -> None:
        """Run simulation against all templates."""
        if self._running:
            return

        weapons = self._state.weapons
        if not weapons:
            self._status_label.configure(text="No weapons configured. Add weapons first.")
            return

        templates = self._tm.list_templates()
        if not templates:
            self._status_label.configure(text="No templates found. Save defender templates first.")
            return

        self._running = True
        self._run_btn.configure(state="disabled")
        self._progress.set(0)
        self._status_label.configure(text="Running comparison...")
        self._comparison_data = []

        for item in self._tree.get_children():
            self._tree.delete(item)

        thread = threading.Thread(
            target=self._compare_thread, args=(weapons, templates), daemon=True
        )
        thread.start()

    def _compare_thread(self, weapons: list, templates: list) -> None:
        """Run comparison in background thread."""
        try:
            attacker_data = Data(**self._state.attacker)
            weapon_data_list = [Data(**w) for w in weapons]

            comparison_data = []
            total = len(templates)

            for idx, tpl in enumerate(templates):
                # Build defender from template data
                defender_dict = {**DEFENDER_DEFAULTS}
                for k, v in tpl.items():
                    if not k.startswith("_") and k in defender_dict:
                        defender_dict[k] = v
                defender_data = Data(**defender_dict)

                results, wipe_percent = simulate(
                    attacker_data, defender_data, weapon_data_list, SIMULATIONS
                )

                avg_kills = sum(r["kills"] for r in results) / SIMULATIONS
                avg_damage = sum(r["damage"] for r in results) / SIMULATIONS

                comparison_data.append({
                    "name": tpl.get("name", "Unnamed"),
                    "avg_kills": round(avg_kills, 2),
                    "avg_damage": round(avg_damage, 2),
                    "wipe_pct": wipe_percent,
                    "results": results,
                    "defender": defender_dict,
                })

                # Update progress
                progress = (idx + 1) / total
                self.after(0, lambda p=progress: self._progress.set(p))

            self.after(0, lambda: self._display_results(comparison_data))
        except Exception as e:
            self.after(0, lambda: self._display_error(str(e)))

    def _display_results(self, comparison_data: list) -> None:
        """Populate table with comparison results."""
        self._progress.set(1.0)
        self._running = False
        self._run_btn.configure(state="normal")
        self._comparison_data = comparison_data

        for item in self._tree.get_children():
            self._tree.delete(item)

        for i, row in enumerate(comparison_data):
            self._tree.insert("", "end", iid=str(i), values=(
                row["name"],
                row["avg_kills"],
                row["avg_damage"],
                f"{row['wipe_pct']}%",
            ))

        self._status_label.configure(
            text=f"Compared against {len(comparison_data)} templates. Click a row for details."
        )

        # Clear detail view
        self._details.configure(state="normal")
        self._details.delete("1.0", "end")
        self._details.insert("1.0", "Click a template row to see per-weapon breakdown.")
        self._details.configure(state="disabled")

    def _display_error(self, message: str) -> None:
        """Show error state."""
        self._progress.set(0)
        self._running = False
        self._run_btn.configure(state="normal")
        self._status_label.configure(text=f"Error: {message}")

    def _on_row_select(self, event=None) -> None:
        """Show per-weapon detail for the selected template."""
        selected = self._tree.selection()
        if not selected or not self._comparison_data:
            return
        idx = int(selected[0])
        if idx < 0 or idx >= len(self._comparison_data):
            return

        text = self._format_detail(idx)
        self._details.configure(state="normal")
        self._details.delete("1.0", "end")
        self._details.insert("1.0", text)
        self._details.configure(state="disabled")

    def _format_detail(self, idx: int) -> str:
        """Format the per-weapon breakdown for a template comparison result."""
        entry = self._comparison_data[idx]
        results = entry["results"]
        defender = entry["defender"]
        wipe = entry["wipe_pct"]
        sims = SIMULATIONS

        lines = []
        lines.append(f"Template: {entry['name']}")
        lines.append(f"Unit Wiped: {wipe}%")
        lines.append("")

        for r in results:
            weapon = r.get("weapon")
            name = getattr(weapon, "name", None) or f"Weapon {r['id'] + 1}"
            lines.append(f"--- {name} (To Wound: {r['to_wound']}+) ---")

            # Special rules
            sustained = getattr(weapon, "sustained_hits", "0")
            if sustained and sustained != "0":
                lines.append(f"  Sustained Hits: {r['sustained'] / sims:.2f}")
            if getattr(weapon, "lethal_hits", False):
                lines.append(f"  Lethal Hits:    {r['crit_hit'] / sims:.2f}")
            if getattr(weapon, "devestating_wounds", False):
                lines.append(f"  Dev. Wounds:    {r['crit_wound'] / sims:.2f}")

            lines.append(f"  Attacks:        {r['attacks'] / sims:.2f}")

            if getattr(weapon, "torrent", False):
                lines.append("  Hits:           N/A (Torrent)")
            else:
                lines.append(f"  Hits:           {r['hits'] / sims:.2f}")

            lines.append(f"  Wounds:         {r['wounds'] / sims:.2f}")
            lines.append(f"  After Saves:    {r['saves'] / sims:.2f}")
            lines.append(f"  Damage:         {r['damage'] / sims:.2f}")

            fnp = defender.get("feel_no_pain", 0)
            if fnp:
                lines.append(f"  After FNP:      {r['fnp'] / sims:.2f}")

            model_count = defender.get("model_count", 1)
            if model_count > 1:
                lines.append(f"  Kills:          {r['kills'] / sims:.2f}")

            lines.append("")

        return "\n".join(lines)

    def _sort_column(self, col: str) -> None:
        """Sort treeview by column (toggle ascending/descending)."""
        data = [(self._tree.set(child, col), child) for child in self._tree.get_children("")]
        try:
            data.sort(key=lambda t: float(t[0].rstrip("%")), reverse=True)
        except ValueError:
            data.sort(key=lambda t: t[0])

        for index, (_, iid) in enumerate(data):
            self._tree.move(iid, "", index)
