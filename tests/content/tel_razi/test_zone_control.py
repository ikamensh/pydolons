from cntent.monsters.tel_razi.triggers.zone_control import zone_control_trigger
from mechanics.events import AttackEvent, ActiveEvent, MovementEvent


def test_zone_control(pirate_band, empty_game, no_chances):
    p1 = pirate_band[0]
    p2 = pirate_band[1]

    empty_game.add_unit(p1, 2 + 2j, "FACTION_1", facing=1j)
    empty_game.add_unit(p2, 2 + 3j, "FACTION_2", facing=1j)

    zone_control_trigger(p1, 1, 1)

    spy = []
    empty_game.events_platform.history.append(spy)

    p1.readiness = 0.9
    p2.readiness = 1.5
    empty_game.order_move(p2, 2 + 4j)

    assert p2.cell.complex == 2 + 3j
    actives_found = 0
    attacks_found = 0
    for event, happened in spy:
        if isinstance(event, AttackEvent):
            attacks_found += 1
        elif isinstance(event, ActiveEvent):
            actives_found += 1
        elif isinstance(event, MovementEvent):
            assert not happened
    assert actives_found == 2
    assert attacks_found == 1


def test_zone_control_no_friendly_fire(pirate_band, empty_game, no_chances):
    p1 = pirate_band[0]
    p2 = pirate_band[1]

    empty_game.add_unit(p1, 2 + 2j, "FACTION_1", facing=1j)
    empty_game.add_unit(p2, 2 + 3j, "FACTION_1", facing=1j)

    zone_control_trigger(p1, 1, 1)

    spy = []
    empty_game.events_platform.history.append(spy)

    p1.readiness = 0.9
    p2.readiness = 1.5
    empty_game.order_move(p2, 2 + 4j)

    assert p2.cell.complex == 2 + 4j

    actives_found = 0
    attacks_found = 0
    for event, happened in spy:
        if isinstance(event, AttackEvent):
            attacks_found += 1
        elif isinstance(event, ActiveEvent):
            actives_found += 1
        elif isinstance(event, MovementEvent):
            assert happened
    assert actives_found == 1
    assert attacks_found == 0


def test_zone_control_need_active(pirate_band, empty_game, no_chances):
    p1 = pirate_band[0]
    p1.actives = []
    p2 = pirate_band[1]

    empty_game.add_unit(p1, 2 + 2j, "FACTION_1", facing=1j)
    empty_game.add_unit(p2, 2 + 3j, "FACTION_1", facing=1j)

    zone_control_trigger(p1, 1, 1)

    spy = []
    empty_game.events_platform.history.append(spy)

    p1.readiness = 0.9
    p2.readiness = 1.5
    empty_game.order_move(p2, 2 + 4j)

    assert p2.cell.complex == 2 + 4j

    actives_found = 0
    attacks_found = 0
    for event, happened in spy:
        if isinstance(event, AttackEvent):
            attacks_found += 1
        elif isinstance(event, ActiveEvent):
            actives_found += 1
        elif isinstance(event, MovementEvent):
            assert happened
    assert actives_found == 1
    assert attacks_found == 0


def test_zone_control_need_readiness(pirate_band, empty_game, no_chances):
    p1 = pirate_band[0]
    p2 = pirate_band[1]

    empty_game.add_unit(p1, 2 + 2j, "FACTION_1", facing=1j)
    empty_game.add_unit(p2, 2 + 3j, "FACTION_2", facing=1j)

    zone_control_trigger(p1, 1, 1)

    spy = []
    empty_game.events_platform.history.append(spy)

    p1.readiness = 0
    p2.readiness = 1.5
    empty_game.order_move(p2, 2 + 4j)

    assert p2.cell.complex == 2 + 4j

    actives_found = 0
    attacks_found = 0

    for event, happened in spy:
        if isinstance(event, AttackEvent):
            attacks_found += 1
        elif isinstance(event, ActiveEvent):
            actives_found += 1
        elif isinstance(event, MovementEvent):
            assert happened

    assert actives_found == 1
    assert attacks_found == 0
