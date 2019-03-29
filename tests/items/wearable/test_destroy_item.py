from mechanics.events import ItemDestroyedEvent
from game_objects.items import EquipmentSlotUids


def test_breaks_into_blueprint(hero, real_weapon):
    hero.equipment.equip_item(real_weapon)

    len_inventory_before = len(hero.inventory.all_items)

    ItemDestroyedEvent(real_weapon)

    len_inventory_after = len(hero.inventory.all_items)

    assert hero.equipment[EquipmentSlotUids.HANDS] is None
    assert len_inventory_after == len_inventory_before + 2


def test_destroyed_on_0_durability(hero, real_weapon):

    hero.equipment.equip_item(real_weapon)

    len_inventory_before = len(hero.inventory.all_items)

    real_weapon.durability = 0

    len_inventory_after = len(hero.inventory.all_items)

    assert hero.equipment[EquipmentSlotUids.HANDS] is None
    assert len_inventory_after == len_inventory_before + 2
