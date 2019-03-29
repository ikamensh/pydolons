from cntent.actives.std.std_misc import wait_active
from mechanics.events import TimePassedEvent


def test_wait(empty_game, hero):
    empty_game.add_unit(hero, 1 + 1j)

    wait_active.cooldown = 1
    units_active = hero.give_active(wait_active)
    assert hero.activate(units_active)      # first activation
    assert not hero.activate(units_active)  # on cooldown

    TimePassedEvent(empty_game, 0.5)
    assert not hero.activate(units_active)  # still on cooldown

    TimePassedEvent(empty_game, 0.501)
    assert hero.activate(units_active)      # no longer on cooldown
