from enum import Enum

# tk types
class TkType(Enum):
    LABEL = 1
    ENTRY = 2
    CHECKBUTTON = 3
    OPTIONMENU = 4
    LISTBOX = 5
    
class RerollType(Enum):
    NO_REROLL = 'None'
    REROLL_ONE = 'Reroll Ones'
    REROLL_ALL = 'Reroll All'
    FISH_ROLLS = 'Fish Rolls'
    
class MinusDamageType(Enum):
    NO_MINUS = 'None'
    MINUS_ONE = 'Minus One'
    MINUS_HALF = 'Minus Half'
    NULL_ONE = 'Null One'
    
class MinusWoundType(Enum):
    NO_MINUS = 'None'
    MINUS_STR_GREATER = 'Minus 1 Wound if Strength Greater'
    MINUS_ALWAYS = 'Minus 1 Wound'