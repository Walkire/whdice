import random
import re
from enums import MinusDamageType, MinusWoundType, RerollType
from utils import DIE_NOTATION, SHORTHAND_NOTATION, has_notation, get_range, bad_roll

# Function to simulate a dice roll with a specified number of sides.
def roll(num_sides = 6):
    return random.randint(1, num_sides)

# Check if the input is a string representing a dice roll or a numeric value
# and roll the dice accordingly. If it's a numeric value, return it as is.
def check_and_roll_numeric(dice):
    if has_notation(dice):
        if re.match(SHORTHAND_NOTATION, dice):
            num_sides = int(re.search(r'(\d+)', dice).group(1))
            result = roll(num_sides)
            return result
        elif re.match(DIE_NOTATION, dice):
            match = re.search(DIE_NOTATION, dice)
            num_dice = int(match.group(1)) or 1
            num_sides = int(match.group(2))
            modifier = int(match.group(3)) if match.group(3) else 0
            result = sum(roll(num_sides) for _ in range(num_dice)) + modifier
            return result
    else:
        return int(dice) if isinstance(dice, str) and dice.isnumeric() else dice

# Calculate the number of successes based on the number of dice rolled,
# the success threshold, and various reroll options.
## Parameters:
# - dice: Number of dice to roll.
# - success: The success threshold (minimum value to count as a success).
# - invert: If True, counts rolls below the success threshold as successes.
# - reroll_all: If True, rerolls all dice that did not succeed.
# - reroll_ones: If True, rerolls only the dice that rolled a one.
# - crit_value: The value that counts as a critical success (default is 6).
def calc_success(dice, success, invert = False, reroll_all = False, reroll_ones = False, crit_value = 6) -> tuple[int, int]:
    total = 0
    ones = 0
    reroll_total = 0
    crits = 0
    reroll_crits = 0
    if success == 0:
        return dice
    
    for _ in range(dice):
        result = roll()
        #ignore tracking ones and crits on saves
        if result == 1 and not invert:
            ones += 1
        if result >= crit_value and not invert:
            crits += 1
            
        #not saves
        if not invert and not result == 1 and (result >= success or result >= crit_value):
            total += 1
        #is save
        elif invert and result < success:
            total += 1
            
    if reroll_all:
        reroll_total, reroll_crits = calc_success(dice - total, success, invert, crit_value = crit_value)
    elif reroll_ones:
        reroll_total, reroll_crits = calc_success(ones, success, invert, crit_value = crit_value)
    
    return reroll_total + total, crits + reroll_crits

def calc_to_wound(strength, toughness, plus_wound = False, minus_wound = MinusWoundType.NO_MINUS.value):
    if strength == 0:
        return 6
    if toughness == 0:
        return 0
    
    # modifiers to wound
    modifier = 0
    if plus_wound:
        modifier += -1
    elif minus_wound == MinusWoundType.MINUS_ALWAYS.value:
        modifier += 1
    elif minus_wound == MinusWoundType.MINUS_STR_GREATER.value and strength > toughness:
        modifier += 1
        
    # modifier cannot be better than -1 or worse than 1
    if modifier > 1:
        modifier = 1
    if modifier < -1:
        modifier = -1

    ts_ratio = toughness / strength
    if ts_ratio >= 2:
        # wound cannot be worse than 6
        return 6 + modifier if modifier < 0 else 6
    if ts_ratio < 2 and ts_ratio > 1:
        return 5 + modifier
    if ts_ratio == 1:
        return 4 + modifier
    if ts_ratio < 1 and ts_ratio > 0.5:
        return 3 + modifier
    if ts_ratio <= 0.5:
        # wound cannot be better than 2
        return 2 + modifier if modifier > 0 else 2

def calc_attacks(total_attacks):
    return check_and_roll_numeric(total_attacks)

def calc_sustained_hits(crits, sustained_hits):
    extra_hits = 0
    for _ in range(crits):
        extra_hits += check_and_roll_numeric(sustained_hits)
    
    return extra_hits

def calc_hits(atk, score = 0, reroll_hit = False, reroll_hit_one = False, crit_hit = 6, plus_hit = False):
    if plus_hit:
        score -= 1
    # to hit cannot be better than 2
    if score < 2:
        score = 2
        
    return calc_success(atk, score, False, reroll_hit, reroll_hit_one, crit_hit)

def calc_wounds(hits, to_wound = 0, reroll_wound = False, reroll_wound_one = False, crit_wound = 6) -> int:
    return calc_success(hits, to_wound, False, reroll_wound, reroll_wound_one, crit_wound)

def calc_saves(wounds, save = 0, invuln = 0, ap = 0, plus_save = False) -> int:
    if plus_save and save > 2:
        save -= 1
    
    final_save = save + ap
    if final_save > invuln and invuln != 0:
        final_save = invuln
        
    # Your save cannot be better than a 3 unless your base save is already better than 3
    if final_save < 3 and save <= 2:
        final_save = 3
        
    return calc_success(wounds, final_save, True) 

def calc_damage(amt, damage = 1, return_as_list = False, minus_damage = MinusDamageType.NO_MINUS.value, reroll_damage = RerollType.NO_REROLL.value) -> int | list:
    # Warhammer calculates damage in order:
    # Replace -> Division -> Multiplication -> Addition -> Subtraction
    damage_list = []
    minimum_roll = 99999
    reroll_one = False
    
    if minus_damage == MinusDamageType.NULL_ONE.value:
        amt -= 1
    if reroll_damage == RerollType.REROLL_ONE.value and has_notation(damage):
        reroll_one = True

    # Simulate all damage rolls and modify them as needed
    if return_as_list:
        for _ in range(amt):
            d = check_and_roll_numeric(damage)
            if reroll_one and d < minimum_roll:
                minimum_roll = d
            elif reroll_damage == RerollType.REROLL_ALL.value and bad_roll(d, damage, threshold=0.2):
                d = check_and_roll_numeric(damage)
            elif minus_damage == MinusDamageType.MINUS_ONE.value and d > 1:
                d -= 1
            elif minus_damage == MinusDamageType.MINUS_HALF.value:
                d = -(-d // 2)
            damage_list.append(d)
        
    if reroll_one:
        damage_list.remove(minimum_roll)
    return damage_list if return_as_list else sum(damage_list)

def calc_feel_no_pain(damage, fnp = 0) -> int | list:
    if fnp > 6 or fnp <= 0:
        return damage
    if fnp == 1:
        if isinstance(damage, list):
            return [0 for _ in damage]
        return 0

    if isinstance(damage, list):
        return [calc_success(d, fnp, True)[0] for d in damage]
    else:
        dmg, _ = calc_success(damage, fnp, True)
        return dmg


def calc_kills(dmg_list: list = [], wounds = 1):
    kills = 0
    current_wound = wounds
    for dmg in dmg_list:
        if dmg >= current_wound:
            kills += 1
            current_wound = wounds
        else:
            current_wound -= dmg

    return kills