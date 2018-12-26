from cntent.monsters.tel_razi.monsters import sentinel
from mechanics.events import EventsChannels

def test_trigger_removed_on_death(empty_game):

    triggers_before = set( empty_game.events_platform.triggers[EventsChannels.MovementChannel]) | \
                     set( empty_game.events_platform.interrupts[EventsChannels.MovementChannel])


    s = sentinel.create(empty_game)
    empty_game.add_unit(s, 1+1j)

    triggers_after = set( empty_game.events_platform.triggers[EventsChannels.MovementChannel]) | \
                     set( empty_game.events_platform.interrupts[EventsChannels.MovementChannel])

    assert len(triggers_before) < len(triggers_after)

    s.health = 0

    triggers_rip = set(empty_game.events_platform.triggers[EventsChannels.MovementChannel]) | \
                           set(empty_game.events_platform.interrupts[EventsChannels.MovementChannel])

    assert len(triggers_before) == len(triggers_rip)




