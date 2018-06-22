from mechanics.abstract.event.event_targeting.EventTargeting import EventTargeting
from game_objects.battlefield_objects.Unit.Unit import Unit
from battlefield.Battlefield import Coordinates

class Event:
    def __init__(self, effects, event_targeting):
        self.effects = effects
        self.event_targeting = event_targeting

    def resolve(self, source, user_targeting):
        if self.event_targeting == EventTargeting.TARGET_UNIT:
            assert isinstance(user_targeting.target, Unit)
            target = user_targeting.target
            for effect in self.effects:
                effect.apply(source, target)