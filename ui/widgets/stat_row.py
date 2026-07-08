"""StatRow — a reusable row widget displaying a label and an input (entry, checkbox, or dropdown)."""

from typing import Any, List, Optional, Callable
import customtkinter


class StatRow(customtkinter.CTkFrame):
    """Single row showing a label and an input widget.

    Supports three widget_type variants:
      - "entry": text/number input
      - "checkbox": boolean toggle
      - "dropdown": option menu from a list of choices
    """

    def __init__(
        self,
        master,
        label: str,
        widget_type: str = "entry",
        options: Optional[List[str]] = None,
        default: Any = None,
        on_change: Optional[Callable] = None,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._widget_type = widget_type
        self._on_change = on_change

        # Layout: label on left, widget on right
        self.grid_columnconfigure(1, weight=1)

        self._label = customtkinter.CTkLabel(self, text=label, anchor="w")
        self._label.grid(row=0, column=0, padx=(0, 8), pady=2, sticky="w")

        if widget_type == "entry":
            self._var = customtkinter.StringVar(value=str(default) if default is not None else "")
            self._widget = customtkinter.CTkEntry(self, textvariable=self._var, width=120)
            if on_change:
                self._var.trace_add("write", lambda *_: self._on_entry_change())
        elif widget_type == "checkbox":
            self._var = customtkinter.BooleanVar(value=bool(default) if default is not None else False)
            self._widget = customtkinter.CTkCheckBox(self, text="", variable=self._var, width=24)
            if on_change:
                self._widget.configure(command=on_change)
        elif widget_type == "dropdown":
            options = options or []
            default_val = str(default) if default is not None else (options[0] if options else "")
            self._var = customtkinter.StringVar(value=default_val)
            self._widget = customtkinter.CTkOptionMenu(
                self, variable=self._var, values=options, width=140
            )
            if on_change:
                self._widget.configure(command=lambda _: on_change())
        else:
            raise ValueError(f"Unknown widget_type: {widget_type!r}")

        self._widget.grid(row=0, column=1, padx=(0, 0), pady=2, sticky="w")

    def get_value(self) -> Any:
        """Return the current value (str for entry/dropdown, bool for checkbox)."""
        if self._widget_type == "checkbox":
            return self._var.get()
        return self._var.get()

    def _on_entry_change(self) -> None:
        """Fire on_change when the entry value changes."""
        if self._on_change:
            self._on_change()

    def set_value(self, value: Any) -> None:
        """Set the current value."""
        if self._widget_type == "checkbox":
            self._var.set(bool(value))
        else:
            self._var.set(str(value))

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the input widget."""
        state = "normal" if enabled else "disabled"
        self._widget.configure(state=state)
