import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
import enums
import sim_functions

class TestDieNotationFunction(unittest.TestCase):
    def test_has_notation_number_int(self):
        self.assertEqual(sim_functions.has_notation(42), False)

    def test_has_notation_number_string(self):
        self.assertEqual(sim_functions.has_notation("42"), False)

    def test_has_notation_shorthand_1(self):
        self.assertEqual(sim_functions.has_notation("d20"), True)

    def test_has_notation_shorthand_2(self):
        self.assertEqual(sim_functions.has_notation("D20"), True)

    def test_has_notation_longform_1(self):
        self.assertEqual(sim_functions.has_notation("1d20"), True)

    def test_has_notation_longform_2(self):
        self.assertEqual(sim_functions.has_notation("1D20"), True)

    def test_has_notation_longform_3(self):
        self.assertEqual(sim_functions.has_notation("1d20+1"), True)

    def test_has_notation_longform_4(self):
        self.assertEqual(sim_functions.has_notation("1D20-1"), True)

class TestCheckAndRollFunction(unittest.TestCase):
    # Test that string numbers return as int
    def test_check_and_roll_numeric_numeric_string(self):
        self.assertEqual(sim_functions.check_and_roll_numeric("42"), 42)

    # Test that int values return as themselves
    def test_check_and_roll_numeric_numeric_int(self):
        self.assertEqual(sim_functions.check_and_roll_numeric(7), 7)

    # Test that shorthand notation will roll correctly
    @patch('sim_functions.roll', return_value=4)
    def test_check_and_roll_numeric_shorthand_notation_with_mod(self, mock_roll):
        result = sim_functions.check_and_roll_numeric("d6")
        self.assertEqual(result, 4)
        
    # Test that shorthand notation with mod will roll correctly
    @patch('sim_functions.roll', return_value=2)
    def test_check_and_roll_numeric_shorthand_notation(self, mock_roll):
        result = sim_functions.check_and_roll_numeric("d6+3")
        self.assertEqual(result, 5)

    # Test that shorthand notation with mod will roll correctly
    @patch('sim_functions.roll', return_value=2)
    def test_check_and_roll_numeric_bad_format(self, mock_roll):
        with self.assertRaises(ValueError) as cm:
            sim_functions.check_and_roll_numeric("6d+3")

        self.assertIn("wrong format", str(cm.exception))

    # Test that long form dice notation will work
    @patch('sim_functions.roll', return_value=3)
    def test_check_and_roll_numeric_die_notation(self, mock_roll):
        result = sim_functions.check_and_roll_numeric("2d6+1")
        self.assertEqual(result, 3 + 3 + 1)  # 2 rolls of 3 + modifier 1

    # Test that something not a string will work
    @patch('sim_functions.roll', return_value=2)
    @patch('sim_functions.has_notation', return_value=True)
    def test_check_and_roll_numeric_tinkerbinder_conversion(self, mock_roll, mock_has_notation):
        class TinkerBinder:
            def __str__(self):
                return "d4"
        result = sim_functions.check_and_roll_numeric(TinkerBinder())
        self.assertEqual(result, 2)

