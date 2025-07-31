from tkinter import ttk
from enums import TkType
from classes.data import Data

def get_var(entry):
    return entry.var() if hasattr(entry, "var") else entry

# fields
# label: String label for the field
# entry: value for the field
# type: Tk field type
# style: object, styles to apply to the field
def build_form(fields, target_frame):
    # Build the form dynamically
    for field in fields:
        needs_label = True
        
        if field["type"] == TkType.LABEL:
            entry = ttk.Label(target_frame, text=get_var(field['entry']))

        elif field["type"] == TkType.ENTRY:
            entry = ttk.Entry(target_frame, textvariable=get_var(field['entry']))

        elif field["type"] == TkType.CHECKBUTTON:
            entry = ttk.Checkbutton(target_frame, text=field['label'], variable=get_var(field['entry']))
            needs_label = False

        elif field["type"] == TkType.OPTIONMENU:
            options = [opt.value for opt in field["options"]]
            entry = ttk.OptionMenu(target_frame, get_var(field['entry']), *options)

        if needs_label:
            label = ttk.Label(target_frame, text=field['label'])
            label_style = field.get('label_style', field.get('style', {}))
            label.grid(**label_style)

        entry_style = field.get('entry_style', field.get('style', {}))
        entry.grid(**entry_style)

def build_weapon_string(weapon: Data):
    return (
        f"A: {weapon.attacks} | "
        f"WS: {weapon.score} | "
        f"S: {weapon.strength} | "
        f"AP: {weapon.ap} | "
        f"D: {weapon.damage}"
    )