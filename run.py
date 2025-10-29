import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from classes.attacker import Attacker
from classes.defender import Defender
from utils import build_weapon_string, format_weapon_details, load_templates
from simulation import simulate

ATTACKER = None
DEFENDER = None
WEAPONS = []
WEAPON_LIST = None

DRAG_INDEX = None
WEAPON_LISTBOX = None

SIMULATIONS = 100000

# Generic reusable result viewer.
# - title: string window title
# - columns: list of column names
# - rows: list of tuples or dicts (each one row of data)
# - detail_callback: function(tree, details_widget, selection) -> None

def show_results_window(title, columns, rows, detail_callback):
    result_window = tk.Toplevel()
    result_window.title(title)

    tree = ttk.Treeview(result_window, columns=columns, show="headings", height=8)
    tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # Configure sorting behavior
    def sort_column(col, reverse=False):
        # Extract data and sort
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        try:
            data.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data.sort(key=lambda t: t[0], reverse=reverse)

        # Reorder tree items
        for index, (_, iid) in enumerate(data):
            tree.move(iid, "", index)

        # Toggle next sort direction
        tree.heading(col, command=lambda: sort_column(col, not reverse))

    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: sort_column(_col, False))
        tree.column(col, anchor="center", width=120)

    # Insert rows
    for i, row in enumerate(rows):
        if isinstance(row, dict):
            values = [row.get(col, "-") for col in columns]
        else:
            values = row
        tree.insert("", "end", iid=str(i), values=values)

    # Details panel
    details = tk.Text(result_window, wrap="word", height=10, width=70, padx=5, pady=5)
    details.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    details.config(state="disabled", font=("Consolas", 11))

    def on_select(event):
        selected = tree.selection()
        if not selected:
            return
        selection_id = int(selected[0])
        detail_callback(tree, details, selection_id)

    tree.bind("<<TreeviewSelect>>", on_select)

    result_window.grid_rowconfigure(1, weight=1)
    result_window.grid_columnconfigure(0, weight=1)

    return result_window

def run_simulation():
    global WEAPONS, ATTACKER, SIMULATIONS

    try:
        if not (ATTACKER or WEAPONS) or not DEFENDER:
            raise Exception("No unit data was found")

        results, wipe_percent = simulate(ATTACKER, DEFENDER, WEAPONS, SIMULATIONS)

        # Setup data
        columns = ("Name", "Attacks", "Hits", "Wounds", "After Saves", "Damage", "After FNP", "Kills")
        rows = [
            (
                r["weapon"].name if r["weapon"].name else "-",
                round(r["attacks"] / SIMULATIONS, 2),
                "N/A" if r["weapon"].torrent else round(r["hits"] / SIMULATIONS, 2),
                round(r["wounds"] / SIMULATIONS, 2),
                round(r["saves"] / SIMULATIONS, 2),
                round(r["damage"] / SIMULATIONS, 2),
                round(r["fnp"] / SIMULATIONS, 2) if DEFENDER.feel_no_pain else "-",
                round(r["kills"] / SIMULATIONS, 2) if DEFENDER.model_count > 1 else "-",
            )
            for r in results
        ]

        def show_weapon_details(tree, details, selection_id):
            text = format_weapon_details(results, DEFENDER, wipe_percent, SIMULATIONS)
            details.config(state="normal")
            details.delete("1.0", tk.END)
            details.insert("end", text)
            details.config(state="disabled")

        show_results_window("Simulation Results", columns, rows, show_weapon_details)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Line: {e.__traceback__.tb_lineno} - {str(e)}")

        
def compare_templates():
    global ATTACKER, WEAPONS, SIMULATIONS
    try:
        templates = load_templates()
        if not templates:
            raise Exception("No templates found in /templates/ folder.")
        if not (ATTACKER or WEAPONS):
            raise Exception("No attacker or weapon data found")

        summary = []
        for data in templates:
            defender = Defender() # Dont include UI for headless
            for k, v in data.items():
                setattr(defender, k, v)
            results, wipe_percent = simulate(ATTACKER, defender, WEAPONS, SIMULATIONS)
            avg_kills = sum(r["kills"] for r in results) / len(results) / SIMULATIONS
            dmg = sum(r["damage"] for r in results) / len(results) / SIMULATIONS
            summary.append({
                "name": data.get("name", "Unnamed Template"),
                "wipe": wipe_percent,
                "dmg": dmg,
                "avg": avg_kills,
                "details": results
            })

        columns = ("Template", "Avg Kills", "Dmg", "Wipe %")
        rows = [(s["name"], round(s["avg"], 2), round(s["dmg"], 2), s["wipe"]) for s in summary]

        def show_template_details(tree, details, selection_id):
            res = summary[selection_id]
            details.config(state="normal")
            details.delete("1.0", tk.END)
            # Build a fake Defender for display so we can show correct wound/model data
            defender = Defender()
            for key, value in templates[selection_id].items():
                setattr(defender, key, value)
            text = format_weapon_details(res["details"], defender, res["wipe"], SIMULATIONS)
            details.insert("end", text)
            details.config(state="disabled")

        show_results_window("Template Comparison", columns, rows, show_template_details)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Line: {e.__traceback__.tb_lineno} - {str(e)}")
         
