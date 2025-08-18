import tkinter as tk
from tkinter import ttk
import re
from enums import TkType
from classes.data import Data

DIE_NOTATION = r'^(\d*)d(\d+)([+-]\d+)?$'
def has_notation(dice):
    return bool(re.match(DIE_NOTATION, str(dice), re.IGNORECASE))

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
            entry = tk.OptionMenu(target_frame, get_var(field['entry']), *options)
            
        elif field["type"] == TkType.LISTBOX:
            variables = tk.Variable(value=get_var(field['entry']))
            entry = ttk.Listbox(target_frame, listvariable=variables)

        if needs_label:
            label = ttk.Label(target_frame, text=field['label'])
            label_style = field.get('label_style', field.get('style', {}))
            label.grid(**label_style)

        entry_style = field.get('entry_style', field.get('style', {}))
        entry.grid(**entry_style)

def build_weapon_string(weapon: Data):
    if weapon.name:
        return f"{weapon.name}"

    return (
        f"A: {weapon.attacks} | "
        f"WS: {weapon.score} | "
        f"S: {weapon.strength} | "
        f"AP: {weapon.ap} | "
        f"D: {weapon.damage}"
    )

def get_range(value):
    if not has_notation(value):
        return value
    if not isinstance(value, str):
        value = str(value)
    
    match = re.match(DIE_NOTATION, value.strip())
    if not match:
        raise ValueError("Invalid dice notation. Try formats like 'd4', '2d6+1', or '1d8-2'")

    num_dice = int(match.group(1)) if match.group(1) else 1
    num_sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0

    min_roll = num_dice * 1 + modifier
    max_roll = num_dice * num_sides + modifier

    return min_roll, max_roll

def bad_roll(roll, notation, threshold) -> bool:
    if not has_notation(notation):
        return None
    
    range_min, range_max = get_range(notation)
    range_size = range_max - range_min + 1
    cutoff = int(range_size * threshold)
    
    return roll <= (range_min + cutoff - 1)
