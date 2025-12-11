import tkinter as tk
from tkinter import ttk
import re
from enums import TkType
from classes.data import Data
import os, json

DIE_NOTATION = r'^(\d*)d(\d+)([+-]\d+)?$'
def has_notation(dice):
    return bool(re.match(DIE_NOTATION, str(dice), re.IGNORECASE))

def get_var(entry):
    return entry.var() if hasattr(entry, "var") else entry

# fields
# label: String label for the field
# entry (required): value for the field
# exclude: removes value from options menu
# depends_on: Tkinter variable that enables/disables field based on its value
# type (required): Tk field type
# style: object, styles to apply to the field
def build_form(fields, target_frame):
    widgets = []
    conditional_widgets = {}
    
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
            exclude = field.get("exclude", [])
            if exclude:
                options = [opt.value for opt in field["options"] if opt not in exclude]
            else:
                options = [opt.value for opt in field["options"]]
            entry = tk.OptionMenu(target_frame, get_var(field['entry']), *options)
            
        elif field["type"] == TkType.LISTBOX:
            variables = tk.Variable(value=get_var(field['entry']))
            entry = ttk.Listbox(target_frame, listvariable=variables)

        if needs_label:
            label = ttk.Label(target_frame, text=field['label'])
            label_style = field.get('label_style', field.get('style', {}))
            label.grid(**label_style)
            widgets.append(label)

        entry_style = field.get('entry_style', field.get('style', {}))
        entry.grid(**entry_style)
        widgets.append(entry)
        
        # Handle conditional enable/disable
        if 'depends_on' in field:
            depends_on = field['depends_on']
            key = id(depends_on)
            if key not in conditional_widgets:
                conditional_widgets[key] = {'obj': depends_on, 'widgets': []}
            conditional_widgets[key]['widgets'].append(entry)
            entry.config(state='disabled')
    
    return widgets, conditional_widgets

def toggle_field_state(conditional_widgets, field_obj, enabled):
    key = id(field_obj)
    if key in conditional_widgets:
        state = 'normal' if enabled else 'disabled'
        for widget in conditional_widgets[key]['widgets']:
            widget.config(state=state)

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

# Returns formatted text showing full per-weapon breakdown
def format_weapon_details(results, defender, wipe_percent, simulations):
    lines = []
    lines.append(f"Chance unit is killed:\n----------------------\n{wipe_percent}%\n")

    for r in results:
        weapon = r["weapon"]
        name = weapon.name if weapon.name else "-"
        lines.append(f"Weapon: {name}")
        lines.append(f"{r['to_hit'] / simulations:.0f}+ to hit")
        lines.append(f"{r['to_wound']}+ to wound")
        lines.append(f"{r['to_save'] / simulations:.0f}+ to save")
        lines.append(f"----------------\n")

        if weapon.sustained_hits and weapon.sustained_hits != "0":
            lines.append(f"Sustained Hits: {r['sustained'] / simulations:.2f}")
        if weapon.lethal_hits:
            lines.append(f"Lethal Hits: {r['crit_hit'] / simulations:.2f}")
        if weapon.devestating_wounds:
            lines.append(f"Devastating Wounds: {r['crit_wound'] / simulations:.2f}")
        if weapon.blast:
            lines.append(f"Blast: {int((defender.model_count / 5) // 1)} extra attacks")

        fnp_value = f"{r['fnp'] / simulations:.2f}" if defender.feel_no_pain else "-"
        kills_value = f"{r['kills'] / simulations:.2f}" if defender.model_count > 1 else "-"

        lines.append(
            f"Attacks: {r['attacks'] / simulations:.2f}\n"
            f"Hits: {'N/A' if weapon.torrent else round(r['hits'] / simulations, 2)}\n"
            f"Wounds: {r['wounds'] / simulations:.2f}\n"
            f"Failed Saves: {r['saves'] / simulations:.2f}\n"
            f"Damage: {r['damage'] / simulations:.2f}\n"
            f"After FNP: {fnp_value}\n"
            f"Kills: {kills_value}"
        )

    return "\n".join(lines)

def load_templates(folder="templates"):
    templates = []
    if not os.path.exists(folder):
        os.makedirs(folder)
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            path = os.path.join(folder, filename)
            with open(path, "r") as f:
                data = json.load(f)
                templates.append(data)
    return templates
