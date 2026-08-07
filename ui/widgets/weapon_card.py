"""WeaponCard — a card widget displaying a weapon's name, stats, and abilities."""

from typing import Callable, Dict, Optional
import customtkinter

from ui.styles import (
    FONT_SECTION, FONT_SMALL, CORNER_RADIUS, COLOR_BORDER,
    COLOR_DANGER, COLOR_DANGER_HOVER, COLOR_NAV_HOVER,
)


class WeaponCard(customtkinter.CTkFrame):
    """Card displaying a weapon summary with click, delete, and duplicate callbacks."""

    def __init__(
        self,
        master,
        weapon_data: Dict,
        on_click: Optional[Callable] = None,
        on_delete: Optional[Callable] = None,
        on_duplicate: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(master, corner_radius=CORNER_RADIUS, border_width=1, border_color=COLOR_BORDER, **kwargs)

        self._weapon_data = weapon_data
        self._on_click = on_click
        self._on_delete = on_delete
        self._on_duplicate = on_duplicate

        self.grid_columnconfigure(0, weight=1)

        # Make the card clickable
        self.bind("<Button-1>", self._handle_click)

        # Name row
        self._name_label = customtkinter.CTkLabel(
            self,
            text=weapon_data.get("name", "Unnamed"),
            font=customtkinter.CTkFont(size=FONT_SECTION[1], weight=FONT_SECTION[2]),
            anchor="w",
        )
        self._name_label.grid(row=0, column=0, padx=10, pady=(8, 2), sticky="w")
        self._name_label.bind("<Button-1>", self._handle_click)

        # Stats row
        self._stats_label = customtkinter.CTkLabel(
            self,
            text=self._format_stats(weapon_data),
            anchor="w",
            text_color=("gray30", "gray70"),
        )
        self._stats_label.grid(row=1, column=0, padx=10, pady=(0, 2), sticky="w")
        self._stats_label.bind("<Button-1>", self._handle_click)

        # Abilities row
        abilities_text = self._format_abilities(weapon_data)
        if abilities_text:
            self._abilities_label = customtkinter.CTkLabel(
                self,
                text=abilities_text,
                anchor="w",
                text_color=("dodgerblue", "deepskyblue"),
                font=customtkinter.CTkFont(size=FONT_SMALL[1]),
            )
            self._abilities_label.grid(row=2, column=0, padx=10, pady=(0, 8), sticky="w")
            self._abilities_label.bind("<Button-1>", self._handle_click)
        else:
            self._abilities_label = None

        # Action buttons (delete, duplicate)
        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=1, rowspan=3, padx=(0, 6), pady=6, sticky="ne")

        if on_duplicate:
            dup_btn = customtkinter.CTkButton(
                btn_frame, text="⧉", width=28, height=28, corner_radius=4,
                fg_color="transparent", hover_color=COLOR_NAV_HOVER,
                command=self._handle_duplicate,
            )
            dup_btn.pack(side="top", pady=(0, 2))

        if on_delete:
            del_btn = customtkinter.CTkButton(
                btn_frame, text="✕", width=28, height=28, corner_radius=4,
                fg_color="transparent", hover_color=COLOR_DANGER_HOVER,
                text_color=("red3", "tomato"),
                command=self._handle_delete,
            )
            del_btn.pack(side="top")

    def _format_stats(self, data: Dict) -> str:
        """Format core stats into a readable string."""
        attacks = data.get("attacks", "?")
        score = data.get("score", "?")
        strength = data.get("strength", "?")
        ap = data.get("ap", "?")
        damage = data.get("damage", "?")
        return f"A:{attacks}  BS/WS:{score}+  S:{strength}  AP:-{ap}  D:{damage}"

    def _format_abilities(self, data: Dict) -> str:
        """Return a comma-separated string of active abilities."""
        ability_keys = [
            ("torrent", "Torrent"),
            ("blast", "Blast"),
            ("lethal_hits", "Lethal Hits"),
            ("devestating_wounds", "Devastating Wounds"),
            ("melta", "Melta"),
            ("ignore_cover", "Ignore Cover"),
            ("psychic", "Psychic"),
        ]
        active = []
        for key, display in ability_keys:
            if data.get(key):
                active.append(display)
        # Sustained hits as a special case (non-zero means active)
        sustained = data.get("sustained_hits", "0")
        if sustained and sustained != "0":
            active.append(f"Sustained Hits {sustained}")
        return ", ".join(active)

    def _handle_click(self, event=None) -> None:
        if self._on_click:
            self._on_click()

    def _handle_delete(self) -> None:
        if self._on_delete:
            self._on_delete()

    def _handle_duplicate(self) -> None:
        if self._on_duplicate:
            self._on_duplicate()

    def update_data(self, weapon_data: Dict) -> None:
        """Update the card display with new weapon data."""
        self._weapon_data = weapon_data
        self._name_label.configure(text=weapon_data.get("name", "Unnamed"))
        self._stats_label.configure(text=self._format_stats(weapon_data))
        abilities_text = self._format_abilities(weapon_data)
        if self._abilities_label:
            self._abilities_label.configure(text=abilities_text)
