from mechanics.buffs import Buff
from mechanics.events import BuffAppliedEvent
from mechanics.turns.AtbTurnsManager import AtbTurnsManager
from game_objects.battlefield_objects import Unit


def test_buff_applies(game, hero):

    buff = Buff(1)
    BuffAppliedEvent(buff, hero)

    assert buff in hero._buffs


def test_buff_expires(game, hero):

    atm = game.turns_manager

    assert isinstance(atm, AtbTurnsManager)

    buff = Buff(1)
    BuffAppliedEvent(buff, hero)

    assert buff in hero._buffs
    assert buff in game.turns_manager.managed

    atm.pass_time(0.5)

    assert buff in hero._buffs
    assert buff in game.turns_manager.managed

    atm.pass_time(0.5)

    assert buff not in hero._buffs
    assert buff not in game.turns_manager.managed


def test_buffs_do_not_stop_units(game, hero):
    atm = game.turns_manager

    assert isinstance(atm, AtbTurnsManager)

    for dur in range(0, 50):
        buff = Buff(dur/10)
        BuffAppliedEvent(buff, hero)

    for i in range(10):
        unit = atm.get_next()
        assert isinstance(unit, Unit)
        unit.readiness = 0

