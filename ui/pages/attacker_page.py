"""Attacker Page — hosts the AttackerPanel with a collapsible weapon list sidebar."""

import customtkinter

from state.app_state import AppState
from ui.styles import (
    BUTTON_HEIGHT, BUTTON_HEIGHT_SMALL, PAGE_PAD_X,
    FONT_SECTION, COLOR_BORDER, COLOR_NAV_HOVER, COLOR_DANGER_HOVER,
)
from ui.widgets.attacker_panel import AttackerPanel
from ui.widgets.weapon_card import WeaponCard


class AttackerPage(customtkinter.CTkFrame):
    """Page for configuring attacker weapon stats.

    Split layout: attacker form on the left, collapsible weapon list on the right.
    """

    def __init__(self, master, state: AppState, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state
        self._weapon_panel_visible = True
        self._cards: list = []
        self._editing_index: int | None = None  # Track which weapon is being edited

        # Split layout: form (weight 2) | weapons panel (weight 1)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # --- Left side: attacker form ---
        left_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)

        self._panel = AttackerPanel(left_frame, on_change=self._on_panel_change)
        self._panel.grid(row=0, column=0, sticky="nsew", padx=(PAGE_PAD_X, 8), pady=(PAGE_PAD_X, 4))

        # Bottom bar with buttons
        bottom_bar = customtkinter.CTkFrame(left_frame, fg_color="transparent")
        bottom_bar.grid(row=1, column=0, sticky="ew", padx=(PAGE_PAD_X, 8), pady=(4, PAGE_PAD_X))

        self._save_btn = customtkinter.CTkButton(
            bottom_bar,
            text="Save as Weapon",
            command=self._save_weapon,
            height=BUTTON_HEIGHT,
        )
        self._save_btn.pack(side="left")

        self._update_btn = customtkinter.CTkButton(
            bottom_bar,
            text="Save Changes",
            command=self._update_weapon,
            height=BUTTON_HEIGHT,
        )
        # Hidden by default, shown when editing
        self._update_btn.pack_forget()

        self._cancel_edit_btn = customtkinter.CTkButton(
            bottom_bar,
            text="Cancel Edit",
            command=self._cancel_edit,
            height=BUTTON_HEIGHT,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
        )
        self._cancel_edit_btn.pack_forget()

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

        self._toggle_btn = customtkinter.CTkButton(
            bottom_bar,
            text="◀ Weapons",
            command=self._toggle_weapon_panel,
            height=BUTTON_HEIGHT,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            width=100,
        )
        self._toggle_btn.pack(side="right")

        # --- Right side: collapsible weapon list ---
        self._weapon_frame = customtkinter.CTkFrame(self, width=280)
        self._weapon_frame.grid(row=0, column=1, sticky="nsew", padx=(0, PAGE_PAD_X), pady=PAGE_PAD_X)
        self._weapon_frame.grid_columnconfigure(0, weight=1)
        self._weapon_frame.grid_rowconfigure(1, weight=1)
        self._weapon_frame.grid_propagate(False)

        # Weapons header
        header = customtkinter.CTkFrame(self._weapon_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))

        weapons_title = customtkinter.CTkLabel(
            header, text="Saved Weapons",
            font=customtkinter.CTkFont(size=FONT_SECTION[1], weight=FONT_SECTION[2]),
        )
        weapons_title.pack(side="left")

        self._weapon_count_label = customtkinter.CTkLabel(
            header, text="(0)", text_color=("gray50", "gray60"),
        )
        self._weapon_count_label.pack(side="left", padx=(6, 0))

        # Scrollable weapon cards
        self._scroll_frame = customtkinter.CTkScrollableFrame(self._weapon_frame)
        self._scroll_frame.grid(row=1, column=0, sticky="nsew", padx=4, pady=(0, 8))
        self._scroll_frame.grid_columnconfigure(0, weight=1)

        self._empty_label = customtkinter.CTkLabel(
            self._scroll_frame,
            text="No weapons yet.\nSave one using the button.",
            text_color=("gray50", "gray60"),
            font=customtkinter.CTkFont(size=11),
        )

        # Load current state
        self._panel.set_values(self._state.attacker)
        self._rebuild_cards()

        # Listen for state changes
        self._state.subscribe(self._on_state_change)

    def _toggle_weapon_panel(self) -> None:
        """Show/hide the weapon list panel."""
        if self._weapon_panel_visible:
            self._weapon_frame.grid_remove()
            self.grid_columnconfigure(1, weight=0, minsize=0)
            self._toggle_btn.configure(text="▶ Weapons")
            self._weapon_panel_visible = False
        else:
            self._weapon_frame.grid()
            self._toggle_btn.configure(text="◀ Weapons")
            self._weapon_panel_visible = True

    def _rebuild_cards(self) -> None:
        """Rebuild weapon cards from state."""
        for card in self._cards:
            card.destroy()
        self._cards.clear()

        weapons = self._state.weapons
        self._weapon_count_label.configure(text=f"({len(weapons)})")

        if not weapons:
            self._empty_label.grid(row=0, column=0, pady=20)
            return

        self._empty_label.grid_remove()

        for idx, weapon_data in enumerate(weapons):
            card = WeaponCard(
                self._scroll_frame,
                weapon_data=weapon_data,
                on_click=lambda i=idx: self._load_weapon(i),
                on_delete=lambda i=idx: self._delete_weapon(i),
                on_duplicate=lambda i=idx: self._duplicate_weapon(i),
            )
            card.grid(row=idx, column=0, sticky="ew", pady=(0, 4))
            self._cards.append(card)

    def _load_weapon(self, index: int) -> None:
        """Load a weapon into the attacker form for editing in place."""
        if 0 <= index < len(self._state.weapons):
            weapon_data = self._state.weapons[index]
            self._panel.set_values(weapon_data)
            self._editing_index = index
            self._set_edit_mode(True)

    def _update_weapon(self) -> None:
        """Save changes back to the weapon being edited."""
        if self._editing_index is not None and 0 <= self._editing_index < len(self._state.weapons):
            values = self._panel.get_values()
            if not values.get("name"):
                values["name"] = f"Weapon {self._editing_index + 1}"
            self._state.weapons[self._editing_index] = values
            self._state._notify()
        self._editing_index = None
        self._set_edit_mode(False)

    def _cancel_edit(self) -> None:
        """Cancel editing and restore the attacker state."""
        self._editing_index = None
        self._set_edit_mode(False)
        self._panel.set_values(self._state.attacker)

    def _set_edit_mode(self, editing: bool) -> None:
        """Toggle between save-new and edit-existing button layouts."""
        if editing:
            self._save_btn.pack_forget()
            self._reset_btn.pack_forget()
            self._update_btn.pack(side="left")
            self._cancel_edit_btn.pack(side="left", padx=(8, 0))
        else:
            self._update_btn.pack_forget()
            self._cancel_edit_btn.pack_forget()
            self._save_btn.pack(side="left")
            self._reset_btn.pack(side="left", padx=(8, 0))

    def _delete_weapon(self, index: int) -> None:
        """Delete weapon at index."""
        self._state.remove_weapon(index)

    def _duplicate_weapon(self, index: int) -> None:
        """Duplicate weapon at index."""
        self._state.duplicate_weapon(index)

    def _on_panel_change(self) -> None:
        """Sync panel values to state when user edits a field."""
        values = self._panel.get_values()
        self._state.update_attacker(**values)

    def _save_weapon(self) -> None:
        """Save the current attacker config as a weapon in the weapon list."""
        values = self._panel.get_values()
        if not values.get("name"):
            values["name"] = f"Weapon {len(self._state.weapons) + 1}"
        self._state.add_weapon(values)

    def _reset(self) -> None:
        """Reset the panel to defaults."""
        self._panel.reset()
        self._on_panel_change()

    def _on_state_change(self) -> None:
        """Called when state changes externally (e.g. undo). Refresh panel and cards."""
        self._panel.set_values(self._state.attacker)
        self._rebuild_cards()
