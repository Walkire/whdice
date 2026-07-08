"""Page manager — handles showing/hiding pages in the main content area."""

import customtkinter


class PageManager:
    """Registers pages and ensures only one is visible at a time."""

    def __init__(self, container: customtkinter.CTkFrame):
        self._container = container
        self._pages: dict[str, customtkinter.CTkFrame] = {}
        self._current_page: str | None = None

    def register(self, name: str, page: customtkinter.CTkFrame) -> None:
        """Register a page frame. It starts hidden (grid_remove)."""
        self._pages[name] = page
        page.grid(row=0, column=0, sticky="nsew")
        page.grid_remove()

    def show(self, name: str) -> None:
        """Show the named page and hide all others."""
        if name not in self._pages:
            return
        for page_name, page in self._pages.items():
            if page_name == name:
                page.grid()
            else:
                page.grid_remove()
        self._current_page = name

        # Notify the page it's now visible (for lazy refresh)
        page = self._pages[name]
        if hasattr(page, "refresh"):
            page.refresh()

    @property
    def current_page(self) -> str | None:
        """Return the name of the currently visible page."""
        return self._current_page

    @property
    def pages(self) -> dict[str, customtkinter.CTkFrame]:
        """Return the registered pages dict."""
        return self._pages
