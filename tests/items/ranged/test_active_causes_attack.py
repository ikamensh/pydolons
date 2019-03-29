

def test_usage_ranged_attack(hero, bow, empty_game, pirate, no_chances):

    actives_no_potion = set(hero.actives)
    hero.equipment.equip_item(bow)

    ranged_attack_active = list(set(hero.actives) - actives_no_potion)[0]

    empty_game.add_unit(hero, (1 + 1j), facing=1j)
    empty_game.add_unit(pirate, (2 + 3j), facing=1j)

    from mechanics.events import RangedAttackEvent

    spy = empty_game.events_platform.collect_history()

    hero.activate(ranged_attack_active, pirate)

    ranged_attack_event = None
    for e, happened in spy:
        if isinstance(e, RangedAttackEvent):
            ranged_attack_event = e

    assert ranged_attack_event is not None
    assert ranged_attack_event.target is pirate
    assert ranged_attack_event.source is hero

    from mechanics.events import DamageEvent
    damage_event = None
    for e, happened in spy:
        if isinstance(e, DamageEvent):
            damage_event = e

    assert damage_event
    assert pirate.health < pirate.max_health


def test_too_close(hero, bow, empty_game, pirate, monkeypatch):

    actives_no_potion = set(hero.actives)
    hero.equipment.equip_item(bow)

    new_active = list(set(hero.actives) - actives_no_potion)[0]

    empty_game.add_unit(hero, (1 + 1j), facing=1j)
    empty_game.add_unit(pirate, (1 + 2j), facing=1j)

    from mechanics.combat import RangedAttack

    spy = []

    def spy_lambda(source, target):
        spy.append((source, target))

    monkeypatch.setattr(RangedAttack, 'ranged_attack', spy_lambda)

    hero.activate(new_active, pirate)

    assert len(spy) == 0


def test_too_far(hero, bow, empty_game, pirate, monkeypatch):
    actives_no_potion = set(hero.actives)
    hero.equipment.equip_item(bow)

    new_active = list(set(hero.actives) - actives_no_potion)[0]

    empty_game.add_unit(hero, (0 + 0j), facing=1j)
    empty_game.add_unit(pirate, (1 + 5j), facing=1j)

    from mechanics.combat import RangedAttack

    spy = []

    def spy_lambda(source, target):
        spy.append((source, target))

    monkeypatch.setattr(RangedAttack, 'ranged_attack', spy_lambda)

    hero.activate(new_active, pirate)

    assert len(spy) == 0


def test_angle(hero, bow, empty_game, pirate, monkeypatch):

    actives_no_potion = set(hero.actives)
    hero.equipment.equip_item(bow)

    new_active = list(set(hero.actives) - actives_no_potion)[0]

    empty_game.add_unit(hero, (1 + 1j), facing=-1j)
    empty_game.add_unit(pirate, (2 + 3j), facing=1j)

    from mechanics.combat import RangedAttack

    spy = []

    def spy_lambda(source, target):
        spy.append((source, target))

    monkeypatch.setattr(RangedAttack, 'ranged_attack', spy_lambda)

    hero.activate(new_active, pirate)

    assert len(spy) == 0
