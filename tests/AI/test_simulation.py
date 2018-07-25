from mechanics.events import MovementEvent
from content.triggers.immortality import immortality
from content.triggers.damage_to_attacker import damage_to_attackers




def test_simulation_units_dont_rly_die(game):
    real_unit_count_before = len( game.battlefield.unit_locations )

    with game.simulation() as sim:
        assert sim is not game

        sim_unit_count_before = len( sim.battlefield.unit_locations )
        units = list(sim.battlefield.unit_locations.keys())

        units[0].health -= 99999

        sim_unit_count_after = len( sim.battlefield.unit_locations )
        assert not units[0].alive
        assert sim_unit_count_after < sim_unit_count_before

    real_unit_count_after = len( game.battlefield.unit_locations )
    assert real_unit_count_after == real_unit_count_before


def test_simulation_units_dont_rly_move(game):
    real_unit = list(game.battlefield.unit_locations.keys())[0]
    real_location_before = game.battlefield.unit_locations[real_unit]

    with game.simulation() as sim:
        assert sim is not game

        sim_unit = list(sim.battlefield.unit_locations.keys())[0]
        sim_location_before = sim.battlefield.unit_locations[sim_unit]

        sim.battlefield.move(sim_unit, 7j)

        assert sim_location_before != sim.battlefield.unit_locations[sim_unit]



    real_location_after = game.battlefield.unit_locations[real_unit]

    assert real_location_before == real_location_after

def test_events_work(game):
    real_unit = list(game.battlefield.unit_locations.keys())[0]
    real_location_before = game.battlefield.unit_locations[real_unit]

    with game.simulation() as sim:
        assert sim is not game

        sim_unit = list(sim.battlefield.unit_locations.keys())[0]
        sim_location_before = sim.battlefield.unit_locations[sim_unit]

        MovementEvent(sim_unit, 7j)

        assert sim_location_before != sim.battlefield.unit_locations[sim_unit]

    real_location_after = game.battlefield.unit_locations[real_unit]

    assert real_location_before == real_location_after


def test_triggers_only_in_sim(game, hero):


    with game.simulation() as sim:

        sim_hero = sim.find_unit(hero)
        trig = immortality(sim_hero)
        sim_hero.health -= 99999
        assert sim_hero.alive

    assert hero.alive
    hero.health -= 99999
    assert not hero.alive


def test_triggers_present_in_sim(game, hero):

    trig = immortality(hero)
    hero.health -= 99999
    assert hero.alive

    with game.simulation() as sim:

        sim_hero = sim.find_unit(hero)
        sim_hero.health -= 99999
        assert sim_hero.alive






