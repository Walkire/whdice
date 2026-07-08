"""Sidebar — vertical navigation panel with page buttons."""

from typing import Callable, List
import customtkinter

from ui.styles import (
    FONT_SIDEBAR_TITLE, SIDEBAR_WIDTH, NAV_BUTTON_HEIGHT,
    CORNER_RADIUS, COLOR_NAV_ACTIVE, COLOR_NAV_HOVER,
    PAGE_PAD_X, PAGE_PAD_Y_TOP, SECTION_GAP,
)


NAV_ITEMS = [
    ("Attacker", "attacker"),
    ("Defender", "defender"),
    ("Weapons", "weapons"),
    ("Results", "results"),
    ("Graphs", "graphs"),
    ("Templates", "templates"),
    ("Settings", "settings"),
]


class Sidebar(customtkinter.CTkFrame):
    """Vertical sidebar with navigation buttons for each page."""

    def __init__(self, master, on_navigate: Callable[[str], None], **kwargs):
        super().__init__(master, width=SIDEBAR_WIDTH, corner_radius=0, **kwargs)
        self.grid_propagate(False)

        self._on_navigate = on_navigate
        self._buttons: dict[str, customtkinter.CTkButton] = {}
        self._active: str | None = None

        # Title label
        title = customtkinter.CTkLabel(
            self, text="Combat Sim",
            font=customtkinter.CTkFont(size=FONT_SIDEBAR_TITLE[1], weight=FONT_SIDEBAR_TITLE[2])
        )
        title.grid(row=0, column=0, padx=PAGE_PAD_X, pady=(PAGE_PAD_Y_TOP, SECTION_GAP * 2), sticky="w")

        # Navigation buttons
        for idx, (label, page_name) in enumerate(NAV_ITEMS, start=1):
            btn = customtkinter.CTkButton(
                self,
                text=label,
                anchor="w",
                height=NAV_BUTTON_HEIGHT,
                corner_radius=6,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=COLOR_NAV_HOVER,
                command=lambda name=page_name: self._handle_click(name),
            )
            btn.grid(row=idx, column=0, padx=8, pady=2, sticky="ew")
            self._buttons[page_name] = btn

        # Push remaining space to bottom
        self.grid_rowconfigure(len(NAV_ITEMS) + 1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _handle_click(self, page_name: str) -> None:
        """Handle nav button click — highlight and call callback."""
        self.set_active(page_name)
        self._on_navigate(page_name)

    def set_active(self, page_name: str) -> None:
        """Highlight the active page button, reset others."""
        self._active = page_name
        for name, btn in self._buttons.items():
            if name == page_name:
                btn.configure(fg_color=COLOR_NAV_ACTIVE)
            else:
                btn.configure(fg_color="transparent")
