import tkinter as tk
from utils import build_form
from enums import TkType, RerollType
from classes.binder import TinkerBinder

class Attacker:
    def __init__(self, main_frame, mod_frame):
        self.attacks = TinkerBinder(tk.StringVar, value="6")
        self.score = TinkerBinder(tk.IntVar, value=3)
        self.strength = TinkerBinder(tk.IntVar,value=5)
        self.ap = TinkerBinder(tk.IntVar, value=1)
        self.damage = TinkerBinder(tk.StringVar, value="2")
        self.critical_hit = TinkerBinder(tk.IntVar, value=6)
        self.critical_wound = TinkerBinder(tk.IntVar, value=6)

        self.torrent = TinkerBinder(tk.IntVar, value=False)
        self.reroll_hits = TinkerBinder(tk.StringVar, value=RerollType.NO_REROLL.value)
        self.reroll_wounds = TinkerBinder(tk.StringVar, value=RerollType.NO_REROLL.value)
        self.reroll_damage = TinkerBinder(tk.StringVar, value=RerollType.NO_REROLL.value)
        self.sustained_hits = TinkerBinder(tk.StringVar, value="0")
        self.lethal_hits = TinkerBinder(tk.IntVar, value=False)
        self.devestating_wounds = TinkerBinder(tk.IntVar, value=False)
        self.blast = TinkerBinder(tk.IntVar, value=False)
        self.plus_wound = TinkerBinder(tk.IntVar, value=False)
        self.plus_hit = TinkerBinder(tk.IntVar, value=False)

        self.main_frame = main_frame
        self.modifier_frame = mod_frame

        self.buildForm()
        self.buildModForm()

    def buildForm(self):
        build_form([
            {"label": "Attacks:", "entry": self.attacks, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Attack Score:", "entry": self.score, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Strength:", "entry": self.strength, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "AP:", "entry": self.ap, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Damage:", "entry": self.damage, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}}
        ], self.main_frame)


    def buildModForm(self):
        build_form([
            {"label": "Reroll Hit", "entry": self.reroll_hits, "options": RerollType, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Reroll Wound", "entry": self.reroll_wounds, "options": RerollType, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Reroll Damage", "entry": self.reroll_damage, "options": RerollType, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
            {"label": "+1 Hit", "entry": self.plus_hit, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
            {"label": "+1 Wound", "entry": self.plus_wound, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Sustained Hit", "entry": self.sustained_hits, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Lethal Hit", "entry": self.lethal_hits, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Torrent", "entry": self.torrent, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Blast", "entry": self.blast, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Devastating Wounds", "entry": self.devestating_wounds, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Critical Hit:", "entry": self.critical_hit, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Critical Wound:", "entry": self.critical_wound, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}}
        ], self.modifier_frame)
