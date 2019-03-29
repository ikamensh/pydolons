from cntent.items.std.std_items import sword_cheap
from cntent.items.std.potions import minor_healing_potion


def test_inventory(char):
    unit = char.unit

    unit.inventory.add(minor_healing_potion)

    new_unit = char.unit
    assert minor_healing_potion in new_unit.inventory.all_items


def test_equipment(char):
    unit = char.unit

    unit.equipment.equip_item(sword_cheap)

    new_unit = char.unit
    assert sword_cheap in new_unit.equipment.all_items
