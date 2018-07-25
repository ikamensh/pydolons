from mechanics.events import Event
from mechanics.events import EventsChannels
import my_context

class BuffDetachedEvent(Event):
    channel = EventsChannels.BuffDetachedChannel

    def __init__(self, buff):
        self.buff = buff
        super().__init__()

    def check_conditions(self):
        return True

    def resolve(self):
        self.buff.attached_to.buffs.remove(self.buff)
        my_context.the_game.turns_manager.remove_buff(self.buff)

    def __repr__(self):
        return f"{self.buff} has detached."
