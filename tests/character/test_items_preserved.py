from character_creation.Character import Character
from cntent.base_types import pirate_basetype
from cntent.items.std.std_items import sword_cheap
from cntent.items.std.potions import minor_healing_potion

import pytest

@pytest.fixture()
def char():
    c = Character(pirate_basetype)
    return c

def test_inventory(char):
    unit = char.unit

    unit.inventory.add(minor_healing_potion)

    new_unit = char.unit
    assert minor_healing_potion in new_unit.inventory