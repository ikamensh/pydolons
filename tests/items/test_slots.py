from game_objects.items import Weapon, SlotTypes, Slot, Item
from mechanics.damage import DamageTypes
import pytest

def test_slot():
    slot = Slot("test slot", SlotTypes.WEAPON)
    weapon1 = Weapon("test axe1", 5, DamageTypes.SLASH, 5)
    weapon2 = Weapon("test axe2", 5, DamageTypes.SLASH, 5)
    slot.content = weapon1
    with pytest.raises(Exception):
        slot.content = weapon2

    slot.take_content()
    slot.content = weapon2
    assert slot.content == weapon2

def test_swap():
    slot1 = Slot("test slot")
    item1 = Item("quack", 3)
    slot1.content = item1

    slot2 = Slot("test slot2")
    item2 = Item("bryak", 3)
    slot2.content = item2

    slot1.swap_item(slot2)

    assert slot1.content == item2
    assert slot2.content == item1

