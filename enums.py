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