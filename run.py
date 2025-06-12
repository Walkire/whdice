import tkinter as tk
from tkinter import messagebox
from sim_functions import calc_hits, calc_damage, calc_to_wound, calc_attacks, calc_saves, calc_kills, calc_wounds, calc_feel_no_pain, calc_sustained_hits
from enums import TkType, RerollType
from data import getFormData

def run_simulation():
    try:
        # ATTACKER
        ATTACKS = str(attacks_entry.get() or 1)
        ATTACK_SCORE = int(attack_score_entry.get() or 0)
        ATTACK_STRENGTH = int(attack_strength_entry.get() or 0)
        ATTACK_AP = int(attack_ap_entry.get() or 0)
        ATTACK_DMG = str(attack_dmg_entry.get() or 1)
        ATTACK_CRIT_HIT = int(attack_crit_hit_entry.get() or 6)
        ATTACK_CRIT_WOUND = int(attack_crit_wound_entry.get() or 6)
        
        #OPTIONS
        MOD_TORRENT = mod_torrent_var.get() or False
        MOD_REROLL_HITS = mod_reroll_hits_var.get() or RerollType.NO_REROLL
        MOD_REROLL_WOUNDS = mod_reroll_wounds_var.get() or RerollType.NO_REROLL
        MOD_SUSTAINED_HITS = str(mod_sustained_hits_var.get() or 0)
        MOD_LETHAL_HITS = mod_lethal_hits_var.get() or False
        MOD_DEVESTATING_WOUNDS = mod_devestating_wounds_var.get() or False
        MOD_BLAST = mod_blast_var.get() or False
        PLUS_WOUND = mod_plus_wound_var.get() or False
        SIMULATIONS = 100000
        
        #DEFENDER
        DEFEND_TOUGHNESS = int(defend_toughness_entry.get() or 0)
        DEFEND_SAVE = int(defend_save_entry.get() or 0)
        DEFEND_INVULN = int(defend_invuln_entry.get() or 0)
        DEFEND_WOUNDS = int(defend_wounds_entry.get() or 1)
        FEEL_NO_PAIN = int(feel_no_pain_entry.get() or 0)
        DEFEND_MODEL_COUNT = int(defend_model_count_entry.get() or 1)

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
        
        AVERAGE_CRIT_HIT = 0
        AVERAGE_CRIT_WOUND = 0

        TO_WOUND = calc_to_wound(ATTACK_STRENGTH, DEFEND_TOUGHNESS, PLUS_WOUND)
        previous_dice = 0
        
        for _ in range(SIMULATIONS):
            added_saves = 0
            added_wounds = 0
            added_damage = 0
            added_sustained_hits = 0
            
            # calc attacks
            previous_dice = calc_attacks(ATTACKS)
            if MOD_BLAST:
                    previous_dice += int((DEFEND_MODEL_COUNT / 5) // 1)
            AVERAGE_ATTACKS += previous_dice
            
            # calc hits
            if not MOD_TORRENT:
                previous_dice, crits = calc_hits(
                atk=previous_dice, 
                score=ATTACK_SCORE, 
                reroll_hit=MOD_REROLL_HITS == RerollType.REROLL_ALL.value, 
                reroll_hit_one=MOD_REROLL_HITS == RerollType.REROLL_ONE.value, 
                crit_hit=ATTACK_CRIT_HIT)
                
                # calc special crits
                if MOD_SUSTAINED_HITS != "0":
                    added_wounds, added_sustained_hits = calc_sustained_hits(crits, MOD_SUSTAINED_HITS)
                    AVERAGE_SUSTAINED_HITS += added_sustained_hits
                    AVERAGE_HITS = AVERAGE_HITS + (previous_dice + added_wounds)
                else:
                    AVERAGE_HITS += previous_dice
                if MOD_LETHAL_HITS:
                    added_saves = crits
                    previous_dice -= crits
                    
                AVERAGE_CRIT_HIT += crits                
            
            # calc wound
            previous_dice, crits = calc_wounds(
                hits=previous_dice + added_wounds, 
                to_wound=TO_WOUND,
                reroll_wound=MOD_REROLL_WOUNDS == RerollType.REROLL_ALL.value, 
                reroll_wound_one=MOD_REROLL_WOUNDS == RerollType.REROLL_ONE.value, 
                crit_wound=ATTACK_CRIT_WOUND
            )
            AVERAGE_WOUNDS += previous_dice
            if MOD_DEVESTATING_WOUNDS:
                added_damage = crits
                previous_dice -= crits
            AVERAGE_CRIT_WOUND += crits
            
            # calc save
            previous_dice, crits = calc_saves(
                wounds=previous_dice + added_saves, 
                save=DEFEND_SAVE, 
                invuln=DEFEND_INVULN, 
                ap=ATTACK_AP)
            AVERAGE_SAVES += previous_dice
            
            # calc damage
            previous_dice = calc_damage(
                amt=previous_dice + added_damage, 
                damage=ATTACK_DMG)
            AVERAGE_DAMAGE += previous_dice
            
            #calc feel no pain
            previous_dice, crits = calc_feel_no_pain(
                damage=previous_dice,
                fnp=FEEL_NO_PAIN
            )
            AVERAGE_FEEL_NO_PAIN += previous_dice
            
            # calc kills
            previous_dice = calc_kills(
                dmg=previous_dice,
                wounds=DEFEND_WOUNDS)
            AVERAGE_KILLS += previous_dice
    
        # Calculate extra after all simulations
        is_dead = False
        
        if AVERAGE_KILLS / SIMULATIONS >= DEFEND_MODEL_COUNT:
            is_dead = True
            
        # Display results using messagebox
        message = f"with {TO_WOUND} to wound\n"
        message += "-------------\n"
        if MOD_BLAST:
            message += f"Attacks - {round(AVERAGE_ATTACKS / SIMULATIONS, 2)} (+blast)\n"
        else:
            message += f"Attacks - {round(AVERAGE_ATTACKS / SIMULATIONS, 2)}\n"
        if MOD_TORRENT:
            message += f"Hits - N/A (Torrent)\n"
        elif MOD_SUSTAINED_HITS != "0":
            message += f"Hits - {round(AVERAGE_HITS / SIMULATIONS, 2)} (+{round(AVERAGE_SUSTAINED_HITS / SIMULATIONS, 2)} sustained hits)\n"
        elif MOD_LETHAL_HITS:
            message += f"Hits - {round(AVERAGE_HITS / SIMULATIONS, 2)} (+{round(AVERAGE_CRIT_HIT / SIMULATIONS, 2)} crits + {round(added_saves / SIMULATIONS, 2)} lethal hits)\n"
        else:
            message += f"Hits - {round(AVERAGE_HITS / SIMULATIONS, 2)}\n"
        if MOD_DEVESTATING_WOUNDS:
            message += f"Wounds - {round(AVERAGE_WOUNDS / SIMULATIONS, 2)} (+{round(AVERAGE_CRIT_WOUND / SIMULATIONS, 2)} crits)\n"
        else:
            message += f"Wounds - {round(AVERAGE_WOUNDS / SIMULATIONS, 2)}\n"
        message += f"Failed Saves - {round(AVERAGE_SAVES / SIMULATIONS, 2)}\n"
        message += f"Damage - {round(AVERAGE_DAMAGE / SIMULATIONS, 2)}\n"
        if FEEL_NO_PAIN:
            message += f"Feel no pain - {round(AVERAGE_FEEL_NO_PAIN / SIMULATIONS, 2)}\n"
        message += f"Kills - {round(AVERAGE_KILLS / SIMULATIONS, 2)}\n"
        if is_dead:
            message += "-------------\n"
            message += "Defender is dead!\n"
        messagebox.showinfo("Simulation Results", message)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        print(f"Line: {e.__traceback__.tb_lineno} - {str(e)}")
        
# Create a Tkinter window
window = tk.Tk()
window.title("Warhammer Combat Simulator")

#order matters
(attacks_entry,
attack_score_entry,
mod_torrent_var,
attack_strength_entry,
attack_ap_entry,
attack_dmg_entry,
mod_reroll_hits_var,
mod_reroll_wounds_var,
mod_sustained_hits_var,
mod_lethal_hits_var,
attack_crit_hit_entry,
mod_devestating_wounds_var,
mod_blast_var,
mod_plus_wound_var,
attack_crit_wound_entry,
defend_toughness_entry,
defend_save_entry,
defend_invuln_entry,
defend_wounds_entry,
defend_model_count_entry,
feel_no_pain_entry,
form_fields) = getFormData()

for field in form_fields:
    needs_label = True
    if field["type"] == TkType.ENTRY:
        if "default" in field:
            field['entry'].set(field['default'])
        entry = tk.Entry(window, textvariable=field['entry'])
    elif field["type"] == TkType.CHECKBUTTON:
        if "default" in field:
            field['entry'].set(field['default'])
        entry = tk.Checkbutton(window, text=field['label'], variable=field['entry'])
        needs_label = False
    elif field["type"] == TkType.OPTIONMENU:
        field['entry'].set(field["default"])
        options = [field['options'].value for field['options'] in RerollType]
        entry = tk.OptionMenu(window, field['entry'], *options)
        
    if needs_label:
        label = tk.Label(window, text=field['label'])
        label_style = field.get('label_style', field.get('style', {}))
        label.grid(**label_style)
    
    entry_style = field.get('entry_style', field.get('style', {}))
    entry.grid(**entry_style)

run_button = tk.Button(window, text="Run Simulation", command=run_simulation)
run_button.grid()

# Run the Tkinter main loop
window.mainloop()