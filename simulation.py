from sim_functions import (
    calc_hits, calc_damage, calc_to_wound, calc_attacks,
    calc_saves, calc_kills, calc_wounds, calc_feel_no_pain, calc_sustained_hits
)
from enums import RerollType, MinusDamageType

# Core simulation logic
# Returns (results, wipe_percent)

def simulate(attacker, defender, weapons, simulations):
    if not (attacker or weapons):
        raise Exception("No attacker or weapon data found")

    UNITS_WIPED = 0
    previous_dice = 0
    results = []

    weapons_to_use = weapons if weapons else [attacker.getValues()]

    for i, weapon in enumerate(weapons_to_use):
        results.append({
            "id": i,
            "to_wound": 0,
            "attacks": 0,
            "hits": 0,
            "wounds": 0,
            "saves": 0,
            "damage": 0,
            "fnp": 0,
            "kills": 0,
            "sustained": 0,
            "crit_hit": 0,
            "crit_wound": 0,
            "weapon": weapon
        })

    for _ in range(simulations):
        total_kills = 0
        last_remainder = 0

        for i, weapon in enumerate(weapons_to_use):
            added_saves = 0
            added_wounds = 0
            added_damage = 0

            results[i]["to_wound"] = calc_to_wound(
                weapon.strength, defender.toughness, weapon.plus_wound, defender.minus_wound
            )

            # Attacks
            previous_dice = calc_attacks(weapon.attacks)
            if weapon.blast:
                previous_dice += int((defender.model_count / 5) // 1)
            results[i]["attacks"] += previous_dice

            # Hits
            if not weapon.torrent:
                previous_dice, crits = calc_hits(
                    atk=previous_dice,
                    score=weapon.score,
                    reroll_hit=weapon.reroll_hits == RerollType.REROLL_ALL.value,
                    reroll_hit_one=weapon.reroll_hits == RerollType.REROLL_ONE.value,
                    crit_hit=weapon.critical_hit,
                    plus_hit=weapon.plus_hit,
                    fish_rolls=weapon.reroll_hits == RerollType.FISH_ROLLS.value
                )
                if weapon.sustained_hits != "0":
                    added_wounds = calc_sustained_hits(crits, weapon.sustained_hits)
                    results[i]["sustained"] += added_wounds
                results[i]["hits"] += previous_dice
                if weapon.lethal_hits:
                    added_saves = crits
                    previous_dice -= crits
                results[i]["crit_hit"] += crits

            # Wounds
            previous_dice, crits = calc_wounds(
                hits=previous_dice + added_wounds,
                to_wound=results[i]["to_wound"],
                reroll_wound=weapon.reroll_wounds == RerollType.REROLL_ALL.value,
                reroll_wound_one=weapon.reroll_wounds == RerollType.REROLL_ONE.value,
                crit_wound=weapon.critical_wound,
                fish_rolls=weapon.reroll_wounds == RerollType.FISH_ROLLS.value
            )
            results[i]["wounds"] += previous_dice
            if weapon.devestating_wounds:
                added_damage = crits
                previous_dice -= crits
            results[i]["crit_wound"] += crits

            # Saves
            previous_dice, crits = calc_saves(
                wounds=previous_dice + added_saves,
                save=defender.save,
                invuln=defender.invuln,
                ap=weapon.ap,
                plus_save=defender.plus_save,
                cover=defender.cover and not attacker.ignore_cover,
                reroll_save=defender.reroll_save
            )
            results[i]["saves"] += previous_dice

            # Damage
            previous_dice = calc_damage(
                amt=previous_dice + added_damage,
                damage=weapon.damage,
                return_as_list=True,
                minus_damage=defender.minus_damage,
                null_damage=defender.minus_damage == MinusDamageType.NULL_ONE.value,
                reroll_damage=weapon.reroll_damage,
                melta=weapon.melta_value if weapon.melta else None
            )
            results[i]["damage"] += sum(previous_dice)

            # Feel No Pain
            previous_dice = calc_feel_no_pain(
                damage=previous_dice,
                fnp=defender.feel_no_pain
            )
            results[i]["fnp"] += sum(previous_dice)

            # Kills
            previous_dice, last_remainder = calc_kills(
                dmg_list=previous_dice,
                wounds=defender.wounds,
                remainder=last_remainder
            )
            results[i]["kills"] += previous_dice
            total_kills += previous_dice

        if total_kills >= defender.model_count:
            UNITS_WIPED += 1

    wipe_percent = round(UNITS_WIPED / simulations * 100, 2)
    return results, wipe_percent
