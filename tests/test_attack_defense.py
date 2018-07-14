from mechanics.chances.ChanceCalculator import ChanceCalculator


import pytest



@pytest.mark.parametrize("attack, defense", [
    (0, 0),
    (0, 10),
    (0, 9000),
    (110, 0),
    (0, 15),
    (19929, 166),
])
def test_zero_one_do_not_change(attack, defense):
    base_chance = 0
    modified_chance = ChanceCalculator.chance(base_chance, attack, defense)
    assert modified_chance == base_chance

    base_chance = 1
    modified_chance = ChanceCalculator.chance(base_chance, attack, defense)
    assert modified_chance == base_chance

def test_attack_increases():
    base_chance = 0.5
    assert ChanceCalculator.chance(base_chance, 10, 0) > base_chance

def test_defence_reduces():
    base_chance = 0.5
    assert ChanceCalculator.chance(base_chance, 0, 10) < base_chance

def test_extreme_attack_close_to_one():
    base_chance = 0.5
    extremely_a_lot = 1e10
    epsilon = 1e-4
    new_chance = ChanceCalculator.chance(base_chance, precision=extremely_a_lot, evasion=0)
    assert abs(new_chance - 1) < epsilon

def test_extreme_defense_close_to_zero():
    base_chance = 0.5
    extremely_a_lot = 1e10
    epsilon = 1e-4
    new_chance = ChanceCalculator.chance(base_chance, precision=0, evasion=extremely_a_lot)
    assert new_chance < epsilon


