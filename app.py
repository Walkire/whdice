"""Main application window — CustomTkinter shell with sidebar navigation."""

import customtkinter

from state import AppState, TemplateManager
from state.autosave import AutoSave
from state.undo import UndoStack
from ui.sidebar import Sidebar
from ui.page_manager import PageManager
from ui.pages.attacker_page import AttackerPage
from ui.pages.defender_page import DefenderPage
from ui.pages.weapon_page import WeaponPage
from ui.pages.results_page import ResultsPage
from ui.pages.graph_page import GraphPage
from ui.pages.template_page import TemplatePage
from ui.pages.settings_page import SettingsPage


class App(customtkinter.CTk):
    """Warhammer Combat Simulator main window."""

    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Warhammer Combat Simulator")
        self.geometry("1200x800")
        customtkinter.set_appearance_mode("dark")

        # State
        self.app_state = AppState()
        self.undo_stack = UndoStack()
        self.app_state.set_undo_stack(self.undo_stack)

        # Auto-save: restore previous session state
        self._autosave = AutoSave()
        saved = self._autosave.load()
        if saved and isinstance(saved, dict) and "attacker" in saved:
            self.app_state.restore(saved)

        # Wire auto-save to state changes
        self.app_state.subscribe(self._on_state_change_autosave)

        # Layout: sidebar on left, page container fills remaining space
        self.grid_columnconfigure(0, weight=0, minsize=160)
        self.grid_columnconfigure(1, weight=1, minsize=600)
        self.grid_rowconfigure(0, weight=1, minsize=400)

        # Minimum window size
        self.minsize(800, 500)

        # Sidebar
        self.sidebar = Sidebar(self, on_navigate=self._show_page)
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        # Page container
        self._page_container = customtkinter.CTkFrame(self, corner_radius=0)
        self._page_container.grid(row=0, column=1, sticky="nsew")
        self._page_container.grid_columnconfigure(0, weight=1)
        self._page_container.grid_rowconfigure(0, weight=1)

        # Page manager
        self.page_manager = PageManager(self._page_container)

        # Register pages
        self._init_pages()

        # Show default page
        self._show_page("attacker")

        # Keyboard shortcuts
        self.bind("<Control-z>", self._on_undo)

    def _init_pages(self) -> None:
        """Create and register all application pages."""
        # Core pages
        self.page_manager.register(
            "attacker", AttackerPage(self._page_container, state=self.app_state)
        )
        self.page_manager.register(
            "defender", DefenderPage(self._page_container, state=self.app_state)
        )
        self.page_manager.register(
            "weapons", WeaponPage(
                self._page_container, state=self.app_state,
                on_edit_weapon=lambda: self._show_page("attacker"),
            )
        )
        self.page_manager.register(
            "results", ResultsPage(self._page_container, state=self.app_state)
        )

        # Graphs page
        self.page_manager.register(
            "graphs", GraphPage(self._page_container, state=self.app_state)
        )

        # Template Library page
        self.template_manager = TemplateManager()
        self.page_manager.register(
            "templates", TemplatePage(
                self._page_container, state=self.app_state,
                template_manager=self.template_manager,
                on_load_template=lambda: self._show_page("defender"),
            )
        )

        # Settings page
        self.page_manager.register(
            "settings", SettingsPage(self._page_container, state=self.app_state)
        )

    def _show_page(self, page_name: str) -> None:
        """Navigate to a page by name."""
        self.page_manager.show(page_name)
        self.sidebar.set_active(page_name)

    def _on_undo(self, event=None) -> None:
        """Handle Ctrl+Z — restore previous state from undo stack."""
        snapshot = self.undo_stack.pop()
        if snapshot is not None:
            self.app_state.restore(snapshot)

    def _on_state_change_autosave(self) -> None:
        """Save current state to disk on every state change."""
        self._autosave.save(self.app_state.snapshot())


if __name__ == "__main__":
    app = App()
    app.mainloop()
