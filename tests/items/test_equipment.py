from game_objects.items import Weapon, Equipment, Slot
from mechanics.damage import DamageTypes
import pytest

def test_can_equip_directly(weapon):
    eq = Equipment()
    eq["hands"] = weapon
    assert eq["hands"] == weapon

def test_type_matters(weapon):
    eq = Equipment()

    with pytest.raises(AssertionError):
        eq["body"] = weapon

def test_equip(weapon):
    inventory_slot = Slot("inventory_01")
    inventory_slot.content = weapon

    eq = Equipment()
    eq.equip(inventory_slot)

    assert eq["hands"] == weapon
    assert inventory_slot.content is None



