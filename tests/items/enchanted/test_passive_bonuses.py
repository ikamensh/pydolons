from game_objects.battlefield_objects import Unit, CharAttributes
from game_objects.attributes import Bonus
from game_objects.items import WearableItem, ItemTypes


def test_equip_gives_bonuses(hero: Unit, empty_game):
    ring = WearableItem("bronze ring", ItemTypes.RING)
    bns = Bonus({CharAttributes.HEALTH: 50})
    ring.bonuses.append(bns)

    health_before = hero.health

    hero.equipment.equip_item(ring)

    health_after = hero.health

    assert health_after > health_before


def test_unequip_removes_bonuses(hero, empty_game):
    ring = WearableItem("bronze ring", ItemTypes.RING, game=empty_game)
    bns = Bonus({CharAttributes.HEALTH: 50})
    ring.bonuses.append(bns)

    hero.equipment.equip_item(ring)

    health_with_ring = hero.health

    hero.equipment.unequip_item(ring)

    assert health_with_ring > hero.health
