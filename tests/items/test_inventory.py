from game_objects.items import Item, Inventory
import pytest

@pytest.fixture()
def full_inventory():
    inv = Inventory(3)

    for i in range(3):
        item = Item("blabla", 3)
        inv.add(item)

    yield inv

def test_len():
    inv = Inventory(10)
    assert len(inv) == 0

    item = Item("blabla", 3)
    inv.add(item)
    assert len(inv) == 1


def test_limited_size():
    inv = Inventory(3)

    for i in range(3):
        item = Item("blabla", 3)
        added = inv.add(item)
        assert added == True

    assert len(inv) == 3

    item = Item("blabla", 3)
    added = inv.add(item)
    assert added == False

    assert len(inv) == 3

def test_can_drop(full_inventory):
    full_inventory.drop(0)
    full_inventory.drop(1)
    full_inventory.drop(2)

    for i in range(3):
        item = Item("blabla", 3)
        added = full_inventory.add(item)
        assert added == True




