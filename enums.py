from enum import Enum

# tk types
class TkType(Enum):
    ENTRY = 1
    CHECKBUTTON = 2
    OPTIONMENU = 3
    
class RerollType(Enum):
    NO_REROLL = 'None'
    REROLL_ONE = 'Reroll Ones'
    REROLL_ALL = 'Reroll All'
    
class MinusDamageType(Enum):
    NO_MINUS = 'None'
    MINUS_ONE = 'Minus One'
    MINUS_HALF = 'Minus Half'
    NULL_ONE = 'Null One'
    
class MinusWoundType(Enum):
    NO_MINUS = 'None'
    MINUS_STR_GREATER = 'Minus 1 Wound if Strength Greater'
    MINUS_ALWAYS = 'Minus 1 Wound'