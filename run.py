import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sim_functions import calc_hits, calc_damage, calc_to_wound, calc_attacks, calc_saves, calc_kills, calc_wounds, calc_feel_no_pain, calc_sustained_hits
from enums import RerollType
from classes.attacker import Attacker
from classes.defender import Defender
from utils import build_weapon_string

ATTACKER = None
DEFENDER = None
WEAPONS = []
WEAPON_LIST = None

DRAG_INDEX = None
WEAPON_LISTBOX = None

SIMULATIONS = 100000

def run_simulation():
    global WEAPONS
    
    try:
        if not (ATTACKER or WEAPONS) or not DEFENDER:
            raise Exception("No unit data was found")

        UNITS_WIPED = 0
        previous_dice = 0
        
        results = []

        weapons_to_use = WEAPONS if WEAPONS else [ATTACKER.getValues()]
        
        for i, weapon in enumerate(weapons_to_use):
            results.append({
                "id": i,
                "to_wound": 0,
                "attacks": 0,
                "hits": 0,
                "wounds": 0,
                "saves": 0,
                "damage": 0,
                "fnp": 0,
                "kills": 0,
                "sustained": 0,
                "crit_hit": 0,
                "crit_wound": 0,
                "weapon": weapon
            })

        for _ in range(SIMULATIONS):
            last_remainder = 0
            total_kills = 0
            for i, weapon in enumerate(weapons_to_use):
                added_saves = 0
                added_wounds = 0
                added_damage = 0
                
                results[i]["to_wound"] = calc_to_wound(weapon.strength, DEFENDER.toughness, weapon.plus_wound, DEFENDER.minus_wound)
                     
                # calc attacks
                previous_dice = calc_attacks(weapon.attacks)
                if weapon.blast:
                        previous_dice += int((DEFENDER.model_count / 5) // 1)
                results[i]["attacks"] += previous_dice
                
                # calc hits
                if not weapon.torrent:
                    previous_dice, crits = calc_hits(
                        atk=previous_dice,
                        score=weapon.score,
                        reroll_hit=weapon.reroll_hits == RerollType.REROLL_ALL.value,
                        reroll_hit_one=weapon.reroll_hits == RerollType.REROLL_ONE.value,
                        crit_hit=weapon.critical_hit,
                        plus_hit=weapon.plus_hit
                    )

                    # calc special crits
                    if weapon.sustained_hits != "0":
                        added_wounds = calc_sustained_hits(crits, weapon.sustained_hits)
                        results[i]["sustained"] += added_wounds
                    results[i]["hits"] += previous_dice
                    if weapon.lethal_hits:
                        added_saves = crits
                        previous_dice -= crits
                        
                    results[i]["crit_hit"] += crits                
                
                # calc wound
                previous_dice, crits = calc_wounds(
                    hits=previous_dice + added_wounds, 
                    to_wound=results[i]["to_wound"],
                    reroll_wound=weapon.reroll_wounds == RerollType.REROLL_ALL.value, 
                    reroll_wound_one=weapon.reroll_wounds == RerollType.REROLL_ONE.value, 
                    crit_wound=weapon.critical_wound
                )
                results[i]["wounds"] += previous_dice
                if weapon.devestating_wounds:
                    added_damage = crits
                    previous_dice -= crits
                results[i]["crit_wound"] += crits
                
                # calc save
                previous_dice, crits = calc_saves(
                    wounds=previous_dice + added_saves, 
                    save=DEFENDER.save, 
                    invuln=DEFENDER.invuln, 
                    ap=weapon.ap,
                    plus_save=DEFENDER.plus_save
                )
                results[i]["saves"] += previous_dice
                
                # calc damage
                previous_dice = calc_damage(
                    amt=previous_dice + added_damage, 
                    damage=weapon.damage,
                    return_as_list=True,
                    minus_damage=DEFENDER.minus_damage,
                    reroll_damage=weapon.reroll_damage
                )
                results[i]["damage"] += sum(previous_dice)

                #calc feel no pain
                previous_dice = calc_feel_no_pain(
                    damage=previous_dice,
                    fnp=DEFENDER.feel_no_pain
                )
                results[i]["fnp"] += sum(previous_dice)
                
                # calc kills
                previous_dice, last_remainder = calc_kills(
                    dmg_list=previous_dice,
                    wounds=DEFENDER.wounds,
                    remainder=last_remainder)
                results[i]["kills"] += previous_dice
                
                total_kills += previous_dice
            
            if total_kills >= DEFENDER.model_count:
                UNITS_WIPED += 1
            
        # Display results
        result_window = tk.Toplevel()
        result_window.title("Simulation Results")

        #Summary Table
        columns = ("Name", "Attacks", "Hits", "Wounds", "After Saves", "Damage", "After FNP", "Kills")
        tree = ttk.Treeview(result_window, columns=columns, show="headings", height=5)
        tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=90)

        wipe_percent = round(UNITS_WIPED / SIMULATIONS * 100, 2) if UNITS_WIPED > 0 else 0

        for i, r in enumerate(results):
            row_data = (
                r["weapon"].name if r["weapon"].name else "-",
                round(r["attacks"] / SIMULATIONS, 2),
                "N/A" if r["weapon"].torrent else round(r["hits"] / SIMULATIONS, 2),
                round(r["wounds"] / SIMULATIONS, 2),
                round(r["saves"] / SIMULATIONS, 2),
                round(r["damage"] / SIMULATIONS, 2),
                round(r["fnp"] / SIMULATIONS, 2) if DEFENDER.feel_no_pain else "-",
                round(r["kills"] / SIMULATIONS, 2) if DEFENDER.model_count > 1 else "-",
            )
            tree.insert("", "end", iid=str(i), values=row_data)

        #Details Section
        details = tk.Text(result_window, wrap="word", height=10, width=70, padx=5, pady=5)
        details.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Default details (global summary)
        global_summary = f"Chance unit is killed:\n----------------------\n{wipe_percent}%"
        details.insert("end", global_summary)
        details.config(state="disabled", font=("Consolas", 11))

        def show_details(event):
            selected = tree.selection()
            if not selected:
                return

            weapon_id = int(selected[0])
            weapon_result = results[weapon_id]

            details.config(state="normal")
            details.delete("1.0", tk.END)

            details_message = f"{global_summary}\n\n"
            if weapon_result['weapon'].name:
                details_message += f"Weapon: {weapon_result['weapon'].name}\n"
            details_message += f"-- With {weapon_result['to_wound']} to wound --\n"
            if weapon_result["weapon"].sustained_hits and weapon_result["weapon"].sustained_hits != "0":
                details_message += f"Sustained Hits: {weapon_result['sustained'] / SIMULATIONS:.2f}\n"
            if weapon_result["weapon"].lethal_hits:
                details_message += f"Lethal Hits: {weapon_result['crit_hit'] / SIMULATIONS:.2f}\n"
            if weapon_result["weapon"].devestating_wounds:
                details_message += f"Devastating Wounds: {weapon_result['crit_wound'] / SIMULATIONS:.2f}\n"
            if weapon_result["weapon"].blast:
                details_message += f"Blast: {int((DEFENDER.model_count / 5) // 1)} extra attacks\n"
            
            details.insert("end", details_message)
            details.config(state="disabled")

        tree.bind("<<TreeviewSelect>>", show_details)

        # Make window resizable
        result_window.grid_rowconfigure(1, weight=1)
        result_window.grid_columnconfigure(0, weight=1)

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
    ATTACKER.resetValues()

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

# Start Tkinter main loop
window.mainloop()