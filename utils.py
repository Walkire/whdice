import tkinter as tk
from enums import TkType


def get_var(entry):
    return entry.var() if hasattr(entry, "var") else entry

def build_form(fields, target_frame):
    # Build the form dynamically
    for field in fields:
        needs_label = True

        if field["type"] == TkType.ENTRY:
            entry = tk.Entry(target_frame, textvariable=get_var(field['entry']))

        elif field["type"] == TkType.CHECKBUTTON:
            entry = tk.Checkbutton(target_frame, text=field['label'], variable=get_var(field['entry']))
            needs_label = False

        elif field["type"] == TkType.OPTIONMENU:
            options = [opt.value for opt in field["options"]]
            entry = tk.OptionMenu(target_frame, get_var(field['entry']), *options)

        if needs_label:
            label = tk.Label(target_frame, text=field['label'])
            label_style = field.get('label_style', field.get('style', {}))
            label.grid(**label_style)

        entry_style = field.get('entry_style', field.get('style', {}))
        entry.grid(**entry_style)