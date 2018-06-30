from game_objects.items import Weapon, Equipment, Slot
from mechanics.damage import DamageTypes
import pytest

def test_can_equip_directly():
    eq = Equipment()
    weapon = Weapon("test axe1", 5, DamageTypes.SLASH, 5)

    eq["hands"] = weapon
    assert eq["hands"] == weapon

def test_type_matters():
    eq = Equipment()
    weapon1 = Weapon("test axe1", 5, DamageTypes.SLASH, 5)

    with pytest.raises(AssertionError):
        eq["body"] = weapon1

def test_equip():
    weapon = Weapon("test axe1", 5, DamageTypes.SLASH, 5)
    inventory_slot = Slot("inventory_01")
    inventory_slot.content = weapon

    eq = Equipment()
    eq.equip(inventory_slot)

    assert eq["hands"] == weapon
    assert inventory_slot.content is None



