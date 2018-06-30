from game_objects.items import ItemTransactions, BodyArmor, Weapon
import pytest

@pytest.fixture(params=[BodyArmor, Weapon])
def different_item(requests):
    armor_or_dmg = 5
    durability = 5
    yield  requests.param(armor_or_dmg, durability)

def test_equip(hero, different_item):
    with ItemTransactions(hero) as trans:
        trans.equipment.equip(different_item)
        item_type = different_item.type

    assert hero.equipment[item_type] is not None


