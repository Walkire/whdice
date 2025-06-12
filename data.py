import tkinter as tk
from enums import TkType, RerollType

def getFormData():
    attacks_entry = tk.StringVar()
    attack_score_entry = tk.IntVar()
    attack_strength_entry = tk.IntVar()
    attack_ap_entry = tk.IntVar()
    attack_dmg_entry = tk.StringVar()
        
    mod_reroll_hits_var = tk.StringVar()
    mod_reroll_wounds_var = tk.StringVar()
    mod_sustained_hits_var = tk.StringVar()
    mod_lethal_hits_var = tk.IntVar()
    mod_torrent_var = tk.IntVar()
    attack_crit_hit_entry = tk.IntVar()
    mod_devestating_wounds_var = tk.IntVar()
    mod_blast_var = tk.IntVar()
    mod_plus_wound_var = tk.IntVar()
    attack_crit_wound_entry = tk.IntVar()

    defend_toughness_entry = tk.IntVar()
    defend_save_entry = tk.IntVar()
    defend_invuln_entry = tk.IntVar()
    defend_wounds_entry = tk.IntVar()
    feel_no_pain_entry = tk.IntVar()
    defend_model_count_entry = tk.IntVar()
    
    form_data = [
        {
            "label": "Attacks:",
            "entry": attacks_entry,
            "default": "2d6",
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Attack Score:",
            "entry": attack_score_entry,
            "default": 3,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Modifier: Torrent",
            "entry": mod_torrent_var,
            "default": 0,
            "type": TkType.CHECKBUTTON,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Attack Strength:",
            "entry": attack_strength_entry,
            "default": 5,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Attack AP:",
            "entry": attack_ap_entry,
            "default": 0,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Attack Damage:",
            "entry": attack_dmg_entry,
            "default": "1",
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Modifier: Reroll Hit",
            "entry": mod_reroll_hits_var,
            "options": RerollType,
            "default": RerollType.NO_REROLL.value,
            "type": TkType.OPTIONMENU,
            "label_style": {
                "row": 0,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            },
            "entry_style": {
                "row": 1,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Modifier: Reroll Wound",
            "entry": mod_reroll_wounds_var,
            "options": RerollType,
            "default": RerollType.NO_REROLL.value,
            "type": TkType.OPTIONMENU,
            "label_style": {
                "row": 2,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            },
            "entry_style": {
                "row": 3,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Modifier: +1 Wound",
            "entry": mod_plus_wound_var,
            "default": 0,
            "type": TkType.CHECKBUTTON,
            "style": {
                "row":4,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Modifier: Sustained Hit",
            "entry": mod_sustained_hits_var,
            "default": 0,
            "type": TkType.ENTRY,
            "label_style": {
                "row": 5,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            },
            "entry_style": {
                "row": 6,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Modifier: Letal Hit",
            "entry": mod_lethal_hits_var,
            "default": 0,
            "type": TkType.CHECKBUTTON,
            "style": {
                "row": 7,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Modifier: Blast",
            "entry": mod_blast_var,
            "default": 0,
            "type": TkType.CHECKBUTTON,
            "style": {
                "row":8,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Critical Hit:",
            "entry": attack_crit_hit_entry,
            "default": 6,
            "type": TkType.ENTRY,
            "label_style": {
                "row": 9,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            },
            "entry_style": {
                "row": 10,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Modifier: Devestating Wounds",
            "entry": mod_devestating_wounds_var,
            "default": 0,
            "type": TkType.CHECKBUTTON,
            "style": {
                "row":11,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Critical Wound (Anti-x):",
            "entry": attack_crit_wound_entry,
            "default": 6,
            "type": TkType.ENTRY,
            "label_style": {
                "row":12,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            },
            "entry_style": {
                "row": 13,
                "column": 1,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Defender Model Count:",
            "entry": defend_model_count_entry,
            "default": 1,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Defender Toughness:",
            "entry": defend_toughness_entry,
            "default": 5,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Defender Save:",
            "entry": defend_save_entry,
            "default": 3,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Defender Invuln:",
            "entry": defend_invuln_entry,
            "default": 0,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Defender Wounds:",
            "entry": defend_wounds_entry,
            "default": 2,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        },
        {
            "label": "Feel No Pain:",
            "entry": feel_no_pain_entry,
            "default": 0,
            "type": TkType.ENTRY,
            "style": {
                "column": 0,
                "padx": 5,
                "sticky": 'w'
            }
        }
    ]

    # order matters
    return (
        attacks_entry,
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
        form_data
    )