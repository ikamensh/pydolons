from game_objects.items import ItemTransactions, Slot
import pytest

def test_equip(hero, diff_item):
    with ItemTransactions(hero) as trans:
        slot = hero.inventory.get_empty_slot()
        slot.content = diff_item
        hero.equipment.equip(slot)

def test_transaction_safe(hero, diff_item):
    slot = hero.inventory.get_empty_slot()
    slot.content = diff_item
    assert len(hero.inventory.all_items) == 1
    with ItemTransactions(hero) as trans:
        trans.take_from(slot)
        assert len(hero.inventory.all_items) == 0

    assert len(hero.inventory.all_items) == 1





