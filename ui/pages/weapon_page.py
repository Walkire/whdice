"""Weapon Management Page — scrollable list of WeaponCards with add/delete/duplicate/reorder."""

import customtkinter

from state.app_state import AppState
from ui.styles import FONT_TITLE, BUTTON_HEIGHT, BUTTON_HEIGHT_SMALL, PAGE_PAD_X, COLOR_NAV_HOVER
from ui.widgets.weapon_card import WeaponCard


class WeaponPage(customtkinter.CTkFrame):
    """Page displaying all saved weapons as cards with management actions.

    Supports add, delete, duplicate, click-to-edit (navigates to attacker page),
    and drag-to-reorder via up/down buttons on each card.
    """

    def __init__(self, master, state: AppState, on_edit_weapon=None, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state
        self._on_edit_weapon = on_edit_weapon
        self._cards: list = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1, minsize=200)

        # Top bar with Add button
        top_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(PAGE_PAD_X, 4))

        title = customtkinter.CTkLabel(
            top_bar, text="Weapons",
            font=customtkinter.CTkFont(size=FONT_TITLE[1], weight=FONT_TITLE[2])
        )
        title.pack(side="left")

        self._add_btn = customtkinter.CTkButton(
            top_bar,
            text="+ Add Weapon",
            command=self._add_weapon,
            height=BUTTON_HEIGHT_SMALL,
        )
        self._add_btn.pack(side="right")

        # Scrollable area for weapon cards
        self._scroll_frame = customtkinter.CTkScrollableFrame(self)
        self._scroll_frame.grid(row=1, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(4, PAGE_PAD_X))
        self._scroll_frame.grid_columnconfigure(0, weight=1)

        # Empty state label
        self._empty_label = customtkinter.CTkLabel(
            self._scroll_frame,
            text="No weapons saved yet.\nUse the Attacker page to configure a weapon, then save it.",
            text_color=("gray50", "gray60"),
        )

        # Initial render
        self._rebuild_cards()

        # Listen for state changes
        self._state.subscribe(self._on_state_change)

    def _rebuild_cards(self) -> None:
        """Rebuild all weapon cards from current state."""
        # Destroy existing cards
        for card in self._cards:
            card.destroy()
        self._cards.clear()

        weapons = self._state.weapons

        if not weapons:
            self._empty_label.grid(row=0, column=0, pady=40)
            return

        self._empty_label.grid_remove()

        for idx, weapon_data in enumerate(weapons):
            card_frame = customtkinter.CTkFrame(self._scroll_frame, fg_color="transparent")
            card_frame.grid(row=idx, column=0, sticky="ew", pady=(0, 6))
            card_frame.grid_columnconfigure(0, weight=1)

            card = WeaponCard(
                card_frame,
                weapon_data=weapon_data,
                on_click=lambda i=idx: self._edit_weapon(i),
                on_delete=lambda i=idx: self._delete_weapon(i),
                on_duplicate=lambda i=idx: self._duplicate_weapon(i),
            )
            card.grid(row=0, column=0, sticky="ew")

            # Reorder buttons
            btn_frame = customtkinter.CTkFrame(card_frame, fg_color="transparent")
            btn_frame.grid(row=0, column=1, padx=(4, 0), sticky="ns")

            up_btn = customtkinter.CTkButton(
                btn_frame, text="▲", width=24, height=24, corner_radius=4,
                fg_color="transparent", hover_color=COLOR_NAV_HOVER,
                command=lambda i=idx: self._move_weapon(i, i - 1),
            )
            up_btn.pack(side="top", pady=(4, 2))

            down_btn = customtkinter.CTkButton(
                btn_frame, text="▼", width=24, height=24, corner_radius=4,
                fg_color="transparent", hover_color=COLOR_NAV_HOVER,
                command=lambda i=idx: self._move_weapon(i, i + 1),
            )
            down_btn.pack(side="top")

            self._cards.append(card_frame)

    def _add_weapon(self) -> None:
        """Add a new weapon using the current attacker state."""
        weapon = dict(self._state.attacker)
        if not weapon.get("name"):
            weapon["name"] = f"Weapon {len(self._state.weapons) + 1}"
        self._state.add_weapon(weapon)

    def _delete_weapon(self, index: int) -> None:
        """Delete weapon at the given index."""
        self._state.remove_weapon(index)

    def _duplicate_weapon(self, index: int) -> None:
        """Duplicate weapon at the given index."""
        self._state.duplicate_weapon(index)

    def _edit_weapon(self, index: int) -> None:
        """Load weapon into attacker panel for editing."""
        if 0 <= index < len(self._state.weapons):
            weapon_data = self._state.weapons[index]
            self._state.update_attacker(**weapon_data)
            if self._on_edit_weapon:
                self._on_edit_weapon()

    def _move_weapon(self, from_idx: int, to_idx: int) -> None:
        """Reorder weapon from one position to another."""
        self._state.reorder_weapons(from_idx, to_idx)

    def _on_state_change(self) -> None:
        """Rebuild cards when state changes."""
        self._rebuild_cards()
