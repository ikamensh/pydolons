from game_objects.items import Equipment, Slot
import pytest

def test_can_equip_directly(weapon):
    eq = Equipment(None)
    eq["hands"] = weapon
    assert eq["hands"] == weapon

def test_type_matters(weapon):
    eq = Equipment(None)

    with pytest.raises(AssertionError):
        eq["body"] = weapon

def test_equip(weapon, hero):
    inventory_slot = Slot("inventory_01")
    inventory_slot.content = weapon

    eq = Equipment(hero)
    eq.equip(inventory_slot)

    assert eq["hands"] == weapon
    assert inventory_slot.content is None



