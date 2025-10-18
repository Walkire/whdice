import tkinter as tk
from utils import build_form
from enums import TkType, MinusDamageType, MinusWoundType, RerollType
from classes.binder import TinkerBinder
from classes.data import Data

DEFAULTS = {
    "toughness": 3,
    "save": 5,
    "invuln": 0,
    "wounds": 1,
    "feel_no_pain": 0,
    "model_count": 10,
    "minus_damage": MinusDamageType.NO_MINUS.value,
    "minus_wound": MinusWoundType.NO_MINUS.value,
    "reroll_save": RerollType.NO_REROLL.value,
    "plus_save": False,
    "cover": False
}

class Defender:
    def __init__(self, main_frame, mod_frame):
        self.toughness = TinkerBinder(tk.IntVar, value=DEFAULTS['toughness'])
        self.save = TinkerBinder(tk.IntVar, value=DEFAULTS['save'])
        self.invuln = TinkerBinder(tk.IntVar, value=DEFAULTS['invuln'])
        self.wounds = TinkerBinder(tk.IntVar, value=DEFAULTS['wounds'])
        self.feel_no_pain = TinkerBinder(tk.IntVar, value=DEFAULTS['feel_no_pain'])
        self.model_count = TinkerBinder(tk.IntVar, value=DEFAULTS['model_count'])

        self.minus_damage = TinkerBinder(tk.StringVar, value=DEFAULTS['minus_damage'])
        self.minus_wound = TinkerBinder(tk.StringVar, value=DEFAULTS['minus_wound'])
        self.reroll_save = TinkerBinder(tk.StringVar, value=DEFAULTS['reroll_save'])
        self.plus_save = TinkerBinder(tk.IntVar, value=DEFAULTS['plus_save'])
        self.cover = TinkerBinder(tk.IntVar, value=DEFAULTS['cover'])

        self.main_frame = main_frame
        self.modifier_frame = mod_frame

        self.buildForm()
        self.buildModForm()

    def buildForm(self):
        build_form([
            {"label": "Model Count:", "entry": self.model_count, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Toughness:", "entry": self.toughness,  "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Save:", "entry": self.save, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Invuln:", "entry": self.invuln, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Wounds:", "entry": self.wounds, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Feel No Pain:", "entry": self.feel_no_pain, "type": TkType.ENTRY, "style": {"sticky": 'w', "padx": 5}},
        ], self.main_frame)


    def buildModForm(self):
        build_form([
            {"label": "Damage reduction", "entry": self.minus_damage, "options": MinusDamageType, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Wound reduction", "entry": self.minus_wound, "options": MinusWoundType, "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Reroll Save", "entry": self.reroll_save, "options": RerollType, "exclude": [RerollType.FISH_ROLLS], "type": TkType.OPTIONMENU, "style": {"sticky": 'w', "padx": 5}},
            {"label": "+1 Save", "entry": self.plus_save, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
            {"label": "Cover", "entry": self.cover, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
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
