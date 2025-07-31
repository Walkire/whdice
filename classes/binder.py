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

    # Type coercion
    def __int__(self):
        return int(self._var.get())

    def __float__(self):
        return float(self._var.get())

    def __str__(self):
        return str(self._var.get())
    
    def __bool__(self):
        return bool(self._var.get())
    
    # Conditionals
    def __eq__(self, other):
        return self.get() == (other.get() if isinstance(other, TinkerBinder) else other)

    def __ne__(self, other):
        return self.get() != (other.get() if isinstance(other, TinkerBinder) else other)

    def __lt__(self, other):
        return self.get() < (other.get() if isinstance(other, TinkerBinder) else other)

    def __le__(self, other):
        return self.get() <= (other.get() if isinstance(other, TinkerBinder) else other)

    def __gt__(self, other):
        return self.get() > (other.get() if isinstance(other, TinkerBinder) else other)

    def __ge__(self, other):
        return self.get() >= (other.get() if isinstance(other, TinkerBinder) else other)
    
    # Arithmetic operations
    def __add__(self, other):
        return self.get() + (other.get() if isinstance(other, TinkerBinder) else other)

    def __sub__(self, other):
        return self.get() - (other.get() if isinstance(other, TinkerBinder) else other)

    def __mul__(self, other):
        return self.get() * (other.get() if isinstance(other, TinkerBinder) else other)

    def __truediv__(self, other):
        return self.get() / (other.get() if isinstance(other, TinkerBinder) else other)

    def __floordiv__(self, other):
        return self.get() // (other.get() if isinstance(other, TinkerBinder) else other)

    def __mod__(self, other):
        return self.get() % (other.get() if isinstance(other, TinkerBinder) else other)

    def __pow__(self, other):
        return self.get() ** (other.get() if isinstance(other, TinkerBinder) else other)

    # Reverse operations
    def __radd__(self, other):
        return other + self.get()

    def __rsub__(self, other):
        return other - self.get()

    def __rmul__(self, other):
        return other * self.get()

    def __rtruediv__(self, other):
        return other / self.get()

    def __rfloordiv__(self, other):
        return other // self.get()

    def __rmod__(self, other):
        return other % self.get()

    def __rpow__(self, other):
        return other ** self.get()
    
    # Delegate all other attribute access to the underlying tk.Variable
    def __getattr__(self, attr):
        return getattr(self._var, attr)
    
    # For debugging
    def __repr__(self):
        return f"TinkerBinder({repr(self.get())})"
