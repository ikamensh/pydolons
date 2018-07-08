import pytest

from mechanics.buffs import Ability
from mechanics.attributes import Attribute, Attributes, get_attrib_by_enum

@pytest.fixture(params=Attributes)
def attrib(request):
    yield request.param

@pytest.fixture()
def inner_power(attrib):
    bonus = Attribute(2, 100, 0)
    inner_power = Ability({attrib: bonus})
    yield inner_power

@pytest.fixture()
def bonus_str(attrib):
    bonus = Attribute(0, 0, 3)
    bonus_str = Ability({attrib: bonus})
    yield bonus_str



def test_str_helps(hero, inner_power, attrib):
    attrib_before = get_attrib_by_enum(hero, attrib)

    hero.abilities.append(inner_power)
    hero.reset()

    attrib_after = get_attrib_by_enum(hero, attrib)

    assert attrib_after > attrib_before

# def test_rescale(hero, inner_power):
#     hp_before = hero.health
#
#     hero.abilities.append(inner_power)
#     hero.rescale()
#
#     hp_after = hero.health
#
#     assert hp_after > hp_before
#
# def test_multiplier(hero, pirate, inner_power):
#
#     hp_before = hero.health
#     hero.abilities.append(inner_power)
#     hero.rescale()
#     delta_hero = hero.health - hp_before
#
#     hp_before = pirate.health
#     pirate.abilities.append(inner_power)
#     pirate.rescale()
#     delta_pirate = pirate.health - hp_before
#
#     assert delta_hero > delta_pirate
#
# def test_bonus(hero, pirate, bonus_str):
#
#     hp_before = hero.health
#     hero.abilities.append(bonus_str)
#     hero.rescale()
#     delta_hero = hero.health - hp_before
#
#     assert delta_hero > 0
#
#     hp_before = pirate.health
#     pirate.abilities.append(bonus_str)
#     pirate.rescale()
#     delta_pirate = pirate.health - hp_before
#
#     assert delta_hero == delta_pirate


