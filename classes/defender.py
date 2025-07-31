import tkinter as tk
from utils import build_form
from enums import TkType, MinusDamageType, MinusWoundType
from classes.binder import TinkerBinder

class Defender:
    def __init__(self, main_frame, mod_frame):
        self.toughness = TinkerBinder(tk.IntVar, value=3)
        self.save = TinkerBinder(tk.IntVar, value=5)
        self.invuln = TinkerBinder(tk.IntVar, value=0)
        self.wounds = TinkerBinder(tk.IntVar, value=1)
        self.feel_no_pain = TinkerBinder(tk.IntVar, value=0)
        self.model_count = TinkerBinder(tk.IntVar, value=10)

        self.minus_damage = TinkerBinder(tk.StringVar, value=MinusDamageType.NO_MINUS.value)
        self.minus_wound = TinkerBinder(tk.StringVar, value=MinusWoundType.NO_MINUS.value)
        self.plus_save = TinkerBinder(tk.IntVar, value=False)

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
            {"label": "+1 Save", "entry": self.plus_save, "type": TkType.CHECKBUTTON, "style": {"sticky": 'w', "padx": 5}},
        ], self.modifier_frame)