class TestCalcSuccessFunction(unittest.TestCase):
    @patch('sim_functions.roll')
    def test_success_threshold(self, mock_roll):
        mock_roll.side_effect = [5, 6, 2, 4, 6]  # Simulated dice rolls
        result = sim_functions.calc_success(5, success=4)
        self.assertEqual(result, (4, 2))  # 4 successes, 2 crits

    @patch('sim_functions.roll')
    def test_calc_success_invert_logic(self, mock_roll):
        mock_roll.side_effect = [1, 2, 3, 4, 5]
        result = sim_functions.calc_success(5, success=4, invert=True)
        self.assertEqual(result, (3, 0))  # 3 rolls < 4

    @patch('sim_functions.roll')
    def test_calc_success_reroll_all(self, mock_roll):
        mock_roll.side_effect = [2, 3, 6, 1, 5, 6, 4, 3]  # Initial + rerolls
        result = sim_functions.calc_success(5, success=5, reroll_all=True)
        self.assertEqual(result, (3, 2))

    @patch('sim_functions.roll')
    def test_calc_success_reroll_ones(self, mock_roll):
        mock_roll.side_effect = [1, 2, 6, 1, 5, 6, 3]  # Initial + rerolls for ones
        result = sim_functions.calc_success(5, success=5, reroll_ones=True)
        self.assertEqual(result, (3, 2))
        
    @patch('sim_functions.roll')
    def test_calc_success_fish_rerolls(self, mock_roll):
        mock_roll.side_effect = [6, 2, 6, 1, 5, 6, 3, 3]  # Initial + rerolls for non crit
        result = sim_functions.calc_success(5, success=5, fish_rolls=True)
        self.assertEqual(result, (3, 3))
        
    @patch('sim_functions.roll')
    def test_calc_success_fish_rerolls_with_crit_change(self, mock_roll):
        mock_roll.side_effect = [4, 2, 4, 1, 5, 6, 3]  # Initial + rerolls for non crit
        result = sim_functions.calc_success(5, success=5, fish_rolls=True, crit_value=4)
        self.assertEqual(result, (4, 4))

    @patch('sim_functions.roll')
    def test_calc_success_success_zero(self, mock_roll):
        result = sim_functions.calc_success(5, success=0)
        self.assertEqual(result, (5, 0))  # All dice count as success with no crit

    @patch('sim_functions.roll')
    def test_calc_success_crit_value(self, mock_roll):
        mock_roll.side_effect = [1, 2, 6, 1, 5]
        result = sim_functions.calc_success(5, success=2, crit_value=5)
        self.assertEqual(result, (3, 2)) 
        
    @patch('sim_functions.roll')
    def test_calc_success_reroll_all_saves(self, mock_roll):
        mock_roll.side_effect = [2, 3, 6, 1, 5, 6, 4, 3]  # Initial + rerolls
        result = sim_functions.calc_success(5, success=4, invert=True, reroll_all=True)
        self.assertEqual(result, (1, 2))
        
    @patch('sim_functions.roll')
    def test_calc_success_reroll_one_save(self, mock_roll):
        mock_roll.side_effect = [4, 2, 6, 1, 3, 5]  # Initial + rerolls
        result = sim_functions.calc_success(5, success=3, invert=True, reroll_ones=True)
        self.assertEqual(result, (1, 1))

class TestCalcWoundFunction(unittest.TestCase):
    # 0 strength should give you a 6 to wound
    def test_calc_to_wound_zero_strength(self):
        self.assertEqual(sim_functions.calc_to_wound(0, 5), 6)

    # wound cannot be better then a 2
    def test_calc_to_wound_zero_toughness(self):
        self.assertEqual(sim_functions.calc_to_wound(5, 0), 2)

    def test_calc_to_wound_equal_strength_toughness(self):
        self.assertEqual(sim_functions.calc_to_wound(4, 4), 4)

    def test_calc_to_wound_strength_greater_than_toughness(self):
        self.assertEqual(sim_functions.calc_to_wound(6, 3), 2)

    def test_calc_to_wound_strength_less_than_toughness(self):
        self.assertEqual(sim_functions.calc_to_wound(3, 6), 6)

    def test_calc_to_wound_plus_wound_modifier(self):
        self.assertEqual(sim_functions.calc_to_wound(4, 4, plus_wound=True), 3)

    def test_calc_to_wound_minus_always_modifier(self):
        self.assertEqual(sim_functions.calc_to_wound(4, 4, minus_wound=enums.MinusWoundType.MINUS_ALWAYS.value), 5)

    def test_calc_to_wound_minus_str_greater_modifier_applies(self):
        self.assertEqual(sim_functions.calc_to_wound(5, 3, minus_wound=enums.MinusWoundType.MINUS_STR_GREATER.value), 4)

    def test_calc_to_wound_minus_str_greater_modifier_does_not_apply(self):
        self.assertEqual(sim_functions.calc_to_wound(3, 5, minus_wound=enums.MinusWoundType.MINUS_STR_GREATER.value), 5)

    def test_calc_to_wound_modifier_bounds(self):
        self.assertEqual(sim_functions.calc_to_wound(4, 4, plus_wound=True, minus_wound=enums.MinusWoundType.MINUS_ALWAYS.value), 4)
        
    def test_calc_to_wound_modifier_bounds_2(self):
        self.assertEqual(sim_functions.calc_to_wound(14, 9, plus_wound=True, minus_wound=enums.MinusWoundType.MINUS_STR_GREATER.value), 3)

