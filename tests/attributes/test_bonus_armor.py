import pytest

from game_objects.attributes import Bonus
from game_objects.battlefield_objects import CharAttributes
from mechanics.damage import Armor, DamageTypes, Damage
from mechanics.events import DamageEvent
from mechanics.buffs import Ability


@pytest.fixture()
def total_armor():
    armor = Armor(10)
    bonus = Bonus({CharAttributes.ARMOR: armor})
    _total_armor = Ability(bonus)

    yield _total_armor


@pytest.fixture()
def broken_armor():
    armor = Armor(-10)
    bonus = Bonus({CharAttributes.ARMOR: armor})
    _total_armor = Ability(bonus)

    yield _total_armor


@pytest.fixture()
def special_armor():
    armor = Armor(armor_dict={DamageTypes.ACID: 100})
    bonus = Bonus({CharAttributes.ARMOR: armor})
    _special_armor = Ability(bonus)

    yield _special_armor


def test_right_type_works(game_hvsp, hero, special_armor):
    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.ACID)
    DamageEvent(dmg, hero)

    dealt_no_armor = hp_before_dmg - hero.health
    hp_before_dmg = hero.health

    hero.add_ability(special_armor)

    DamageEvent(dmg, hero)
    dealt_armor = hp_before_dmg - hero.health

    assert dealt_no_armor > dealt_armor


def test_wrong_type_useless(game_hvsp, hero, special_armor):
    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.FIRE)
    DamageEvent(dmg, hero)

    dealt_no_armor = hp_before_dmg - hero.health
    hp_before_dmg = hero.health

    hero.add_ability(special_armor)

    DamageEvent(dmg, hero)
    dealt_armor = hp_before_dmg - hero.health

    assert dealt_no_armor == dealt_armor


def test_armor_reduces_damage(game_hvsp, hero, total_armor):

    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.FIRE)
    DamageEvent(dmg, hero)

    dealt_no_armor = hp_before_dmg - hero.health
    hp_before_dmg = hero.health

    hero.add_ability(total_armor)

    DamageEvent(dmg, hero)
    dealt_armor = hp_before_dmg - hero.health

    assert dealt_no_armor > dealt_armor


def test_ability_stacks(game_hvsp, hero, total_armor):

    hp_before_dmg = hero.health
    dmg = Damage(50, DamageTypes.FIRE)

    total_armor.apply_to(hero)
    DamageEvent(dmg, hero)
    dealt_armor1 = hp_before_dmg - hero.health

    hp_before_dmg = hero.health
    hero.add_ability(total_armor)
    DamageEvent(dmg, hero)
    dealt_armor2 = hp_before_dmg - hero.health

    assert dealt_armor1 > dealt_armor2


def test_negative_armor(game_hvsp, hero, broken_armor):

    hp_before_dmg = hero.health
    armor = Armor(30)
    hero.natural_armor = armor
    dmg = Damage(50, DamageTypes.FIRE)
    DamageEvent(dmg, hero)

    dealt_armor = hp_before_dmg - hero.health
    hp_before_dmg = hero.health

    hero.add_ability(broken_armor)

    DamageEvent(dmg, hero)
    dealt_reduced_armor = hp_before_dmg - hero.health

    assert dealt_reduced_armor > dealt_armor
