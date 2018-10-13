from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels

class UnitDiedEvent(Event):
    channel = EventsChannels.UnitDiedChannel

    def __init__(self, game, unit):
        assert unit.game is game
        self.unit = unit
        self.killer = unit.last_damaged_by
        super().__init__(game)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.game.unit_died(self.unit)

    def __repr__(self):
        if self.killer:
            if self.killer != self.unit:
                return "{} is killed by {}".format(self.unit, self.killer)
            else:
                return "{} commits suicide.".format(self.unit)
        else:
            return "{} dies.".format(self.unit)
