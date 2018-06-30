from game_objects.items import ItemTransactions, BodyArmor, Weapon, Slot
from mechanics.damage import DamageTypes
import pytest

weapon = Weapon("test axe1", 5, DamageTypes.SLASH, 5)
armor = BodyArmor("da armor", 3, 3)

@pytest.fixture(params=[weapon, armor])
def diff_item(request):
    item = request.param
    yield item

def test_equip_random_slot(hero, diff_item):
    slot = Slot("test slot")
    slot.content = diff_item
    with ItemTransactions(hero) as trans:
        with pytest.raises(AssertionError):
            trans.equip(slot)

def test_equip(hero, diff_item):
    with ItemTransactions(hero) as trans:
        slot = hero.inventory.get_empty_slot()
        slot.content = diff_item
        trans.equip(slot)

def test_transaction_safe(hero, diff_item):
    slot = hero.inventory.get_empty_slot()
    slot.content = diff_item
    assert len(hero.inventory) == 1
    with ItemTransactions(hero) as trans:
        trans.take_from(slot)
        assert len(hero.inventory) == 0

    assert len(hero.inventory) == 1





