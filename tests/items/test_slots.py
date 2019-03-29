from game_objects.items import ItemTypes, Slot
import pytest
import copy


def test_slot(weapon):
    slot = Slot("test slot", ItemTypes.WEAPON)
    weapon2 = copy.copy(weapon)
    slot.content = weapon
    with pytest.raises(Exception):
        slot.content = weapon2

    slot.pop_item()
    slot.content = weapon2
    assert slot.content == weapon2


def test_swap(weapon):
    slot1 = Slot("test slot")
    item1 = weapon
    slot1.content = item1

    slot2 = Slot("test slot2")
    item2 = copy.copy(item1)
    slot2.content = item2

    slot1.swap_item(slot2)

    assert slot1.content == item2
    assert slot2.content == item1
