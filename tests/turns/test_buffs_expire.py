from mechanics.buffs import Buff
from mechanics.events import BuffAppliedEvent
from mechanics.turns.AtbTurnsManager import AtbTurnsManager
from game_objects.battlefield_objects import Unit


def test_buff_applies(game_hvsp, hero):

    buff = Buff(1)
    BuffAppliedEvent(buff, hero)

    assert buff in hero.buffs


def test_buff_expires(game_hvsp, hero):

    atm = game_hvsp.turns_manager

    assert isinstance(atm, AtbTurnsManager)

    buff = Buff(1)
    BuffAppliedEvent(buff, hero)

    assert buff in hero.buffs
    assert buff in game_hvsp.turns_manager.managed

    atm.pass_time(0.5)

    assert buff in hero.buffs
    assert buff in game_hvsp.turns_manager.managed

    atm.pass_time(0.5)

    assert buff not in hero.buffs
    assert buff not in game_hvsp.turns_manager.managed


def test_buffs_do_not_stop_units(game_hvsp, hero):
    atm = game_hvsp.turns_manager

    assert isinstance(atm, AtbTurnsManager)

    for dur in range(0, 50):
        buff = Buff(dur / 10)
        BuffAppliedEvent(buff, hero)

    for i in range(10):
        unit = atm.get_next()
        assert isinstance(unit, Unit)
        unit.readiness = 0