def refresh_weapon_list():
    # Rebuilds the Listbox display from WEAPONS
    display_strings = [build_weapon_string(wpn) for wpn in WEAPONS]
    WEAPON_LIST.set(display_strings)

def save_attacker():
    # Add the current attacker weapon config to the WEAPONS list and refresh UI
    current_weapon = ATTACKER.getValues()
    WEAPONS.append(current_weapon)
    refresh_weapon_list()

def delete_selected_weapon():
    # Remove selected weapon(s) from WEAPONS list and refresh UI
    selected_indices = WEAPON_LISTBOX.curselection()
    if not selected_indices:
        return
    for index in reversed(selected_indices):
        del WEAPONS[index]
    refresh_weapon_list()

def on_drag_start(event):
    global DRAG_INDEX
    DRAG_INDEX = event.widget.nearest(event.y)

def on_drag_motion(event):
    index = event.widget.nearest(event.y)
    event.widget.selection_clear(0, tk.END)
    event.widget.selection_set(index)

def on_drag_drop(event):
    global DRAG_INDEX
    drag_end_index = event.widget.nearest(event.y)
    if DRAG_INDEX is None or drag_end_index == DRAG_INDEX:
        return
    WEAPONS.insert(drag_end_index, WEAPONS.pop(DRAG_INDEX))
    refresh_weapon_list()
    event.widget.selection_clear(0, tk.END)
    event.widget.selection_set(drag_end_index)
    DRAG_INDEX = None
    
# Create a Tkinter window
window = tk.Tk()
window.title("Warhammer Combat Simulator")

# Create frames for grouping
attacker_frame = ttk.LabelFrame(window, text="Attacker")
attacker_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

attacker_mod_frame = ttk.LabelFrame(window, text="Attack Modifiers")
attacker_mod_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nw')

defender_frame = ttk.LabelFrame(window, text="Defender")
defender_frame.grid(row=0, column=2, padx=10, pady=10, sticky='ne')

defender_mod_frame = ttk.LabelFrame(window, text="Defender Modifiers")
defender_mod_frame.grid(row=0, column=3, padx=10, pady=10, sticky='ne')

simulation_frame = ttk.LabelFrame(window, text="Simulations")
simulation_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nw')

WEAPON_LIST = tk.Variable(value=[])
WEAPON_LISTBOX = tk.Listbox(simulation_frame, listvariable=WEAPON_LIST, height=8, width=40)
WEAPON_LISTBOX.grid(row=0, column=0, padx=5, pady=5, sticky='w')

WEAPON_LISTBOX.bind("<Button-1>", on_drag_start)
WEAPON_LISTBOX.bind("<B1-Motion>", on_drag_motion)
WEAPON_LISTBOX.bind("<ButtonRelease-1>", on_drag_drop)

button_frame = ttk.Frame(simulation_frame)
button_frame.grid(row=1, column=0, padx=5, pady=2, sticky='w')

save_button = ttk.Button(button_frame, text="Save", command=save_attacker)
save_button.pack(side='left', padx=(0, 4))

delete_button = ttk.Button(button_frame, text="Delete", command=delete_selected_weapon)
delete_button.pack(side='left')

ATTACKER = Attacker(attacker_frame, attacker_mod_frame)
DEFENDER = Defender(defender_frame, defender_mod_frame)

# Add simulation button
run_button = ttk.Button(window, text="Run Simulation", command=run_simulation)
run_button.grid(row=1, column=3, columnspan=1, pady=10)

# Add simulation button
run_button = ttk.Button(window, text="Check Templates", command=compare_templates)
run_button.grid(row=1, column=2, columnspan=1, pady=10)

# Start Tkinter main loop
window.mainloop()