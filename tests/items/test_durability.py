from mechanics.combat import Attack
import pytest


def test_loses_durability(hero, weapon, pirate, armor, no_chances):
    hero.equipment["hands"] = weapon
    pirate.equipment["body"] = armor

    weapon_dur_before = weapon.durability
    armor_dur_before = armor.durability

    Attack.attack(hero, pirate)

    weapon_dur_after = weapon.durability
    armor_dur_after = armor.durability

    assert weapon_dur_after < weapon_dur_before
    assert armor_dur_after < armor_dur_before


def test_weapon_degrades(weapon):

    dmg_amount_before = weapon.damage.amount
    weapon.durability /= 2

    dmg_amount_after = weapon.damage.amount

    assert dmg_amount_after < dmg_amount_before


def test_armor_degrades(armor):
    armor_before = sum(armor.armor.values())
    armor.durability /= 2

    armor_after = sum(armor.armor.values())

    assert armor_after < armor_before


def test_maximum_holds(weapon):
    maximum = weapon.max_durability
    weapon.durability += maximum * 2
    assert weapon.durability == maximum

def test_zero_holds(armor):
    maximum = armor.max_durability
    armor.durability -= maximum * 2
    assert armor.durability == 0
