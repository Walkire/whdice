import tkinter as tk
import re
from enums import TkType

SHORTHAND_NOTATION = r'^d(\d+)$'
DIE_NOTATION = r'^(\d+)d(\d+)([+-]\d+)?$'
def has_notation(dice):
    if isinstance(dice, int): return False
    return bool(re.match(SHORTHAND_NOTATION, dice, re.IGNORECASE) or re.match(DIE_NOTATION, dice, re.IGNORECASE))

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

def get_range(value):
    if not has_notation(value):
        return value
    
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