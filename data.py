import tkinter as tk
from enums import TkType, RerollType, MinusDamageType, MinusWoundType

def getAttackerForm():
    attacks_entry = tk.StringVar()
    attack_score_entry = tk.IntVar()
    attack_strength_entry = tk.IntVar()
    attack_ap_entry = tk.IntVar()
    attack_dmg_entry = tk.StringVar()

    form_data = [
        {"label": "Attacks:", "entry": attacks_entry, "default": "2d6", "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Attack Score:", "entry": attack_score_entry, "default": 3, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Strength:", "entry": attack_strength_entry, "default": 5, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "AP:", "entry": attack_ap_entry, "default": 0, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Damage:", "entry": attack_dmg_entry, "default": "1", "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
    ]

    return (
        attacks_entry,
        attack_score_entry,
        attack_strength_entry,
        attack_ap_entry,
        attack_dmg_entry,
        form_data
    )
    
def getAtkModifiersForm():
    mod_reroll_hits_var = tk.StringVar()
    mod_reroll_wounds_var = tk.StringVar()
    mod_sustained_hits_var = tk.StringVar()
    mod_lethal_hits_var = tk.IntVar()
    mod_torrent_var = tk.IntVar()
    mod_devestating_wounds_var = tk.IntVar()
    mod_blast_var = tk.IntVar()
    mod_plus_wound_var = tk.IntVar()
    mod_plus_hit_var = tk.IntVar()
    attack_crit_hit_entry = tk.IntVar()
    attack_crit_wound_entry = tk.IntVar()

    form_data = [
        {"label": "Reroll Hit", "entry": mod_reroll_hits_var, "options": RerollType, "default": RerollType.NO_REROLL.value, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Reroll Wound", "entry": mod_reroll_wounds_var, "options": RerollType, "default": RerollType.NO_REROLL.value, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
        {"label": "+1 Hit", "entry": mod_plus_hit_var, "default": 0, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
        {"label": "+1 Wound", "entry": mod_plus_wound_var, "default": 0, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Sustained Hit", "entry": mod_sustained_hits_var, "default": 0, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Lethal Hit", "entry": mod_lethal_hits_var, "default": 0, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Torrent", "entry": mod_torrent_var, "default": 0, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Blast", "entry": mod_blast_var, "default": 0, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Devastating Wounds", "entry": mod_devestating_wounds_var, "default": 0, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Critical Hit:", "entry": attack_crit_hit_entry, "default": 6, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Critical Wound:", "entry": attack_crit_wound_entry, "default": 6, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
    ]

    return (
        mod_reroll_hits_var,
        mod_reroll_wounds_var,
        mod_sustained_hits_var,
        mod_lethal_hits_var,
        mod_torrent_var,
        mod_devestating_wounds_var,
        mod_blast_var,
        mod_plus_hit_var,
        mod_plus_wound_var,
        attack_crit_hit_entry,
        attack_crit_wound_entry,
        form_data
    )
    

def getDefenderForm():
    defend_toughness_entry = tk.IntVar()
    defend_save_entry = tk.IntVar()
    defend_invuln_entry = tk.IntVar()
    defend_wounds_entry = tk.IntVar()
    feel_no_pain_entry = tk.IntVar()
    defend_model_count_entry = tk.IntVar()

    form_data = [
        {"label": "Model Count:", "entry": defend_model_count_entry, "default": 1, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Toughness:", "entry": defend_toughness_entry, "default": 5, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Save:", "entry": defend_save_entry, "default": 3, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Invuln:", "entry": defend_invuln_entry, "default": 0, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Wounds:", "entry": defend_wounds_entry, "default": 2, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Feel No Pain:", "entry": feel_no_pain_entry, "default": 0, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
    ]

    return (
        defend_toughness_entry,
        defend_save_entry,
        defend_invuln_entry,
        defend_wounds_entry,
        defend_model_count_entry,
        feel_no_pain_entry,
        form_data
    )
    
def getDefModifiersForm():
    mod_minus_damage = tk.StringVar()
    mod_minus_wound = tk.StringVar()
    mod_plus_save = tk.IntVar()

    form_data = [
        {"label": "Damage reduction", "entry": mod_minus_damage, "options": MinusDamageType, "default": MinusDamageType.NO_MINUS.value, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
        {"label": "Wound reduction", "entry": mod_minus_wound, "options": MinusWoundType, "default": MinusWoundType.NO_MINUS.value, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
        {"label": "+1 Save", "entry": mod_plus_save, "default": 0, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
    ]

    return (
        mod_minus_damage,
        mod_minus_wound,
        mod_plus_save,
        form_data
    )