"""KeywordSelector — dropdown selectors for reroll types and modifiers."""

from typing import Callable, Dict, List, Optional
import customtkinter


class KeywordSelector(customtkinter.CTkFrame):
    """A set of dropdown selectors for reroll types and modifiers.

    Parameters
    ----------
    keywords : dict[str, list[str]]
        Mapping of keyword label -> list of option values.
        Example: {"Reroll Hits": ["None", "Reroll Ones", "Reroll All", "Fish Rolls"]}
    """

    def __init__(
        self,
        master,
        keywords: Dict[str, List[str]],
        on_change: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._on_change = on_change
        self._menus: Dict[str, customtkinter.CTkOptionMenu] = {}
        self._vars: Dict[str, customtkinter.StringVar] = {}

        # Section label
        label = customtkinter.CTkLabel(
            self, text="Keywords & Modifiers", font=customtkinter.CTkFont(weight="bold")
        )
        label.grid(row=0, column=0, columnspan=2, pady=(4, 4), sticky="w")

        self.grid_columnconfigure(1, weight=1)

        for idx, (keyword_label, options) in enumerate(keywords.items(), start=1):
            lbl = customtkinter.CTkLabel(self, text=keyword_label, anchor="w")
            lbl.grid(row=idx, column=0, padx=(0, 8), pady=3, sticky="w")

            var = customtkinter.StringVar(value=options[0] if options else "")
            menu = customtkinter.CTkOptionMenu(
                self,
                variable=var,
                values=options,
                width=150,
            )
            if on_change:
                menu.configure(command=lambda _, cb=on_change: cb())
            menu.grid(row=idx, column=1, padx=(0, 0), pady=3, sticky="w")

            self._vars[keyword_label] = var
            self._menus[keyword_label] = menu

    def get_selections(self) -> Dict[str, str]:
        """Return current selections as a dict of label -> selected value."""
        return {label: var.get() for label, var in self._vars.items()}

    def set_selections(self, selections: Dict[str, str]) -> None:
        """Set dropdown values from a dict. Keys not present are left unchanged."""
        for label, value in selections.items():
            if label in self._vars:
                self._vars[label].set(value)
