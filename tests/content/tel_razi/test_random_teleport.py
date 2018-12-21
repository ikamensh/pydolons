from cntent.monsters.tel_razi.triggers.teleport_on_hit import random_teleport_trigger
from mechanics.events import AttackEvent, ActiveEvent, MovementEvent
from mechanics.actives import Cost


def test_random_teleport(pirate_band, empty_game, no_chances):
    p1 = pirate_band[0]
    p2 = pirate_band[1]

    empty_game.add_unit(p1, 2+2j,"FACTION_1", facing=1j)
    empty_game.add_unit(p2, 2+3j,"FACTION_2", facing=1j)

    random_teleport_trigger(p2, 4, 1, Cost(readiness=0.1))

    spy = []
    empty_game.events_platform.history.append(spy)

    p1.readiness = 2
    p2.readiness = 0.5
    empty_game.order_attack(p1, p2)

    assert empty_game.battlefield.unit_locations[p2].complex != 2+3j
    actives_found = 0
    attacks_found = 0
    moves_found = 0
    for event, happened in spy:
        if isinstance(event, AttackEvent):
            attacks_found +=1
        elif isinstance(event, ActiveEvent):
            actives_found +=1
        elif isinstance(event, MovementEvent):
            moves_found += 1

    assert actives_found == 1
    assert attacks_found == 1
    assert moves_found == 1


def test_random_teleport_cost_blocks(pirate_band, empty_game, no_chances):
    p1 = pirate_band[0]
    p2 = pirate_band[1]

    empty_game.add_unit(p1, 2 + 2j, "FACTION_1", facing=1j)
    empty_game.add_unit(p2, 2 + 3j, "FACTION_2", facing=1j)

    random_teleport_trigger(p2, 4, 1, Cost(readiness=0.1, mana=99999))

    spy = []
    empty_game.events_platform.history.append(spy)

    p1.readiness = 2
    p2.readiness = 0.5
    empty_game.order_attack(p1, p2)

    assert empty_game.battlefield.unit_locations[p2].complex == 2 + 3j
    actives_found = 0
    attacks_found = 0
    moves_found = 0
    for event, happened in spy:
        if isinstance(event, AttackEvent):
            attacks_found += 1
        elif isinstance(event, ActiveEvent):
            actives_found += 1
        elif isinstance(event, MovementEvent):
            moves_found += 1

    assert actives_found == 1
    assert attacks_found == 1
    assert moves_found == 0


def test_random_teleport_chance_blocks(pirate_band, empty_game, no_chances):
    p1 = pirate_band[0]
    p2 = pirate_band[1]

    empty_game.add_unit(p1, 2 + 2j, "FACTION_1", facing=1j)
    empty_game.add_unit(p2, 2 + 3j, "FACTION_2", facing=1j)

    random_teleport_trigger(p2, 4, 0, Cost(readiness=0.1))

    spy = []
    empty_game.events_platform.history.append(spy)

    p1.readiness = 2
    p2.readiness = 0.5
    empty_game.order_attack(p1, p2)

    assert empty_game.battlefield.unit_locations[p2].complex == 2 + 3j
    actives_found = 0
    attacks_found = 0
    moves_found = 0
    for event, happened in spy:
        if isinstance(event, AttackEvent):
            attacks_found += 1
        elif isinstance(event, ActiveEvent):
            actives_found += 1
        elif isinstance(event, MovementEvent):
            moves_found += 1

    assert actives_found == 1
    assert attacks_found == 1
    assert moves_found == 0

def test_dying_unit_dies(pirate_band, empty_game, no_chances):
    p1 = pirate_band[0]
    p2 = pirate_band[1]

    empty_game.add_unit(p1, 2 + 2j, "FACTION_1", facing=1j)
    empty_game.add_unit(p2, 2 + 3j, "FACTION_2", facing=1j)

    random_teleport_trigger(p2, 4, 1, Cost(readiness=0.1))
    p2.health = 1

    p1.readiness = 2
    p2.readiness = 0.5
    empty_game.order_attack(p1, p2)
    pass # no exceptions thrown



