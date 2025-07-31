import re

SHORTHAND_NOTATION = r'^d(\d+)$'
DIE_NOTATION = r'^(\d*)d(\d+)([+-]\d+)?$'

def has_notation(dice):
    return bool(re.match(SHORTHAND_NOTATION, dice) or re.match(DIE_NOTATION, dice))

def get_range(value):
    if not has_notation(value):
        return value
    
    match = re.match(DIE_NOTATION, value.strip())
    if not match:
        raise ValueError("Invalid dice notation. Try formats like 'd4', '2d6+1', or '1d8-2'")

    num_dice = int(match.group(1)) if match.group(1) else 1
    num_sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0

    min_roll = num_dice * 1 + modifier
    max_roll = num_dice * num_sides + modifier

    return min_roll, max_roll

def bad_roll(roll, notation, threshold) -> bool:
    if not has_notation(notation):
        return None
    
    range_min, range_max = get_range(notation)
    range_size = range_max - range_min + 1
    cutoff = int(range_size * threshold)
    
    return roll <= (range_min + cutoff - 1)