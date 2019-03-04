from mechanics.events import DamageEvent


def test_move_into_obstacle_attack(empty_game, hero, obstacle, no_chances):

    empty_game.add_unit(hero, 1+1j, facing=1)
    empty_game.add_obstacle(obstacle, 2+1j)

    empty_game.the_hero = hero
    hero.readiness = 1

    spy = empty_game.events_platform.collect_history()

    empty_game.ui_order(2,1)

    damage_event_present = False
    for event, happened in spy:
        if isinstance(event, DamageEvent):
            damage_event_present = True

    assert damage_event_present
