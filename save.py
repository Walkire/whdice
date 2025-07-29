import tkinter as tk
from enums import TkType

test = []

def save():
    test_data = {"label": "Attacks:", "entry": tk.StringVar(), "default": "2d6", "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}}
    test.append(test_data)
    return test
     