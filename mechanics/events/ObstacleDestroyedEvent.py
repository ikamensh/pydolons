from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
import my_globals

class ObstacleDestroyedEvent(Event):
    channel = EventsChannels.ObstacleDestroyedChannel

    def __init__(self, unit):
        self.unit = unit
        self.killer = unit.last_damaged_by
        super().__init__()

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.unit.alive = False
        my_globals.the_game.obstacle_destroyed(self.unit)

    def __repr__(self):
        if self.killer:
            return "{} was destroyed by {}".format(self.unit, self.killer)
        else:
            return "{} was destroyed.".format(self.unit)