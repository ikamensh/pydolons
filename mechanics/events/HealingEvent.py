from mechanics.events import EventsChannels
from mechanics.events.src.Event import Event

class HealingEvent(Event):
    channel = EventsChannels.HealingChannel

    def __init__(self, game, healing_amount, target, *, source=None):
        self.source = source
        self.target = target
        self.healing_amount = healing_amount
        super().__init__(game)

    def check_conditions(self):
        return self.target.alive and self.healing_amount > 0

    def resolve(self):
        self.target.health += self.healing_amount

    def __repr__(self):
        return f"{self.target} is healed for {self.healing_amount}" \
               + f"by {self.source}" if self.source else ""