class TestCalcSavesFunction(unittest.TestCase):
    @patch('sim_functions.calc_success')
    def test_calc_saves_plus_save_applied(self, mock_calc_success):
        mock_calc_success.return_value = 3
        result = sim_functions.calc_saves(wounds=5, save=4, ap=0, plus_save=True)
        self.assertEqual(result, 3)
        mock_calc_success.assert_called_with(5, 3, True, False, False) # final save is 3

    @patch('sim_functions.calc_success')
    def test_calc_saves_invuln_better_than_save(self, mock_calc_success):
        mock_calc_success.return_value = 2
        result = sim_functions.calc_saves(wounds=4, save=5, ap=1, invuln=4)
        self.assertEqual(result, 2)
        mock_calc_success.assert_called_with(4, 4, True, False, False) # final save is the invuln

    @patch('sim_functions.calc_success')
    def test_calc_saves_final_save_cannot_be_better_than_3(self, mock_calc_success):
        mock_calc_success.return_value = 1
        result = sim_functions.calc_saves(wounds=2, save=3, plus_save = True)
        self.assertEqual(result, 1)
        mock_calc_success.assert_called_with(2, 3, True, False, False)

    @patch('sim_functions.calc_success')
    def test_calc_saves_base_save_better_than_3_allows_better_final_save(self, mock_calc_success):
        mock_calc_success.return_value = 4
        result = sim_functions.calc_saves(wounds=6, save=2, ap=1, plus_save = True)
        self.assertEqual(result, 4)
        mock_calc_success.assert_called_with(6, 2, True, False, False)

    @patch('sim_functions.calc_success')
    def test_calc_saves_no_modifiers(self, mock_calc_success):
        mock_calc_success.return_value = 5
        result = sim_functions.calc_saves(wounds=5, save=3)
        self.assertEqual(result, 5)
        mock_calc_success.assert_called_with(5, 3, True, False, False)
        
    @patch('sim_functions.calc_success')
    def test_calc_saves_cover(self, mock_calc_success):
        mock_calc_success.return_value = 5
        result = sim_functions.calc_saves(wounds=5, save=4, cover=True)
        self.assertEqual(result, 5)
        mock_calc_success.assert_called_with(5, 3, True, False, False)

class TestCalcDamageFunction(unittest.TestCase):
    def test_calc_damage_no_modifiers(self):
        self.assertEqual(sim_functions.calc_damage(3, damage=2, return_as_list=False), 6)
    
    @patch('sim_functions.check_and_roll_numeric', return_value=6)
    def test_calc_damage_as_notation(self, mock_roll):
        self.assertEqual(sim_functions.calc_damage(3, damage="1d6", return_as_list=False), 18)
        
    @patch('sim_functions.check_and_roll_numeric')
    def test_calc_damage_with_reroll_all(self, mock_roll):
        mock_roll.side_effect = [1, 6, 1, 4] # rolls are in pairs
        self.assertEqual(sim_functions.calc_damage(2, damage="1d6", return_as_list=False, reroll_damage=enums.RerollType.REROLL_ALL.value), 10) 
        
    @patch('sim_functions.check_and_roll_numeric')
    def test_calc_damage_with_reroll_one(self, mock_roll):
        mock_roll.side_effect = [4, 1, 5, 6]
        self.assertEqual(sim_functions.calc_damage(3, damage="1d6", return_as_list=False, reroll_damage=enums.RerollType.REROLL_ONE.value), 15) 

    def test_calc_damage_return_as_list(self):
        self.assertEqual(sim_functions.calc_damage(3, damage=2, return_as_list=True), [2, 2, 2])

    def test_calc_damage_null_one_modifier(self):
        self.assertEqual(sim_functions.calc_damage(3, damage=2, return_as_list=True, minus_damage=enums.MinusDamageType.NULL_ONE.value), [2, 2])

    def test_calc_damage_minus_one_modifier(self):
        self.assertEqual(sim_functions.calc_damage(3, damage=2, return_as_list=True, minus_damage=enums.MinusDamageType.MINUS_ONE.value), [1, 1, 1])

    def test_calc_damage_minus_half_modifier(self):
        self.assertEqual(sim_functions.calc_damage(3, damage=5, return_as_list=True, minus_damage=enums.MinusDamageType.MINUS_HALF.value), [3, 3, 3])

    def test_calc_damage_zero_amt(self):
        self.assertEqual(sim_functions.calc_damage(0, damage=5, return_as_list=True), [])

class TestCalcKillsFunction(unittest.TestCase):
    def test_calc_kills_one_health(self):
        damage = [1, 1, 1]
        self.assertEqual(sim_functions.calc_kills(dmg_list=damage, wounds=1), (3, 1))

    def test_calc_kills_overkill(self):
        damage = [20, 20, 20]
        self.assertEqual(sim_functions.calc_kills(dmg_list=damage, wounds=1), (3, 1))

    def test_calc_kills_no_kill(self):
        damage = [1, 1, 1]
        self.assertEqual(sim_functions.calc_kills(dmg_list=damage, wounds=4), (0, 1))

    def test_calc_kills_multiple_damage(self):
        damage = [2, 2, 2]
        self.assertEqual(sim_functions.calc_kills(dmg_list=damage, wounds=4), (1, 2))
        
    def test_calc_kills_has_remainder(self):
        damage = [2, 2, 2]
        self.assertEqual(sim_functions.calc_kills(dmg_list=damage, wounds=4, remainder=2), (2, 4))

if __name__ == '__main__':
    unittest.main()