import pytest

from game_objects.attributes import Bonus
from game_objects.battlefield_objects import CharAttributes
from mechanics.damage import Resistances, DamageTypes, Damage
from mechanics.events import DamageEvent
from mechanics.buffs import Ability


@pytest.fixture()
def total_resist():
    resists = Resistances({dt:0.5 for dt in DamageTypes})
    bonus = Bonus({CharAttributes.RESISTANCES: resists})
    _total_resist = Ability([bonus])

    yield _total_resist

@pytest.fixture()
def special_resist():
    resist = Resistances({DamageTypes.ACID:100})
    bonus = Bonus({CharAttributes.RESISTANCES: resist})
    _special_resist = Ability([bonus])

    yield _special_resist

@pytest.fixture()
def vulnerability():
    resists = Resistances({dt:-0.5 for dt in DamageTypes})
    bonus = Bonus({CharAttributes.RESISTANCES: resists})
    _vulnerability = Ability([bonus])

    yield _vulnerability


def test_right_type_works(game_hvsp, hero, special_resist):
    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.ACID)
    DamageEvent(dmg, hero)

    dealt_no_armor = hp_before_dmg - hero.health
    hp_before_dmg = hero.health

    hero.add_ability(special_resist)

    DamageEvent(dmg, hero)
    dealt_armor = hp_before_dmg - hero.health

    assert dealt_no_armor > dealt_armor


def test_wrong_type_useless(game_hvsp, hero, special_resist):
    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.FIRE)
    DamageEvent(dmg, hero)

    dealt_no_armor = hp_before_dmg - hero.health
    hp_before_dmg = hero.health

    hero.add_ability(special_resist)

    DamageEvent(dmg, hero)
    dealt_armor = hp_before_dmg - hero.health

    assert dealt_no_armor == dealt_armor

def test_armor_reduces_damage(game_hvsp, hero, total_resist):

    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.FIRE)
    DamageEvent(dmg, hero)

    dealt_no_armor = hp_before_dmg - hero.health
    hp_before_dmg = hero.health

    hero.add_ability(total_resist)

    DamageEvent(dmg, hero)
    dealt_armor = hp_before_dmg - hero.health

    assert dealt_no_armor > dealt_armor


def test_ability_stacks(game_hvsp, hero, total_resist):

    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.FIRE)

    hero.add_ability(total_resist)
    DamageEvent(dmg, hero)
    dealt_armor1 = hp_before_dmg - hero.health

    hp_before_dmg = hero.health
    import copy
    hero.add_ability(copy.deepcopy(total_resist))
    DamageEvent(dmg, hero)
    dealt_armor2 = hp_before_dmg - hero.health

    assert dealt_armor1 > dealt_armor2


def test_negative_armor(game_hvsp, hero, vulnerability):

    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.FIRE)
    DamageEvent(dmg, hero)

    dealt_armor = hp_before_dmg - hero.health
    hp_before_dmg = hero.health

    hero.add_ability(vulnerability)

    DamageEvent(dmg, hero)
    dealt_reduced_armor = hp_before_dmg - hero.health

    assert dealt_reduced_armor > dealt_armor