from mechanics.flexi_targeting.event.Event import Event
from mechanics.flexi_targeting.event.event_targeting.EventTargeting import EventTargeting

from DreamGame import DreamGame

class ChainEvent:
    def __init__(self, effects, event_targeting, n_hits, no_self=True):
        self.effects = effects
        self.event_targeting = event_targeting
        self.units_hit=[]
        self.no_self = no_self
        self.n_hits = n_hits

    def resolve(self, source, user_targeting):
        if self.no_self:
            self.units_hit.append(source)

        if self.event_targeting == EventTargeting.TARGET_UNIT:
            assert isinstance(user_targeting.target, Unit)
            target_unit = user_targeting.target
            for effect in self.effects:
                effect.apply(source, target_unit)

        elif self.event_targeting == EventTargeting.UNIT_ON_TARGET_CELL:
            assert isinstance(user_targeting.target, Coordinates)
            target_unit = DreamGame.get_unit_at(user_targeting.target)
            for effect in self.effects:
                effect.apply(source, target_unit)

        self.n_hits -= 1
        while self.n_hits > 0:
            units = DreamGame.get_units_distances_from(DreamGame.get_location(target_unit))
            for chained_unit, _ in units:
                if chained_unit not in self.units_hit:
                    self.units_hit.append(chained_unit)
                    self.n_hits -= 1
                    for effect in self.effects:
                        effect.apply(source, chained_unit)
                    target_unit = chained_unit
                    break
