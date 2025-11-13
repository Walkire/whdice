from utils import build_form, toggle_field_state
from classes.binder import TinkerBinder

class BaseUnit:
    def __init__(self):
        self.conditional_widgets = {}
    
    def setup_conditional_traces(self):
        for key, data in self.conditional_widgets.items():
            field_obj = data['obj']
            if hasattr(field_obj, 'var'):
                field_obj.var().trace('w', lambda *args, fo=field_obj: self.toggle_conditional_visibility(fo))
    
    def toggle_conditional_visibility(self, field_obj):
        toggle_field_state(self.conditional_widgets, field_obj, bool(field_obj.get()))
    
    def getValues(self):
        values = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, TinkerBinder):
                values[attr_name] = attr.get()
        return values
    
    def resetValues(self, defaults):
        for key, value in defaults.items():
            attr = getattr(self, key, None)
            if isinstance(attr, TinkerBinder):
                attr.set(value)