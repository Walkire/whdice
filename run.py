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
        if not ATTACKER or not DEFENDER:
            raise Exception("No unit data was found")

        #VARS
        # Used for final average calculations
        AVERAGE_ATTACKS = 0
        AVERAGE_HITS = 0
        AVERAGE_WOUNDS = 0
        AVERAGE_SAVES = 0
        AVERAGE_DAMAGE = 0
        AVERAGE_KILLS = 0
        AVERAGE_FEEL_NO_PAIN = 0
        AVERAGE_SUSTAINED_HITS = 0
        
        UNITS_WIPED = 0
        
        AVERAGE_CRIT_HIT = 0
        AVERAGE_CRIT_WOUND = 0

        previous_dice = 0

        weapons_to_use = WEAPONS if WEAPONS else [ATTACKER.getValues()]

        for _ in range(SIMULATIONS):
            for weapon in weapons_to_use:
                added_saves = 0
                added_wounds = 0
                added_damage = 0
                last_remainder = 0
                total_kills = 0
                
                TO_WOUND = calc_to_wound(weapon.strength, DEFENDER.toughness, weapon.plus_wound, DEFENDER.minus_wound)
                     
                # calc attacks
                previous_dice = calc_attacks(weapon.attacks)
                if weapon.blast:
                        previous_dice += int((DEFENDER.model_count / 5) // 1)
                AVERAGE_ATTACKS += previous_dice
                
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
                        AVERAGE_SUSTAINED_HITS += added_wounds
                    AVERAGE_HITS += previous_dice
                    if weapon.lethal_hits:
                        added_saves = crits
                        previous_dice -= crits
                        
                    AVERAGE_CRIT_HIT += crits                
                
                # calc wound
                previous_dice, crits = calc_wounds(
                    hits=previous_dice + added_wounds, 
                    to_wound=TO_WOUND,
                    reroll_wound=weapon.reroll_wounds == RerollType.REROLL_ALL.value, 
                    reroll_wound_one=weapon.reroll_wounds == RerollType.REROLL_ONE.value, 
                    crit_wound=weapon.critical_wound
                )
                AVERAGE_WOUNDS += previous_dice
                if weapon.devestating_wounds:
                    added_damage = crits
                    previous_dice -= crits
                AVERAGE_CRIT_WOUND += crits
                
                # calc save
                previous_dice, crits = calc_saves(
                    wounds=previous_dice + added_saves, 
                    save=DEFENDER.save, 
                    invuln=DEFENDER.invuln, 
                    ap=weapon.ap,
                    plus_save=DEFENDER.plus_save
                )
                AVERAGE_SAVES += previous_dice
                
                # calc damage
                previous_dice = calc_damage(
                    amt=previous_dice + added_damage, 
                    damage=weapon.damage,
                    return_as_list=True,
                    minus_damage=DEFENDER.minus_damage,
                    reroll_damage=weapon.reroll_damage
                )
                AVERAGE_DAMAGE += sum(previous_dice)

                #calc feel no pain
                previous_dice = calc_feel_no_pain(
                    damage=previous_dice,
                    fnp=DEFENDER.feel_no_pain
                )
                AVERAGE_FEEL_NO_PAIN += sum(previous_dice)
                
                # calc kills
                previous_dice, last_remainder = calc_kills(
                    dmg_list=previous_dice,
                    wounds=DEFENDER.wounds,
                    remainder=last_remainder)
                AVERAGE_KILLS += previous_dice
                
                total_kills += previous_dice

            if total_kills >= DEFENDER.model_count:
                UNITS_WIPED += 1
            
        # Display results using messagebox
        message = f"with {TO_WOUND} to wound\n"
        message += "-------------\n"
        if ATTACKER.blast:
            message += f"Attacks - {round(AVERAGE_ATTACKS / SIMULATIONS, 2)} (+blast)\n"
        else:
            message += f"Attacks - {round(AVERAGE_ATTACKS / SIMULATIONS, 2)}\n"
        if ATTACKER.torrent:
            message += f"Hits - N/A (Torrent)\n"
        elif ATTACKER.sustained_hits != "0":
            message += f"Hits - {round(AVERAGE_HITS / SIMULATIONS, 2)} (+{round(AVERAGE_SUSTAINED_HITS / SIMULATIONS, 2)} sustained hits)\n"
        elif ATTACKER.lethal_hits:
            message += f"Hits - {round(AVERAGE_HITS / SIMULATIONS, 2)} (+{round(AVERAGE_CRIT_HIT / SIMULATIONS, 2)} crits + {round(added_saves / SIMULATIONS, 2)} lethal hits)\n"
        else:
            message += f"Hits - {round(AVERAGE_HITS / SIMULATIONS, 2)}\n"
        if ATTACKER.devestating_wounds:
            message += f"Wounds - {round(AVERAGE_WOUNDS / SIMULATIONS, 2)} ({round(AVERAGE_CRIT_WOUND / SIMULATIONS, 2)} Dev)\n"
        else:
            message += f"Wounds - {round(AVERAGE_WOUNDS / SIMULATIONS, 2)}\n"
        message += f"Failed Saves - {round(AVERAGE_SAVES / SIMULATIONS, 2)}\n"
        message += f"Damage - {round(AVERAGE_DAMAGE / SIMULATIONS, 2)}\n"
        if DEFENDER.feel_no_pain:
            message += f"Damage after FNP - {round(AVERAGE_FEEL_NO_PAIN / SIMULATIONS, 2)}\n"
        if DEFENDER.model_count > 1:
            message += f"Kills - {round(AVERAGE_KILLS / SIMULATIONS, 2)}\n"
        if UNITS_WIPED > 0:
            message += "-------------\n"
            message += f"Percent chance unit dies - {round(UNITS_WIPED / SIMULATIONS * 100, 2)}%\n"
        messagebox.showinfo("Simulation Results", message)
        
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

delete_button = ttk.Button(simulation_frame, text="Delete", command=delete_selected_weapon)
delete_button.grid(row=1, column=0, padx=5, pady=2, sticky='w')

ATTACKER = Attacker(attacker_frame, attacker_mod_frame)
DEFENDER = Defender(defender_frame, defender_mod_frame)

# Add simulation button
run_button = ttk.Button(window, text="Run Simulation", command=run_simulation)
run_button.grid(row=1, column=3, columnspan=1, pady=10)

save_button = ttk.Button(window, text="Save", command=save_attacker)
save_button.grid(row=1, column=2, columnspan=1, pady=10)

# Start Tkinter main loop
window.mainloop()