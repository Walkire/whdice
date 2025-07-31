import tkinter as tk
from utils import build_form
from enums import TkType, RerollType
from classes.binder import TinkerBinder
from classes.data import Data

DEFAULTS = {
    "attacks": "6",
    "score": 3,
    "strength": 5,
    "ap": 1,
    "damage": "2",
    "critical_hit": 6,
    "critical_wound": 6,
    "torrent": False,
    "reroll_hits": RerollType.NO_REROLL.value,
    "reroll_wounds": RerollType.NO_REROLL.value,
    "reroll_damage": RerollType.NO_REROLL.value,
    "sustained_hits": "0",
    "lethal_hits": False,
    "devestating_wounds": False,
    "blast": False,
    "plus_wound": False,
    "plus_hit": False
}

class Attacker:
    def __init__(self, main_frame, mod_frame):
        self.attacks = TinkerBinder(tk.StringVar, value=DEFAULTS['attacks'])
        self.score = TinkerBinder(tk.IntVar, value=DEFAULTS['score'])
        self.strength = TinkerBinder(tk.IntVar,value=DEFAULTS['strength'])
        self.ap = TinkerBinder(tk.IntVar, value=DEFAULTS['ap'])
        self.damage = TinkerBinder(tk.StringVar, value=DEFAULTS['damage'])
        self.critical_hit = TinkerBinder(tk.IntVar, value=DEFAULTS['critical_hit'])
        self.critical_wound = TinkerBinder(tk.IntVar, value=DEFAULTS['critical_wound'])

        self.torrent = TinkerBinder(tk.IntVar, DEFAULTS['torrent'])
        self.reroll_hits = TinkerBinder(tk.StringVar, value=DEFAULTS['reroll_hits'])
        self.reroll_wounds = TinkerBinder(tk.StringVar, value=DEFAULTS['reroll_wounds'])
        self.reroll_damage = TinkerBinder(tk.StringVar, value=DEFAULTS['reroll_damage'])
        self.sustained_hits = TinkerBinder(tk.StringVar, value=DEFAULTS['sustained_hits'])
        self.lethal_hits = TinkerBinder(tk.IntVar, value=DEFAULTS['lethal_hits'])
        self.devestating_wounds = TinkerBinder(tk.IntVar, value=DEFAULTS['devestating_wounds'])
        self.blast = TinkerBinder(tk.IntVar, value=DEFAULTS['blast'])
        self.plus_wound = TinkerBinder(tk.IntVar, value=DEFAULTS['plus_wound'])
        self.plus_hit = TinkerBinder(tk.IntVar, value=DEFAULTS['plus_hit'])

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

    def getValues(self):
        values = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, TinkerBinder):
                values[attr_name] = attr.get()
        return Data(**values)

    
    def resetValues(self):
        for key, value in DEFAULTS.items():
            attr = getattr(self, key, None)
            if isinstance(attr, TinkerBinder):
                attr.set(value)
