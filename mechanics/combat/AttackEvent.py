from mechanics.events.Event import Event
from mechanics.events.EventsPlatform import EventsChannels
from mechanics.damage import DamageEvent
from mechanics.chances.CritHitGrazeMiss import ImpactCalculator, ImpactFactor


class AttackEvent(Event):
    channel = EventsChannels.AttackChannel
    def __init__(self, source, target, damage):
        self.source = source
        self.target = target
        self.damage = damage
        super().__init__()

    def check_conditions(self):
        return all( (self.source, self.source.alive, self.target, self.target.alive) )

    def resolve(self):
        impact = ImpactCalculator.roll_impact(self.source.unarmed_chances, self.source.melee_precision,
                                              self.target.melee_evasion)
        if impact is not ImpactFactor.MISS:
            unit_died = DamageEvent(self.damage, self.target, source=self.source, impact_factor = impact)
            self.result = unit_died
        else:
            print("MISS")

    def __repr__(self):
        return "{} attacks {}.".format(self.source, self.target)