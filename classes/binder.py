import tkinter as tk

class TinkerBinder:
    def __init__(self, var_type, value=None):
        self._var = var_type()
        if value is not None:
            self._var.set(value)

    def get(self):
        return self._var.get()

    def set(self, value):
        self._var.set(value)

    def var(self):
        return self._var

    def __int__(self):
        return int(self._var.get())

    def __float__(self):
        return float(self._var.get())

    def __str__(self):
        return str(self._var.get())

    # Delegate all other attribute access to the underlying tk.Variable
    def __getattr__(self, attr):
        return getattr(self._var, attr)


