import random
import pytest
from character.masteries import Masteries, MasteriesEnum

def test_incremental_cost_grows():
    m = Masteries()

    old_cost = 0

    for i in range(1000):
        c = m.increment_cost(i)
        assert c > old_cost
        old_cost = c


def test_cost_depends_only_directly(var_mastery):
    m = Masteries()
    initial_exp = 123

    m.exp_spent[var_mastery] = initial_exp

    cost_before = m.calculate_cost(var_mastery)

    for other_m in set(MasteriesEnum) - {var_mastery}:
        m.exp_spent[other_m] = random.randint(0, 1000000)

    assert m.calculate_cost(var_mastery) == cost_before


@pytest.mark.parametrize("lvl", [0, 1, 3, 7, 15, 155])
def test_cum_cost_eq_level(some_mastery, lvl):
    m = Masteries()
    cost = m.cumulative_cost(lvl)
    m.exp_spent[some_mastery] = cost
    assert m.values[some_mastery] == lvl



def test_cum_cost():
    m = Masteries()
    assert m.cumulative_cost(0) == 0

    old_cost = 0

    for i in range(1, 1000):
        c = m.cumulative_cost(i)
        assert c > old_cost
        old_cost = c