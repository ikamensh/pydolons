from mechanics.events import MovementEvent
from cntent.triggers.immortality import immortality


def test_simulation_units_dont_rly_die(minigame):
    real_unit_count_before = len(minigame.battlefield.unit_locations)

    sim = minigame.simulation()
    assert sim is not minigame

    sim_unit_count_before = len( sim.battlefield.unit_locations )
    units = list(sim.battlefield.unit_locations.keys())

    units[0].health -= 99999

    sim_unit_count_after = len( sim.battlefield.unit_locations )
    assert not units[0].alive
    assert sim_unit_count_after < sim_unit_count_before

    real_unit_count_after = len(minigame.battlefield.unit_locations)
    assert real_unit_count_after == real_unit_count_before


def test_simulation_units_dont_rly_move(minigame):
    real_unit = list(minigame.battlefield.unit_locations.keys())[0]
    real_location_before = minigame.battlefield.unit_locations[real_unit]

    sim = minigame.simulation()
    assert sim is not minigame

    sim_unit = list(sim.battlefield.unit_locations.keys())[0]
    sim_location_before = sim.battlefield.unit_locations[sim_unit]

    sim.battlefield.move(sim_unit, 0j)

    assert sim_location_before != sim.battlefield.unit_locations[sim_unit]



    real_location_after = minigame.battlefield.unit_locations[real_unit]

    assert real_location_before == real_location_after

def test_events_work(minigame):
    real_unit = list(minigame.battlefield.unit_locations.keys())[0]
    real_location_before = minigame.battlefield.unit_locations[real_unit]

    sim = minigame.simulation()
    assert sim is not minigame

    sim_unit = list(sim.battlefield.unit_locations.keys())[0]
    sim_location_before = sim.battlefield.unit_locations[sim_unit]

    MovementEvent(sim_unit, 0j)

    assert sim_location_before != sim.battlefield.unit_locations[sim_unit]

    real_location_after = minigame.battlefield.unit_locations[real_unit]

    assert real_location_before == real_location_after


def test_triggers_only_in_sim(minigame, hero):
    sim = minigame.simulation()
    sim_hero = sim.find_unit(hero)
    trig = immortality(sim_hero)
    sim_hero.health -= 99999
    assert sim_hero.alive

    assert hero.alive
    hero.health -= 99999
    assert not hero.alive


def test_triggers_present_in_sim(minigame, hero):

    trig = immortality(hero)
    hero.health -= 99999
    assert hero.alive


    sim = minigame.simulation()
    sim_hero = sim.find_unit(hero)
    sim_hero.health -= 99999
    assert sim_hero.alive

def test_sim_persists(minigame):
    sim = minigame.simulation()
    assert sim is not minigame
    pirate = list(sim.battlefield.unit_locations.keys())[0]
    pirate.health -= 99999
    assert not pirate.alive

    assert sim is not minigame
    assert not pirate.alive


def test_hp_transfered(minigame, hero):

    hero.health -= 200
    hero.mana -= 100
    hero.stamina -= 11
    sim = minigame.simulation()
    sim_hero = sim.find_unit(hero)

    assert hero.health == sim_hero.health
    assert hero.mana == sim_hero.mana
    assert hero.stamina == sim_hero.stamina







