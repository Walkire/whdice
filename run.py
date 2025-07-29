import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sim_functions import calc_hits, calc_damage, calc_to_wound, calc_attacks, calc_saves, calc_kills, calc_wounds, calc_feel_no_pain, calc_sustained_hits
from enums import TkType, RerollType, MinusDamageType, MinusWoundType
from data import getAttackerForm, getDefenderForm, getAtkModifiersForm, getDefModifiersForm
from utils import build_form
from classes.attacker import Attacker

ATTACKER = None
SIMULATIONS = 100000

def run_simulation():
    try:
        if not ATTACKER:
            raise Exception("No attacker data was found")
        
        #DEFENDER
        DEFEND_TOUGHNESS = int(defend_toughness_entry.get() or 0)
        DEFEND_SAVE = int(defend_save_entry.get() or 0)
        DEFEND_INVULN = int(defend_invuln_entry.get() or 0)
        DEFEND_WOUNDS = int(defend_wounds_entry.get() or 1)
        FEEL_NO_PAIN = int(feel_no_pain_entry.get() or 0)
        DEFEND_MODEL_COUNT = int(defend_model_count_entry.get() or 1)
        
        # DEFENDER MODIFIERS
        MOD_MINUS_DAMAGE = mod_minus_damage_var.get() or MinusDamageType.NO_MINUS
        MOD_MINUS_WOUND = mod_minus_wound_var.get() or MinusWoundType.NO_MINUS.value
        MOD_PLUS_SAVE = mod_plus_save_var.get() or False

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

        TO_WOUND = calc_to_wound(ATTACKER.strength, DEFEND_TOUGHNESS, ATTACKER.plus_wound.get(), MOD_MINUS_WOUND)
        previous_dice = 0
        
        for _ in range(SIMULATIONS):
            added_saves = 0
            added_wounds = 0
            added_damage = 0
            
            # calc attacks
            previous_dice = calc_attacks(ATTACKER.attacks)
            if ATTACKER.blast:
                    previous_dice += int((DEFEND_MODEL_COUNT / 5) // 1)
            AVERAGE_ATTACKS += previous_dice
            
            # calc hits
            if not ATTACKER.torrent:
                previous_dice, crits = calc_hits(
                    atk=previous_dice,
                    score=ATTACKER.score,
                    reroll_hit=ATTACKER.reroll_hits == RerollType.REROLL_ALL.value,
                    reroll_hit_one=ATTACKER.reroll_hits == RerollType.REROLL_ONE.value,
                    crit_hit=ATTACKER.critical_hit,
                    plus_hit=ATTACKER.plus_hit
                )

                # calc special crits
                if ATTACKER.sustained_hits != "0":
                    added_wounds = calc_sustained_hits(crits, ATTACKER.sustained_hits)
                    AVERAGE_SUSTAINED_HITS += added_wounds
                AVERAGE_HITS += previous_dice
                if ATTACKER.lethal_hits:
                    added_saves = crits
                    previous_dice -= crits
                    
                AVERAGE_CRIT_HIT += crits                
            
            # calc wound
            previous_dice, crits = calc_wounds(
                hits=previous_dice + added_wounds, 
                to_wound=TO_WOUND,
                reroll_wound=ATTACKER.reroll_wounds == RerollType.REROLL_ALL.value, 
                reroll_wound_one=ATTACKER.reroll_wounds == RerollType.REROLL_ONE.value, 
                crit_wound=ATTACKER.critical_wound
            )
            AVERAGE_WOUNDS += previous_dice
            if ATTACKER.devestating_wounds:
                added_damage = crits
                previous_dice -= crits
            AVERAGE_CRIT_WOUND += crits
            
            # calc save
            previous_dice, crits = calc_saves(
                wounds=previous_dice + added_saves, 
                save=DEFEND_SAVE, 
                invuln=DEFEND_INVULN, 
                ap=ATTACKER.ap,
                plus_save=MOD_PLUS_SAVE
            )
            AVERAGE_SAVES += previous_dice
            
            # calc damage
            previous_dice = calc_damage(
                amt=previous_dice + added_damage, 
                damage=ATTACKER.damage,
                return_as_list=True,
                minus_damage=MOD_MINUS_DAMAGE
            )
            AVERAGE_DAMAGE += sum(previous_dice)

            #calc feel no pain
            previous_dice = calc_feel_no_pain(
                damage=previous_dice,
                fnp=FEEL_NO_PAIN
            )
            AVERAGE_FEEL_NO_PAIN += sum(previous_dice)
            
            # calc kills
            previous_dice = calc_kills(
                dmg_list=previous_dice,
                wounds=DEFEND_WOUNDS)
            AVERAGE_KILLS += previous_dice

            if previous_dice >= DEFEND_MODEL_COUNT:
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
        if FEEL_NO_PAIN:
            message += f"Damage after FNP - {round(AVERAGE_FEEL_NO_PAIN / SIMULATIONS, 2)}\n"
        if DEFEND_MODEL_COUNT > 1:
            message += f"Kills - {round(AVERAGE_KILLS / SIMULATIONS, 2)}\n"
        if UNITS_WIPED > 0:
            message += "-------------\n"
            message += f"Percent chance unit dies - {round(UNITS_WIPED / SIMULATIONS * 100, 2)}%\n"
        messagebox.showinfo("Simulation Results", message)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Line: {e.__traceback__.tb_lineno} - {str(e)}")

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

print("Main Before:",attacker_frame)
print("Mod Before:",attacker_mod_frame)
ATTACKER = Attacker(attacker_frame, attacker_mod_frame)

#get form data and build GUI
(defend_toughness_entry, defend_save_entry, defend_invuln_entry, defend_wounds_entry, defend_model_count_entry, feel_no_pain_entry, defender_form_data) = getDefenderForm()
build_form(defender_form_data, defender_frame)

(mod_minus_damage_var, mod_minus_wound_var, mod_plus_save_var, defender_mod_form_data) = getDefModifiersForm()
build_form(defender_mod_form_data, defender_mod_frame)

# Add simulation button
run_button = tk.Button(window, text="Run Simulation", command=run_simulation)
run_button.grid(row=1, column=3, columnspan=2, pady=10)

# Start Tkinter main loop
window.mainloop()