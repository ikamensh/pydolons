from mechanics.events.Event import Event
from mechanics.events.EventsPlatform import EventsChannels
import my_globals

class UnitDiedEvent(Event):
    channel = EventsChannels.UnitDiedChannel

    def __init__(self, unit, killer):
        self.unit = unit
        self.killer = killer
        super().__init__()

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        my_globals.the_game.unit_died(self.unit)

    def __repr__(self):
        if self.killer:
            if self.killer != self.unit:
                return "{} is killed by {}".format(self.unit, self.killer)
            else:
                return "{} commits suicide.".format(self.unit)
        else:
            return "{} dies.".format(self.unit)