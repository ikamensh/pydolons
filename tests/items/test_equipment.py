from game_objects.items import Equipment, Slot, EquipmentSlotUids
import pytest

def test_can_equip_directly(weapon, hero):
    eq = Equipment(hero)
    eq.equip_item(weapon)
    assert eq[EquipmentSlotUids.HANDS] is weapon


def test_equip(weapon, hero):
    inventory_slot = Slot("inventory_01")
    inventory_slot.content = weapon

    eq = Equipment(hero)
    eq.equip(inventory_slot)

    assert eq[EquipmentSlotUids.HANDS] is weapon
    assert inventory_slot.content is None



