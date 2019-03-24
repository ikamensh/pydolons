from contextlib import contextmanager

@contextmanager
def virtual(unit):
    health_before = unit.health
    mana_before = unit.mana
    stamina_before = unit.stamina
    readiness_before = unit.readiness

    yield

    unit.health = health_before
    unit.mana = mana_before
    unit.stamina = stamina_before
    unit.readiness = readiness_before

@contextmanager
def simulate_death(game, unit):
    position = game.get_location(unit)
    facing = unit.facing
    fraction = game.fractions[unit]
    game.unit_died(unit)
    yield
    game.add_unit(unit, position, facing, fraction)

